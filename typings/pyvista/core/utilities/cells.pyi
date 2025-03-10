"""
This type stub file was generated by pyright.
"""

from typing import TYPE_CHECKING
from pyvista.core import _vtk_core as _vtk
from pyvista.core._typing_core import MatrixLike, NumpyArray

"""
This type stub file was generated by pyright.
"""
if TYPE_CHECKING:
    ...
def ncells_from_cells(cells: NumpyArray[int]) -> int:
    """Get the number of cells from a VTK cell connectivity array.

    Parameters
    ----------
    cells : numpy.ndarray
        A VTK cell connectivity array.

    Returns
    -------
    int
        The number of cells extracted from the given cell connectivity array.

    """
    ...

def numpy_to_idarr(ind: MatrixLike[int], deep: bool = ..., return_ind: bool = ...) -> tuple[_vtk.vtkIdTypeArray, NumpyArray[int]] | _vtk.vtkIdTypeArray:
    """Safely convert a numpy array to a vtkIdTypeArray.

    Parameters
    ----------
    ind : sequence[int]
        Input sequence to be converted to a vtkIdTypeArray. Can be either a mask
        or an integer array-like.
    deep : bool, default: False
        If ``True``, deep copy the input data. If ``False``, do not deep copy
        the input data.
    return_ind : bool, default: False
        If ``True``, also return the input array after it has been cast to the
        proper dtype.

    Returns
    -------
    vtkIdTypeArray
        Converted array as a vtkIdTypeArray.
    numpy.ndarray
        The input array after it has been cast to the proper dtype. Only
        returned if `return_ind` is set to ``True``.

    Raises
    ------
    TypeError
        If the input array is not a mask or an integer array-like.

    """
    ...

def create_mixed_cells(mixed_cell_dict, nr_points=...):
    """Generate the required cell arrays for the creation of a pyvista.UnstructuredGrid from a cell dictionary.

    This function generates all required cell arrays according to a given cell
    dictionary. The given cell-dictionary should contain a proper
    mapping of vtk_type -> np.ndarray (int), where the given ndarray
    for each cell-type has to be an array of dimensions [N, D] or
    [N*D], where N is the number of cells and D is the size of the
    cells for the given type (e.g. 3 for triangles).  Multiple
    vtk_type keys with associated arrays can be present in one
    dictionary.  This function only accepts cell types of fixed size
    and not dynamic sized cells like ``vtk.VTK_POLYGON``

    Parameters
    ----------
    mixed_cell_dict : dict
        A dictionary that maps VTK-Enum-types (e.g. VTK_TRIANGLE) to
        np.ndarrays of type int.  The ``np.ndarrays`` describe the cell
        connectivity.
    nr_points : int, optional
        Number of points of the grid. Used only to allow additional runtime
        checks for invalid indices.

    Returns
    -------
    cell_types : numpy.ndarray (uint8)
        Types of each cell.

    cell_arr : numpy.ndarray (int)
        VTK-cell array.

    Raises
    ------
    ValueError
        If any of the cell types are not supported, have dynamic sized
        cells, map to values with wrong size, or cell indices point
        outside the given number of points.

    Examples
    --------
    Create the cell arrays containing two triangles.

    This will generate cell arrays to generate a mesh with two
    disconnected triangles from 6 points.

    >>> import numpy as np
    >>> import vtk
    >>> from pyvista.core.utilities.cells import create_mixed_cells
    >>> cell_types, cell_arr = create_mixed_cells(
    ...     {vtk.VTK_TRIANGLE: np.array([[0, 1, 2], [3, 4, 5]])}
    ... )
    """
    ...

def get_mixed_cells(vtkobj):
    """Create the cells dictionary from the given pyvista.UnstructuredGrid.

    This functions creates a cells dictionary (see
    create_mixed_cells), with a mapping vtk_type -> np.ndarray (int)
    for fixed size cell types. The returned dictionary will have
    arrays of size [N, D], where N is the number of cells and D is the
    size of the cells for the given type (e.g. 3 for triangles).

    Parameters
    ----------
    vtkobj : pyvista.UnstructuredGrid
        The unstructured grid for which the cells dictionary should be computed.

    Returns
    -------
    dict
        Dictionary of cells.

    Raises
    ------
    ValueError
        If vtkobj is not a pyvista.UnstructuredGrid, any of the
        present cells are unsupported, or have dynamic cell sizes,
        like VTK_POLYGON.
    """
    ...

