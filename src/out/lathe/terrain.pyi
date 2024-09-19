import numpy as np
from .mylogger import log as log, std_con as std_con
from .osi import noise4array as noise4array
from .util import Mesh as Mesh, MeshArray as MeshArray, Vector as Vector
from numba import jit as jit, njit as njit
from numpy.typing import NDArray as NDArray

def arr_sample_noise(world_mesh: Mesh, roughness: float, strength: float, feature_size: float, radius: int, world_seed: int) -> MeshArray: ...
def sample_noise(points, roughness, strength, feature_size, radius) -> NDArray[np.float64]: ...
def sample_octaves(points, octaves, init_roughness, init_strength, roughness, persistence, feature_size, radius) -> NDArray[np.float64]:
    """Samples multiple octaves of noise to generate elevations.

    Arguments:
        points -- _description_
        octaves -- _description_
        init_roughness -- _description_
        init_strength -- _description_
        roughness -- _description_
        persistence -- _description_
        radius -- _description_

    Returns:
        Array of elevations.
    """
