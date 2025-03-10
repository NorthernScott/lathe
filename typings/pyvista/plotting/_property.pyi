"""
This type stub file was generated by pyright.
"""

from pyvista.core.utilities.misc import no_new_attr
from . import _vtk
from .colors import Color
from .opts import InterpolationType

"""This module contains the Property class."""
@no_new_attr
class Property(_vtk.vtkProperty):
    """Wrap vtkProperty and expose it pythonically.

    This class is used to set the property of actors.

    Parameters
    ----------
    theme : pyvista.plotting.themes.Theme, optional
        Plot-specific theme.

    interpolation : str, default: :attr:`pyvista.plotting.themes._LightingConfig.interpolation`
        Set the method of shading. One of the following:

        * ``'Physically based rendering'`` - Physically based rendering.
        * ``'pbr'`` - Alias for Physically based rendering.
        * ``'Phong'`` - Phong shading.
        * ``'Gouraud'`` - Gouraud shading.
        * ``'Flat'`` - Flat Shading.

        This parameter is case insensitive.

    color : ColorLike, default: :attr:`pyvista.plotting.themes.Theme.color`
        Used to make the entire mesh have a single solid color.
        Either a string, RGB list, or hex color string.  For example:
        ``color='white'``, ``color='w'``, ``color=[1.0, 1.0, 1.0]``, or
        ``color='#FFFFFF'``. Color will be overridden if scalars are
        specified.

    style : str, default: 'surface'
        Visualization style of the mesh.  One of the following:
        ``style='surface'``, ``style='wireframe'``, ``style='points'``.
        Note that ``'wireframe'`` only shows a wireframe of the outer
        geometry.

    metallic : float, default: :attr:`pyvista.plotting.themes._LightingConfig.metallic`
        Usually this value is either 0 or 1 for a real material but any
        value in between is valid. This parameter is only used by PBR
        :attr:`interpolation`.

    roughness : float, default: :attr:`pyvista.plotting.themes._LightingConfig.roughness`
        This value has to be between 0 (glossy) and 1 (rough). A glossy
        material has reflections and a high specular part. This parameter
        is only used by PBR :attr:`interpolation`.

    point_size : float, default: :attr:`pyvista.plotting.themes.Theme.point_size`
        Size of the points represented by this property.

    opacity : float, default: :attr:`pyvista.plotting.themes.Theme.opacity`
        Opacity of the mesh. A single float value that will be applied globally
        opacity of the mesh and uniformly applied everywhere - should be
        between 0 and 1.

    ambient : float, default: :attr:`pyvista.plotting.themes._LightingConfig.ambient`
        When lighting is enabled, this is the amount of light in the range
        of 0 to 1 that reaches the actor when not directed at the light
        source emitted from the viewer.

    diffuse : float, default: :attr:`pyvista.plotting.themes._LightingConfig.diffuse`
        The diffuse lighting coefficient.

    specular : float, default: :attr:`pyvista.plotting.themes._LightingConfig.specular`
        The specular lighting coefficient.

    specular_power : float, default: :attr:`pyvista.plotting.themes._LightingConfig.specular_power`
        The specular power. Must be between 0.0 and 128.0.

    show_edges : bool, default: :attr:`pyvista.plotting.themes.Theme.show_edges`
        Shows the edges.  Does not apply to a wireframe representation.

    edge_color : ColorLike, default: :attr:`pyvista.plotting.themes.Theme.edge_color`
        The solid color to give the edges when ``show_edges=True``.
        Either a string, RGB list, or hex color string.

    render_points_as_spheres : bool, default: :attr:`pyvista.plotting.themes.Theme.render_points_as_spheres`
        Render points as spheres rather than dots.

    render_lines_as_tubes : bool, default: :attr:`pyvista.plotting.themes.Theme.render_lines_as_tubes`
        Show lines as thick tubes rather than flat lines.  Control
        the width with ``line_width``.

    lighting : bool, default: :attr:`pyvista.plotting.themes.Theme.lighting`
        Enable or disable view direction lighting.

    line_width : float, default: :attr:`pyvista.plotting.themes.Theme.line_width`
        Thickness of lines.  Only valid for wireframe and surface
        representations.

    culling : str | bool, optional
        Does not render faces that are culled. This can be helpful for
        dense surface meshes, especially when edges are visible, but can
        cause flat meshes to be partially displayed. Defaults to
        ``'none'``. One of the following:

        * ``"back"`` - Enable backface culling
        * ``"front"`` - Enable frontface culling
        * ``'none'`` - Disable both backface and frontface culling

    edge_opacity : float, default: :attr:`pyvista.plotting.themes.Theme.edge_opacity`
        Edge opacity of the mesh. A single float value that will be applied globally
        edge opacity of the mesh and uniformly applied everywhere - should be
        between 0 and 1.

        .. note::
            `edge_opacity` uses ``SetEdgeOpacity`` as the underlying method which
            requires VTK version 9.3 or higher. If ``SetEdgeOpacity`` is not
            available, `edge_opacity` is set to 1.

    Examples
    --------
    Create a :class:`pyvista.Actor` and assign properties to it.

    >>> import pyvista as pv
    >>> actor = pv.Actor()
    >>> actor.prop = pv.Property(
    ...     color='r',
    ...     show_edges=True,
    ...     interpolation='Physically based rendering',
    ...     metallic=0.5,
    ...     roughness=0.1,
    ... )

    Visualize how the property would look when applied to a mesh.

    >>> actor.prop.plot()

    Set custom properties not directly available in
    :func:`pyvista.Plotter.add_mesh`. Here, we set diffuse, ambient, and
    specular power and colors.

    >>> pl = pv.Plotter()
    >>> actor = pl.add_mesh(pv.Sphere())
    >>> prop = actor.prop
    >>> prop.diffuse = 0.6
    >>> prop.diffuse_color = 'w'
    >>> prop.ambient = 0.3
    >>> prop.ambient_color = 'r'
    >>> prop.specular = 0.5
    >>> prop.specular_color = 'b'
    >>> pl.show()

    """
    _theme = ...
    _color_set = ...
    def __init__(self, theme=..., interpolation=..., color=..., style=..., metallic=..., roughness=..., point_size=..., opacity=..., ambient=..., diffuse=..., specular=..., specular_power=..., show_edges=..., edge_color=..., render_points_as_spheres=..., render_lines_as_tubes=..., lighting=..., line_width=..., culling=..., edge_opacity=...) -> None:
        """Initialize this property."""
        ...
    
    @property
    def style(self) -> str:
        """Return or set the visualization style of the mesh.

        One of the following (case insensitive):

        * ``'surface'``
        * ``'wireframe'``
        * ``'points'``

        Examples
        --------
        Get the default style and visualize it.

        >>> import pyvista as pv
        >>> prop = pv.Property()
        >>> prop.style
        'Surface'

        >>> prop.plot()

        Visualize the wireframe style.

        >>> prop.style = 'wireframe'
        >>> prop.plot()

        Visualize the points style.

        >>> prop.style = 'points'
        >>> prop.point_size = 5.0
        >>> prop.plot()
        """
        ...
    
    @style.setter
    def style(self, new_style: str): # -> None:
        ...
    
    @property
    def color(self) -> Color:
        """Return or set the color of this property.

        Either a string, RGB list, or hex color string.  For example:
        ``color='white'``, ``color='w'``, ``color=[1.0, 1.0, 1.0]``, or
        ``color='#FFFFFF'``. Color will be overridden if scalars are
        specified.

        Examples
        --------
        Get the default color and visualize it.

        >>> import pyvista as pv
        >>> prop = pv.Property()
        >>> prop.color
        Color(name='lightblue', hex='#add8e6ff', opacity=255)

        >>> prop.plot()

        Visualize a red color.

        >>> prop.color = 'red'
        >>> prop.plot()

        Visualize an RGB color.

        >>> prop.color = (0.5, 0.5, 0.1)
        >>> prop.plot()

        """
        ...
    
    @color.setter
    def color(self, value): # -> None:
        ...
    
    @property
    def edge_color(self) -> Color:
        """Return or set the edge color of this property.

        The solid color to give the edges when ``show_edges=True``.
        Either a string, RGB list, or hex color string.

        Examples
        --------
        Get the default edge color and visualize it. Set the edge's visibility
        to ``True`` so we can see them.

        >>> import pyvista as pv
        >>> prop = pv.Property()
        >>> prop.edge_color
        Color(name='black', hex='#000000ff', opacity=255)

        >>> prop.show_edges = True
        >>> prop.plot()

        Visualize red edges.

        >>> prop.edge_color = 'red'
        >>> prop.plot()

        """
        ...
    
    @edge_color.setter
    def edge_color(self, value): # -> None:
        ...
    
    @property
    def opacity(self) -> float:
        """Return or set the opacity of this property.

        The opacity is applied to the surface uniformly.

        Property has range ``[0.0, 1.0]``. A value of ``1.0`` is totally opaque
        and ``0.0`` is completely transparent.

        Examples
        --------
        Get the default opacity and visualize it.

        >>> import pyvista as pv
        >>> prop = pv.Property()
        >>> prop.opacity
        1.0

        >>> prop.plot()

        Visualize an opacity value of ``0.75``.

        >>> prop.opacity = 0.75
        >>> prop.plot()

        Visualize an opacity of ``0.25``.

        >>> prop.opacity = 0.25
        >>> prop.plot()

        """
        ...
    
    @opacity.setter
    def opacity(self, value: float): # -> None:
        ...
    
    @property
    def edge_opacity(self) -> float:
        """Return or set the edge opacity of this property.

        Edge opacity of the mesh. A single float value that will be applied globally
        edge opacity of the mesh and uniformly applied everywhere. Between 0 and 1.

        .. note::
            `edge_opacity` uses ``SetEdgeOpacity`` as the underlying method which
            requires VTK version 9.3 or higher. If ``SetEdgeOpacity`` is not
            available, `edge_opacity` is set to 1.

        Examples
        --------
        Get the default edge opacity and visualize it.

        >>> import pyvista as pv
        >>> prop = pv.Property()
        >>> prop.edge_opacity
        1.0
        >>> prop.show_edges = True
        >>> prop.plot()

        Visualize an edge opacity of ``0.75``.

        >>> prop.edge_opacity = 0.75
        >>> prop.plot()

        Visualize wn edge opacity of ``0.25``.

        >>> prop.edge_opacity = 0.25
        >>> prop.plot()

        """
        ...
    
    @edge_opacity.setter
    def edge_opacity(self, value: float): # -> None:
        ...
    
    @property
    def show_edges(self) -> bool:
        """Return or set the visibility of edges.

        Shows or hides the edges. Does not apply to a wireframe
        :attr:`style`.

        Examples
        --------
        Get the default edge visibility and visualize it.

        >>> import pyvista as pv
        >>> prop = pv.Property()
        >>> prop.show_edges
        False
        >>> prop.plot()

        Visualize setting the visibility to ``True``.

        >>> prop.show_edges = True
        >>> prop.plot()

        """
        ...
    
    @show_edges.setter
    def show_edges(self, value: bool): # -> None:
        ...
    
    @property
    def lighting(self) -> bool:
        """Return or set view direction lighting.

        Examples
        --------
        Get the default lighting and visualize it

        >>> import pyvista as pv
        >>> prop = pv.Property()
        >>> prop.lighting
        True
        >>> prop.plot()

        Visualize disabled lighting.

        >>> prop.lighting = False
        >>> prop.plot()

        """
        ...
    
    @lighting.setter
    def lighting(self, value: bool): # -> None:
        ...
    
    @property
    def ambient(self) -> float:
        """Return or set ambient.

        Default :attr:`pyvista.plotting.themes._LightingConfig.ambient`.

        When lighting is enabled, this is the amount of light that reaches
        the actor when not directed at the light source emitted from the
        viewer.

        Property has range ``[0.0, 1.0]``.

        Examples
        --------
        Get the default ambient value and visualize it.

        >>> import pyvista as pv
        >>> prop = pv.Property()
        >>> prop.ambient
        0.0

        >>> prop.plot()

        Visualize ambient at ``0.25``.

        >>> prop.ambient = 0.25
        >>> prop.plot()

        Visualize ambient at ``0.75``.

        >>> prop.ambient = 0.75
        >>> prop.plot()

        """
        ...
    
    @ambient.setter
    def ambient(self, value: float): # -> None:
        ...
    
    @property
    def diffuse(self) -> float:
        """Return or set the diffuse lighting coefficient.

        Default :attr:`pyvista.plotting.themes._LightingConfig.diffuse`.

        This is the scattering of light by reflection or
        transmission. Diffuse reflection results when light strikes an
        irregular surface such as a frosted window or the surface of a
        frosted or coated light bulb.

        Property has range ``[0.0, 1.0]``.

        Examples
        --------
        Get the default diffuse value and visualize it.

        >>> import pyvista as pv
        >>> prop = pv.Property()
        >>> prop.diffuse
        1.0
        >>> prop.plot()

        Visualize diffuse at ``0.5``.

        >>> prop.diffuse = 0.5
        >>> prop.plot()

        Visualize diffuse at ``0.0``.

        >>> prop.diffuse = 0.0
        >>> prop.plot()

        """
        ...
    
    @diffuse.setter
    def diffuse(self, value: float): # -> None:
        ...
    
    @property
    def specular(self) -> float:
        """Return or set specular.

        Default :attr:`pyvista.plotting.themes._LightingConfig.specular`.

        Specular lighting simulates the bright spot of a light that appears
        on shiny objects.

        Property has range ``[0.0, 1.0]``.

        Examples
        --------
        Get the default specular value and visualize it with Phong shading.

        >>> import pyvista as pv
        >>> prop = pv.Property()
        >>> prop.specular
        0.0
        >>> prop.interpolation = 'phong'
        >>> prop.plot()

        Visualize specular at ``0.5``.

        >>> prop.specular = 0.5
        >>> prop.plot()

        Visualize specular at ``1.0``.

        >>> prop.specular = 1.0
        >>> prop.plot()

        """
        ...
    
    @specular.setter
    def specular(self, value: float): # -> None:
        ...
    
    @property
    def specular_power(self) -> float:
        """Return or set specular power.

        Default :attr:`pyvista.plotting.themes._LightingConfig.specular_power`.

        Property has range ``[0, 128]``.

        Examples
        --------
        Get the default specular power value and visualize it with ``specular = 1.0``
        and Phong shading.

        >>> import pyvista as pv
        >>> prop = pv.Property()
        >>> prop.specular_power
        100.0
        >>> prop.specular = 1.0
        >>> prop.interpolation = 'phong'
        >>> prop.plot()

        Visualize specular power at ``50.0``.

        >>> prop.specular_power = 50.0
        >>> prop.plot()

        Visualize specular power at ``10.0``.

        >>> prop.specular_power = 10.0
        >>> prop.plot()

        """
        ...
    
    @specular_power.setter
    def specular_power(self, value: float): # -> None:
        ...
    
    @property
    def metallic(self) -> float:
        """Return or set metallic.

        Default :attr:`pyvista.plotting.themes._LightingConfig.metallic`.

        This requires that the :attr:`interpolation` be set to ``'Physically based
        rendering'``.

        Property has range ``[0.0, 1.0]``.

        Examples
        --------
        Get the default metallic value and visualize it.

        >>> import pyvista as pv
        >>> prop = pv.Property()
        >>> prop.interpolation = 'pbr'  # required
        >>> prop.metallic
        0.0
        >>> prop.plot()

        Visualize metallic at ``0.5``.

        >>> prop.metallic = 0.5
        >>> prop.plot()

        Visualize metallic at ``1.0``.

        >>> prop.metallic = 1.0
        >>> prop.plot()

        """
        ...
    
    @metallic.setter
    def metallic(self, value: float): # -> None:
        ...
    
    @property
    def roughness(self) -> float:
        """Return or set roughness.

        Default :attr:`pyvista.plotting.themes._LightingConfig.roughness`.

        This requires that the :attr:`interpolation` be set to ``'Physically based
        rendering'``.

        Property has range ``[0.0, 1.0]``. A value of 0 is glossy and a value of 1
        is rough.

        Examples
        --------
        Get the default roughness value.

        >>> import pyvista as pv
        >>> prop = pv.Property()
        >>> prop.roughness
        0.5

        Visualize default roughness with metallic of ``0.5`` and physically-based
        rendering.

        >>> prop.interpolation = 'pbr'
        >>> prop.metallic = 0.5
        >>> prop.plot()

        Visualize roughness at ``0.1``.

        >>> prop.roughness = 0.0
        >>> prop.plot()

        Visualize roughness at ``1.0``.

        >>> prop.roughness = 1.0
        >>> prop.plot()

        """
        ...
    
    @roughness.setter
    def roughness(self, value: bool): # -> None:
        ...
    
    @property
    def interpolation(self) -> InterpolationType:
        """Return or set the method of shading.

        Defaults to :attr:`pyvista.plotting.themes._LightingConfig.interpolation`.

        One of the following options.

        * ``'Physically based rendering'`` - Physically based rendering.
        * ``'pbr'`` - Alias for Physically based rendering.
        * ``'Phong'`` - Phong shading.
        * ``'Gouraud'`` - Gouraud shading.
        * ``'Flat'`` - Flat Shading.

        This parameter is case insensitive.

        Examples
        --------
        Get the default interpolation and visualize it.

        >>> import pyvista as pv
        >>> prop = pv.Property()
        >>> prop.interpolation
        <InterpolationType.FLAT: 0>
        >>> prop.plot()

        Visualize gouraud shading.

        >>> prop.interpolation = 'gouraud'
        >>> prop.plot()

        Visualize phong shading.

        >>> prop.interpolation = 'phong'
        >>> prop.plot()

        Visualize physically based rendering.

        >>> prop.interpolation = 'pbr'
        >>> prop.plot()

        """
        ...
    
    @interpolation.setter
    def interpolation(self, value: str | int | InterpolationType): # -> None:
        ...
    
    @property
    def render_points_as_spheres(self) -> bool:
        """Return or set rendering points as spheres.

        Defaults to :attr:`pyvista.plotting.themes.Theme.render_points_as_spheres`.

        Requires representation style be set to ``'points'``.

        Examples
        --------
        Get the default point rendering and visualize it.

        >>> import pyvista as pv
        >>> prop = pv.Property()
        >>> prop.render_points_as_spheres
        False
        >>> prop.style = 'points'
        >>> prop.point_size = 20
        >>> prop.plot()

        Visualize rendering points as spheres.

        >>> prop.render_points_as_spheres = True
        >>> prop.plot()

        """
        ...
    
    @render_points_as_spheres.setter
    def render_points_as_spheres(self, value: bool): # -> None:
        ...
    
    @property
    def render_lines_as_tubes(self) -> bool:
        """Return or set rendering lines as tubes.

        Defaults to :attr:`pyvista.plotting.themes.Theme.render_lines_as_tubes`.

        Requires lines in the scene, e.g. with :attr:`style` set to ``'wireframe'`` or
        :attr:`show_edges` set to ``True``.

        Examples
        --------
        Get the default line rendering and visualize it.

        >>> import pyvista as pv
        >>> prop = pv.Property()
        >>> prop.render_lines_as_tubes
        False
        >>> prop.show_edges = True
        >>> prop.line_width = 10
        >>> prop.edge_color = 'yellow'
        >>> prop.plot()

        Visualize rendering lines as tubes.

        >>> prop.render_lines_as_tubes = True
        >>> prop.plot()

        """
        ...
    
    @render_lines_as_tubes.setter
    def render_lines_as_tubes(self, value: bool): # -> None:
        ...
    
    @property
    def line_width(self) -> float:
        """Return or set the line width.

        Defaults to :attr:`pyvista.plotting.themes.Theme.line_width`.

        The width is expressed in screen units and must be positive.

        Examples
        --------
        Get the default line width and visualize it.
        >>> import pyvista as pv
        >>> prop = pv.Property()
        >>> prop.line_width
        1.0

        >>> prop.show_edges = True
        >>> prop.plot()

        Visualize a line width of ``5.0``.

        >>> prop.line_width = 5.0
        >>> prop.plot()

        Visualize a line width of ``10.0``.

        >>> prop.line_width = 10.0
        >>> prop.plot()

        """
        ...
    
    @line_width.setter
    def line_width(self, value: float): # -> None:
        ...
    
    @property
    def point_size(self): # -> float:
        """Return or set the point size.

        Defaults to :attr:`pyvista.plotting.themes.Theme.point_size`.

        This requires that the :attr:`style` be set to ``'points'``.

        The size is expressed in screen units and must be positive.

        Examples
        --------
        Get the default point size and visualize it.

        >>> import pyvista as pv
        >>> prop = pv.Property()
        >>> prop.point_size
        5.0
        >>> prop.style = 'points'
        >>> prop.plot()

        Visualize a point size of ``10.0``.

        >>> prop.point_size = 10.0
        >>> prop.plot()

        Visualize a point size of ``50.0``.

        >>> prop.point_size = 50.0
        >>> prop.plot()

        """
        ...
    
    @point_size.setter
    def point_size(self, new_size): # -> None:
        ...
    
    @property
    def culling(self) -> str:
        """Return or set face culling.

        Does not render faces that are culled. This can be helpful for dense
        surface meshes, especially when edges are visible, but can cause flat
        meshes to be partially displayed. Defaults to ``'none'``. One of the
        following:

        * ``"back"`` - Enable backface culling
        * ``"front"`` - Enable frontface culling
        * ``'none'`` - Disable both backface and frontface culling

        Examples
        --------
        Get the default culling value and visualize it.

        >>> import pyvista as pv
        >>> prop = pv.Property()
        >>> prop.culling
        'none'


        >>> prop.plot()

        Visualize backface culling. This looks the same as the default culling
        ``'none'`` because the forward facing faces are already obscuring the
        back faces.

        >>> prop.culling = 'back'
        >>> prop.plot()

        Plot frontface culling. Here, the forward facing faces are hidden
        entirely.

        >>> prop.culling = 'front'
        >>> prop.plot()

        """
        ...
    
    @culling.setter
    def culling(self, value): # -> None:
        ...
    
    @property
    def ambient_color(self) -> Color:
        """Return or set the ambient color of this property.

        Either a string, RGB list, or hex color string.  For example:
        ``color='white'``, ``color='w'``, ``color=[1.0, 1.0, 1.0]``, or
        ``color='#FFFFFF'``. Color will be overridden if scalars are
        specified.

        Examples
        --------
        Get the default ambient color and visualize it with ``ambient = 0.5``.

        >>> import pyvista as pv
        >>> prop = pv.Property()
        >>> prop.ambient_color
        Color(name='lightblue', hex='#add8e6ff', opacity=255)

        >>> prop.ambient = 0.5
        >>> prop.plot()

        Visualize red ambient color.

        >>> prop.ambient_color = 'red'
        >>> prop.plot()

        """
        ...
    
    @ambient_color.setter
    def ambient_color(self, value): # -> None:
        ...
    
    @property
    def specular_color(self) -> Color:
        """Return or set the specular color of this property.

        Either a string, RGB list, or hex color string.  For example:
        ``color='white'``, ``color='w'``, ``color=[1.0, 1.0, 1.0]``, or
        ``color='#FFFFFF'``.

        Examples
        --------
        Get the default specular color and visualize it with ``specular = 0.5`` and
        Phong shading.

        >>> import pyvista as pv
        >>> prop = pv.Property()
        >>> prop.specular_color
        Color(name='lightblue', hex='#add8e6ff', opacity=255)

        >>> prop.specular = 0.5
        >>> prop.interpolation = 'phong'
        >>> prop.plot()

        Visualize red specular color.

        >>> prop.specular_color = 'red'
        >>> prop.plot()

        Visualize white specular color.

        >>> prop.specular_color = 'white'
        >>> prop.plot()
        """
        ...
    
    @specular_color.setter
    def specular_color(self, value): # -> None:
        ...
    
    @property
    def diffuse_color(self) -> Color:
        """Return or set the diffuse color of this property.

        Either a string, RGB list, or hex color string.  For example:
        ``color='white'``, ``color='w'``, ``color=[1.0, 1.0, 1.0]``, or
        ``color='#FFFFFF'``.

        Examples
        --------
        Get the default diffuse color and visualize it with ``diffuse = 0.5``.

        >>> import pyvista as pv
        >>> prop = pv.Property()
        >>> prop.ambient_color
        Color(name='lightblue', hex='#add8e6ff', opacity=255)

        >>> prop.diffuse = 0.5
        >>> prop.plot()

        Visualize red diffuse color.

        >>> prop.diffuse_color = 'red'
        >>> prop.plot()

        Visualize white diffuse color.

        >>> prop.diffuse_color = 'white'
        >>> prop.plot()

        """
        ...
    
    @diffuse_color.setter
    def diffuse_color(self, value): # -> None:
        ...
    
    @property
    def anisotropy(self) -> float:
        """Return or set the anisotropy coefficient.

        This value controls the anisotropy of the material (0.0 means
        isotropic). This requires that the :attr:`interpolation` be set
        to ``'Physically based rendering'``.

        For further details see `PBR Journey Part 2 : Anisotropy model with VTK
        <https://www.kitware.com/pbr-journey-part-2-anisotropy-model-with-vtk/>`_

        Property has range ``[0.0, 1.0]``.

        Notes
        -----
        This attribute requires VTK v9.1.0 or newer.

        Examples
        --------
        Get the default anisotropy and visualize it with physically-based rendering.

        >>> import pyvista as pv
        >>> prop = pv.Property()
        >>> prop.anisotropy
        0.0

        >>> prop.interpolation = 'pbr'  # required
        >>> prop.plot()

        """
        ...
    
    @anisotropy.setter
    def anisotropy(self, value: float): # -> None:
        ...
    
    def plot(self, **kwargs) -> None:
        """Plot this property on the Stanford Bunny.

        This is useful for visualizing how this property would be applied to an
        actor.

        Parameters
        ----------
        **kwargs : dict, optional
            Keyword arguments for :class:`pyvista.Plotter`.

        Examples
        --------
        >>> import pyvista as pv
        >>> prop = pv.Property(
        ...     show_edges=True,
        ...     color='brown',
        ...     edge_color='blue',
        ...     line_width=4,
        ...     specular=1.0,
        ... )
        >>> prop.plot()

        """
        ...
    
    def copy(self) -> Property:
        """Create a deep copy of this property.

        Returns
        -------
        pyvista.Property
            Deep copy of this property.

        Examples
        --------
        >>> import pyvista as pv
        >>> prop = pv.Property()
        >>> prop_copy = prop.copy()

        """
        ...
    
    def __repr__(self): # -> str:
        """Representation of this property."""
        ...
    


