"""
This type stub file was generated by pyright.
"""

"""
This type stub file was generated by pyright.
"""
def glyphs(grid_sz=...):
    """Create several parametric supertoroids using VTK's glyph table functionality.

    Parameters
    ----------
    grid_sz : int, default: 3
        Create ``grid_sz x grid_sz`` supertoroids.

    Returns
    -------
    pyvista.PolyData
        Mesh of supertoroids.

    See Also
    --------
    plot_glyphs

    Examples
    --------
    >>> from pyvista import demos
    >>> mesh = demos.glyphs()
    >>> mesh.plot()

    """
    ...

def plot_glyphs(grid_sz=..., **kwargs):
    """Plot several parametric supertoroids using VTK's glyph table functionality.

    Parameters
    ----------
    grid_sz : int, default: 3
        Create ``grid_sz x grid_sz`` supertoroids.

    **kwargs : dict, optional
        All additional keyword arguments will be passed to
        :func:`pyvista.Plotter.add_mesh`.

    Returns
    -------
    various
        See :func:`show <pyvista.Plotter.show>`.

    Examples
    --------
    >>> from pyvista import demos
    >>> demos.plot_glyphs()

    """
    ...

def orientation_cube():
    """Return a dictionary containing the meshes composing an orientation cube.

    Returns
    -------
    dict
        Dictionary containing the meshes composing an orientation cube.

    Examples
    --------
    Load the cube mesh and plot it

    >>> import pyvista as pv
    >>> from pyvista import demos
    >>> ocube = demos.orientation_cube()
    >>> pl = pv.Plotter()
    >>> _ = pl.add_mesh(ocube['cube'], show_edges=True)
    >>> _ = pl.add_mesh(ocube['x_p'], color='blue')
    >>> _ = pl.add_mesh(ocube['x_n'], color='blue')
    >>> _ = pl.add_mesh(ocube['y_p'], color='green')
    >>> _ = pl.add_mesh(ocube['y_n'], color='green')
    >>> _ = pl.add_mesh(ocube['z_p'], color='red')
    >>> _ = pl.add_mesh(ocube['z_n'], color='red')
    >>> pl.show_axes()
    >>> pl.show()

    """
    ...

def orientation_plotter():
    """Return a plotter containing the orientation cube.

    Returns
    -------
    pyvista.Plotter
        Orientation cube plotter.

    Examples
    --------
    >>> from pyvista import demos
    >>> plotter = demos.orientation_plotter()
    >>> plotter.show()

    """
    ...

def plot_wave(fps=..., frequency=..., wavetime=..., notebook=...):
    """Plot a 3D moving wave in a render window.

    Parameters
    ----------
    fps : int, default: 30
        Maximum frames per second to display.

    frequency : float, default: 1.0
        Wave cycles per second (Hz).

    wavetime : float, default: 3.0
        The desired total display time in seconds.

    notebook : bool, optional
        When ``True``, the resulting plot is placed inline a jupyter
        notebook.  Assumes a jupyter console is active.

    Returns
    -------
    numpy.ndarray
        Position of points at last frame.

    Examples
    --------
    >>> from pyvista import demos
    >>> out = demos.plot_wave()

    """
    ...

def plot_ants_plane(notebook=...):
    """Plot two ants and airplane.

    Demonstrate how to create a plot class to plot multiple meshes while
    adding scalars and text.

    This example plots the following:

    .. code:: python

       >>> import pyvista as pv
       >>> from pyvista import examples

       Load and shrink airplane

       >>> airplane = examples.load_airplane()
       >>> airplane.points /= 10

       Rotate and translate ant so it is on the plane.

       >>> ant = examples.load_ant()
       >>> _ = ant.rotate_x(90, inplace=True)
       >>> _ = ant.translate([90, 60, 15], inplace=True)

       Make a copy and add another ant.

       >>> ant_copy = ant.translate([30, 0, -10], inplace=False)

       Create plotting object.

       >>> plotter = pv.Plotter()
       >>> _ = plotter.add_mesh(ant, 'r')
       >>> _ = plotter.add_mesh(ant_copy, 'b')

       Add airplane mesh and make the color equal to the Y position.

       >>> plane_scalars = airplane.points[:, 1]
       >>> _ = plotter.add_mesh(
       ...     airplane,
       ...     scalars=plane_scalars,
       ...     scalar_bar_args={'title': 'Plane Y Location'},
       ... )
       >>> _ = plotter.add_text('Ants and Plane Example')
       >>> plotter.show()

    Parameters
    ----------
    notebook : bool, optional
        When ``True``, the resulting plot is placed inline a jupyter
        notebook.  Assumes a jupyter console is active.

    Examples
    --------
    >>> from pyvista import demos
    >>> demos.plot_ants_plane()

    """
    ...

def plot_beam(notebook=...):
    """Plot a beam with displacement.

    Parameters
    ----------
    notebook : bool, optional
        When ``True``, the resulting plot is placed inline a jupyter
        notebook.  Assumes a jupyter console is active.

    Examples
    --------
    >>> from pyvista import demos
    >>> demos.plot_beam()

    """
    ...

def plot_datasets(dataset_type=...):
    """Plot the pyvista dataset types.

    This demo plots the following PyVista dataset types:

    * :class:`pyvista.PolyData`
    * :class:`pyvista.UnstructuredGrid`
    * :class:`pyvista.ImageData`
    * :class:`pyvista.RectilinearGrid`
    * :class:`pyvista.StructuredGrid`

    Parameters
    ----------
    dataset_type : str, optional
        If set, plot just that dataset.  Must be one of the following:

        * ``'PolyData'``
        * ``'UnstructuredGrid'``
        * ``'ImageData'``
        * ``'RectilinearGrid'``
        * ``'StructuredGrid'``

    Examples
    --------
    >>> from pyvista import demos
    >>> demos.plot_datasets()

    """
    ...

