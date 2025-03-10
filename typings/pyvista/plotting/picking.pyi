"""
This type stub file was generated by pyright.
"""

import pyvista
from functools import wraps
from . import _vtk
from .opts import ElementType

"""Module managing picking events."""
PICKED_REPRESENTATION_NAMES = ...
class RectangleSelection:
    """Internal data structure for rectangle based selections.

    Parameters
    ----------
    frustum : _vtk.vtkPlanes
        Frustum that defines the selection.
    viewport : tuple[float, float, float, float]
        The selected viewport coordinates, given as ``(x0, y0, x1, y1)``.

    """
    def __init__(self, frustum, viewport) -> None:
        ...
    
    @property
    def frustum(self) -> _vtk.vtkPlanes:
        """Get the selected frustum through the scene."""
        ...
    
    @property
    def frustum_mesh(self) -> pyvista.PolyData:
        """Get the frustum as a PyVista mesh."""
        ...
    
    @property
    def viewport(self) -> tuple[float, float, float, float]:
        """Get the selected viewport coordinates.

        Coordinates are given as: ``(x0, y0, x1, y1)``
        """
        ...
    


class PointPickingElementHandler:
    """Internal picking handler for element-based picking.

    This handler is only valid for single point picking operations.

    Parameters
    ----------
    mode : ElementType, optional
        The element type to pick.
    callback : callable, optional
        A callback function to be executed on picking events.
    """
    def __init__(self, mode: ElementType = ..., callback=...) -> None:
        ...
    
    @property
    def picker(self): # -> None:
        """Get or set the picker instance."""
        ...
    
    @picker.setter
    def picker(self, picker): # -> None:
        ...
    
    def get_mesh(self): # -> DataSet | pyvista_ndarray | None:
        """Get the picked mesh.

        Returns
        -------
        pyvista.DataSet
            Picked mesh.

        """
        ...
    
    def get_cell(self, picked_point): # -> PointSet | Any | DataSet | pyvista_ndarray | <subclass of DataSet and MultiBlock> | <subclass of pyvista_ndarray and MultiBlock> | None:
        """Get the picked cell of the picked mesh.

        Parameters
        ----------
        picked_point : sequence[float]
            Coordinates of the picked point.

        Returns
        -------
        pyvista.UnstructuredGrid
            UnstructuredGrid containing the picked cell.

        """
        ...
    
    def get_face(self, picked_point): # -> UnstructuredGrid | Any:
        """Get the picked face of the picked cell.

        Parameters
        ----------
        picked_point : sequence[float]
            Coordinates of the picked point.

        Returns
        -------
        pyvista.UnstructuredGrid
            UnstructuredGrid containing the picked face.

        """
        ...
    
    def get_edge(self, picked_point): # -> Any | UnstructuredGrid:
        """Get the picked edge of the picked cell.

        Parameters
        ----------
        picked_point : sequence[float]
            Coordinates of the picked point.

        Returns
        -------
        pyvista.UnstructuredGrid
            UnstructuredGrid containing the picked edge.

        """
        ...
    
    def get_point(self, picked_point): # -> PolyData:
        """Get the picked point of the picked mesh.

        Parameters
        ----------
        picked_point : sequence[float]
            Coordinates of the picked point.

        Returns
        -------
        pyvista.PolyData
            Picked mesh containing the point.

        """
        ...
    
    def __call__(self, picked_point, picker): # -> None:
        """Perform the pick."""
        ...
    


