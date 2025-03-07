import numpy as np
from numpy.typing import NDArray as NDArray

def sample_noise(points: NDArray[np.float64], roughness: float, strength: float, radius: int) -> NDArray[np.float64]:
    """Samples 4-dimension simplex noise at each point in the input array.

    Args:
        points (NDArray[np.float64]): A 3d array of points.
        roughness (float): The roughness (frequency) of the noise.
        strength (float): The strength (persistence) of the noise.
        radius (int): The radius of the world.

    Returns:
        elevations: A NDArray[np.float64] of elevations for each point in the input array.
    """
def sample_octaves(points: NDArray[np.float64], octaves: int, init_roughness: float, init_strength: float, roughness: float, persistence: float, radius: int, seed: int) -> NDArray[np.float64]:
    """Iterates through the noise function multiple times to create a more complex noise pattern.

    Args:
        points (NDArray[np.float64]): A 3d array of points.
        octaves (int): The number of times to iterate through the noise function.
        init_roughness (float): A starting value for the roughness.
        init_strength (float): A starting value for the strength.
        roughness (float): A multiplier for the roughness.
        persistence (float): A multiplier for the strength.
        radius (int): The radius of the world.
        seed (int): The seed for the noise generator.

    Returns:
        elevations: A NDArray[np.float64] of elevations for each point in the input array.
    """
