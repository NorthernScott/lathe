import numpy as np
from _typeshed import Incomplete
from numpy.typing import NDArray
from pyvista import PolyData

RIGHT_ANGLE: float
SEMICIRCLE: float
CIRCLE: float
PHI: float
SQRT5: float
SEC_IN_MIN: float
type Mesh = PolyData[int, tuple[float, float, float], int]
type MeshArray = NDArray[np.float64]
type Vector = tuple[float, float, float]

def fib(n) -> int:
    """Finds an approximation of the fibonacci number for a given ordinal.

    Arguments:
        n -- Input ordinals.

    Returns:
        Returns an approximation of the nth fibonacci number.

    """
def sign(n) -> int:
    """Gets the sign of an input number.

    Arguments:
        n -- Input number whose sign will be sampled.

    Returns:
        Integer representing the sign of the input number. 1 for positive, -1 for negative, and 0 for 0.
    """
def now() -> str:
    """
    Gets the current date and time in a formatted string.

    Returns:
        str: A formatted string representing the current date and time, with the format %Y-%m-%d-%H-%M-%S.
    """
def fibonacci_sphere(points: NDArray) -> NDArray:
    """_summary_

    Arguments:
        points -- _description_

    Returns:
        _description_
    """
def create_mesh(radius: int, recursion: int, origin: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> Mesh:
    """
    Creates an icosphere mesh object with the specified radius and recursion level (number of vertices and faces).

    Args:
        radius (int): The radius of the world.
        recursion (int): he number of recursions used in creating the icosphere mesh.
        origin (tuple[float, float, float], optional): The origin (centrepoint) of the mesh. Defaults to (0.0, 0.0, 0.0).

    Returns:
        Mesh: Pyvista icosphere mesh object with the specified radius, recursion level, and origin.
    """
def rescale(elevations: NDArray, zmin: int, zmax: int, mid: Incomplete | None = None, mode: Incomplete | None = None, u_min: Incomplete | None = None, u_max: Incomplete | None = None) -> NDArray:
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
def xyz2latlon(mesh: PolyData, radius: int) -> tuple[MeshArray, MeshArray]:
    """
    Converts XYZ coordinates to spherical coordinates using the PyVista Cartesian-to-Spherical function, and then to radius and degrees using the Numpy.degrees function.

    Args:
        mesh (PolyData): The Pyvista mesh object.
        radius (int): The world radius.

    Returns:
        lat, lon (tuple[MeshArray, MeshArray]): A tuple of numpy arrays containing the latitude and longitude in degrees.
    """
def save_world(name: str, parameters: dict, mesh: type[PolyData], now: str = ...) -> None:
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
