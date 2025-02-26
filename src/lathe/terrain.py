# -*- coding: utf-8 -*-


import numpy as np
import opensimplex as osi
from mylogger import std_con
from numba import prange
from numpy.typing import NDArray


def sample_noise(
    points: NDArray[np.float64],
    roughness: float,
    strength: float,
    radius: int,
) -> NDArray[np.float64]:
    """Samples 4-dimension simplex noise at each point in the input array.

    Args:
        points (NDArray[np.float64]): A 3d array of points.
        roughness (float): The roughness (frequency) of the noise.
        strength (float): The strength (persistence) of the noise.
        radius (int): The radius of the world.

    Returns:
        elevations: A NDArray[np.float64] of elevations for each point in the input array.
    """
    elevations = np.ones(len(points), dtype=np.float64)
    rough_verts = points * roughness

    for v in prange(len(rough_verts)):
        elevations[v] = osi.noise4(
            x=rough_verts[v][0],
            y=rough_verts[v][1],
            z=rough_verts[v][2],
            w=1,
        )

    return elevations * strength * radius


def sample_octaves(
    points: NDArray[np.float64],
    octaves: int,
    init_roughness: float,
    init_strength: float,
    roughness: float,
    persistence: float,
    radius: int,
    seed: int,
) -> NDArray[np.float64]:
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

    # Initialize noise generator seed.

    if seed == 0:
        osi.random_seed()
    else:
        osi.seed(seed)

    # Initialize elevations array.
    elevations = np.ones(shape=len(points), dtype=np.float64)

    # INFO: In Bob's separate-sampling experiment, rough/strength pairs of (1.6, 0.4) (5, 0.2) and (24, 0.02) were good for 3 octaves. The final 3 results were added and then multiplied by 0.4

    # Pre-compute roughness and strength values for each octave
    roughness_values = np.array(
        [(init_roughness * (roughness**i)) / radius for i in range(octaves)]
    )
    strength_values = np.array(
        [(init_strength * (persistence**i)) / radius for i in range(octaves)]
    )

    for i in prange(octaves):
        std_con.print(f"Octave: {i+1} ", "\r\n")
        elevations += sample_noise(
            points=points,
            roughness=roughness_values[i],
            strength=strength_values[i],
            radius=radius,
        )

    return elevations
