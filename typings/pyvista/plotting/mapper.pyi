"""
This type stub file was generated by pyright.
"""

import pyvista
from typing import TYPE_CHECKING
from pyvista.core.utilities.arrays import FieldAssociation
from pyvista.core.utilities.misc import abstract_class, no_new_attr
from . import _vtk
from .lookup_table import LookupTable
from pyvista.core._typing_core import BoundsLike

"""
This type stub file was generated by pyright.
"""
if TYPE_CHECKING:
    ...
@abstract_class
class _BaseMapper(_vtk.vtkAbstractMapper):
    """Base Mapper with methods common to other mappers."""
    _new_attr_exceptions = ...
    def __init__(self, theme=..., **kwargs) -> None:
        ...
    
    @property
    def bounds(self) -> BoundsLike:
        """Return the bounds of this mapper.

        Examples
        --------
        >>> import pyvista as pv
        >>> mapper = pv.DataSetMapper(dataset=pv.Cube())
        >>> mapper.bounds
        (-0.5, 0.5, -0.5, 0.5, -0.5, 0.5)

        """
        ...
    
    def copy(self) -> _BaseMapper:
        """Create a copy of this mapper.

        Returns
        -------
        pyvista.DataSetMapper
            A copy of this dataset mapper.

        Examples
        --------
        >>> import pyvista as pv
        >>> mapper = pv.DataSetMapper(dataset=pv.Cube())
        >>> mapper_copy = mapper.copy()

        """
        ...
    
    @property
    def scalar_range(self) -> tuple[float, float]:
        """Return or set the scalar range.

        Examples
        --------
        Return the scalar range of a mapper.

        >>> import pyvista as pv
        >>> mesh = pv.Sphere()
        >>> pl = pv.Plotter()
        >>> actor = pl.add_mesh(mesh, scalars=mesh.points[:, 2])
        >>> actor.mapper.scalar_range
        (-0.5, 0.5)
        >>> pl.close()

        Return the scalar range of a composite dataset. In this example it's
        set to its default value of ``(0.0, 1.0)``.

        >>> import pyvista as pv
        >>> dataset = pv.MultiBlock(
        ...     [pv.Cube(), pv.Sphere(center=(0, 0, 1))]
        ... )
        >>> pl = pv.Plotter()
        >>> actor, mapper = pl.add_composite(dataset)
        >>> mapper.scalar_range
        (0.0, 1.0)
        >>> pl.close()

        """
        ...
    
    @scalar_range.setter
    def scalar_range(self, clim):
        ...
    
    @property
    def lookup_table(self) -> pyvista.LookupTable:
        """Return or set the lookup table.

        Examples
        --------
        Return the lookup table of a dataset mapper.

        >>> import pyvista as pv
        >>> mesh = pv.Sphere()
        >>> pl = pv.Plotter()
        >>> actor = pl.add_mesh(
        ...     mesh, scalars=mesh.points[:, 2], cmap='bwr'
        ... )
        >>> actor.mapper.lookup_table
        LookupTable (...)
          Table Range:                (-0.5, 0.5)
          N Values:                   256
          Above Range Color:          None
          Below Range Color:          None
          NAN Color:                  Color(name='darkgray', hex='#a9a9a9ff', opacity=255)
          Log Scale:                  False
          Color Map:                  "bwr"

        Return the lookup table of a composite dataset mapper.

        >>> import pyvista as pv
        >>> dataset = pv.MultiBlock(
        ...     [pv.Cube(), pv.Sphere(center=(0, 0, 1))]
        ... )
        >>> pl = pv.Plotter()
        >>> actor, mapper = pl.add_composite(dataset)
        >>> mapper.lookup_table  # doctest:+SKIP
        <vtkmodules.vtkCommonCore.vtkLookupTable(...) at ...>

        """
        ...
    
    @lookup_table.setter
    def lookup_table(self, table):
        ...
    
    @property
    def color_mode(self) -> str:
        """Return or set the color mode.

        Either ``'direct'``, or ``'map'``.

        * ``'direct'`` - All integer types are treated as colors with values in
          the range 0-255 and floating types are treated as colors with values
          in the range 0.0-1.0
        * ``'map'`` - All scalar data will be mapped through the lookup table.

        """
        ...
    
    @color_mode.setter
    def color_mode(self, value: str):
        ...
    
    @property
    def interpolate_before_map(self) -> bool:
        """Return or set the interpolation of scalars before mapping.

        Enabling makes for a smoother scalars display.  When ``False``,
        OpenGL will interpolate the mapped colors which can result in
        showing colors that are not present in the color map.

        Examples
        --------
        Disable interpolation before mapping.

        >>> import pyvista as pv
        >>> dataset = pv.MultiBlock(
        ...     [pv.Cube(), pv.Sphere(center=(0, 0, 1))]
        ... )
        >>> dataset[0].point_data['data'] = dataset[0].points[:, 2]
        >>> dataset[1].point_data['data'] = dataset[1].points[:, 2]
        >>> pl = pv.Plotter()
        >>> actor, mapper = pl.add_composite(
        ...     dataset,
        ...     show_scalar_bar=False,
        ...     n_colors=3,
        ...     cmap='bwr',
        ... )
        >>> mapper.interpolate_before_map = False
        >>> pl.show()

        Enable interpolation before mapping.

        >>> pl = pv.Plotter()
        >>> actor, mapper = pl.add_composite(
        ...     dataset,
        ...     show_scalar_bar=False,
        ...     n_colors=3,
        ...     cmap='bwr',
        ... )
        >>> mapper.interpolate_before_map = True
        >>> pl.show()

        See :ref:`interpolate_before_mapping_example` for additional
        explanation regarding this attribute.

        """
        ...
    
    @interpolate_before_map.setter
    def interpolate_before_map(self, value: bool):
        ...
    
    @property
    def array_name(self) -> str:
        """Return or set the array name or number and component to color by.

        Examples
        --------
        Show the name of the active scalars in the mapper.

        >>> import pyvista as pv
        >>> mesh = pv.Sphere()
        >>> mesh['my_scalars'] = mesh.points[:, 2]
        >>> pl = pv.Plotter()
        >>> actor = pl.add_mesh(mesh, scalars='my_scalars')
        >>> actor.mapper.array_name
        'my_scalars'
        >>> pl.close()

        """
        ...
    
    @array_name.setter
    def array_name(self, name: str):
        """Return or set the array name or number and component to color by."""
        ...
    
    @property
    def scalar_map_mode(self) -> str:
        """Return or set the scalar map mode.

        Examples
        --------
        Show that the scalar map mode is set to ``'point'`` when setting the
        active scalars to point data.

        >>> import pyvista as pv
        >>> dataset = pv.MultiBlock(
        ...     [pv.Cube(), pv.Sphere(center=(0, 0, 1))]
        ... )
        >>> dataset[0].point_data['data'] = dataset[0].points[:, 2]
        >>> dataset[1].point_data['data'] = dataset[1].points[:, 2]
        >>> pl = pv.Plotter()
        >>> actor, mapper = pl.add_composite(
        ...     dataset, scalars='data', show_scalar_bar=False
        ... )
        >>> mapper.scalar_map_mode
        'point'
        >>> pl.close()

        """
        ...
    
    @scalar_map_mode.setter
    def scalar_map_mode(self, scalar_mode: str | FieldAssociation):
        ...
    
    @property
    def scalar_visibility(self) -> bool:
        """Return or set the scalar visibility.

        Examples
        --------
        Show that scalar visibility is ``False``.

        >>> import pyvista as pv
        >>> mesh = pv.Sphere()
        >>> pl = pv.Plotter()
        >>> actor = pl.add_mesh(mesh)
        >>> actor.mapper.scalar_visibility
        False
        >>> pl.close()

        Show that scalar visibility is ``True``.

        >>> import pyvista as pv
        >>> dataset = pv.MultiBlock(
        ...     [pv.Cube(), pv.Sphere(center=(0, 0, 1))]
        ... )
        >>> dataset[0].point_data['data'] = dataset[0].points[:, 2]
        >>> dataset[1].point_data['data'] = dataset[1].points[:, 2]
        >>> pl = pv.Plotter()
        >>> actor, mapper = pl.add_composite(dataset, scalars='data')
        >>> mapper.scalar_visibility
        True
        >>> pl.close()

        """
        ...
    
    @scalar_visibility.setter
    def scalar_visibility(self, value: bool):
        ...
    
    def update(self):
        """Update this mapper."""
        ...
    


