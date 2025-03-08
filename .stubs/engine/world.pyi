from _typeshed import Incomplete
from pyvista import pyvista_ndarray as PVNDArray

class World:
    elevation_scalars: PVNDArray
    init_roughness: Incomplete
    init_strength: Incomplete
    name: Incomplete
    num_plates: Incomplete
    ocean_percent: Incomplete
    ocean_point: Incomplete
    octaves: Incomplete
    origin: Incomplete
    persistence: Incomplete
    radius: Incomplete
    raw_elevations: PVNDArray
    recursion: Incomplete
    rescaled_elevations: PVNDArray
    roughness: Incomplete
    seed: Incomplete
    seed_string: Incomplete
    verbosity: Incomplete
    zmax: Incomplete
    zmin: Incomplete
    zrange: Incomplete
    zscale: Incomplete
    ztilt: Incomplete
    mesh: Incomplete
    def __init__(self, name: str = '', num_plates: int = 12, ocean_percent: float = 0.55, octaves: int = 8, radius: int = 6378100, recursion: int = 7, seed: int = 0, verbosity: str = 'WARN', zmax: int = 9567, zmin: int = -9567, zscale: int = 20, ztilt: float = 23.4) -> None:
        '''Initialize the new instance of the World(PolyData) class.

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

        '''
    def generate_elevations(self) -> None: ...
    def create_tectonic_plates(self, num_plates) -> None:
        """Create tectonic plates from the 3D mesh.

        Args:
            num_plates (int): Number of tectonic plates to create.
        """
