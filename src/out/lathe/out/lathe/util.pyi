from _typeshed import Incomplete as Incomplete
from numpy.typing import NDArray as NDArray
from pyvista import PolyData

RIGHT_ANGLE: float
SEMICIRCLE: float
CIRCLE: float
PHI: float
SQRT5: float
SEC_IN_MIN: float
Mesh = PolyData[int, tuple[float, float, float], int]
MeshArray: Incomplete
Vector = tuple[float, float, float]

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
def now() -> str: ...
def fibonacci_sphere(points: NDArray) -> NDArray:
    """_summary_

    Arguments:
        points -- _description_

    Returns:
        _description_
    """
def create_mesh(radius, recursion, ztilt) -> None:
    """Initializes a polyhedral mesh, applies axial tilt, and creates point and face arrays.

    Arguments:
        radius -- _description_
        recursion -- _description_
        z_tilt -- _description_

    Returns:
        Pyvista mesh object with corresponding numpy array of points. Separate arrays of points and faces.
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
def xyz2latlon(x, y, z, r) -> None:
    """Convert 3D spatial XYZ coordinates into Latitude and Longitude.
    x -- X coordinate.
    y -- Y coordinate.
    z -- Z coordinate.
    r -- World radius."""
def save_world(name: str, parameters: dict, mesh: PolyData, mesh_format: str = 'obj', now: str = ...) -> None: ...
