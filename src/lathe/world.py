import json  # noqa: D100
import random
from pathlib import Path

import numpy as np
import opensimplex as osi
from numba import prange
from pyvista import Icosphere
from pyvista import pyvista_ndarray as PVNDArray


class World(object):
    def __init__(
        self,
        init_roughness: float = 1.5,
        init_strength: float = 0.4,
        name: str = "",
        ocean_percent: float = 0.55,
        octaves: int = 8,
        origin: tuple = (0.0, 0.0, 0.0),
        persistence: float = 0.5,
        radius: int = 6378100,
        recursion: int = 7,
        roughness: float = 2.5,
        seed: int = 0,
        verbosity: str = "WARN",
        zmax: int = 9567,
        zmin: int = -9567,
        zscale: int = 20,
        ztilt: float = 23.4,
    ) -> None:
        """Initialize the new instance of the World(PolyData) class.

        Args:
            init_roughness (float): Sets the initial roughness (frequency) of the first octave of noise.
            init_strength (float): Sets the initial strength (amplitude) of the first octave of noise.
            name (str): Name of the world. Defaults to "".
            ocean_percent (float):  Factor used to set sea level relative to elevation range. Defaults to 0.55,
            octaves (int): Factor to set noise complexity. Defaults to 8.
            origin (tuple): The origin point of the world in (X,Y,Z) coordinates. Defaults to (0.0, 0.0, 0.0).
            persistence (float): Multiply strength by this much per octave.
            radius (int): Radius of the world. Defaults to 6378100 m.
            recursion (int): Level of detail of the world mesh. Defaults to 7.
            roughness (float): Multiply roughness by this much per octave.
            scale (int): Scaling factor used to make elevations visible when displayed. Defaults to 20x.
            seed (int): Seed used for noise generation. Defaults to a random integer.
            verbosity (str): Verbosity of the logger. Defaults to "WARN."
            zmax (int): Maximum world elevation. Defaults to 9567 m.
            zmin (int): Minimum world elevation. Defaults to -9567 m.
            ztilt (float): Axial tilt of the world. Defaults to 23.4 degrees.

        """
        # Initialize variables and pre-calculate values.
        name.strip()
        seed_min: int = 1
        seed_max: int = 255
        seed_string: str = ""
        zrange: int = zmax - zmin
        ocean_point: float = zrange * ocean_percent

        # Initialize instance variables.
        self.elevation_scalars: PVNDArray = []
        self.init_roughness = init_roughness
        self.init_strength = init_strength
        self.name = name
        self.ocean_percent = ocean_percent
        self.ocean_point = ocean_point
        self.octaves = octaves
        self.origin = origin
        self.persistence = persistence
        self.radius = radius
        self.raw_elevations: PVNDArray = []
        self.recursion = recursion
        self.rescaled_elevations: PVNDArray = []
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
                raise ValueError
            elif self.name == "":
                self.name = self.get_name()
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

    def get_name(self) -> str:
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
        def generate_raw_elevations(self) -> PVNDArray:
            # Initialize noise generator seed.
            if self.seed == 0:
                osi.random_seed()
            else:
                osi.seed(self.seed)

            # Initialize elevations array.
            raw_elevations = np.ones(shape=len(self.mesh.points), dtype=np.float64)

            # INFO: In Bob's separate-sampling experiment, rough/strength pairs of (1.6, 0.4), (5, 0.2), and (24, 0.02) were good for 3 octaves. The final 3 results were added and then multiplied by 0.4

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

            return raw_elevations

        def calculate_elevation_scalars(self, raw_elevations: PVNDArray) -> PVNDArray:
            # Calculate elevation scalars.
            elevation_scalars = (raw_elevations + self.radius) / self.radius

            # Apply elevation scalars to mesh.
            self.mesh.points[:, 0] *= elevation_scalars
            self.mesh.points[:, 1] *= elevation_scalars
            self.mesh.points[:, 2] *= elevation_scalars

            return elevation_scalars

        def rescale_elevations(zmin, zrange, raw_elevations: PVNDArray) -> PVNDArray:
            """Re-scale (normalize) an array to a given zmin and zmax bound.
            elevations -- The input array.
            zmin -- The desired new min value.
            zmax -- The desired new max value.
            mid -- Optionally rescale the zmin & zmax values separately.
            Mid should be between elevations's existing min and max values.
            mode -- Optionally rescale ONLY the 'zmin' or 'zmax' values.
            u_min -- Optionally specify an absolute value for elevations min.
            u_max -- Optionally specify an absolute value for elevations max.
            (u_min and u_max are useful for snapshotting when you're processing several
            arrays with different ranges and need them to retain their relationship to
            each other within the new zmin and zmax bounds.)

            """
            # Calculate constants.
            emin = np.min(raw_elevations)
            emax = np.max(raw_elevations)
            erange = emax - emin

            # Rescale elevations.
            rescaled_elevations = ((raw_elevations - emin) / erange) * zrange + zmin

            return rescaled_elevations

        # Generate elevation noise, elevation scalars, and rescaled elevation values.
        raw_elevations = generate_raw_elevations(self)
        calculate_elevation_scalars(self, raw_elevations)
        rescaled_elevations = rescale_elevations(self.zmin, self.zrange, raw_elevations)

        # Add rescaled elevations as scalar dataset.
        self.mesh.point_data["Elevations"] = rescaled_elevations
