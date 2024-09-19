import numpy as np
from mylogger import log as log, std_con as std_con
from numpy.typing import NDArray as NDArray

def generate_plates(elevations, num_plates): ...
def simulate_tectonics(elevations, plates, velocities, num_steps) -> np.ndarray:
    """
    # Assume elevations is a 2D numpy array
    # Assume plates is a 2D numpy array of the same shape, where each cell contains the index of the plate it belongs to
    # Assume velocities is a dictionary where the keys are plate indices and the values are (dx, dy) tuples
    """