class PickingInterface:
    """An internal class to hold core picking related features."""
    def __init__(self, *args, **kwargs) -> None:
        """Initialize the picking interface."""
        ...
    
    @property
    def picked_point(self): # -> None:
        """Return the picked point.

        This returns the picked point after selecting a point.

        Returns
        -------
        numpy.ndarray or None
            Picked point if available.

        """
        ...
    
    def get_pick_position(self):
        """Get the pick position or area.

        Returns
        -------
        sequence
            Picked position or area as ``(x0, y0, x1, y1)``.

        """
        ...
    
    def pick_click_position(self):
        """Get corresponding click location in the 3D plot.

        Returns
        -------
        tuple
            Three item tuple with the 3D picked position.

        """
        ...
    
    def pick_mouse_position(self):
        """Get corresponding mouse location in the 3D plot.

        Returns
        -------
        tuple
            Three item tuple with the 3D picked position.

        """
        ...
    
    def disable_picking(self): # -> None:
        """Disable any active picking and remove observers.

        Examples
        --------
        Enable and then disable picking.

        >>> import pyvista as pv
        >>> mesh = pv.Sphere(center=(1, 0, 0))
        >>> cube = pv.Cube()
        >>> pl = pv.Plotter()
        >>> _ = pl.add_mesh(mesh)
        >>> _ = pl.add_mesh(cube)
        >>> _ = pl.enable_mesh_picking()
        >>> pl.disable_picking()

        """
        ...
    
    def enable_point_picking(self, callback=..., tolerance=..., left_clicking=..., picker=..., show_message=..., font_size=..., color=..., point_size=..., show_point=..., use_picker=..., pickable_window=..., clear_on_no_selection=..., **kwargs): # -> None:
        """Enable picking at points under the cursor.

        Enable picking a point at the mouse location in the render
        view using the right mouse button. This point is saved to the
        ``.picked_point`` attribute on the plotter. Pass a callback
        that takes that point as an argument. The picked
        point can either be a point on the first intersecting mesh, or
        a point in the 3D window.

        The ``picker`` choice will help determine how the point picking
        is performed.

        Parameters
        ----------
        callback : callable, optional
            When input, calls this callable after a pick is made. The
            picked point is input as the first parameter to this
            callable.

        tolerance : float, tolerance: 0.025
            Specify tolerance for performing pick operation. Tolerance
            is specified as fraction of rendering window
            size. Rendering window size is measured across diagonal.
            This is only valid for some choices of ``picker``.

        left_clicking : bool, default: False
            When ``True``, points can be picked by clicking the left mouse
            button. Default is to use the right mouse button.

        picker : str | PickerType, optional
            Choice of VTK picker class type:

                * ``'hardware'``: Uses ``vtkHardwarePicker`` which is more
                  performant for large geometries (default).
                * ``'cell'``: Uses ``vtkCellPicker``.
                * ``'point'``: Uses ``vtkPointPicker`` which will snap to
                  points on the surface of the mesh.
                * ``'volume'``: Uses ``vtkVolumePicker``.

        show_message : bool | str, default: True
            Show the message about how to use the point picking
            tool. If this is a string, that will be the message shown.

        font_size : int, default: 18
            Sets the size of the message.

        color : ColorLike, default: "pink"
            The color of the selected mesh when shown.

        point_size : int, default: 10
            Size of picked points if ``show_point`` is ``True``.

        show_point : bool, default: True
            Show the picked point after clicking.

        use_picker : bool, default: False
            When ``True``, the callback will also be passed the picker.

        pickable_window : bool, default: False
            When ``True`` and the chosen picker supports it, points in the
            3D window are pickable.

        clear_on_no_selection : bool, default: True
            Clear the selections when no point is selected.

        **kwargs : dict, optional
            All remaining keyword arguments are used to control how
            the picked point is interactively displayed.

        Examples
        --------
        Enable point picking with a custom message.

        >>> import pyvista as pv
        >>> pl = pv.Plotter()
        >>> _ = pl.add_mesh(pv.Sphere())
        >>> _ = pl.add_mesh(pv.Cube(), pickable=False)
        >>> pl.enable_point_picking(show_message='Pick a point')

        See :ref:`point_picking_example` for a full example using this method.

        """
        ...
    
    def enable_rectangle_picking(self, callback=..., show_message=..., font_size=..., start=..., show_frustum=..., style=..., color=..., **kwargs): # -> None:
        """Enable rectangle based picking at cells.

        Press ``"r"`` to enable rectangle based selection. Press
        ``"r"`` again to turn it off.

        Picking with the rectangle selection tool provides two values that
        are passed as the ``RectangleSelection`` object in the callback:

        1. ``RectangleSelection.viewport``: the viewport coordinates of the
           selection rectangle.
        2. ``RectangleSelection.frustum``: the full frustum made from
           the selection rectangle into the scene.

        Parameters
        ----------
        callback : callable, optional
            When input, calls this callable after a selection is made.
            The ``RectangleSelection`` is the only passed argument
            containing the viewport coordinates of the selection and the
            projected frustum.

        show_message : bool | str, default: True
            Show the message about how to use the cell picking tool. If this
            is a string, that will be the message shown.

        font_size : int, default: 18
            Sets the font size of the message.

        start : bool, default: True
            Automatically start the cell selection tool.

        show_frustum : bool, default: False
            Show the frustum in the scene.

        style : str, default: "wireframe"
            Visualization style of the selection frustum. One of the
            following: ``style='surface'``, ``style='wireframe'``, or
            ``style='points'``.

        color : ColorLike, default: "pink"
            The color of the selected frustum when shown.

        **kwargs : dict, optional
            All remaining keyword arguments are used to control how
            the selection frustum is interactively displayed.

        Examples
        --------
        Add a mesh and a cube to a plot and enable cell picking.

        >>> import pyvista as pv
        >>> mesh = pv.Sphere(center=(1, 0, 0))
        >>> cube = pv.Cube()
        >>> pl = pv.Plotter()
        >>> _ = pl.add_mesh(mesh)
        >>> _ = pl.add_mesh(cube)
        >>> _ = pl.enable_rectangle_picking()

        """
        ...
    


