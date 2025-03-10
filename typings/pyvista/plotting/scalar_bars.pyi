"""
This type stub file was generated by pyright.
"""

"""
This type stub file was generated by pyright.
"""
class ScalarBars:
    """Plotter Scalar Bars.

    Parameters
    ----------
    plotter : pyvista.Plotter
        Plotter that the scalar bars are associated with.

    """
    def __init__(self, plotter) -> None:
        """Initialize ScalarBars."""
        ...
    
    def clear(self):
        """Remove all scalar bars and resets all scalar bar properties."""
        ...
    
    def __repr__(self):
        """Nice representation of this class."""
        ...
    
    def remove_scalar_bar(self, title=..., render=...):
        """Remove a scalar bar.

        Parameters
        ----------
        title : str, optional
            Title of the scalar bar to remove.  Required if there is
            more than one scalar bar.

        render : bool, default: True
            Render upon scalar bar removal.  Set this to ``False`` to
            stop the render window from rendering when a scalar bar
            is removed.

        Examples
        --------
        Remove a scalar bar from a plotter.

        >>> import pyvista as pv
        >>> mesh = pv.Sphere()
        >>> mesh['data'] = mesh.points[:, 2]
        >>> pl = pv.Plotter()
        >>> _ = pl.add_mesh(mesh, cmap='coolwarm')
        >>> pl.remove_scalar_bar()
        >>> pl.show()

        """
        ...
    
    def __len__(self):
        """Return the number of scalar bar actors."""
        ...
    
    def __getitem__(self, index):
        """Return a scalar bar actor."""
        ...
    
    def keys(self):
        """Scalar bar keys."""
        ...
    
    def values(self):
        """Scalar bar values."""
        ...
    
    def items(self):
        """Scalar bar items."""
        ...
    
    def __contains__(self, key):
        """Check if a title is a valid actors."""
        ...
    
    def add_scalar_bar(self, title=..., mapper=..., n_labels=..., italic=..., bold=..., title_font_size=..., label_font_size=..., color=..., font_family=..., shadow=..., width=..., height=..., position_x=..., position_y=..., vertical=..., interactive=..., fmt=..., use_opacity=..., outline=..., nan_annotation=..., below_label=..., above_label=..., background_color=..., n_colors=..., fill=..., render=..., theme=..., unconstrained_font_size=...):
        """Create scalar bar using the ranges as set by the last input mesh.

        Parameters
        ----------
        title : str, default: ""
            Title of the scalar bar.  Default is rendered as an empty title.

        mapper : vtkMapper, optional
            Mapper used for the scalar bar.  Defaults to the last
            mapper created by the plotter.

        n_labels : int, default: 5
            Number of labels to use for the scalar bar.

        italic : bool, default: False
            Italicises title and bar labels.

        bold : bool, default: False
            Bolds title and bar labels.

        title_font_size : float, optional
            Sets the size of the title font.  Defaults to ``None`` and is sized
            according to :attr:`pyvista.plotting.themes.Theme.font`.

        label_font_size : float, optional
            Sets the size of the title font.  Defaults to ``None`` and is sized
            according to :attr:`pyvista.plotting.themes.Theme.font`.

        color : ColorLike, optional
            Either a string, rgb list, or hex color string.  Default
            set by :attr:`pyvista.plotting.themes.Theme.font`.  Can be
            in one of the following formats:

            * ``color='white'``
            * ``color='w'``
            * ``color=[1.0, 1.0, 1.0]``
            * ``color='#FFFFFF'``

        font_family : {'courier', 'times', 'arial'}
            Font family.  Default is set by
            :attr:`pyvista.plotting.themes.Theme.font`.

        shadow : bool, default: False
            Adds a black shadow to the text.

        width : float, optional
            The percentage (0 to 1) width of the window for the colorbar.
            Default set by
            :attr:`pyvista.plotting.themes.Theme.colorbar_vertical` or
            :attr:`pyvista.plotting.themes.Theme.colorbar_horizontal`
            depending on the value of ``vertical``.

        height : float, optional
            The percentage (0 to 1) height of the window for the
            colorbar.  Default set by
            :attr:`pyvista.plotting.themes.Theme.colorbar_vertical` or
            :attr:`pyvista.plotting.themes.Theme.colorbar_horizontal`
            depending on the value of ``vertical``.

        position_x : float, optional
            The percentage (0 to 1) along the windows's horizontal
            direction to place the bottom left corner of the colorbar.
            Default set by
            :attr:`pyvista.plotting.themes.Theme.colorbar_vertical` or
            :attr:`pyvista.plotting.themes.Theme.colorbar_horizontal`
            depending on the value of ``vertical``.

        position_y : float, optional
            The percentage (0 to 1) along the windows's vertical
            direction to place the bottom left corner of the colorbar.
            Default set by
            :attr:`pyvista.plotting.themes.Theme.colorbar_vertical` or
            :attr:`pyvista.plotting.themes.Theme.colorbar_horizontal`
            depending on the value of ``vertical``.

        vertical : bool, optional
            Use vertical or horizontal scalar bar.  Default set by
            :attr:`pyvista.plotting.themes.Theme.colorbar_orientation`.

        interactive : bool, optional
            Use a widget to control the size and location of the scalar bar.
            Default set by :attr:`pyvista.plotting.themes.Theme.interactive`.

        fmt : str, optional
            ``printf`` format for labels.
            Default set by :attr:`pyvista.plotting.themes.Theme.font`.

        use_opacity : bool, default: True
            Optionally display the opacity mapping on the scalar bar.

        outline : bool, default: False
            Optionally outline the scalar bar to make opacity mappings more
            obvious.

        nan_annotation : bool, default: False
            Annotate the NaN color.

        below_label : str, optional
            String annotation for values below the scalars range.

        above_label : str, optional
            String annotation for values above the scalars range.

        background_color : ColorLike, optional
            The color used for the background in RGB format.

        n_colors : int, optional
            The maximum number of color displayed in the scalar bar.

        fill : bool, default: False
            Draw a filled box behind the scalar bar with the
            ``background_color``.

        render : bool, default: False
            Force a render when True.

        theme : pyvista.plotting.themes.Theme, optional
            Plot-specific theme.  By default, calling from the
            ``Plotter``, will use the plotter theme.  Setting to
            ``None`` will use the global theme.

        unconstrained_font_size : bool, default: False
            Whether the font size of title and labels is unconstrained.
            When it is constrained, the size of the scalar bar will constrain the font size.
            When it is not, the size of the font will always be respected.
            Using custom labels will force this to be ``True``.

            .. versionadded:: 0.44.0

        Returns
        -------
        vtk.vtkScalarBarActor
            Scalar bar actor.

        Notes
        -----
        Setting ``title_font_size``, or ``label_font_size`` disables
        automatic font sizing for both the title and label.

        Examples
        --------
        Add a custom interactive scalar bar that is horizontal, has an
        outline, and has a custom formatting.

        >>> import pyvista as pv
        >>> sphere = pv.Sphere()
        >>> sphere['Data'] = sphere.points[:, 2]
        >>> plotter = pv.Plotter()
        >>> _ = plotter.add_mesh(sphere, show_scalar_bar=False)
        >>> _ = plotter.add_scalar_bar(
        ...     'Data',
        ...     interactive=True,
        ...     vertical=False,
        ...     title_font_size=35,
        ...     label_font_size=30,
        ...     outline=True,
        ...     fmt='%10.5f',
        ... )
        >>> plotter.show()

        """
        ...
    


