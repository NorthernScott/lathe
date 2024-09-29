# -*- coding: utf-8 -*-


import numpy as np
from numba import prange
import opensimplex as osi
from numpy.typing import NDArray


def sample_noise(
    points, roughness, strength, feature_size, radius
) -> NDArray[np.float64]:
    elevations = np.ones(len(points), dtype=np.float64)
    rough_verts = points * roughness

    for v in prange(len(rough_verts)):
        elevations[v] = osi.noise4(
            x=rough_verts[v][0] / feature_size,
            y=rough_verts[v][1] / feature_size,
            z=rough_verts[v][2] / feature_size,
            w=1 / feature_size,
        )

    # ?: Adding +1 to elevation moves negative values in the 0-1 range. Multiplying by 0.5 drags any values > 1 back into the 0-1 range. I'm not sure if multiplying by the radius is the proper thing to do in my next implementation.

    return (elevations + 1) * 0.5 * strength * radius


def v_sample_noise(
    points: NDArray[np.float64],
    roughness: float,
    strength: float,
    feature_size: float,
    radius: float,
) -> NDArray[np.float64]:
    # Vectorized operations
    rough_verts = points * roughness
    scaled_verts = rough_verts / feature_size
    w_value = 1 / feature_size

    # Vectorized noise computation
    elevations = osi.noise4(
        x=scaled_verts[:, 0], y=scaled_verts[:, 1], z=scaled_verts[:, 2], w=w_value
    )

    # Adjust elevations
    return (elevations + 1) * 0.5 * strength * radius


def sample_octaves(
    points,
    octaves,
    init_roughness,
    init_strength,
    roughness,
    persistence,
    feature_size,
    radius,
) -> NDArray[np.float64]:
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

    # Initialize elevations array.

    elevations = np.zeros(shape=len(points), dtype=np.float64)

    # NOTE: In my separate-sampling experiment, rough/strength pairs of (1.6, 0.4) (5, 0.2) and (24, 0.02) were good for 3 octaves. The final 3 results were added and then multiplied by 0.4

    for i in prange(octaves):
        elevations += sample_noise(
            points=points,
            roughness=init_roughness / radius,
            strength=init_strength / radius,
            feature_size=feature_size,
            radius=radius,
        )
        init_roughness *= roughness
        init_strength *= persistence

    return elevations
