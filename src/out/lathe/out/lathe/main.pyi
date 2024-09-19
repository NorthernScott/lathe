import numpy as np
from typing_extensions import Annotated

RADIUS: int
FEATURE_SIZE: np.float64
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

def getPlanetName() -> str: ...
def main(name: Annotated[str, None], save: Annotated[bool, None] = False, seed: Annotated[int, None] = 0, radius: Annotated[int, None] = ..., feature_size: Annotated[float, None] = ..., recursion: Annotated[int, None] = ..., ztilt: Annotated[float, None] = ..., zmin: Annotated[int, None] = ..., zmax: Annotated[int, None] = ..., ocean_percent: Annotated[float, None] = ..., zscale: Annotated[int, None] = ..., octaves: Annotated[int, None] = ..., loglevel: Annotated[str, None] = ..., platesnum: Annotated[int, None] = ...) -> None:
    """A program to procedurally generate worlds.

    Returns:

        A 3D icosphere mesh with elevation data provided in cartesian coordinates.
    """
