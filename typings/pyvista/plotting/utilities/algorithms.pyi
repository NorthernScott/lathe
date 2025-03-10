"""
This type stub file was generated by pyright.
"""

from pyvista.plotting import _vtk

"""
This type stub file was generated by pyright.
"""
def algorithm_to_mesh_handler(mesh_or_algo, port=...):
    """Handle vtkAlgorithms where mesh objects are expected.

    This is a convenience method to handle vtkAlgorithms when passed to methods
    that expect a :class:`pyvista.DataSet`. This method will check if the passed
    object is a ``vtk.vtkAlgorithm`` or ``vtk.vtkAlgorithmOutput`` and if so,
    return that algorithm's output dataset (mesh) as the mesh to be used by the
    calling function.

    Parameters
    ----------
    mesh_or_algo : pyvista.DataSet | vtk.vtkAlgorithm | vtk.vtkAlgorithmOutput
        The input to be used as a data set (mesh) or vtkAlgorithm object.

    port : int, default: 0
        If the input (``mesh_or_algo``) is an algorithm, this specifies which output
        port to use on that algorithm for the returned mesh.

    Returns
    -------
    mesh : pyvista.DataSet
        The resulting mesh data set from the input.

    algorithm : vtk.vtkAlgorithm or vtk.vtkAlgorithmOutput or None
        If an algorithm is passed, it will be returned. Otherwise returns ``None``.

    """
    ...

def set_algorithm_input(alg, inp, port=...):
    """Set the input to a vtkAlgorithm.

    Parameters
    ----------
    alg : vtk.vtkAlgorithm
        The algorithm whose input is being set.

    inp : vtk.vtkAlgorithm | vtk.vtkAlgorithmOutput | vtk.vtkDataObject
        The input to the algorithm.

    port : int, default: 0
        The input port.

    """
    ...

class PreserveTypeAlgorithmBase(_vtk.VTKPythonAlgorithmBase):
    """Base algorithm to preserve type.

    Parameters
    ----------
    nInputPorts : int, default: 1
        Number of input ports for the algorithm.

    nOutputPorts : int, default: 1
        Number of output ports for the algorithm.

    """
    def __init__(self, nInputPorts=..., nOutputPorts=...) -> None:
        """Initialize algorithm."""
        ...
    
    def GetInputData(self, inInfo, port, idx):
        """
        Get input data object.

        This will convert ``vtkPointSet`` to ``vtkPolyData``.

        Parameters
        ----------
        inInfo : vtk.vtkInformation
            The information object associated with the input port.

        port : int
            The index of the input port.

        idx : int
            The index of the data object within the input port.

        Returns
        -------
        _vtk.vtkDataObject
            The input data object.
        """
        ...
    
    def RequestDataObject(self, _request, inInfo, outInfo):
        """Preserve data type.

        Parameters
        ----------
        _request : vtk.vtkInformation
            The request object for the filter.

        inInfo : vtk.vtkInformationVector
            The input information vector for the filter.

        outInfo : vtk.vtkInformationVector
            The output information vector for the filter.

        Returns
        -------
        int
            Returns 1 if successful.
        """
        ...
    


class ActiveScalarsAlgorithm(PreserveTypeAlgorithmBase):
    """Algorithm to control active scalars.

    The output of this filter is a shallow copy of the input data
    set with the active scalars set as specified.

    Parameters
    ----------
    name : str
        Name of scalars used to set as active on the output mesh.
        Accepts a string name of an array that is present on the mesh.
        Array should be sized as a single vector.

    preference : str, default: 'point'
        When ``mesh.n_points == mesh.n_cells`` and setting
        scalars, this parameter sets how the scalars will be
        mapped to the mesh.  The default, ``'point'``, causes the
        scalars to be associated with the mesh points.  Can be
        either ``'point'`` or ``'cell'``.

    """
    def __init__(self, name: str, preference: str = ...) -> None:
        """Initialize algorithm."""
        ...
    
    def RequestData(self, _request, inInfo, outInfo):
        """Perform algorithm execution.

        Parameters
        ----------
        _request : vtk.vtkInformation
            The request object.
        inInfo : vtk.vtkInformationVector
            Information about the input data.
        outInfo : vtk.vtkInformationVector
            Information about the output data.

        Returns
        -------
        int
            1 on success.

        """
        ...
    


class PointSetToPolyDataAlgorithm(_vtk.VTKPythonAlgorithmBase):
    """Algorithm to cast PointSet to PolyData.

    This is implemented with :func:`pyvista.PointSet.cast_to_polydata`.

    """
    def __init__(self) -> None:
        """Initialize algorithm."""
        ...
    
    def RequestData(self, _request, inInfo, outInfo):
        """
        Perform algorithm execution.

        Parameters
        ----------
        _request : vtk.vtkInformation
            Information associated with the request.
        inInfo : vtk.vtkInformationVector
            Information about the input data.
        outInfo : vtk.vtkInformationVector
            Information about the output data.

        Returns
        -------
        int
            1 when successful.
        """
        ...
    


