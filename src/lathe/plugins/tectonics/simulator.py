"""Tectonic plate simulation plugin with realistic geological processes."""

import asyncio
from typing import Any, Callable

import numpy as np
from numpy.typing import NDArray
from pyvista import LookupTable
from scipy.spatial import KDTree

from lathe.models.world import World
from lathe.plugins.base import PluginMetadata, PluginResult, SimulationPlugin


class TectonicsSimulatorPlugin(SimulationPlugin):
    """Simulates tectonic plates with realistic geological processes.

    This plugin:
    1. Generates tectonic plates with random velocities
    2. Simulates plate movement over time
    3. Detects boundary types (convergent/divergent/transform)
    4. Modifies elevation based on plate interactions
    5. Creates mountains at collision zones
    6. Creates trenches at subduction zones
    7. Creates ridges at spreading centers
    """

    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="tectonics",
            version="2.0.0",
            dependencies=["terrain"],
            description="Simulates tectonic plates with realistic geological processes",
            author="Lathe",
        )

    def validate_params(self, params: dict[str, Any]) -> tuple[bool, str]:
        """Validate tectonics parameters."""
        num_plates = params.get("num_plates", 12)
        if not isinstance(num_plates, int) or num_plates < 2 or num_plates > 100:
            return False, "num_plates must be an integer between 2 and 100"

        simulation_steps = params.get("simulation_steps", 50)
        if not isinstance(simulation_steps, int) or simulation_steps < 1 or simulation_steps > 1000:
            return False, "simulation_steps must be an integer between 1 and 1000"

        return True, ""

    def get_required_data_layers(self) -> list[str]:
        return ["elevation", "landforms"]

    def get_produced_data_layers(self) -> list[str]:
        return ["plate_id", "plate_distance", "plate_boundary", "boundary_type"]

    async def execute(
        self,
        world: World,
        params: dict[str, Any],
        progress_callback: Callable[[float, str], None] | None = None,
    ) -> PluginResult:
        """Simulate tectonic plates.

        Args:
            world: World to modify
            params: Generation parameters:
                - num_plates (int): Number of tectonic plates (default: 12)
                - simulation_steps (int): Number of simulation iterations (default: 50)
                - mountain_strength (float): Strength of mountain formation (default: 1.0)
                - trench_strength (float): Strength of trench formation (default: 0.8)
                - ridge_strength (float): Strength of ridge formation (default: 0.5)
            progress_callback: Optional progress callback

        Returns:
            PluginResult with success status
        """
        num_plates = params.get("num_plates", 12)
        simulation_steps = params.get("simulation_steps", 50)

        if progress_callback:
            progress_callback(0.0, "Initializing tectonic simulation")

        # Run computation in thread pool
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            self._simulate_tectonics_sync,
            world,
            num_plates,
            simulation_steps,
            params,
            progress_callback,
        )

        if progress_callback:
            progress_callback(1.0, "Tectonic simulation complete")

        return result

    def _simulate_tectonics_sync(
        self,
        world: World,
        num_plates: int,
        simulation_steps: int,
        params: dict[str, Any],
        progress_callback: Callable[[float, str], None] | None,
    ) -> PluginResult:
        """Synchronous tectonics simulation (runs in thread pool)."""
        try:
            # Get parameters
            mountain_strength = params.get("mountain_strength", 1.0)
            trench_strength = params.get("trench_strength", 0.8)
            ridge_strength = params.get("ridge_strength", 0.5)

            if progress_callback:
                progress_callback(0.05, "Generating tectonic plates")

            # Step 1: Generate plates
            plate_data = self._generate_plates(world, num_plates)

            if progress_callback:
                progress_callback(0.15, "Assigning plate velocities")

            # Step 2: Assign velocities
            plate_velocities = self._assign_plate_velocities(world, num_plates, plate_data["plate_centers"])

            if progress_callback:
                progress_callback(0.20, "Building neighbor graph")

            # Step 3: Build neighbor graph for boundary detection
            neighbors = self._build_neighbor_graph(world)

            # Get initial elevation
            elevation = world.get_data_layer("elevation").copy()
            landforms = world.get_data_layer("landforms")

            if progress_callback:
                progress_callback(0.25, f"Simulating {simulation_steps} time steps")

            # Step 4: Simulate plate movement and interactions
            for step in range(simulation_steps):
                if progress_callback and step % 10 == 0:
                    progress = 0.25 + (step / simulation_steps) * 0.50
                    progress_callback(progress, f"Simulating step {step + 1}/{simulation_steps}")

                # Detect boundaries
                boundaries = self._detect_boundaries(
                    plate_data["plate_ids"],
                    neighbors,
                )

                # Classify boundary types
                boundary_types = self._classify_boundaries(
                    world,
                    boundaries,
                    plate_data["plate_ids"],
                    plate_velocities,
                    neighbors,
                )

                # Modify elevation based on boundary interactions
                elevation = self._apply_tectonic_forces(
                    elevation,
                    landforms,
                    boundaries,
                    boundary_types,
                    mountain_strength,
                    trench_strength,
                    ridge_strength,
                )

            if progress_callback:
                progress_callback(0.80, "Applying elevation changes")

            # Update world with modified elevation
            world.add_data_layer("elevation", elevation, overwrite=True)

            # Warp mesh by new elevation
            world.warp_by_elevation(layer_name="elevation", factor=10.0)
            world.compute_normals()

            if progress_callback:
                progress_callback(0.85, "Storing plate data")

            # Store plate data
            world.add_data_layer("plate_id", plate_data["plate_ids"].astype(np.float64), overwrite=True)
            world.add_data_layer("plate_distance", plate_data["plate_distances"].astype(np.float64), overwrite=True)

            # Create boundary mask
            boundary_mask = np.zeros(world.num_points)
            for boundary_point in boundaries:
                boundary_mask[boundary_point] = 1.0
            world.add_data_layer("plate_boundary", boundary_mask, overwrite=True)

            # Store boundary types (0=none, 1=convergent, 2=divergent, 3=transform)
            boundary_type_layer = np.zeros(world.num_points)
            for point, btype in boundary_types.items():
                if btype == "convergent":
                    boundary_type_layer[point] = 1.0
                elif btype == "divergent":
                    boundary_type_layer[point] = 2.0
                elif btype == "transform":
                    boundary_type_layer[point] = 3.0
            world.add_data_layer("boundary_type", boundary_type_layer, overwrite=True)

            if progress_callback:
                progress_callback(0.90, "Computing statistics")

            # Calculate statistics
            stats = self._calculate_stats(
                plate_data["plate_ids"],
                landforms,
                boundaries,
                boundary_types,
                num_plates,
            )

            # Store metadata
            world.metadata["tectonic_plates"] = {
                "num_plates": num_plates,
                "simulation_steps": simulation_steps,
                "plate_centers": plate_data["plate_centers"].tolist(),
                "plate_velocities": {int(k): v.tolist() for k, v in plate_velocities.items()},
                "stats": stats,
            }

            if progress_callback:
                progress_callback(0.95, "Creating visualization colormap")

            # Create colormap for visualization
            annotations = {i: f"Plate {i}" for i in range(num_plates)}
            color_map = LookupTable(
                cmap="Accent",
                n_values=num_plates,
                scalar_range=(0, num_plates - 1),
                annotations=annotations,
            )

            world.metadata["tectonic_colormap"] = color_map

            return PluginResult(
                success=True,
                message=f"Simulated {num_plates} tectonic plates over {simulation_steps} steps",
                data={
                    "num_plates": num_plates,
                    "simulation_steps": simulation_steps,
                    "boundaries_created": len(boundaries),
                    "convergent_boundaries": stats["boundary_counts"]["convergent"],
                    "divergent_boundaries": stats["boundary_counts"]["divergent"],
                    "transform_boundaries": stats["boundary_counts"]["transform"],
                },
            )

        except Exception as e:
            return PluginResult(
                success=False,
                message=f"Tectonic simulation failed: {e}",
            )

    def _generate_plates(self, world: World, num_plates: int) -> dict[str, Any]:
        """Generate tectonic plates using Voronoi segmentation.

        Args:
            world: World object
            num_plates: Number of plates to create

        Returns:
            Dictionary with plate_ids, plate_distances, and plate_centers
        """
        # Generate random plate centers from mesh points
        plate_centers = world.mesh.points[
            np.random.choice(world.num_points, num_plates, replace=False)
        ]

        # Build KDTree for nearest-neighbor assignment
        tree = KDTree(data=plate_centers)

        # Assign each mesh point to nearest plate
        distances, plate_indices = tree.query(x=world.mesh.points)

        return {
            "plate_ids": plate_indices,
            "plate_distances": distances,
            "plate_centers": plate_centers,
        }

    def _assign_plate_velocities(
        self,
        world: World,
        num_plates: int,
        plate_centers: NDArray,
    ) -> dict[int, NDArray]:
        """Assign random tangent velocities to each plate.

        Velocities are tangent to the sphere surface at the plate center.

        Args:
            world: World object
            num_plates: Number of plates
            plate_centers: Center points of each plate

        Returns:
            Dictionary mapping plate_id to velocity vector (3D)
        """
        velocities = {}

        for plate_id in range(num_plates):
            center = plate_centers[plate_id]

            # Normalize center to get radial direction
            radial = center / np.linalg.norm(center)

            # Generate a random tangent vector
            # Start with a random vector
            random_vec = np.random.randn(3)

            # Make it tangent by removing radial component
            tangent = random_vec - np.dot(random_vec, radial) * radial

            # Normalize and scale
            tangent = tangent / np.linalg.norm(tangent)

            # Random speed between 0.5 and 2.0
            speed = np.random.uniform(0.5, 2.0)
            velocity = tangent * speed

            velocities[plate_id] = velocity

        return velocities

    def _build_neighbor_graph(self, world: World) -> dict[int, list[int]]:
        """Build graph of neighboring points on the mesh.

        Args:
            world: World object

        Returns:
            Dictionary mapping point index to list of neighbor indices
        """
        neighbors = {i: [] for i in range(world.num_points)}

        # Extract faces (triangles)
        faces = world.mesh.faces.reshape(-1, 4)[:, 1:]  # Skip the "3" prefix

        # For each face, all three vertices are neighbors
        for face in faces:
            a, b, c = face
            neighbors[a].extend([b, c])
            neighbors[b].extend([a, c])
            neighbors[c].extend([a, b])

        # Remove duplicates
        for point in neighbors:
            neighbors[point] = list(set(neighbors[point]))

        return neighbors

    def _detect_boundaries(
        self,
        plate_ids: NDArray,
        neighbors: dict[int, list[int]],
    ) -> set[int]:
        """Detect plate boundary points.

        A point is on a boundary if any of its neighbors belong to a different plate.

        Args:
            plate_ids: Array of plate IDs for each point
            neighbors: Neighbor graph

        Returns:
            Set of point indices that are on plate boundaries
        """
        boundaries = set()

        for point, neighbor_list in neighbors.items():
            point_plate = plate_ids[point]

            for neighbor in neighbor_list:
                if plate_ids[neighbor] != point_plate:
                    boundaries.add(point)
                    break

        return boundaries

    def _classify_boundaries(
        self,
        world: World,
        boundaries: set[int],
        plate_ids: NDArray,
        plate_velocities: dict[int, NDArray],
        neighbors: dict[int, list[int]],
    ) -> dict[int, str]:
        """Classify boundary points as convergent, divergent, or transform.

        Args:
            world: World object
            boundaries: Set of boundary point indices
            plate_ids: Array of plate IDs
            plate_velocities: Dictionary of plate velocities
            neighbors: Neighbor graph

        Returns:
            Dictionary mapping boundary point to boundary type
        """
        boundary_types = {}

        for point in boundaries:
            point_plate = plate_ids[point]
            point_pos = world.mesh.points[point]
            point_vel = plate_velocities[point_plate]

            # Find neighbors in different plates
            neighboring_plates = set()
            for neighbor in neighbors[point]:
                neighbor_plate = plate_ids[neighbor]
                if neighbor_plate != point_plate:
                    neighboring_plates.add(neighbor_plate)

            # Check each neighboring plate
            convergence_scores = []
            for neighbor_plate in neighboring_plates:
                neighbor_vel = plate_velocities[neighbor_plate]

                # Relative velocity
                relative_vel = point_vel - neighbor_vel

                # Direction from point to neighbor plate center
                # (approximate - just use first neighbor in that plate)
                neighbor_point = None
                for n in neighbors[point]:
                    if plate_ids[n] == neighbor_plate:
                        neighbor_point = n
                        break

                if neighbor_point is not None:
                    neighbor_pos = world.mesh.points[neighbor_point]
                    direction = neighbor_pos - point_pos

                    # Normalize
                    direction = direction / (np.linalg.norm(direction) + 1e-10)

                    # Dot product: positive = moving apart, negative = moving together
                    convergence = -np.dot(relative_vel, direction)
                    convergence_scores.append(convergence)

            # Average convergence across all neighboring plates
            if convergence_scores:
                avg_convergence = np.mean(convergence_scores)

                if avg_convergence > 0.3:
                    boundary_types[point] = "convergent"
                elif avg_convergence < -0.3:
                    boundary_types[point] = "divergent"
                else:
                    boundary_types[point] = "transform"
            else:
                boundary_types[point] = "transform"

        return boundary_types

    def _apply_tectonic_forces(
        self,
        elevation: NDArray,
        landforms: NDArray,
        boundaries: set[int],
        boundary_types: dict[int, str],
        mountain_strength: float,
        trench_strength: float,
        ridge_strength: float,
    ) -> NDArray:
        """Apply tectonic forces to modify elevation.

        Args:
            elevation: Current elevation array
            landforms: Landform mask (1=land, 0=ocean)
            boundaries: Set of boundary points
            boundary_types: Dictionary of boundary types
            mountain_strength: Strength of mountain formation
            trench_strength: Strength of trench formation
            ridge_strength: Strength of ridge formation

        Returns:
            Modified elevation array
        """
        new_elevation = elevation.copy()

        for point in boundaries:
            boundary_type = boundary_types.get(point, "transform")
            is_land = landforms[point] > 0.5
            current_elev = elevation[point]

            if boundary_type == "convergent":
                # Convergent boundaries: collision creates mountains or trenches
                if is_land:
                    # Continental-continental collision → Mountains
                    new_elevation[point] += mountain_strength * 50.0
                else:
                    # Oceanic-oceanic or oceanic-continental → Trench
                    new_elevation[point] -= trench_strength * 80.0

            elif boundary_type == "divergent":
                # Divergent boundaries: spreading creates ridges
                if not is_land:
                    # Mid-ocean ridge
                    new_elevation[point] += ridge_strength * 30.0
                else:
                    # Continental rift
                    new_elevation[point] -= ridge_strength * 20.0

            elif boundary_type == "transform":
                # Transform boundaries: minimal elevation change
                # Add small random noise to simulate fault activity
                new_elevation[point] += np.random.uniform(-5.0, 5.0)

        return new_elevation

    def _calculate_stats(
        self,
        plate_ids: NDArray,
        landforms: NDArray,
        boundaries: set[int],
        boundary_types: dict[int, str],
        num_plates: int,
    ) -> dict[str, Any]:
        """Calculate statistics for tectonic simulation.

        Args:
            plate_ids: Array of plate IDs
            landforms: Landform mask
            boundaries: Set of boundary points
            boundary_types: Dictionary of boundary types
            num_plates: Number of plates

        Returns:
            Dictionary of statistics
        """
        stats = {"plates": {}, "boundary_counts": {}}

        # Plate statistics
        for plate_id in range(num_plates):
            mask = plate_ids == plate_id
            plate_points = np.sum(mask)
            land_points = np.sum(mask & (landforms > 0.5))
            ocean_points = plate_points - land_points

            stats["plates"][f"plate_{plate_id}"] = {
                "total_points": int(plate_points),
                "land_points": int(land_points),
                "ocean_points": int(ocean_points),
                "land_percent": float(land_points / plate_points * 100) if plate_points > 0 else 0.0,
            }

        # Boundary type counts
        boundary_counts = {"convergent": 0, "divergent": 0, "transform": 0}
        for btype in boundary_types.values():
            boundary_counts[btype] += 1

        stats["boundary_counts"] = boundary_counts
        stats["total_boundaries"] = len(boundaries)

        return stats
