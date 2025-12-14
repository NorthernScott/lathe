"""HDF5-based storage for world mesh data."""

import json
from pathlib import Path
from typing import Any
from uuid import UUID

import h5py
import numpy as np
from numpy.typing import NDArray

from lathe.models.world import World, WorldParameters


class MeshStore:
    """Manages storage and retrieval of world mesh data using HDF5.

    HDF5 file structure:
        /mesh/
            points          - Nx3 array of vertex positions
            faces           - Mx3 array of face indices
            original_points - Nx3 array of original sphere points
        /scalars/
            <layer_name>    - N-length arrays for each data layer
        /metadata/
            parameters      - JSON string of WorldParameters
            world_metadata  - JSON string of world.metadata dict
    """

    def __init__(self, storage_dir: Path | str = "./data/worlds"):
        """Initialize the mesh store.

        Args:
            storage_dir: Directory to store HDF5 files
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _get_file_path(self, world_id: UUID) -> Path:
        """Get HDF5 file path for a world.

        Args:
            world_id: World UUID

        Returns:
            Path to HDF5 file
        """
        return self.storage_dir / f"world_{world_id}.h5"

    def save_world(self, world: World, compress: bool = True) -> Path:
        """Save a world to HDF5.

        Args:
            world: World to save
            compress: Whether to compress data (slower save, smaller file)

        Returns:
            Path to saved file
        """
        file_path = self._get_file_path(world.id)

        compression = "gzip" if compress else None
        compression_opts = 9 if compress else None

        with h5py.File(file_path, "w") as f:
            # Create groups
            mesh_group = f.create_group("mesh")
            scalars_group = f.create_group("scalars")
            metadata_group = f.create_group("metadata")

            # Save mesh geometry
            mesh_group.create_dataset(
                "points",
                data=world.mesh.points,
                compression=compression,
                compression_opts=compression_opts,
            )

            # Save faces (convert to numpy array)
            faces_array = self._extract_faces(world)
            mesh_group.create_dataset(
                "faces",
                data=faces_array,
                compression=compression,
                compression_opts=compression_opts,
            )

            # Save original points
            mesh_group.create_dataset(
                "original_points",
                data=world._original_points,
                compression=compression,
                compression_opts=compression_opts,
            )

            # Save all data layers
            for layer_name in world.list_data_layers():
                layer_data = world.get_data_layer(layer_name)
                if layer_data is not None:
                    scalars_group.create_dataset(
                        layer_name,
                        data=layer_data,
                        compression=compression,
                        compression_opts=compression_opts,
                    )

            # Save metadata
            params_dict = {
                "name": world.params.name,
                "radius": world.params.radius,
                "recursion": world.params.recursion,
                "seed": world.params.seed,
                "ocean_percent": world.params.ocean_percent,
                "zmax": world.params.zmax,
                "zmin": world.params.zmin,
                "zscale": world.params.zscale,
                "ztilt": world.params.ztilt,
            }

            metadata_group.attrs["parameters"] = json.dumps(params_dict)
            metadata_group.attrs["world_id"] = str(world.id)
            metadata_group.attrs["world_metadata"] = json.dumps(
                world.metadata,
                default=str,  # Convert non-serializable types to strings
            )

        return file_path

    def load_world(self, world_id: UUID) -> World:
        """Load a world from HDF5.

        Args:
            world_id: UUID of world to load

        Returns:
            Loaded World object

        Raises:
            FileNotFoundError: If world file doesn't exist
        """
        file_path = self._get_file_path(world_id)

        if not file_path.exists():
            msg = f"World file not found: {file_path}"
            raise FileNotFoundError(msg)

        with h5py.File(file_path, "r") as f:
            # Load parameters
            params_json = f["metadata"].attrs["parameters"]
            params_dict = json.loads(params_json)
            params = WorldParameters(**params_dict)

            # Create world
            world = World(params=params, world_id=world_id)

            # Load mesh geometry
            world.mesh.points[:] = f["mesh/points"][:]

            # Note: We don't reload faces as PyVista creates them automatically
            # based on the Icosphere topology

            # Load original points
            world._original_points = f["mesh/original_points"][:]

            # Load all scalar data layers
            if "scalars" in f:
                for layer_name in f["scalars"].keys():
                    layer_data = f[f"scalars/{layer_name}"][:]
                    world.add_data_layer(layer_name, layer_data, overwrite=True)

            # Load metadata
            if "world_metadata" in f["metadata"].attrs:
                metadata_json = f["metadata"].attrs["world_metadata"]
                world.metadata = json.loads(metadata_json)

            # Recompute normals
            world.compute_normals()

        return world

    def delete_world(self, world_id: UUID) -> bool:
        """Delete a world's HDF5 file.

        Args:
            world_id: UUID of world to delete

        Returns:
            True if deleted, False if file didn't exist
        """
        file_path = self._get_file_path(world_id)

        if file_path.exists():
            file_path.unlink()
            return True
        return False

    def world_exists(self, world_id: UUID) -> bool:
        """Check if a world file exists.

        Args:
            world_id: World UUID

        Returns:
            True if world file exists
        """
        return self._get_file_path(world_id).exists()

    def list_worlds(self) -> list[dict[str, Any]]:
        """List all worlds in the storage directory.

        Returns:
            List of world info dictionaries
        """
        worlds = []

        for file_path in self.storage_dir.glob("world_*.h5"):
            try:
                with h5py.File(file_path, "r") as f:
                    world_id = f["metadata"].attrs.get("world_id", "unknown")
                    params_json = f["metadata"].attrs.get("parameters", "{}")
                    params = json.loads(params_json)

                    worlds.append(
                        {
                            "world_id": world_id,
                            "name": params.get("name", "Unnamed"),
                            "file_path": str(file_path),
                            "file_size_mb": file_path.stat().st_size / (1024 * 1024),
                            "num_points": f["mesh/points"].shape[0],
                            "data_layers": list(f["scalars"].keys()) if "scalars" in f else [],
                        }
                    )
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

        return worlds

    def get_world_info(self, world_id: UUID) -> dict[str, Any] | None:
        """Get information about a world without loading it fully.

        Args:
            world_id: World UUID

        Returns:
            World info dictionary or None if not found
        """
        file_path = self._get_file_path(world_id)

        if not file_path.exists():
            return None

        try:
            with h5py.File(file_path, "r") as f:
                params_json = f["metadata"].attrs.get("parameters", "{}")
                params = json.loads(params_json)

                metadata_json = f["metadata"].attrs.get("world_metadata", "{}")
                metadata = json.loads(metadata_json)

                return {
                    "world_id": str(world_id),
                    "name": params.get("name", "Unnamed"),
                    "parameters": params,
                    "metadata": metadata,
                    "file_path": str(file_path),
                    "file_size_mb": file_path.stat().st_size / (1024 * 1024),
                    "num_points": f["mesh/points"].shape[0],
                    "num_faces": f["mesh/faces"].shape[0] if "mesh/faces" in f else 0,
                    "data_layers": list(f["scalars"].keys()) if "scalars" in f else [],
                }
        except Exception as e:
            print(f"Error reading world info: {e}")
            return None

    def _extract_faces(self, world: World) -> NDArray[np.int64]:
        """Extract face indices from PyVista mesh.

        Args:
            world: World with mesh

        Returns:
            Nx3 array of face indices
        """
        # PyVista stores faces as [n_points, i1, i2, ..., in, n_points, ...]
        # We need to extract just the triangle indices
        faces_flat = world.mesh.faces
        n_faces = world.num_faces

        faces_array = np.zeros((n_faces, 3), dtype=np.int64)

        idx = 0
        for i in range(n_faces):
            n_points = faces_flat[idx]
            if n_points == 3:  # Triangle
                faces_array[i] = faces_flat[idx + 1 : idx + 4]
            idx += n_points + 1

        return faces_array

    def export_to_vtk(self, world_id: UUID, output_path: Path | str) -> None:
        """Export a world to VTK format for external visualization.

        Args:
            world_id: World UUID
            output_path: Path to output VTK file
        """
        world = self.load_world(world_id)
        world.mesh.save(str(output_path))

    def get_data_layer(
        self,
        world_id: UUID,
        layer_name: str,
    ) -> NDArray[np.float64] | None:
        """Load a single data layer without loading entire world.

        Args:
            world_id: World UUID
            layer_name: Name of data layer

        Returns:
            Data array or None if not found
        """
        file_path = self._get_file_path(world_id)

        if not file_path.exists():
            return None

        try:
            with h5py.File(file_path, "r") as f:
                if f"scalars/{layer_name}" in f:
                    return f[f"scalars/{layer_name}"][:]
        except Exception as e:
            print(f"Error loading data layer: {e}")

        return None