class AddIDsAlgorithm(PreserveTypeAlgorithmBase):
    """Algorithm to add point or cell IDs.

    Output of this filter is a shallow copy of the input with
    point and/or cell ID arrays added.

    Parameters
    ----------
    point_ids : bool, default: True
        Whether to add point IDs.

    cell_ids : bool, default: True
        Whether to add cell IDs.

    Raises
    ------
    ValueError
        If neither point IDs nor cell IDs are set.
    """
    def __init__(self, point_ids=..., cell_ids=...) -> None:
        """Initialize algorithm."""
        ...
    
    def RequestData(self, _request, inInfo, outInfo):
        """
        Perform algorithm execution.

        Parameters
        ----------
        _request : vtk.vtkInformation
            Information associated with the request.
        inInfo : vtk.vtkInformationVector
            Information about the input data.
        outInfo : vtk.vtkInformationVector
            Information about the output data.

        Returns
        -------
        int
            Returns 1 if the algorithm was successful.

        Raises
        ------
        Exception
            If the algorithm fails to execute properly.
        """
        ...
    


class CrinkleAlgorithm(_vtk.VTKPythonAlgorithmBase):
    """Algorithm to crinkle cell IDs."""
    def __init__(self) -> None:
        """Initialize algorithm."""
        ...
    
    def RequestData(self, _request, inInfo, outInfo):
        """Perform algorithm execution based on the input data and produce the output.

        Parameters
        ----------
        _request : vtk.vtkInformation
            The request information associated with the algorithm.
        inInfo : vtk.vtkInformationVector
            Information vector describing the input data.
        outInfo : vtk.vtkInformationVector
            Information vector where the output data should be placed.

        Returns
        -------
        int
            Status of the execution. Returns 1 on successful completion.

        """
        ...
    


def outline_algorithm(inp, generate_faces=...):
    """Add vtkOutlineFilter to pipeline.

    Parameters
    ----------
    inp : pyvista.Common
        Input data to be filtered.
    generate_faces : bool, default: False
        Whether to generate faces for the outline.

    Returns
    -------
    vtk.vtkOutlineFilter
        Outline filter applied to the input data.
    """
    ...

def extract_surface_algorithm(inp, pass_pointid=..., pass_cellid=..., nonlinear_subdivision=...):
    """Add vtkDataSetSurfaceFilter to pipeline.

    Parameters
    ----------
    inp : pyvista.Common
        Input data to be filtered.
    pass_pointid : bool, default: False
        If ``True``, pass point IDs to the output.
    pass_cellid : bool, default: False
        If ``True``, pass cell IDs to the output.
    nonlinear_subdivision : int, default: 1
        Level of nonlinear subdivision.

    Returns
    -------
    vtk.vtkDataSetSurfaceFilter
        Surface filter applied to the input data.
    """
    ...

def active_scalars_algorithm(inp, name, preference=...):
    """Add a filter that sets the active scalars.

    Parameters
    ----------
    inp : pyvista.Common
        Input data to be filtered.
    name : str
        Name of the scalars to set as active.
    preference : str, default: 'point'
        Preference for the scalars to be set as active. Options are 'point', 'cell', or 'field'.

    Returns
    -------
    vtk.vtkAlgorithm
        Active scalars filter applied to the input data.
    """
    ...

def pointset_to_polydata_algorithm(inp):
    """Add a filter that casts PointSet to PolyData.

    Parameters
    ----------
    inp : pyvista.PointSet
        Input point set to be cast to PolyData.

    Returns
    -------
    vtk.vtkAlgorithm
        Filter that casts the input PointSet to PolyData.
    """
    ...

def add_ids_algorithm(inp, point_ids=..., cell_ids=...):
    """Add a filter that adds point and/or cell IDs.

    Parameters
    ----------
    inp : pyvista.DataSet
        The input data to which the IDs will be added.
    point_ids : bool, default: True
        If ``True``, point IDs will be added to the input data.
    cell_ids : bool, default: True
        If ``True``, cell IDs will be added to the input data.

    Returns
    -------
    AddIDsAlgorithm
        AddIDsAlgorithm filter.
    """
    ...

def crinkle_algorithm(clip, source):
    """Add a filter that crinkles a clip.

    Parameters
    ----------
    clip : pyvista.DataSet
        The input data to be crinkled.
    source : pyvista.DataSet
        The source of the crinkle.

    Returns
    -------
    CrinkleAlgorithm
        CrinkleAlgorithm filter.

    """
    ...

def cell_data_to_point_data_algorithm(inp, pass_cell_data=...):
    """Add a filter that converts cell data to point data.

    Parameters
    ----------
    inp : pyvista.DataSet
        The input data whose cell data will be converted to point data.
    pass_cell_data : bool, default: False
        If ``True``, the original cell data will be passed to the output.

    Returns
    -------
    vtk.vtkCellDataToPointData
        The vtkCellDataToPointData filter.
    """
    ...

def point_data_to_cell_data_algorithm(inp, pass_point_data=...):
    """Add a filter that converts point data to cell data.

    Parameters
    ----------
    inp : pyvista.DataSet
        The input data whose point data will be converted to cell data.
    pass_point_data : bool, default: False
        If ``True``, the original point data will be passed to the output.

    Returns
    -------
    vtk.vtkPointDataToCellData
        ``vtkPointDataToCellData`` algorithm.
    """
    ...

def triangulate_algorithm(inp):
    """
    Triangulate the input data.

    Parameters
    ----------
    inp : vtk.vtkDataObject
        The input data to be triangulated.

    Returns
    -------
    vtk.vtkTriangleFilter
        The triangle filter that has been applied to the input data.
    """
    ...

def decimation_algorithm(inp, target_reduction):
    """
    Decimate the input data to the target reduction.

    Parameters
    ----------
    inp : vtk.vtkDataObject
        The input data to be decimated.
    target_reduction : float
        The target reduction amount, as a fraction of the original data.

    Returns
    -------
    vtk.vtkQuadricDecimation
        The decimation algorithm that has been applied to the input data.
    """
    ...

