import numpy as np
from .mylogger import log as log, std_con as std_con
from .terrain import arr_sample_noise as arr_sample_noise, sample_octaves as sample_octaves
from .util import Mesh as Mesh, MeshArray as MeshArray, create_mesh as create_mesh, now as now, rescale as rescale, save_world as save_world
from .viz import viz as viz
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