@no_new_attr
class _DataSetMapper(_BaseMapper):
    """Base wrapper for _vtk.vtkDataSetMapper.

    Parameters
    ----------
    dataset : pyvista.DataSet, optional
        Dataset to assign to this mapper.

    theme : pyvista.plotting.themes.Theme, optional
        Plot-specific theme.

    """
    _cmap = ...
    def __init__(self, dataset: pyvista.DataSet | None = ..., theme: pyvista.themes.Theme | None = ...) -> None:
        """Initialize this class."""
        ...
    
    @property
    def dataset(self) -> pyvista.core.dataset.DataSet | None:
        """Return or set the dataset assigned to this mapper."""
        ...
    
    @dataset.setter
    def dataset(self, obj: pyvista.core.dataset.DataSet | _vtk.vtkAlgorithm | _vtk.vtkAlgorithmOutput):
        ...
    
    def as_rgba(self):
        """Convert the active scalars to RGBA.

        This method is used to convert the active scalars to a fixed RGBA array
        and is used for certain mappers that do not support the "map" color
        mode.

        """
        ...
    
    def set_scalars(self, scalars, scalars_name, n_colors=..., scalar_bar_args=..., rgb=..., component=..., preference=..., custom_opac=..., annotations=..., log_scale=..., nan_color=..., above_color=..., below_color=..., cmap=..., flip_scalars=..., opacity=..., categories=..., clim=...):
        """Set the scalars on this mapper.

        Parameters
        ----------
        scalars : numpy.ndarray
            Array of scalars to assign to the mapper.

        scalars_name : str
            If the name of this array exists, scalars is ignored. Otherwise,
            the scalars will be added to the existing dataset and this
            parameter is the name to assign the scalars.

        n_colors : int, default: 256
            Number of colors to use when displaying scalars.

        scalar_bar_args : dict, optional
            Dictionary of keyword arguments to pass when adding the
            scalar bar to the scene. For options, see
            :func:`pyvista.Plotter.add_scalar_bar`.

        rgb : bool, default: False
            If an 2 dimensional array is passed as the scalars, plot
            those values as RGB(A) colors. ``rgba`` is also an
            accepted alias for this.  Opacity (the A) is optional.  If
            a scalars array ending with ``"_rgba"`` is passed, the default
            becomes ``True``.  This can be overridden by setting this
            parameter to ``False``.

        component : int, optional
            Set component of vector valued scalars to plot.  Must be
            nonnegative, if supplied. If ``None``, the magnitude of
            the vector is plotted.

        preference : str, default: 'Point'
            When ``dataset.n_points == dataset.n_cells`` and setting scalars,
            this parameter sets how the scalars will be mapped to the mesh.
            Can be either ``'point'`` or ``'cell'``.

        custom_opac : bool, default: False
            Use custom opacity.

        annotations : dict, optional
            Pass a dictionary of annotations. Keys are the float
            values in the scalars range to annotate on the scalar bar
            and the values are the string annotations.

        log_scale : bool, default: False
            Use log scale when mapping data to colors. Scalars less
            than zero are mapped to the smallest representable
            positive float.

        nan_color : pyvista.ColorLike, optional
            The color to use for all ``NaN`` values in the plotted
            scalar array.

        above_color : pyvista.ColorLike, optional
            Solid color for values below the scalars range
            (``clim``). This will automatically set the scalar bar
            ``above_label`` to ``'above'``.

        below_color : pyvista.ColorLike, optional
            Solid color for values below the scalars range
            (``clim``). This will automatically set the scalar bar
            ``below_label`` to ``'below'``.

        cmap : str, list, or pyvista.LookupTable
            Name of the Matplotlib colormap to use when mapping the
            ``scalars``.  See available Matplotlib colormaps.  Only applicable
            for when displaying ``scalars``.
            ``colormap`` is also an accepted alias for this. If
            ``colorcet`` or ``cmocean`` are installed, their colormaps can be
            specified by name.

            You can also specify a list of colors to override an existing
            colormap with a custom one.  For example, to create a three color
            colormap you might specify ``['green', 'red', 'blue']``.

            This parameter also accepts a :class:`pyvista.LookupTable`. If this
            is set, all parameters controlling the color map like ``n_colors``
            will be ignored.

        flip_scalars : bool, default: False
            Flip direction of cmap. Most colormaps allow ``*_r`` suffix to do
            this as well.

        opacity : str or numpy.ndarray, optional
            Opacity mapping for the scalars array.
            A string can also be specified to map the scalars range to a
            predefined opacity transfer function (options include: 'linear',
            'linear_r', 'geom', 'geom_r'). Or you can pass a custom made
            transfer function that is an array either ``n_colors`` in length or
            shorter.

        categories : bool, default: False
            If set to ``True``, then the number of unique values in the scalar
            array will be used as the ``n_colors`` argument.

        clim : Sequence, optional
            Color bar range for scalars.  Defaults to minimum and
            maximum of scalars array.  Example: ``(-1, 2)``.

        """
        ...
    
    @property
    def cmap(self) -> str | None:
        """Colormap assigned to this mapper."""
        ...
    
    @property
    def resolve(self) -> str:
        """Set or return the global flag to avoid z-buffer resolution.

        A global flag that controls whether the coincident topology
        (e.g., a line on top of a polygon) is shifted to avoid
        z-buffer resolution (and hence rendering problems).

        If not off, there are two methods to choose from.
        `polygon_offset` uses graphics systems calls to shift polygons,
        lines, and points from each other.
        `shift_zbuffer` is a legacy method that is used to remap the z-buffer
        to distinguish vertices, lines, and polygons,
        but does not always produce acceptable results.
        You should only use the polygon_offset method (or none) at this point.

        Returns
        -------
        str
            Global flag to avoid z-buffer resolution.
            Must be either `off`, `polygon_offset` or `shift_zbuffer`.

        Examples
        --------
        >>> import pyvista as pv
        >>> from pyvista import examples

        >>> mesh = examples.download_tri_quadratic_hexahedron()
        >>> surface_sep = mesh.separate_cells().extract_surface(
        ...     nonlinear_subdivision=4
        ... )
        >>> edges = surface_sep.extract_feature_edges()
        >>> surface = mesh.extract_surface(nonlinear_subdivision=4)

        >>> plotter = pv.Plotter()
        >>> _ = plotter.add_mesh(
        ...     surface, smooth_shading=True, split_sharp_edges=True
        ... )
        >>> actor = plotter.add_mesh(edges, color='k', line_width=3)
        >>> actor.mapper.resolve = "polygon_offset"
        >>> plotter.show()

        """
        ...
    
    @resolve.setter
    def resolve(self, resolve):
        ...
    
    def set_custom_opacity(self, opacity, color, n_colors, preference=...):
        """Set custom opacity.

        Parameters
        ----------
        opacity : numpy.ndarray
            Opacity array to color the dataset. Array length must match either
            the number of points or cells.

        color : pyvista.ColorLike
            The color to use with the opacity array.

        n_colors : int
            Number of colors to use.

        preference : str, default: 'point'
            Either ``'point'`` or ``'cell'``. Used when the number of cells
            matches the number of points.

        """
        ...
    
    def __repr__(self):
        """Representation of the mapper."""
        ...
    


