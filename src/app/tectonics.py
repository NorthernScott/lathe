# -*- coding: utf-8 -*-

# import external dependencies
import numpy as np
from numpy.typing import NDArray
from scipy.ndimage import label
from scipy.signal import argrelmax

# import internal modules
from mylogger import std_con, log


def generate_plates(elevations, num_plates):
    # Find all local maxima
    local_max = argrelmax(data=elevations, axis=0, mode="wrap")

    # Get the elevations at the local maxima
    peak_elevations = elevations[local_max]

    # Find the indices of the num_plates highest peaks
    highest_peaks = np.argpartition(a=peak_elevations, kth=-num_plates, axis=0)[
        -num_plates:
    ]

    # Create an array of zeros with the same shape as elevations
    plates = np.zeros_like(elevations)

    # Assign each of the highest peaks to a different plate
    velocities = {}
    for i, peak_index in enumerate(highest_peaks):
        coordinates = tuple(coord[peak_index] for coord in local_max)
        plates[coordinates] = i + 1
        velocities[i + 1] = (
            np.random.uniform(-1, 1),
            np.random.uniform(-1, 1),
        )  # Assign a random velocity

    # Label the remaining cells
    plates, _ = label(plates)

    return plates, velocities


def simulate_tectonics(elevations, plates, velocities, num_steps) -> np.ndarray:
    """
    # Assume elevations is a 2D numpy array
    # Assume plates is a 2D numpy array of the same shape, where each cell contains the index of the plate it belongs to
    # Assume velocities is a dictionary where the keys are plate indices and the values are (dx, dy) tuples
    """

    for _ in range(num_steps):
        # Move plates
        for plate_index, (dx, dy) in velocities.items():
            plates[plates == plate_index] = np.roll(
                a=plates[plates == plate_index], shift=(dy, dx), axis=0
            )

        # Handle collisions
        for y in range(elevations.shape[0]):
            for x in range(elevations.shape[1]):
                neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                for nx, ny in neighbors:
                    if (
                        plates[y, x] != plates[ny, nx]
                        and np.dot(velocities[plates[y, x]], (nx - x, ny - y)) > 0
                    ):
                        # Plates are different and moving towards each other
                        elevations[y, x] += 1  # Increase elevation

    return elevations
