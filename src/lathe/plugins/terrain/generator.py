"""Terrain generation plugin using OpenSimplex noise."""

import asyncio
from typing import Any, Callable

import numpy as np
import opensimplex as osi
from numpy.typing import NDArray

from lathe.models.world import World
from lathe.plugins.base import PluginMetadata, PluginResult, SimulationPlugin


class TerrainGeneratorPlugin(SimulationPlugin):
    """Generates terrain elevations using multi-octave OpenSimplex noise."""

    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="terrain",
            version="1.0.0",
            dependencies=[],
            description="Generates realistic terrain elevations using OpenSimplex noise",
            author="Lathe",
        )

    def validate_params(self, params: dict[str, Any]) -> tuple[bool, str]:
        """Validate terrain generation parameters."""
        octaves = params.get("octaves", 8)
        if not isinstance(octaves, int) or octaves < 1 or octaves > 16:
            return False, "octaves must be an integer between 1 and 16"

        init_roughness = params.get("init_roughness", 1.5)
        if not isinstance(init_roughness, (int, float)) or init_roughness <= 0:
            return False, "init_roughness must be a positive number"

        init_strength = params.get("init_strength", 0.4)
        if not isinstance(init_strength, (int, float)) or init_strength <= 0:
            return False, "init_strength must be a positive number"

        return True, ""

    def get_produced_data_layers(self) -> list[str]:
        return ["elevation", "elevation_raw", "elevation_scalars", "landforms"]

    async def execute(
        self,
        world: World,
        params: dict[str, Any],
        progress_callback: Callable[[float, str], None] | None = None,
    ) -> PluginResult:
        """Generate terrain elevations.

        Args:
            world: World to modify
            params: Generation parameters:
                - octaves (int): Number of noise octaves (default: 8)
                - init_roughness (float): Initial frequency multiplier (default: 1.5)
                - init_strength (float): Initial amplitude multiplier (default: 0.4)
                - roughness (float): Frequency multiplier per octave (default: 2.5)
                - persistence (float): Amplitude multiplier per octave (default: 0.5)
            progress_callback: Optional progress callback

        Returns:
            PluginResult with success status
        """
        # Extract parameters
        octaves = params.get("octaves", 8)
        init_roughness = params.get("init_roughness", 1.5)
        init_strength = params.get("init_strength", 0.4)
        roughness = params.get("roughness", 2.5)
        persistence = params.get("persistence", 0.5)

        if progress_callback:
            progress_callback(0.0, "Initializing terrain generation")

        # Run computation in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            self._generate_terrain_sync,
            world,
            octaves,
            init_roughness,
            init_strength,
            roughness,
            persistence,
            progress_callback,
        )

        if progress_callback:
            progress_callback(1.0, "Terrain generation complete")

        return result

    def _generate_terrain_sync(
        self,
        world: World,
        octaves: int,
        init_roughness: float,
        init_strength: float,
        roughness: float,
        persistence: float,
        progress_callback: Callable[[float, str], None] | None,
    ) -> PluginResult:
        """Synchronous terrain generation (runs in thread pool)."""
        try:
            # Initialize noise generator seed
            if world.params.seed == 0:
                osi.random_seed()
            else:
                osi.seed(seed=world.params.seed)

            radius = world.params.radius
            num_points = world.num_points

            # Initialize raw elevations array
            raw_elevations: NDArray[np.float64] = np.zeros(num_points, dtype=np.float64)

            # Pre-compute roughness and strength values for each octave
            roughness_values: NDArray[np.float64] = np.array(
                [(init_roughness * (roughness**i)) / radius for i in range(octaves)]
            )
            strength_values: NDArray[np.float64] = np.array(
                [(init_strength * (persistence**i)) / radius for i in range(octaves)]
            )

            if progress_callback:
                progress_callback(0.1, "Generating noise octaves")

            # Generate noise for each octave
            for i in range(octaves):
                octave_progress = 0.1 + (0.7 * (i / octaves))
                if progress_callback:
                    progress_callback(octave_progress, f"Processing octave {i + 1}/{octaves}")

                rough_verts: NDArray[np.float64] = world.mesh.points * roughness_values[i]
                octave_elevations: NDArray[np.float64] = np.ones(num_points, dtype=np.float64)

                # Generate noise for each vertex
                for v in range(len(rough_verts)):
                    octave_elevations[v] = osi.noise4(
                        x=rough_verts[v][0],
                        y=rough_verts[v][1],
                        z=rough_verts[v][2],
                        w=1,
                    )

                raw_elevations += octave_elevations * strength_values[i] * radius

            # Store raw elevations
            world.add_data_layer("elevation_raw", raw_elevations, overwrite=True)

            if progress_callback:
                progress_callback(0.8, "Computing elevation scalars")

            # Calculate elevation scalars
            elevation_scalars = (raw_elevations + radius) / radius
            world.add_data_layer("elevation_scalars", elevation_scalars, overwrite=True)

            # Apply scalars to mesh geometry
            world.mesh.points[:, 0] *= elevation_scalars
            world.mesh.points[:, 1] *= elevation_scalars
            world.mesh.points[:, 2] *= elevation_scalars

            if progress_callback:
                progress_callback(0.9, "Rescaling elevations")

            # Rescale elevations to world's elevation range
            emin = np.min(elevation_scalars)
            emax = np.max(elevation_scalars)
            erange: float = emax - emin

            rescaled_elevations = (
                ((elevation_scalars - emin) / erange) * (world.params.zmax - world.params.zmin)
                + world.params.zmin
            )
            world.add_data_layer("elevation", rescaled_elevations, overwrite=True)

            # Create landform mask (land vs ocean)
            sea_level = world.params.zmin + (world.params.zmax - world.params.zmin) * world.params.ocean_percent
            landforms = rescaled_elevations >= sea_level
            world.add_data_layer("landforms", landforms.astype(np.float64), overwrite=True)

            if progress_callback:
                progress_callback(0.95, "Computing normals and warping mesh")

            # Compute normals
            world.compute_normals()

            # Warp mesh by elevations
            world.warp_by_elevation(layer_name="elevation")

            # Calculate statistics
            land_percent = np.sum(landforms) / num_points * 100
            elevation_stats = {
                "min": float(np.min(rescaled_elevations)),
                "max": float(np.max(rescaled_elevations)),
                "mean": float(np.mean(rescaled_elevations)),
                "std": float(np.std(rescaled_elevations)),
                "land_percent": float(land_percent),
                "ocean_percent": float(100 - land_percent),
            }

            return PluginResult(
                success=True,
                message=f"Terrain generated: {land_percent:.1f}% land, {100 - land_percent:.1f}% ocean",
                data=elevation_stats,
            )

        except Exception as e:
            return PluginResult(
                success=False,
                message=f"Terrain generation failed: {e}",
            )