class DataSetMapper(_DataSetMapper, _vtk.vtkDataSetMapper):
    """Wrap _vtk.vtkDataSetMapper.

    Parameters
    ----------
    dataset : pyvista.DataSet, optional
        Dataset to assign to this mapper.

    theme : pyvista.plotting.themes.Theme, optional
        Plot-specific theme.

    Examples
    --------
    Create a mapper outside :class:`pyvista.Plotter` and assign it to an
    actor.

    >>> import pyvista as pv
    >>> mesh = pv.Cube()
    >>> mapper = pv.DataSetMapper(dataset=mesh)
    >>> actor = pv.Actor(mapper=mapper)
    >>> actor.plot()

    """
    def __init__(self, dataset: pyvista.DataSet | None = ..., theme: pyvista.themes.Theme | None = ...) -> None:
        """Initialize this class."""
        ...
    


@no_new_attr
class PointGaussianMapper(_DataSetMapper, _vtk.vtkPointGaussianMapper):
    """Wrap vtkPointGaussianMapper.

    Parameters
    ----------
    theme : pyvista.Theme, optional
        The theme to be used.
    emissive : bool, optional
        Whether or not the point should appear emissive. Default is set by the
        theme's ``lighting_params.emissive``.
    scale_factor : float, default: 1.0
        Scale factor applied to the point size.

    """
    def __init__(self, theme=..., emissive=..., scale_factor=...) -> None:
        ...
    
    @property
    def emissive(self) -> bool:
        """Set or return emissive.

        This treats points as emissive light sources. Two points that overlap
        will have their brightness combined.
        """
        ...
    
    @emissive.setter
    def emissive(self, value: bool):
        ...
    
    @property
    def scale_factor(self) -> float:
        """Set or return the scale factor.

        Ranges from 0 to 1. A value of 0 will cause the splats to be rendered
        as simple points. Defaults to 1.0.

        """
        ...
    
    @scale_factor.setter
    def scale_factor(self, value: float):
        ...
    
    @property
    def scale_array(self) -> str:
        """Set or return the name of the array used to scale the splats.

        Scalars used to scale the gaussian points. Accepts a string
        name of an array that is present on the mesh.

        Notes
        -----
        Setting this automatically sets ``scale_factor = 1.0``.

        Examples
        --------
        Plot spheres using `style='points_gaussian'` style and scale them by
        radius.

        >>> import numpy as np
        >>> import pyvista as pv
        >>> n_spheres = 1_000
        >>> pos = np.random.random((n_spheres, 3))
        >>> rad = np.random.random(n_spheres) * 0.01
        >>> pdata = pv.PolyData(pos)
        >>> pdata['radius'] = rad
        >>> pl = pv.Plotter()
        >>> actor = pl.add_mesh(
        ...     pdata,
        ...     style='points_gaussian',
        ...     emissive=False,
        ...     render_points_as_spheres=True,
        ... )
        >>> actor.mapper.scale_array = 'radius'
        >>> pl.show()
        """
        ...
    
    @scale_array.setter
    def scale_array(self, name: str):
        ...
    
    def use_circular_splat(self, opacity: float = ...):
        """Set the fragment shader code to create a circular splat.

        Parameters
        ----------
        opacity : float, default: 1.0
            Desired opacity between 0 and 1.

        Notes
        -----
        This very close to ParaView's PointGaussianMapper, but uses opacity to
        modify the scale as the opacity cannot be set from the actor's property.
        """
        ...
    
    def use_default_splat(self):
        """Clear the fragment shader and use the default splat."""
        ...
    
    def __repr__(self):
        """Representation of the Gaussian mapper."""
        ...
    


