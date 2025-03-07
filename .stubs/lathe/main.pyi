from _typeshed import Incomplete
from numpy.typing import NDArray as NDArray
from pyvista import PolyData
from typing import Annotated
from util import Mesh as Mesh, MeshArray as MeshArray

LOGLEVEL: str
LOGFORMAT: str
INIT_ROUGHNESS: float
INIT_STRENGTH: float
ROUGHNESS: float
PERSISTENCE: float
PLATESNUM: int

class World(PolyData):
    def __new__(cls) -> object:
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
    scale: Incomplete
    verbosity: Incomplete
    origin: Incomplete
    mesh: object
    def __init__(self, name: str = '', seed: int = 0, radius: int = 6378100, recursion: int = 7, octaves: int = 8, origin: tuple = (0.0, 0.0, 0.0), ztilt: float = 23.4, zmin: int = -9567, zmax: int = 9567, ocean_percent: float = 0.55, scale: int = 20, verbosity: str = 'WARN') -> None:
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

def main(name: Annotated[str, None], save: Annotated[bool, None] = False, visualize: Annotated[bool, None] = True, seed: Annotated[int, None] = 0, radius: Annotated[int, None] = ..., recursion: Annotated[int, None] = ..., ztilt: Annotated[float, None] = ..., zmin: Annotated[int, None] = ..., zmax: Annotated[int, None] = ..., ocean_percent: Annotated[float, None] = ..., scale: Annotated[int, None] = ..., octaves: Annotated[int, None] = ..., loglevel: Annotated[str, None] = ..., platesnum: Annotated[int, None] = ...) -> None:
    """Generate a 3D mesh of a planet, apply elevations, and visualize the result.

    Args:
        name (str, optional): A name for the world.
        save (bool, optional): Whether to save world. Defaults to False.
        visualize (bool, optional): Whether to display the world. Defaults to True.
        seed (int, optional): The world seed to be used. Defaults to a random number.
        radius (int, optional): The radius of the world in meters.
        recursion (int, optional): The number of recursions used in creating the mesh.
        ztilt (float, optional): Controls the z-axis tilt of the planet.
        zmin (int, optional): The lowest elevation on the planet.
        zmax (int, optional): The highest elevation value on the planet.
        ocean_percent (float, optional): The global sea level relative to elevation.
        scale (int, optional): A multiplier to make elevations visible when displayed.
        octaves (int, optional): The number of octaves to use for noise sampling.
        loglevel (str, optional): The verbosity of the logger.
        platesnum (int, optional): The number of tectonic plates to create. -Not used.-

    Returns:
        None.

    """
