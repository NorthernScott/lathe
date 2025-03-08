import json  # noqa: D100
import random
from pathlib import Path

import numpy as np
import opensimplex as osi
from numba import prange
from pyvista import Icosphere
from pyvista import pyvista_ndarray as PVNDArray
from scipy.spatial import KDTree


class World:
    def __init__(
        self,
        name: str = "",
        num_plates: int = 12,
        ocean_percent: float = 0.55,
        octaves: int = 8,
        radius: int = 6378100,
        recursion: int = 7,
        seed: int = 0,
        verbosity: str = "WARN",
        zmax: int = 9567,
        zmin: int = -9567,
        zscale: int = 20,
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
        # Initialize variables and pre-calculate values.
        name.strip()  # Strips whitespace and non-displaying characters from name.
        seed_min: int = 1  # OpenSimplex expects a seed value between 1-255.
        seed_max: int = 255  # OpenSimplex expects a seed value between 1-255.
        seed_string: str = ""  # Initializes an empty seed string for use in later output.
        zrange: int = zmax - zmin  # Calculates the elevation range.
        ocean_point: float = zrange * ocean_percent  # Applies the ocean_percent to elevation range.
        init_roughness: float = 1.5  # Sets the initial roughness (frequency) of noise.
        init_strength: float = 0.4  # Sets the initial strength (amplitude) of noise.
        persistence: float = 0.5  # Amplitude value to multiply noise by each octave.
        roughness: float = 2.5  # Frequency value to multiply noise by each octave.
        origin: tuple = (0.0, 0.0, 0.0)  # The origin point of the sphere in (X,Y,Z) coordinates.

        # Initialize instance variables.
        self.elevation_scalars: PVNDArray = PVNDArray([])
        self.init_roughness = init_roughness
        self.init_strength = init_strength
        self.name = name
        self.num_plates = num_plates
        self.ocean_percent = ocean_percent
        self.ocean_point = ocean_point
        self.octaves = octaves
        self.origin = origin
        self.persistence = persistence
        self.radius = radius
        self.raw_elevations: PVNDArray = PVNDArray([])
        self.recursion = recursion
        self.rescaled_elevations: PVNDArray = PVNDArray([])
        self.roughness = roughness
        self.seed = seed
        self.seed_string = seed_string
        self.verbosity = verbosity
        self.zmax = zmax
        self.zmin = zmin
        self.zrange = zrange
        self.zscale = zscale
        self.ztilt = ztilt

        # Initialize mesh.
        self.mesh = Icosphere(radius=self.radius, nsub=self.recursion, center=self.origin)

        # Check name for validity.
        try:
            if not self.name.isalnum() and not len(self.name) <= 24:
                raise ValueError  # TODO: Develop string input sanitization util function.
            elif self.name == "":
                self.name = self._get_name()
                pass
            else:
                pass
        except ValueError as e:
            e

        # Check seed.
        try:
            if self.seed != 0 and (self.seed < seed_min or self.seed > seed_max):
                self.seed = 0
                self.seed_string = "Random"
            else:
                self.seed_string = str(self.seed)
                pass
        except ValueError as e:
            e
        except TypeError as e:
            e

    def _get_name(self) -> str:
        """Return a random planet name from planetnames.json."""
        file_path = Path(Path(__file__).parents[2], "planetnames.json")

        try:
            with Path.open(file_path, "r") as f:
                data = json.load(fp=f)
                names = data["planetNames"]
                self.name = random.choice(seq=names)
        except FileNotFoundError as e:
            e

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

        for i in prange(self.octaves):
            rough_verts = self.mesh.points * roughness_values[i]
            octave_elevations = np.ones(len(self.mesh.points), dtype=np.float64)

            for v in prange(len(rough_verts)):
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
        self.mesh.points[:, 0] *= elevation_scalars
        self.mesh.points[:, 1] *= elevation_scalars
        self.mesh.points[:, 2] *= elevation_scalars

        # Calculate constants for rescaling.
        emin = np.min(raw_elevations)
        emax = np.max(raw_elevations)
        erange = emax - emin

        # Rescale elevations.
        rescaled_elevations = ((raw_elevations - emin) / erange) * self.zrange + self.zmin

        # Add rescaled elevations as scalar dataset.
        self.mesh.point_data["Elevations"] = rescaled_elevations

    def create_tectonic_plates(self, num_plates) -> None:
        """Create tectonic plates from the 3D mesh.

        Args:
            num_plates (int): Number of tectonic plates to create.
        """
        # Randomly seed plate centers
        plate_centers = self.mesh.points[np.random.choice(len(self.mesh.points), num_plates, replace=False)]

        # Create a KDTree for fast nearest-neighbor lookup
        tree = KDTree(plate_centers)

        # Assign each point to the nearest plate center
        distances, plate_indices = tree.query(self.mesh.points)

        # Store the plate indices as a scalar dataset
        self.mesh.point_data["PlateIndices"] = plate_indices

        # Optionally, you can visualize the plates by assigning random colors to each plate
        plate_colors = np.random.rand(num_plates, 3)
        colors = plate_colors[plate_indices]
        self.mesh.point_data["PlateColors"] = colors

        print(f"Created {num_plates} tectonic plates.")