@abstract_class
class _BaseVolumeMapper(_BaseMapper):
    """Volume mapper class to override methods and attributes for to volume mappers."""
    def __init__(self, theme=...) -> None:
        """Initialize this class."""
        ...
    
    @property
    def interpolate_before_map(self):
        """Interpolate before map is not supported with volume mappers."""
        ...
    
    @interpolate_before_map.setter
    def interpolate_before_map(self, *args):
        ...
    
    @property
    def dataset(self):
        """Return or set the dataset assigned to this mapper."""
        ...
    
    @dataset.setter
    def dataset(self, obj: pyvista.core.dataset.DataSet | _vtk.vtkAlgorithm | _vtk.vtkAlgorithmOutput):
        ...
    
    @property
    def lookup_table(self):
        ...
    
    @lookup_table.setter
    def lookup_table(self, lut):
        ...
    
    @property
    def scalar_range(self) -> tuple[float, float]:
        """Return or set the scalar range."""
        ...
    
    @scalar_range.setter
    def scalar_range(self, clim):
        ...
    
    @property
    def blend_mode(self) -> str:
        """Return or set the blend mode.

        One of the following:

        * ``"composite"``
        * ``"maximum"``
        * ``"minimum"``
        * ``"average"``
        * ``"additive"``

        Also accepts integer values corresponding to
        ``vtk.vtkVolumeMapper.BlendModes``. For example
        ``vtk.vtkVolumeMapper.COMPOSITE_BLEND``.

        """
        ...
    
    @blend_mode.setter
    def blend_mode(self, value: str | int):
        ...
    
    def __del__(self):
        ...
    


class FixedPointVolumeRayCastMapper(_BaseVolumeMapper, _vtk.vtkFixedPointVolumeRayCastMapper):
    """Wrap _vtk.vtkFixedPointVolumeRayCastMapper."""
    ...


class GPUVolumeRayCastMapper(_BaseVolumeMapper, _vtk.vtkGPUVolumeRayCastMapper):
    """Wrap _vtk.vtkGPUVolumeRayCastMapper."""
    ...


class OpenGLGPUVolumeRayCastMapper(_BaseVolumeMapper, _vtk.vtkOpenGLGPUVolumeRayCastMapper):
    """Wrap _vtk.vtkOpenGLGPUVolumeRayCastMapper."""
    ...


class SmartVolumeMapper(_BaseVolumeMapper, _vtk.vtkSmartVolumeMapper):
    """Wrap _vtk.vtkSmartVolumeMapper."""
    ...


class UnstructuredGridVolumeRayCastMapper(_BaseVolumeMapper, _vtk.vtkUnstructuredGridVolumeRayCastMapper):
    """Wrap _vtk.vtkUnstructuredGridVolumeMapper."""
    ...


