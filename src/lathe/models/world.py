"""World model representing a generated planetary world."""

from dataclasses import dataclass
from typing import Any
from uuid import UUID, uuid4

import numpy as np
from numpy.typing import NDArray
from pyvista import Icosphere, PolyData


@dataclass
class WorldParameters:
    """Parameters for world generation."""

    name: str = ""
    radius: int = 6378100  # Earth radius in meters
    recursion: int = 6  # Mesh subdivision level
    seed: int = 0  # Random seed (0 = random)
    ocean_percent: float = 0.55
    zmax: int = 9567  # Maximum elevation in meters
    zmin: int = -9567  # Minimum elevation in meters
    zscale: float = 20.0  # Visualization scale factor
    ztilt: float = 23.4  # Axial tilt in degrees


class World:
    """Represents a generated planetary world.

    The World object contains:
    - A 3D mesh (PyVista Icosphere)
    - Data layers stored as point_data on the mesh
    - Generation parameters and metadata
    """

    def __init__(self, params: WorldParameters | None = None, world_id: UUID | None = None):
        """Initialize a new world.

        Args:
            params: World generation parameters
            world_id: Optional UUID for the world (generated if not provided)
        """
        self.id = world_id or uuid4()
        self.params = params or WorldParameters()

        # Initialize mesh
        self.mesh: PolyData = Icosphere(
            radius=self.params.radius,
            nsub=self.params.recursion,
            center=(0.0, 0.0, 0.0),
        )

        # Store original points for potential reset
        self._original_points: NDArray[np.float64] = self.mesh.points.copy()

        # Metadata
        self.metadata: dict[str, Any] = {
            "generation_complete": False,
            "pipeline_steps": [],
            "created_at": None,
            "generation_time_seconds": 0.0,
        }

    @property
    def num_points(self) -> int:
        """Number of mesh points."""
        return len(self.mesh.points)

    @property
    def num_faces(self) -> int:
        """Number of mesh faces."""
        return self.mesh.n_cells

    def add_data_layer(
        self,
        name: str,
        data: NDArray[np.float64],
        overwrite: bool = False,
    ) -> None:
        """Add a data layer to the mesh.

        Args:
            name: Name of the data layer
            data: Array of values (must match number of mesh points)
            overwrite: Whether to overwrite existing layer

        Raises:
            ValueError: If data length doesn't match mesh points or layer exists
        """
        if len(data) != self.num_points:
            msg = f"Data length {len(data)} doesn't match mesh points {self.num_points}"
            raise ValueError(msg)

        if name in self.mesh.point_data and not overwrite:
            msg = f"Data layer '{name}' already exists. Set overwrite=True to replace."
            raise ValueError(msg)

        self.mesh.point_data[name] = data

    def get_data_layer(self, name: str) -> NDArray[np.float64] | None:
        """Get a data layer from the mesh.

        Args:
            name: Name of the data layer

        Returns:
            Data array or None if not found
        """
        return self.mesh.point_data.get(name)

    def has_data_layer(self, name: str) -> bool:
        """Check if a data layer exists.

        Args:
            name: Name of the data layer

        Returns:
            True if layer exists
        """
        return name in self.mesh.point_data

    def list_data_layers(self) -> list[str]:
        """List all available data layers.

        Returns:
            List of data layer names
        """
        return list(self.mesh.point_data.keys())

    def reset_mesh_geometry(self) -> None:
        """Reset mesh geometry to original sphere."""
        self.mesh.points[:] = self._original_points.copy()

    def warp_by_elevation(self, layer_name: str = "elevation", factor: float | None = None) -> None:
        """Warp mesh geometry based on elevation data.

        Args:
            layer_name: Name of elevation data layer
            factor: Warping factor (defaults to self.params.zscale)
        """
        if not self.has_data_layer(layer_name):
            msg = f"Data layer '{layer_name}' not found"
            raise ValueError(msg)

        factor = factor if factor is not None else -self.params.zscale

        self.mesh.warp_by_scalar(
            scalars=layer_name,
            factor=factor,
            inplace=True,
        )

    def compute_normals(self) -> None:
        """Compute mesh normals."""
        self.mesh.compute_normals(inplace=True)

    def get_neighbors(
        self,
        point_index: int,
        radius: float,
    ) -> NDArray[np.int64]:
        """Get indices of points within a given radius of a point.

        Args:
            point_index: Index of the center point
            radius: Search radius in meters

        Returns:
            Array of point indices within radius
        """
        center = self.mesh.points[point_index]
        distances = np.linalg.norm(self.mesh.points - center, axis=1)
        return np.where(distances <= radius)[0]

    def to_dict(self) -> dict[str, Any]:
        """Convert world to dictionary representation.

        Returns:
            Dictionary containing world metadata
        """
        return {
            "id": str(self.id),
            "name": self.params.name,
            "parameters": {
                "radius": self.params.radius,
                "recursion": self.params.recursion,
                "seed": self.params.seed,
                "ocean_percent": self.params.ocean_percent,
                "zmax": self.params.zmax,
                "zmin": self.params.zmin,
                "zscale": self.params.zscale,
                "ztilt": self.params.ztilt,
            },
            "metadata": self.metadata,
            "num_points": self.num_points,
            "num_faces": self.num_faces,
            "data_layers": self.list_data_layers(),
        }
