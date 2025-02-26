# -*- coding: utf-8 -*-

# Import core libraries.
import json
from datetime import datetime
from math import copysign, cos, pi, sin, sqrt
from pathlib import Path
# import os

# Import third-party modules.
import numpy as np
from numba import prange
from numpy.typing import NDArray
from pyvista import Icosphere, PolyData, cartesian_to_spherical as c2s

# Import internal modules.
from mylogger import std_con

# Define mathmatical constants.
RIGHT_ANGLE: float = pi / 2
SEMICIRCLE: float = pi
CIRCLE: float = pi * 2
PHI: float = 1.61803398874989484820
SQRT5: float = sqrt(5)
SEC_IN_MIN = 60.0

# Define custom types.
type Mesh = PolyData[int, tuple[float, float, float], int]
type MeshArray = NDArray[np.float64]
type Vector = tuple[float, float, float]


# Mathematical functions.
def fib(n) -> int:
    """Finds an approximation of the fibonacci number for a given ordinal.

    Arguments:
        n -- Input ordinals.

    Returns:
        Returns an approximation of the nth fibonacci number.

    """
    return int(round(PHI**n / SQRT5))


def sign(n) -> int:
    """Gets the sign of an input number.

    Arguments:
        n -- Input number whose sign will be sampled.

    Returns:
        Integer representing the sign of the input number. 1 for positive, -1 for negative, and 0 for 0.
    """
    return copysign(1, n)


def now() -> str:
    """
    Gets the current date and time in a formatted string.

    Returns:
        str: A formatted string representing the current date and time, with the format %Y-%m-%d-%H-%M-%S.
    """
    return datetime.now().strftime(format="%Y-%m-%d-%H-%M-%S")


def fibonacci_sphere(points: NDArray) -> NDArray:
    """_summary_

    Arguments:
        points -- _description_

    Returns:
        _description_
    """
    samples = points
    # fib_array: NDArray = np.ndarray(shape=(samples, 3), dtype=np.float64)

    for i in prange(samples):
        y: float = 1 - (i / float(samples - 1)) * 2  # y goes from 1 to -1
        radius: float = sqrt(1 - y * y)  # radius at y

        theta: float = PHI * i  # golden angle increment

        x: float = cos(theta) * radius
        z: float = sin(theta) * radius

        samples[i][0] = x
        samples[i][1] = y
        samples[i][2] = z

    return samples


def create_mesh(
    radius: int, recursion: int, origin: tuple[float, float, float] = (0.0, 0.0, 0.0)
) -> Mesh:
    """
    Creates an icosphere mesh object with the specified radius and recursion level (number of vertices and faces).

    Args:
        radius (int): The radius of the world.
        recursion (int): he number of recursions used in creating the icosphere mesh.
        origin (tuple[float, float, float], optional): The origin (centrepoint) of the mesh. Defaults to (0.0, 0.0, 0.0).

    Returns:
        Mesh: Pyvista icosphere mesh object with the specified radius, recursion level, and origin.
    """
    world_mesh: Mesh = Icosphere(radius=radius, center=origin, nsub=recursion)

    return world_mesh


# TODO: Simplify this rescale function. I am only using one version of it.
def rescale(
    elevations: NDArray,
    zmin: int,
    zmax: int,
    mid=None,
    mode=None,
    u_min=None,
    u_max=None,
) -> NDArray:
    """Re-scale (normalize) an array to a given zmin and zmax bound.
    elevations -- The input array.
    zmin -- The desired new min value.
    zmax -- The desired new max value.
    mid -- Optionally rescale the zmin & zmax values separately.
    Mid should be between elevations's existing min and max values.
    mode -- Optionally rescale ONLY the 'zmin' or 'zmax' values.
    u_min -- Optionally specify an absolute value for elevations min.
    u_max -- Optionally specify an absolute value for elevations max.
    (u_min and u_max are useful for snapshotting when you're processing several
    arrays with different ranges and need them to retain their relationship to
    each other within the new zmin and zmax bounds.)
    """
    new_array: NDArray = np.copy(a=elevations)

    emin: float = np.min(a=elevations)
    emax: float = np.max(a=elevations)

    if u_min is not None and u_min < emin:
        emin = u_min
    if u_max is not None and u_max > emax:
        emax = u_max

    if mode is None:
        e_range: float = emax - emin
        z_range: int = zmax - zmin

        new_array = ((elevations - emin) / e_range) * z_range + zmin

    elif mode == "zmin":
        if mid is None:
            print("ERROR: Must supply a middle value to use rescale modes.")
            print("Continuing with unmodified data.")
            return elevations

        e_range = mid - emin
        z_range = mid - zmin
        new_array = np.where(
            elevations <= mid,
            ((elevations - emin) / e_range) * z_range + zmin,
            elevations,
        )

    elif mode == "zmax":
        if mid is None:
            print("ERROR: Must supply a middle value to use rescale modes.")
            print("Continuing with unmodified data.")
            return elevations

        e_range = emax - mid
        z_range = zmax - mid
        new_array = np.where(
            elevations >= mid,
            ((elevations - mid) / e_range) * z_range + mid,
            elevations,
        )

    return new_array


def xyz2latlon(mesh: PolyData) -> MeshArray:
    """
    Converts XYZ coordinates to spherical coordinates using the PyVista Cartesian-to-Spherical function, and then to radius and degrees using the Numpy.degrees function.

    Args:
        mesh (PolyData): The Pyvista mesh object.

    Returns:
        MeshArray: A NumPy array with shape (,3) and dtype of np.float64, containing the spherical coordinates in degrees (latitude, longitude, radius).
    """
    r, phi, theta = c2s(mesh.points[:, 0], mesh.points[:, 1], mesh.points[:, 2])
    lat = np.degrees(phi)
    lon = np.degrees(theta)

    coords: MeshArray = np.column_stack((lat, lon))

    std_con.print(f"Sample of Lat-Lon Coordinates:\r\n {coords} \r\n")

    return coords


def save_world(
    name: str,
    parameters: dict,
    mesh: type[PolyData],
    now: str = now(),
) -> None:
    """
    Saves the world configuration parameters and mesh to the output directory.

    Args:
        name (str): The world name.
        parameters (dict): The world configuration parameters.
        mesh (type[PolyData]): A Pyvista mesh object.
        now (str, optional): Creation time timestamp.

    Returns:
        none: No return.
    """
    Path("./outputs/").mkdir(parents=True, exist_ok=True)

    filename = str(object=f"{name}-{now}")

    # TODO: Add in selectors for config format and mesh format.
    config_extension: str = ".json"
    mesh_extension: str = ".ply"

    # TODO: Implement os.path logic.
    # script_dir = os.path.dirname(__file__)
    # config_file_path = os.path.join(script_dir, filename, config_extension)
    # mesh_file_path = os.path.join(script_dir, filename, mesh_extension)
    config_file = Path("./outputs/", filename + config_extension)
    mesh_file = Path("./outputs/", filename + mesh_extension)

    # Save the world configuration parameters to a JSON file.
    with open(file=config_file, mode="w") as fp:
        json.dump(obj=parameters, fp=fp)
        fp.close()

    # Save the mesh to a file.
    mesh.save(filename=mesh_file, binary=True, texture=None, recompute_normals=True)

    std_con.print(f"Saved world as {filename}.\r\n")

    return None