class PickingMethods(PickingInterface):
    """Internal class to contain picking utilities."""
    def __init__(self, *args, **kwargs) -> None:
        """Initialize the picking methods."""
        ...
    
    @property
    def picked_actor(self): # -> None:
        """Return the picked mesh.

        This returns the picked actor after selecting a mesh with
        :func:`enable_surface_point_picking <pyvista.Plotter.enable_surface_point_picking>` or
        :func:`enable_mesh_picking <pyvista.Plotter.enable_mesh_picking>`.

        Returns
        -------
        pyvista.Actor or None
            Picked actor if available.

        """
        ...
    
    @property
    def picked_mesh(self): # -> None:
        """Return the picked mesh.

        This returns the picked mesh after selecting a mesh with
        :func:`enable_surface_point_picking <pyvista.Plotter.enable_surface_point_picking>` or
        :func:`enable_mesh_picking <pyvista.Plotter.enable_mesh_picking>`.

        Returns
        -------
        pyvista.DataSet or None
            Picked mesh if available.

        """
        ...
    
    @property
    def picked_cell(self): # -> None:
        """Return the picked cell.

        This returns the picked cell after selecting a cell.

        Returns
        -------
        pyvista.Cell or None
            Picked cell if available.

        """
        ...
    
    @property
    def picked_cells(self): # -> None:
        """Return the picked cells.

        This returns the picked cells after selecting cells.

        Returns
        -------
        pyvista.Cell or None
            Picked cell if available.

        """
        ...
    
    @property
    def picked_block_index(self): # -> None:
        """Return the picked block index.

        This returns the picked block index after selecting a point with
        :func:`enable_point_picking <pyvista.Plotter.enable_point_picking>`.

        Returns
        -------
        int or None
            Picked block if available. If ``-1``, then a non-composite dataset
            was selected.

        """
        ...
    
    @wraps(PickingInterface.disable_picking)
    def disable_picking(self): # -> None:
        """Disable picking."""
        ...
    
    def enable_surface_point_picking(self, callback=..., show_message=..., font_size=..., color=..., show_point=..., point_size=..., tolerance=..., pickable_window=..., left_clicking=..., picker=..., use_picker=..., clear_on_no_selection=..., **kwargs): # -> None:
        """Enable picking of a point on the surface of a mesh.

        Parameters
        ----------
        callback : callable, optional
            When input, calls this callable after a selection is made. The
            ``mesh`` is input as the first parameter to this callable.

        show_message : bool | str, default: True
            Show the message about how to use the mesh picking tool. If this
            is a string, that will be the message shown.

        font_size : int, default: 18
            Sets the font size of the message.

        color : ColorLike, default: "pink"
            The color of the selected mesh when shown.

        show_point : bool, default: True
            Show the selection interactively.

        point_size : int, default: 10
            Size of picked points if ``show_point`` is ``True``.

        tolerance : float, default: 0.025
            Specify tolerance for performing pick operation. Tolerance
            is specified as fraction of rendering window
            size. Rendering window size is measured across diagonal.

            .. warning::
                This is ignored with the ``'hardware'`` ``picker``.

        pickable_window : bool, default: False
            When ``True``, points in the 3D window are pickable.

        left_clicking : bool, default: False
            When ``True``, meshes can be picked by clicking the left
            mousebutton.

            .. note::
               If enabled, left-clicking will **not** display the bounding box
               around the picked mesh.

        picker : str | PickerType, optional
            Choice of VTK picker class type:

                * ``'hardware'``: Uses ``vtkHardwarePicker`` which is more
                  performant for large geometries (default).
                * ``'cell'``: Uses ``vtkCellPicker``.
                * ``'point'``: Uses ``vtkPointPicker`` which will snap to
                  points on the surface of the mesh.
                * ``'volume'``: Uses ``vtkVolumePicker``.

        use_picker : bool, default: False
            When ``True``, the callback will also be passed the picker.

        clear_on_no_selection : bool, default: True
            Clear the selections when no point is selected.

        **kwargs : dict, optional
            All remaining keyword arguments are used to control how
            the picked path is interactively displayed.

        Notes
        -----
        Picked point can be accessed from :attr:`picked_point
        <pyvista.Plotter.picked_point>` attribute.

        Examples
        --------
        Add a cube to a plot and enable cell picking.

        >>> import pyvista as pv
        >>> cube = pv.Cube()
        >>> pl = pv.Plotter()
        >>> _ = pl.add_mesh(cube)
        >>> _ = pl.enable_surface_point_picking()

        See :ref:`surface_point_picking_example` for a full example using this method.

        """
        ...
    
    def enable_mesh_picking(self, callback=..., show=..., show_message=..., style=..., line_width=..., color=..., font_size=..., left_clicking=..., use_actor=..., picker=..., **kwargs): # -> None:
        """Enable picking of a mesh.

        Parameters
        ----------
        callback : callable, optional
            When input, calls this callable after a selection is made. The
            ``mesh`` is input as the first parameter to this callable.

        show : bool, default: True
            Show the selection interactively. Best when combined with
            ``left_clicking``.

        show_message : bool | str, default: True
            Show the message about how to use the mesh picking tool. If this
            is a string, that will be the message shown.

        style : str, default: "wireframe"
            Visualization style of the selection. One of the following:

            * ``'surface'``
            * ``'wireframe'``
            * ``'points'``

        line_width : float, default: 5.0
            Thickness of selected mesh edges.

        color : ColorLike, default: "pink"
            The color of the selected mesh when shown.

        font_size : int, default: 18
            Sets the font size of the message.

        left_clicking : bool, default: False
            When ``True``, meshes can be picked by clicking the left
            mousebutton.

            .. note::
               If enabled, left-clicking will **not** display the bounding box
               around the picked point.

        use_actor : bool, default: False
            If True, the callback will be passed the picked actor instead of
            the mesh object.

        picker : str | PickerType, optional
            Choice of VTK picker class type:

                * ``'hardware'``: Uses ``vtkHardwarePicker`` which is more
                  performant for large geometries (default).
                * ``'cell'``: Uses ``vtkCellPicker``.
                * ``'point'``: Uses ``vtkPointPicker`` which will snap to
                  points on the surface of the mesh.
                * ``'volume'``: Uses ``vtkVolumePicker``.


        **kwargs : dict, optional
            All remaining keyword arguments are used to control how
            the picked path is interactively displayed.

        Returns
        -------
        vtk.vtkPropPicker
            Property picker.

        Examples
        --------
        Add a sphere and a cube to a plot and enable mesh picking. Enable
        ``left_clicking`` to immediately start picking on the left click and
        disable showing the box. You can still press the ``p`` key to select
        meshes.

        >>> import pyvista as pv
        >>> mesh = pv.Sphere(center=(1, 0, 0))
        >>> cube = pv.Cube()
        >>> pl = pv.Plotter()
        >>> _ = pl.add_mesh(mesh)
        >>> _ = pl.add_mesh(cube)
        >>> _ = pl.enable_mesh_picking()

        See :ref:`mesh_picking_example` for a full example using this method.

        """
        ...
    
    def enable_rectangle_through_picking(self, callback=..., show=..., style=..., line_width=..., color=..., show_message=..., font_size=..., start=..., show_frustum=..., **kwargs): # -> None:
        """Enable rectangle based cell picking through the scene.

        Parameters
        ----------
        callback : callable, optional
            When input, calls this callable after a selection is made.
            The picked cells is the only passed argument.

        show : bool, default: True
            Show the selection interactively.

        style : str, default: "wireframe"
            Visualization style of the selection frustum. One of the
            following: ``style='surface'``, ``style='wireframe'``, or
            ``style='points'``.

        line_width : float, default: 5.0
            Thickness of selected mesh edges.

        color : ColorLike, default: "pink"
            The color of the selected frustum when shown.

        show_message : bool | str, default: True
            Show the message about how to use the cell picking tool. If this
            is a string, that will be the message shown.

        font_size : int, default: 18
            Sets the font size of the message.

        start : bool, default: True
            Automatically start the cell selection tool.

        show_frustum : bool, default: False
            Show the frustum in the scene.

        **kwargs : dict, optional
            All remaining keyword arguments are used to control how
            the selection frustum is interactively displayed.

        """
        ...
    
    def enable_rectangle_visible_picking(self, callback=..., show=..., style=..., line_width=..., color=..., show_message=..., font_size=..., start=..., show_frustum=..., **kwargs): # -> None:
        """Enable rectangle based cell picking on visible surfaces.

        Parameters
        ----------
        callback : callable, optional
            When input, calls this callable after a selection is made.
            The picked cells is the only passed argument.

        show : bool, default: True
            Show the selection interactively.

        style : str, default: "wireframe"
            Visualization style of the selection frustum. One of the
            following: ``style='surface'``, ``style='wireframe'``, or
            ``style='points'``.

        line_width : float, default: 5.0
            Thickness of selected mesh edges.

        color : ColorLike, default: "pink"
            The color of the selected frustum when shown.

        show_message : bool | str, default: True
            Show the message about how to use the cell picking tool. If this
            is a string, that will be the message shown.

        font_size : int, default: 18
            Sets the font size of the message.

        start : bool, default: True
            Automatically start the cell selection tool.

        show_frustum : bool, default: False
            Show the frustum in the scene.

        **kwargs : dict, optional
            All remaining keyword arguments are used to control how
            the selection frustum is interactively displayed.

        """
        ...
    
    def enable_cell_picking(self, callback=..., through=..., show=..., show_message=..., style=..., line_width=..., color=..., font_size=..., start=..., show_frustum=..., **kwargs): # -> None:
        """Enable picking of cells with a rectangle selection tool.

        Press ``"r"`` to enable rectangle based selection.  Press
        ``"r"`` again to turn it off. Selection will be saved to
        ``self.picked_cells``.

        All meshes in the scene are available for picking by default.
        If you would like to only pick a single mesh in the scene,
        use the ``pickable=False`` argument when adding the other
        meshes to the scene.

        When multiple meshes are being picked, the picked cells
        in ``self.picked_cells`` will be a :class:`MultiBlock`
        dataset for each mesh's selection.

        Uses last input mesh for input by default.

        .. warning::
           Visible cell picking (``through=False``) will only work if
           the mesh is displayed with a ``'surface'`` representation
           style (the default).

        Parameters
        ----------
        callback : callable, optional
            When input, calls this callable after a selection is made.
            The picked_cells are input as the first parameter to this
            callable.

        through : bool, default: True
            When ``True`` the picker will select all cells
            through the mesh(es). When ``False``, the picker will select
            only visible cells on the selected surface(s).

        show : bool, default: True
            Show the selection interactively.

        show_message : bool | str, default: True
            Show the message about how to use the cell picking tool. If this
            is a string, that will be the message shown.

        style : str, default: "wireframe"
            Visualization style of the selection.  One of the
            following: ``style='surface'``, ``style='wireframe'``, or
            ``style='points'``.

        line_width : float, default: 5.0
            Thickness of selected mesh edges.

        color : ColorLike, default: "pink"
            The color of the selected mesh when shown.

        font_size : int, default: 18
            Sets the font size of the message.

        start : bool, default: True
            Automatically start the cell selection tool.

        show_frustum : bool, default: False
            Show the frustum in the scene.

        **kwargs : dict, optional
            All remaining keyword arguments are used to control how
            the selection is interactively displayed.

        Examples
        --------
        Add a mesh and a cube to a plot and enable cell picking.

        >>> import pyvista as pv
        >>> mesh = pv.Sphere(center=(1, 0, 0))
        >>> cube = pv.Cube()
        >>> pl = pv.Plotter()
        >>> _ = pl.add_mesh(mesh)
        >>> _ = pl.add_mesh(cube)
        >>> _ = pl.enable_cell_picking()

        """
        ...
    
    def enable_element_picking(self, callback=..., mode=..., show=..., show_message=..., font_size=..., color=..., tolerance=..., pickable_window=..., left_clicking=..., picker=..., **kwargs): # -> None:
        """Select individual elements on a mesh.

        Parameters
        ----------
        callback : callable, optional
            When input, calls this callable after a selection is made. The
            ``mesh`` is input as the first parameter to this callable.

        mode : str | ElementType, default: "cell"
            The picking mode. Either ``"mesh"``, ``"cell"``, ``"face"``,
            ``"edge"``, or ``"point"``.

        show : bool, default: True
            Show the selection interactively.

        show_message : bool | str, default: True
            Show the message about how to use the mesh picking tool. If this
            is a string, that will be the message shown.

        font_size : int, default: 18
            Sets the font size of the message.

        color : ColorLike, default: "pink"
            The color of the selected mesh when shown.

        tolerance : float, default: 0.025
            Specify tolerance for performing pick operation. Tolerance
            is specified as fraction of rendering window
            size. Rendering window size is measured across diagonal.

            .. warning::
                This is ignored with the ``'hardware'`` ``picker``.

        pickable_window : bool, default: False
            When ``True``, points in the 3D window are pickable.

        left_clicking : bool, default: False
            When ``True``, meshes can be picked by clicking the left
            mousebutton.

            .. note::
               If enabled, left-clicking will **not** display the bounding box
               around the picked mesh.

        picker : str | PickerType, optional
            Choice of VTK picker class type:

                * ``'hardware'``: Uses ``vtkHardwarePicker`` which is more
                  performant for large geometries (default).
                * ``'cell'``: Uses ``vtkCellPicker``.
                * ``'point'``: Uses ``vtkPointPicker`` which will snap to
                  points on the surface of the mesh.
                * ``'volume'``: Uses ``vtkVolumePicker``.

        **kwargs : dict, optional
            All remaining keyword arguments are used to control how
            the picked path is interactively displayed.

        """
        ...
    
    def enable_block_picking(self, callback=..., side=...): # -> None:
        """Enable composite block picking.

        Use this picker to return the index of a DataSet when using composite
        dataset like :class:`pyvista.MultiBlock` and pass it to a callback.

        Parameters
        ----------
        callback : callable, optional
            When input, this picker calls this callable after a selection is
            made. The composite index is passed to ``callback`` as the first
            argument and the dataset as the second argument.

        side : str, default: "left"
            The mouse button to track (either ``'left'`` or ``'right'``).
            Also accepts ``'r'`` or ``'l'``.

        Notes
        -----
        The picked block index can be accessed from :attr:`picked_block_index
        <pyvista.Plotter.picked_block_index>` attribute.

        Examples
        --------
        Enable block picking with a multiblock dataset. Left clicking will turn
        blocks blue while right picking will turn the block back to the default
        color.

        >>> import pyvista as pv
        >>> multiblock = pv.MultiBlock(
        ...     [pv.Cube(), pv.Sphere(center=(0, 0, 1))]
        ... )
        >>> pl = pv.Plotter()
        >>> actor, mapper = pl.add_composite(multiblock)
        >>> def turn_blue(index, dataset):
        ...     mapper.block_attr[index].color = 'blue'
        ...
        >>> pl.enable_block_picking(callback=turn_blue, side='left')
        >>> def clear_color(index, dataset):
        ...     mapper.block_attr[index].color = None
        ...
        >>> pl.enable_block_picking(callback=clear_color, side='right')
        >>> pl.show()

        """
        ...
    


