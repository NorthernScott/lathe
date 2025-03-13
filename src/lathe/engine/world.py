import json
import random
from pathlib import Path
from typing import TYPE_CHECKING
from math import floor

import numpy as np
import opensimplex as osi
from pyvista import Icosphere
from scipy.spatial import KDTree

if TYPE_CHECKING:
    from pyvista.core.pointset import PolyData
    from numpy.typing import NDArray


class World:
    """Class used to initialize, handle, and generate all world information."""
    def __init__(
        self,
        name: str = "",
        ocean_percent: float = 0.55,
        octaves: int = 8,
        radius: int = 6378100,
        recursion: int = 9,
        seed: int = 0,
        verbosity: str = "WARN",
        zmax: int = 9567,
        zmin: int = -9567,
        zscale: float = 15,  # Was: 0.5e-5, -10 or -20
        ztilt: float = 23.4,
    ) -> None:
        """Class used to initialize, handle, and generate all world information.

        Args:
            name (str, optional): Name of the world. Must be alphanumeric, and less-than-or-equal to 24 characters. If none is provided, a random name is generated.

            ocean_percent (float, optional): Factor used to set sea level relative to elevation range. Defaults to 0.55.

            octaves (int, optional): Factor to set noise complexity. Defaults to 8.

            radius (int, optional): Radius of the world in meters. Defaults to 6378100.

            recursion (int, optional): Level of detail of the world mesh. Defaults to 9.

            seed (int, optional): Seed used for noise generation. Defaults to 0.

            verbosity (str, optional): Verbosity of the logger. Defaults to "WARN".

            zmax (int, optional): Maximum world elevation in meters. Defaults to 9567 m.

            zmin (int, optional): Minimum world elevation in meters. Defaults to -9567 m.

            zscale (float, optional): Scaling factor used to make elevations visible when displayed. Defaults to 0.5^-5.

            ztilt (float, optional): Axial tilt of the world in degrees. Defaults to 23.4.
        """

        # Initialize instance variables.
        self.init_roughness: float = 1.5  # Sets the initial roughness (frequency) of noise.
        self.init_strength: float = 0.4  # Sets the initial strength (amplitude) of noise.
        self.name: str = name.strip()
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

        self.ztilt: float = ztilt

        # Initialize mesh.
        self.mesh: PolyData = Icosphere(radius=self.radius, nsub=self.recursion, center=self.origin)

        # Initialize calculated variables.
        self.num_plates: int = floor(self.radius / 500_000)
        self.zscale: float = -zscale
        self.zrange: int = self.zmax - self.zmin
        self.ocean_point: float = self.zrange * ocean_percent  # Applies the ocean_percent to elevation range.

        # Check name for validity.
        try:
            if not self.name.isalnum() and not len(self.name) <= 24:
                pass  # TODO: Develop string input sanitization util function.
            elif self.name == "":
                self.name = self._get_name()
                pass
            else:
                pass
        except ValueError:
            pass  # TODO: Implement error handling.

        # Check seed.
        try:
            if self.seed != 0 and (self.seed < self.seed_min or self.seed > self.seed_max):
                self.seed = 0
                self.seed_string = "Random"
            else:
                self.seed_string = str(object=self.seed)
                pass
        except ValueError:
            pass  # TODO: Implement error handling.
        except TypeError:
            pass  # TODO: Implement error handling.

    def _get_name(self) -> str:
        """Return a random planet name from planetnames.json."""
        file_path = Path(Path(__file__).parents[2], "planetnames.json")

        try:
            with Path.open(file_path, "r") as f:
                data: ... = json.load(fp=f)
                names: ... = data["planetNames"]
                self.name = random.choice(seq=names)
        except FileNotFoundError:
            pass  # TODO: Implement error handling.

        return self.name

    def generate_elevations(self) -> None:
        """Generates raw elevations to be used in world generation. Converts them to scalars and applies them to ```self.world.mesh```."""

        # Initialize noise generator seed.
        if self.seed == 0:
            osi.random_seed()
        else:
            osi.seed(seed=self.seed)

        # Declare raw_elevations array.
        raw_elevations: NDArray[np.float64] = np.zeros(len(self.mesh.points), dtype=np.float64)

        # Pre-compute roughness and strength values for each octave
        roughness_values: NDArray[np.float64] = np.array(
            object=[(self.init_roughness * (self.roughness**i)) / self.radius for i in range(self.octaves)]
        )
        strength_values: NDArray[np.float64] = np.array(
            object=[(self.init_strength * (self.persistence**i)) / self.radius for i in range(self.octaves)]
        )

        for i in range(self.octaves):
            rough_verts: NDArray[np.float64] = self.mesh.points * roughness_values[i]
            octave_elevations: NDArray[np.float64] = np.ones(len(self.mesh.points), dtype=np.float64)

            for v in range(len(rough_verts)):
                octave_elevations[v] = osi.noise4(
                    x=rough_verts[v][0],
                    y=rough_verts[v][1],
                    z=rough_verts[v][2],
                    w=1,
                )

            raw_elevations += octave_elevations * strength_values[i] * self.radius
            self.mesh.point_data["Raw Elevations"] = raw_elevations

        # Calculate elevation scalars.
        elevation_scalars: NDArray[np.float64] = (raw_elevations + self.radius) / self.radius
        self.mesh.point_data["Elevation Scalars"] = elevation_scalars

        # Apply elevation scalars to mesh.
        self.mesh.points[:, 0] *= elevation_scalars  # type: ignore
        self.mesh.points[:, 1] *= elevation_scalars  # type: ignore
        self.mesh.points[:, 2] *= elevation_scalars  # type: ignore

        # Calculate constants for rescaling.
        erange: float = np.max(raw_elevations) - np.min(raw_elevations)

        # Rescale elevations.
        rescaled_elevations = ((raw_elevations - np.min(raw_elevations)) / erange) * self.zrange + self.zmin

        # Add rescaled elevations as scalar dataset.
        self.mesh.point_data["Elevations"] = rescaled_elevations

        # Compute normals.
        self.mesh.compute_normals(inplace=True)

        # Warp mesh by elevations and zscale factor.
        self.mesh.warp_by_scalar(
            scalars="Elevations",
            factor=self.zscale,
            inplace=True,
        )

    def create_tectonic_plates(self, num_plates: int = 0) -> None:
        """
        Create <num_plates> tectonic plates to use in world generation.

        Args:
            num_plates (int, optional): The number of tectonic plates to create. Defaults to the radius / 500,000.
        """
        if num_plates == 0:
            num_plates = self.num_plates
        # Randomly seed plate centers.
        plate_centers: NDArray[np.float64] = self.mesh.points[
            np.random.choice(len(self.mesh.points), num_plates, replace=False)
        ]

        # Ensure plate_centers contains only finite values
        if not np.all(np.isfinite(plate_centers)):
            raise ValueError("plate_centers contains NaN or infinite values")

        # Create a KDTree for fast nearest-neighbor lookup
        tree = KDTree(data=plate_centers)

        # Assign each point to the nearest plate center
        distances, plate_indices = tree.query(x=self.mesh.points)

        # Store the plate indices as a scalar dataset
        self.mesh.point_data["Tectonic Plates"] = plate_indices
