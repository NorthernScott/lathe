# -*- coding: utf-8 -*-


import json
from datetime import datetime
from math import copysign, cos, pi, sin, sqrt
from pathlib import Path

import numpy as np
from numba import prange
from numpy.typing import NDArray
from pyvista import Icosphere, PolyData, save_meshio

# Mathmatical constants
RIGHT_ANGLE: float = pi / 2
SEMICIRCLE: float = pi
CIRCLE: float = pi * 2
PHI: float = 1.61803398874989484820
SQRT5: float = sqrt(5)
SEC_IN_MIN = 60.0

# Custom types
type Mesh = PolyData[int, tuple[float, float, float], int]
type MeshArray = NDArray[np.float64]
type Vector = tuple[float, float, float]


# Mathematical functions
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


def create_mesh(radius, recursion, ztilt):
    """Initializes a polyhedral mesh, applies axial tilt, and creates point and face arrays.

    Arguments:
        radius -- _description_
        recursion -- _description_
        z_tilt -- _description_

    Returns:
        Pyvista mesh object with corresponding numpy array of points. Separate arrays of points and faces.
    """
    world_mesh: Mesh = Icosphere(radius=radius, center=(0.0, 0.0, 0.0), nsub=recursion)

    # points = axis_rotation(world_mesh.points, z_tilt, inplace=False, deg=True, axis="z")
    # points = np.array(world_mesh.points)
    # faces = np.array(world_mesh.faces)

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


def xyz2latlon(x, y, z, r):
    """Convert 3D spatial XYZ coordinates into Latitude and Longitude.
    x -- X coordinate.
    y -- Y coordinate.
    z -- Z coordinate.
    r -- World radius."""
    # Old method; will output NaNs if (Z/R) > 1 or (Z/R) < -1
    # lat = np.degrees(np.arcsin(z / r))

    # Constrain the value to -1 to 1 before doing arcsin
    lat = np.degrees(np.arcsin(min(max((z / r), -1), 1)))
    lon = np.degrees(np.arctan2(y, x))

    #    lat = math.asin(z / r)
    #    lon = math.atan2(y, x)
    return (lat, lon)


def save_world(
    name: str,
    parameters: dict,
    mesh: PolyData,
    mesh_format: str = "obj",
    now: str = now(),
) -> None:
    Path("./outputs/").mkdir(parents=True, exist_ok=True)

    filename = str(object=f"{name}-{now}")

    # TODO: Add in selectors for config format and mesh format.
    config_extension: str = ".json"
    mesh_extension: str = ".obj"

    config_file = Path("./outputs/", filename + config_extension)
    mesh_file = Path("./outputs/", filename + mesh_extension)

    with open(file=config_file, mode="w") as fp:
        json.dump(obj=parameters, fp=fp)
        fp.close()

    save_meshio(filename=mesh_file, mesh=mesh)

    return None