class PickingHelper(PickingMethods):
    """Internal container class to contain picking helper methods."""
    def __init__(self, *args, **kwargs) -> None:
        """Initialize the picking methods."""
        ...
    
    def fly_to_mouse_position(self, focus=...): # -> None:
        """Focus on last stored mouse position."""
        ...
    
    def enable_fly_to_right_click(self, callback=...): # -> None:
        """Set the camera to track right click positions.

        A convenience method to track right click positions and fly to
        the picked point in the scene. The callback will be passed the
        point in 3D space.

        Parameters
        ----------
        callback : callable
            Callback to call immediately after right clicking.

        """
        ...
    
    def enable_path_picking(self, callback=..., show_message=..., font_size=..., color=..., point_size=..., line_width=..., show_path=..., tolerance=..., **kwargs): # -> None:
        """Enable picking at paths.

        This is a convenience method for :func:`enable_point_picking
        <pyvista.Plotter.enable_point_picking>` to keep track of the
        picked points and create a line using those points.

        The line is saved to the ``.picked_path`` attribute of this
        plotter

        Parameters
        ----------
        callback : callable, optional
            When given, calls this callable after a pick is made.  The
            entire picked path is passed as the only parameter to this
            callable.

        show_message : bool | str, default: True
            Show the message about how to use the point picking
            tool. If this is a string, that will be the message shown.

        font_size : int, default: 18
            Sets the size of the message.

        color : ColorLike, default: "pink"
            The color of the selected mesh when shown.

        point_size : int, default: 10
            Size of picked points if ``show_path`` is ``True``.

        line_width : float, default: 5.0
            Thickness of path representation if ``show_path`` is
            ``True``.

        show_path : bool, default: True
            Show the picked path interactively.

        tolerance : float, default: 0.025
            Specify tolerance for performing pick operation. Tolerance
            is specified as fraction of rendering window
            size.  Rendering window size is measured across diagonal.

        **kwargs : dict, optional
            All remaining keyword arguments are used to control how
            the picked path is interactively displayed.

        """
        ...
    
    def enable_geodesic_picking(self, callback=..., show_message=..., font_size=..., color=..., point_size=..., line_width=..., tolerance=..., show_path=..., keep_order=..., **kwargs): # -> None:
        """Enable picking at geodesic paths.

        This is a convenience method for ``enable_point_picking`` to
        keep track of the picked points and create a geodesic path
        using those points.

        The geodesic path is saved to the ``.picked_geodesic``
        attribute of this plotter.

        Parameters
        ----------
        callback : callable, optional
            When given, calls this callable after a pick is made.  The
            entire picked, geodesic path is passed as the only
            parameter to this callable.

        show_message : bool | str, default: True
            Show the message about how to use the point picking
            tool. If this is a string, that will be the message shown.

        font_size : int, default: 18
            Sets the size of the message.

        color : ColorLike, default: "pink"
            The color of the selected mesh when shown.

        point_size : int, default: 10
            Size of picked points if ``show_path`` is ``True``.

        line_width : float, default: 5.0
            Thickness of path representation if ``show_path`` is
            ``True``.

        tolerance : float, default: 0.025
            Specify tolerance for performing pick operation. Tolerance
            is specified as fraction of rendering window
            size.  Rendering window size is measured across diagonal.

        show_path : bool, default: True
            Show the picked path interactively.

        keep_order : bool, default: True
            If ``True``, the created geodesic path is a single ordered
            and cleaned line from the first point to the last.

            .. note::

                In older versions there were apparent discontinuities
                in the resulting path due to the behavior of the
                underlying VTK filter which corresponds to
                ``keep_order=False``.

            .. versionadded:: 0.32.0

        **kwargs : dict, optional
            All remaining keyword arguments are used to control how
            the picked path is interactively displayed.

        """
        ...
    
    def enable_horizon_picking(self, callback=..., normal=..., width=..., show_message=..., font_size=..., color=..., point_size=..., line_width=..., show_path=..., opacity=..., show_horizon=..., **kwargs): # -> None:
        """Enable horizon picking.

        Helper for the ``enable_path_picking`` method to also show a
        ribbon surface along the picked path. Ribbon is saved under
        ``.picked_horizon``.

        Parameters
        ----------
        callback : callable, optional
            When given, calls this callable after a pick is made.  The
            entire picked path is passed as the only parameter to this
            callable.

        normal : sequence[float], default: (0.0, 0.0, 1.0)
            The normal to the horizon surface's projection plane.

        width : float, optional
            The width of the horizon surface. Default behaviour will
            dynamically change the surface width depending on its
            length.

        show_message : bool | str, default: True
            Show the message about how to use the horizon picking
            tool. If this is a string, that will be the message shown.

        font_size : int, default: 18
            Sets the font size of the message.

        color : ColorLike, default: "pink"
            The color of the horizon surface if shown.

        point_size : int, default: 10
            Size of picked points if ``show_horizon`` is ``True``.

        line_width : float, default: 5.0
            Thickness of path representation if ``show_horizon`` is
            ``True``.

        show_path : bool, default: True
            Show the picked path that the horizon is built from
            interactively.

        opacity : float, default: 0.75
            The opacity of the horizon surface if shown.

        show_horizon : bool, default: True
            Show the picked horizon surface interactively.

        **kwargs : dict, optional
            All remaining keyword arguments are used to control how
            the picked path is interactively displayed.

        """
        ...
    


