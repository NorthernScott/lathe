from numpy.typing import NDArray as NDArray
from typing import Annotated
from util import Mesh as Mesh, MeshArray as MeshArray

RADIUS: int
ZMIN: int
ZMAX: int
ZRANGE: float
ZTILT: float
ZSCALE: int
OCEAN_PERCENT: float
OCEAN_POINT: float
RECURSION: int
OCTAVES: int
LOGLEVEL: str
LOGFORMAT: str
INIT_ROUGHNESS: float
INIT_STRENGTH: float
ROUGHNESS: float
PERSISTENCE: float
PLATESNUM: int
SEED_MIN: int
SEED_MAX: int

def getPlanetName() -> str:
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
