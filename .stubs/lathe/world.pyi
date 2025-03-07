import pyvista as pv
from _typeshed import Incomplete

class World(pv.PolyData):
    def __new__(cls) -> World:
        """Instantiate new instance of the World(PolyData) class."""
    name: Incomplete
    seed: Incomplete
    radius: Incomplete
    recursion: Incomplete
    octaves: Incomplete
    ztilt: Incomplete
    zmin: Incomplete
    zmax: Incomplete
    zrange: Incomplete
    ocean_percent: Incomplete
    ocean_point: Incomplete
    zscale: Incomplete
    verbosity: Incomplete
    origin: Incomplete
    mesh: object
    def __init__(self, name: str = '', seed: int = 0, radius: int = 6378100, recursion: int = 7, octaves: int = 8, origin: tuple = (0.0, 0.0, 0.0), ztilt: float = 23.4, zmin: int = -9567, zmax: int = 9567, ocean_percent: float = 0.55, zscale: int = 20, verbosity: str = 'WARN') -> None:
        '''Initialize the new instance of the World(PolyData) class.

        Args:
            name (str): Name of the world. Defaults to "".
            seed (int): Seed used for noise generation. Defaults to a random integer.
            radius (int): Radius of the world. Defaults to 6378100 m.
            recursion (int): Level of detail of the world mesh. Defaults to 7.
            octaves (int): Factor to set noise complexity. Defaults to 8.
            origin (tuple): The origin point of the world in (X,Y,Z) coordinates. Defaults to (0.0, 0.0, 0.0).
            ztilt (float): Axial tilt of the world. Defaults to 23.4 degrees.
            zmin (int): Minimum world elevation. Defaults to -9567 m.
            zmax (int): Maximum world elevation. Defaults to 9567 m.
            ocean_percent (float):  Factor used to set sea level relative to elevation range. Defaults to 0.55,
            scale (int): Scaling factor used to make elevations visible when displayed. Defaults to 20x.
            verbosity (str): Verbosity of the logger. Defaults to "WARN."

        '''
    def get_name(self) -> str:
        """Return a random planet name from planetnames.json."""

test: Incomplete
