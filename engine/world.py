import json
import random
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
import opensimplex as osi
from pyvista import Icosphere  # type: ignore Icosphere is a special case of PolyData
from scipy.spatial import KDTree

if TYPE_CHECKING:
    from pyvista.core.pointset import PolyData
    from numpy.typing import NDArray


class World:
    def __init__(
        self,
        name: str = "",
        num_plates: int = 12,
        ocean_percent: float = 0.55,
        octaves: int = 8,
        radius: int = 6378100,
        recursion: int = 9,
        seed: int = 0,
        verbosity: str = "WARN",
        zmax: int = 9567,
        zmin: int = -9567,
        zscale: int = 10,
        ztilt: float = 23.4,
    ) -> None:
        """Initialize the new instance of the World(PolyData) class.

        Args:
            name (str): Name of the world. Must be alphanumeric, and lte 24 characters.
            num_plates (int): Number of tectonic plates to generate. Defaults to 12.
            ocean_percent (float):  Factor used to set sea level relative to elevation range. Defaults to 0.55.
            octaves (int): Factor to set noise complexity. Defaults to 8.
            radius (int): Radius of the world. Defaults to 6378100 m.
            recursion (int): Level of detail of the world mesh. Defaults to 7.
            seed (int): Seed used for noise generation. Defaults to a random integer.
            verbosity (str): Verbosity of the logger. Defaults to "WARN."
            zmax (int): Maximum world elevation. Defaults to 9567 m.
            zmin (int): Minimum world elevation. Defaults to -9567 m.
            zscale (int): Scaling factor used to make elevations visible when displayed. Defaults to 20x.
            ztilt (float): Axial tilt of the world. Defaults to 23.4 degrees.

        """

        # Initialize instance variables.
        self.init_roughness: float = 1.5  # Sets the initial roughness (frequency) of noise.
        self.init_strength: float = 0.4  # Sets the initial strength (amplitude) of noise.
        self.mesh: PolyData = Icosphere(radius=self.radius, nsub=self.recursion, center=self.origin)
        self.name: str = name.strip()
        self.num_plates: int = num_plates
        self.ocean_percent: float = ocean_percent
        self.octaves: int = octaves
        self.origin: tuple[float, float, float] = (
            0.0,
            0.0,
            0.0,
        )  # The origin point of the sphere in (X,Y,Z) coordinates.
        self.persistence: float = 0.5  # Amplitude value to multiply noise by each octave.
        self.radius: int = radius
        self.recursion: int = recursion
        self.roughness: float = 2.5  # Frequency value to multiply noise by each octave.
        self.seed: int = seed
        self.seed_min: int = 1
        self.seed_max: int = 255
        self.seed_string: str = ""
        self.verbosity: str = verbosity
        self.zmax: int = zmax
        self.zmin: int = zmin
        self.zscale: int = zscale
        self.ztilt: float = ztilt

        # Initialize calculated variables.
        self.zrange: int = self.zmax - self.zmin
        self.ocean_point: float = self.zrange * ocean_percent  # Applies the ocean_percent to elevation range.
        self.raw_elevations: NDArray[np.float64] = np.empty(shape=len(self.mesh.points), dtype=np.float64)  # type: ignore
        self.elevation_scalars: NDArray[np.float64] = np.empty(shape=len(self.raw_elevations), dtype=np.float64)
        self.rescaled_elevations: NDArray[np.float64] = np.empty(shape=len(self.raw_elevations), dtype=np.float64)

        # Check name for validity.
        try:
            if not self.name.isalnum() and not len(self.name) <= 24:
                raise ValueError  # TODO: Develop string input sanitization util function.
            elif self.name == "":
                self.name = self._get_name()
                pass
            else:
                pass
        except ValueError:
            raise ValueError  # TODO: Implement error handling.

        # Check seed.
        try:
            if self.seed != 0 and (self.seed < self.seed_min or self.seed > self.seed_max):
                self.seed = 0
                self.seed_string = "Random"
            else:
                self.seed_string = str(object=self.seed)
                pass
        except ValueError:
            raise ValueError  # TODO: Implement error handling.
        except TypeError:
            raise TypeError  # TODO: Implement error handling.

    def _get_name(self) -> str:
        """Return a random planet name from planetnames.json."""
        file_path = Path(Path(__file__).parents[2], "planetnames.json")

        try:
            with Path.open(file_path, "r") as f:
                data: ... = json.load(fp=f)
                names: ... = data["planetNames"]
                self.name = random.choice(seq=names)
        except FileNotFoundError:
            raise FileNotFoundError  # TODO: Implement error handling.

        return self.name

    def generate_elevations(self) -> None:
        # Initialize noise generator seed.
        if self.seed == 0:
            osi.random_seed()
        else:
            osi.seed(self.seed)

        # Initialize elevations array.
        raw_elevations = np.ones(shape=len(self.mesh.points), dtype=np.float64)

        # Pre-compute roughness and strength values for each octave
        roughness_values = np.array(
            [(self.init_roughness * (self.roughness**i)) / self.radius for i in range(self.octaves)]
        )
        strength_values = np.array(
            [(self.init_strength * (self.persistence**i)) / self.radius for i in range(self.octaves)]
        )

        for i in range(self.octaves):
            rough_verts = self.mesh.points * roughness_values[i]
            octave_elevations = np.ones(len(self.mesh.points), dtype=np.float64)

            for v in range(len(rough_verts)):
                octave_elevations[v] = osi.noise4(
                    x=rough_verts[v][0],
                    y=rough_verts[v][1],
                    z=rough_verts[v][2],
                    w=1,
                )

            raw_elevations += octave_elevations * strength_values[i] * self.radius

        # Calculate elevation scalars.
        elevation_scalars = (raw_elevations + self.radius) / self.radius

        # Apply elevation scalars to mesh.
        self.mesh.points[:, 0] *= elevation_scalars  # type: ignore
        self.mesh.points[:, 1] *= elevation_scalars  # type: ignore
        self.mesh.points[:, 2] *= elevation_scalars  # type: ignore

        # Calculate constants for rescaling.
        erange = np.max(raw_elevations) - np.min(raw_elevations)

        # Rescale elevations.
        rescaled_elevations = ((raw_elevations - np.min(raw_elevations)) / erange) * self.zrange + self.zmin

        # Add rescaled elevations as scalar dataset.
        self.mesh.point_data["Elevations"] = rescaled_elevations

    def create_tectonic_plates(self) -> None:
        """Create tectonic plates from the 3D mesh.

        Args:
            num_plates (int): Number of tectonic plates to create.
        """
        # Randomly seed plate centers
        plate_centers: NDArray[np.float64] = self.mesh.points[
            np.random.choice(len(self.mesh.points), self.num_plates, replace=False)
        ]

        # Create a KDTree for fast nearest-neighbor lookup
        tree = KDTree(plate_centers)

        # Assign each point to the nearest plate center
        distances: float | list[int]  # type: ignore
        plate_indices: int | list[int]

        distances, plate_indices = tree.query(x=self.mesh.points)  # type: ignore

        # Store the plate indices as a scalar dataset
        self.mesh.point_data["PlateIndices"] = plate_indices  # type: ignore

        # Optionally, you can visualize the plates by assigning random colors to each plate
        plate_colors = np.random.rand(self.num_plates, 3)
        colors = plate_colors[plate_indices]
        self.mesh.point_data["PlateColors"] = colors

        print(f"Created {self.num_plates} tectonic plates.")
