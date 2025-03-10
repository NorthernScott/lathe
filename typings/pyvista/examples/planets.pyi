"""
This type stub file was generated by pyright.
"""

"""
This type stub file was generated by pyright.
"""
def load_sun(radius=..., lat_resolution=..., lon_resolution=...):
    """Load the Sun as a textured sphere.

    Parameters
    ----------
    radius : float, default: 1.0
        Sphere radius.

    lat_resolution : int, default: 50
        Set the number of points in the latitude direction.

    lon_resolution : int, default: 100
        Set the number of points in the longitude direction.

    Returns
    -------
    pyvista.PolyData
        Sun dataset.

    Examples
    --------
    >>> import pyvista as pv
    >>> from pyvista import examples
    >>> mesh = examples.planets.load_sun()
    >>> texture = examples.planets.download_sun_surface(texture=True)
    >>> pl = pv.Plotter()
    >>> image_path = examples.planets.download_stars_sky_background(
    ...     load=False
    ... )
    >>> pl.add_background_image(image_path)
    >>> _ = pl.add_mesh(mesh, texture=texture)
    >>> pl.show()

    """
    ...

def load_moon(radius=..., lat_resolution=..., lon_resolution=...):
    """Load the Moon as a textured sphere.

    Parameters
    ----------
    radius : float, default: 1.0
        Sphere radius.

    lat_resolution : int, default: 50
        Set the number of points in the latitude direction.

    lon_resolution : int, default: 100
        Set the number of points in the longitude direction.

    Returns
    -------
    pyvista.PolyData
        Moon dataset.

    Examples
    --------
    >>> import pyvista as pv
    >>> from pyvista import examples
    >>> mesh = examples.planets.load_moon()
    >>> texture = examples.planets.download_moon_surface(texture=True)
    >>> pl = pv.Plotter()
    >>> image_path = examples.planets.download_stars_sky_background(
    ...     load=False
    ... )
    >>> pl.add_background_image(image_path)
    >>> _ = pl.add_mesh(mesh, texture=texture)
    >>> pl.show()

    """
    ...

def load_mercury(radius=..., lat_resolution=..., lon_resolution=...):
    """Load the planet Mercury as a textured sphere.

    Parameters
    ----------
    radius : float, default: 1.0
        Sphere radius.

    lat_resolution : int, default: 50
        Set the number of points in the latitude direction.

    lon_resolution : int, default: 100
        Set the number of points in the longitude direction.

    Returns
    -------
    pyvista.PolyData
        Mercury dataset.

    Examples
    --------
    >>> import pyvista as pv
    >>> from pyvista import examples
    >>> mesh = examples.planets.load_mercury()
    >>> texture = examples.planets.download_mercury_surface(texture=True)
    >>> pl = pv.Plotter()
    >>> image_path = examples.planets.download_stars_sky_background(
    ...     load=False
    ... )
    >>> pl.add_background_image(image_path)
    >>> _ = pl.add_mesh(mesh, texture=texture)
    >>> pl.show()

    """
    ...

def load_venus(radius=..., lat_resolution=..., lon_resolution=...):
    """Load the planet Venus as a textured sphere.

    Parameters
    ----------
    radius : float, default: 1.0
        Sphere radius.

    lat_resolution : int, default: 50
        Set the number of points in the latitude direction.

    lon_resolution : int, default: 100
        Set the number of points in the longitude direction.

    Returns
    -------
    pyvista.PolyData
        Venus dataset.

    Examples
    --------
    >>> import pyvista as pv
    >>> from pyvista import examples
    >>> mesh = examples.planets.load_venus()
    >>> texture = examples.planets.download_venus_surface(texture=True)
    >>> pl = pv.Plotter()
    >>> image_path = examples.planets.download_stars_sky_background(
    ...     load=False
    ... )
    >>> pl.add_background_image(image_path)
    >>> _ = pl.add_mesh(mesh, texture=texture)
    >>> pl.show()

    """
    ...

def load_earth(radius=..., lat_resolution=..., lon_resolution=...):
    """Load the planet Earth as a textured sphere.

    Parameters
    ----------
    radius : float, default: 1.0
        Sphere radius.

    lat_resolution : int, default: 50
        Set the number of points in the latitude direction.

    lon_resolution : int, default: 100
        Set the number of points in the longitude direction.

    Returns
    -------
    pyvista.PolyData
        Earth dataset.

    Examples
    --------
    >>> import pyvista as pv
    >>> from pyvista import examples
    >>> mesh = examples.planets.load_earth()
    >>> texture = examples.load_globe_texture()
    >>> pl = pv.Plotter()
    >>> image_path = examples.planets.download_stars_sky_background(
    ...     load=False
    ... )
    >>> pl.add_background_image(image_path)
    >>> _ = pl.add_mesh(mesh, texture=texture)
    >>> pl.show()

    """
    ...

def load_mars(radius=..., lat_resolution=..., lon_resolution=...):
    """Load the planet Mars as a textured Sphere.

    Parameters
    ----------
    radius : float, default: 1.0
        Sphere radius.

    lat_resolution : int, default: 50
        Set the number of points in the latitude direction.

    lon_resolution : int, default: 100
        Set the number of points in the longitude direction.

    Returns
    -------
    pyvista.PolyData
        Mars dataset.

    Examples
    --------
    >>> import pyvista as pv
    >>> from pyvista import examples
    >>> mesh = examples.planets.load_mars()
    >>> texture = examples.planets.download_mars_surface(texture=True)
    >>> pl = pv.Plotter()
    >>> image_path = examples.planets.download_stars_sky_background(
    ...     load=False
    ... )
    >>> pl.add_background_image(image_path)
    >>> _ = pl.add_mesh(mesh, texture=texture)
    >>> pl.show()

    """
    ...

def load_jupiter(radius=..., lat_resolution=..., lon_resolution=...):
    """Load the planet Jupiter as a textured sphere.

    Parameters
    ----------
    radius : float, default: 1.0
        Sphere radius.

    lat_resolution : int, default: 50
        Set the number of points in the latitude direction.

    lon_resolution : int, default: 100
        Set the number of points in the longitude direction.

    Returns
    -------
    pyvista.PolyData
        Jupiter dataset.

    Examples
    --------
    >>> import pyvista as pv
    >>> from pyvista import examples
    >>> mesh = examples.planets.load_jupiter()
    >>> texture = examples.planets.download_jupiter_surface(texture=True)
    >>> pl = pv.Plotter()
    >>> image_path = examples.planets.download_stars_sky_background(
    ...     load=False
    ... )
    >>> pl.add_background_image(image_path)
    >>> _ = pl.add_mesh(mesh, texture=texture)
    >>> pl.show()

    """
    ...

def load_saturn(radius=..., lat_resolution=..., lon_resolution=...):
    """Load the planet Saturn as a textured sphere.

    Parameters
    ----------
    radius : float, default: 1.0
        Sphere radius.

    lat_resolution : int, default: 50
        Set the number of points in the latitude direction.

    lon_resolution : int, default: 100
        Set the number of points in the longitude direction.

    Returns
    -------
    pyvista.PolyData
        Saturn dataset.

    Examples
    --------
    >>> import pyvista as pv
    >>> from pyvista import examples
    >>> mesh = examples.planets.load_saturn()
    >>> texture = examples.planets.download_saturn_surface(texture=True)
    >>> pl = pv.Plotter()
    >>> image_path = examples.planets.download_stars_sky_background(
    ...     load=False
    ... )
    >>> pl.add_background_image(image_path)
    >>> _ = pl.add_mesh(mesh, texture=texture)
    >>> pl.show()

    """
    ...

def load_saturn_rings(inner=..., outer=..., c_res=...):
    """Load the planet Saturn's rings.

    Arguments are passed on to :func:`pyvista.Disc`.

    Parameters
    ----------
    inner : float, optional
        The inner radius.

    outer : float, optional
        The outer radius.

    c_res : int, optional
        The number of points in the circumferential direction.

    Returns
    -------
    pyvista.PolyData
        Dataset with texture for Saturn's rings.

    Examples
    --------
    >>> import pyvista as pv
    >>> from pyvista import examples
    >>> mesh = examples.planets.load_saturn_rings()
    >>> texture = examples.planets.download_saturn_rings(texture=True)
    >>> pl = pv.Plotter()
    >>> image_path = examples.planets.download_stars_sky_background(
    ...     load=False
    ... )
    >>> pl.add_background_image(image_path)
    >>> _ = pl.add_mesh(mesh, texture=texture)
    >>> pl.show()

    """
    ...

def load_uranus(radius=..., lat_resolution=..., lon_resolution=...):
    """Load the planet Uranus as a textured sphere.

    Parameters
    ----------
    radius : float, default: 1.0
        Sphere radius.

    lat_resolution : int, default: 50
        Set the number of points in the latitude direction.

    lon_resolution : int, default: 100
        Set the number of points in the longitude direction.

    Returns
    -------
    pyvista.PolyData
        Uranus dataset.

    Examples
    --------
    >>> import pyvista as pv
    >>> from pyvista import examples
    >>> mesh = examples.planets.load_uranus()
    >>> texture = examples.planets.download_uranus_surface(texture=True)
    >>> pl = pv.Plotter()
    >>> image_path = examples.planets.download_stars_sky_background(
    ...     load=False
    ... )
    >>> pl.add_background_image(image_path)
    >>> _ = pl.add_mesh(mesh, texture=texture)
    >>> pl.show()

    """
    ...

def load_neptune(radius=..., lat_resolution=..., lon_resolution=...):
    """Load the planet Neptune as a textured sphere.

    Parameters
    ----------
    radius : float, default: 1.0
        Sphere radius.

    lat_resolution : int, default: 50
        Set the number of points in the latitude direction.

    lon_resolution : int, default: 100
        Set the number of points in the longitude direction.

    Returns
    -------
    pyvista.PolyData
        Neptune dataset.

    Examples
    --------
    >>> import pyvista as pv
    >>> from pyvista import examples
    >>> mesh = examples.planets.load_neptune()
    >>> texture = examples.planets.download_neptune_surface(texture=True)
    >>> pl = pv.Plotter()
    >>> image_path = examples.planets.download_stars_sky_background(
    ...     load=False
    ... )
    >>> pl.add_background_image(image_path)
    >>> _ = pl.add_mesh(mesh, texture=texture)
    >>> pl.show()

    """
    ...

def load_pluto(radius=..., lat_resolution=..., lon_resolution=...):
    """Load the dwarf planet Pluto as a textured sphere.

    Parameters
    ----------
    radius : float, default: 1.0
        Sphere radius.

    lat_resolution : int, default: 50
        Set the number of points in the latitude direction.

    lon_resolution : int, default: 100
        Set the number of points in the longitude direction.

    Returns
    -------
    pyvista.PolyData
        Pluto dataset.

    Examples
    --------
    >>> import pyvista as pv
    >>> from pyvista import examples
    >>> mesh = examples.planets.load_pluto()
    >>> texture = examples.planets.download_pluto_surface(texture=True)
    >>> pl = pv.Plotter()
    >>> image_path = examples.planets.download_stars_sky_background(
    ...     load=False
    ... )
    >>> pl.add_background_image(image_path)
    >>> _ = pl.add_mesh(mesh, texture=texture)
    >>> pl.show()

    """
    ...

def download_sun_surface(texture=..., load=...):
    """Download the surface of the Sun.

    Textures obtained from `Solar Textures
    <https://www.solarsystemscope.com/textures/>`_.

    Parameters
    ----------
    texture : bool, default: False
        Set to ``True`` when loading the surface as a texture.

    load : bool, default: True
        Load the dataset. When ``False``, return the path to the file.

    Returns
    -------
    pyvista.DataSet, pyvista.Texture, or str
        Texture, Dataset, or path to the file depending on the ``load`` and
        ``texture`` parameters.

    Examples
    --------
    >>> from pyvista import examples
    >>> texture = examples.planets.download_sun_surface(texture=True)
    >>> texture.plot(zoom='tight', show_axes=False)

    """
    ...

def download_moon_surface(texture=..., load=...):
    """Download the surface of the Earth's Moon.

    Textures obtained from `Solar Textures
    <https://www.solarsystemscope.com/textures/>`_.

    Parameters
    ----------
    texture : bool, default: False
        Set to ``True`` when loading the surface as a texture.

    load : bool, default: True
        Load the dataset. When ``False``, return the path to the file.

    Returns
    -------
    pyvista.DataSet, pyvista.Texture, or str
        Texture, Dataset, or path to the file depending on the ``load`` and
        ``texture`` parameters.

    Examples
    --------
    >>> from pyvista import examples
    >>> texture = examples.planets.download_moon_surface(texture=True)
    >>> texture.plot(zoom='tight', show_axes=False)

    """
    ...

def download_mercury_surface(texture=..., load=...):
    """Download the surface of planet Mercury.

    Textures obtained from `Solar Textures
    <https://www.solarsystemscope.com/textures/>`_.

    Parameters
    ----------
    texture : bool, default: False
        Set to ``True`` when loading the surface as a texture.

    load : bool, default: True
        Load the dataset. When ``False``, return the path to the file.

    Returns
    -------
    pyvista.DataSet, pyvista.Texture, or str
        Texture, Dataset, or path to the file depending on the ``load`` and
        ``texture`` parameters.

    Examples
    --------
    >>> from pyvista import examples
    >>> texture = examples.planets.download_mercury_surface(texture=True)
    >>> texture.plot(zoom='tight', show_axes=False)

    """
    ...

def download_venus_surface(atmosphere=..., texture=..., load=...):
    """Download the surface or atmosphere of Planet Venus.

    Textures obtained from `Solar Textures
    <https://www.solarsystemscope.com/textures/>`_.

    Parameters
    ----------
    atmosphere : bool, optional
        Load the atmosphere texture when ``True``.

    texture : bool, default: False
        Set to ``True`` when loading the surface as a texture.

    load : bool, default: True
        Load the dataset. When ``False``, return the path to the file.

    Returns
    -------
    pyvista.DataSet, pyvista.Texture, or str
        Texture, Dataset, or path to the file depending on the ``load`` and
        ``texture`` parameters.

    Examples
    --------
    >>> from pyvista import examples
    >>> texture = examples.planets.download_venus_surface(texture=True)
    >>> texture.plot(zoom='tight', show_axes=False)

    """
    ...

def download_mars_surface(texture=..., load=...):
    """Download the surface of the planet Mars.

    Textures obtained from `Solar Textures
    <https://www.solarsystemscope.com/textures/>`_.

    Parameters
    ----------
    texture : bool, default: False
        Set to ``True`` when loading the surface as a texture.

    load : bool, default: True
        Load the dataset. When ``False``, return the path to the file.

    Returns
    -------
    pyvista.DataSet, pyvista.Texture, or str
        Texture, Dataset, or path to the file depending on the ``load`` and
        ``texture`` parameters.

    Examples
    --------
    >>> from pyvista import examples
    >>> texture = examples.planets.download_mars_surface(texture=True)
    >>> texture.plot(zoom='tight', show_axes=False)

    """
    ...

def download_jupiter_surface(texture=..., load=...):
    """Download the surface of the planet Jupiter.

    Textures obtained from `Solar Textures
    <https://www.solarsystemscope.com/textures/>`_.

    Parameters
    ----------
    texture : bool, default: False
        Set to ``True`` when loading the surface as a texture.

    load : bool, default: True
        Load the dataset. When ``False``, return the path to the file.

    Returns
    -------
    pyvista.DataSet, pyvista.Texture, or str
        Texture, Dataset, or path to the file depending on the ``load`` and
        ``texture`` parameters.

    Examples
    --------
    >>> from pyvista import examples
    >>> texture = examples.planets.download_jupiter_surface(texture=True)
    >>> texture.plot(zoom='tight', show_axes=False)

    """
    ...

def download_saturn_surface(texture=..., load=...):
    """Download the surface of the planet Saturn.

    Textures obtained from `Solar Textures
    <https://www.solarsystemscope.com/textures/>`_.

    Parameters
    ----------
    texture : bool, default: False
        Set to ``True`` when loading the surface as a texture.

    load : bool, default: True
        Load the dataset. When ``False``, return the path to the file.

    Returns
    -------
    pyvista.DataSet, pyvista.Texture, or str
        Texture, Dataset, or path to the file depending on the ``load`` and
        ``texture`` parameters.

    Examples
    --------
    >>> from pyvista import examples
    >>> texture = examples.planets.download_saturn_surface(texture=True)
    >>> texture.plot(zoom='tight', show_axes=False)

    """
    ...

def download_saturn_rings(texture=..., load=...):
    """Download the texture of Saturn's rings.

    Textures obtained from `Solar Textures
    <https://www.solarsystemscope.com/textures/>`_.

    Parameters
    ----------
    texture : bool, default: False
        Set to ``True`` when loading the surface as a texture.

    load : bool, default: True
        Load the dataset. When ``False``, return the path to the file.

    Returns
    -------
    pyvista.ImageData, pyvista.Texture, or str
        Dataset, texture, or filename of the Saturn's rings.

    Examples
    --------
    >>> from pyvista import examples
    >>> texture = examples.planets.download_saturn_rings(texture=True)
    >>> texture.plot(cpos='xy')

    """
    ...

def download_uranus_surface(texture=..., load=...):
    """Download and the texture of the surface of planet Uranus.

    Textures obtained from `Solar Textures
    <https://www.solarsystemscope.com/textures/>`_.

    Parameters
    ----------
    texture : bool, default: False
        Set to ``True`` when loading the surface as a texture.

    load : bool, default: True
        Load the dataset. When ``False``, return the path to the file.

    Returns
    -------
    pyvista.DataSet, pyvista.Texture, or str
        Texture, Dataset, or path to the file depending on the ``load`` and
        ``texture`` parameters.

    Examples
    --------
    >>> from pyvista import examples
    >>> texture = examples.planets.download_uranus_surface(texture=True)
    >>> texture.plot(zoom='tight', show_axes=False)

    """
    ...

def download_neptune_surface(texture=..., load=...):
    """Download the texture of the surface of planet Neptune.

    Textures obtained from `Solar Textures
    <https://www.solarsystemscope.com/textures/>`_.

    Parameters
    ----------
    texture : bool, default: False
        Set to ``True`` when loading the surface as a texture.

    load : bool, default: True
        Load the dataset. When ``False``, return the path to the file.

    Returns
    -------
    pyvista.DataSet, pyvista.Texture, or str
        Texture, Dataset, or path to the file depending on the ``load`` and
        ``texture`` parameters.

    Examples
    --------
    >>> from pyvista import examples
    >>> texture = examples.planets.download_neptune_surface(texture=True)
    >>> texture.plot(zoom='tight', show_axes=False)

    """
    ...

def download_pluto_surface(texture=..., load=...):
    """Download the texture of the surface of the dwarf planet Pluto.

    Textures obtained from `Solar Textures
    <https://www.solarsystemscope.com/textures/>`_.

    Parameters
    ----------
    texture : bool, default: False
        Set to ``True`` when loading the surface as a texture.

    load : bool, default: True
        Load the dataset. When ``False``, return the path to the file.

    Returns
    -------
    pyvista.DataSet, pyvista.Texture, or str
        Texture, Dataset, or path to the file depending on the ``load`` and
        ``texture`` parameters.

    Examples
    --------
    >>> from pyvista import examples
    >>> texture = examples.planets.download_pluto_surface(texture=True)
    >>> texture.plot(zoom='tight', show_axes=False)

    """
    ...

def download_stars_sky_background(texture=..., load=...):
    """Download the night sky stars texture.

    Textures obtained from `tamaskis/planet3D-MATLAB
    <https://github.com/tamaskis/planet3D-MATLAB>`_.

    Parameters
    ----------
    texture : bool, default: False
        Set to ``True`` when loading the surface as a texture.

    load : bool, default: True
        Load the dataset. When ``False``, return the path to the file.

    Returns
    -------
    pyvista.DataSet, pyvista.Texture, or str
        Texture, Dataset, or path to the file depending on the ``load`` and
        ``texture`` parameters.

    Examples
    --------
    Load the night sky image as a background image.

    >>> from pyvista import examples
    >>> import pyvista as pv
    >>> pl = pv.Plotter()
    >>> image_path = examples.planets.download_stars_sky_background(
    ...     load=False
    ... )
    >>> pl.add_background_image(image_path)
    >>> pl.show()

    See :func:`load_mars` for another example using this dataset.

    """
    ...

def download_milkyway_sky_background(texture=..., load=...):
    """Download the sky texture of the Milky Way galaxy.

    Textures obtained from `tamaskis/planet3D-MATLAB
    <https://github.com/tamaskis/planet3D-MATLAB>`_.

    Parameters
    ----------
    texture : bool, default: False
        Set to ``True`` when loading the surface as a texture.

    load : bool, default: True
        Load the dataset. When ``False``, return the path to the file.

    Returns
    -------
    pyvista.DataSet, pyvista.Texture, or str
        Texture, Dataset, or path to the file depending on the ``load`` and
        ``texture`` parameters.

    Examples
    --------
    Load the Milky Way sky image as a background image.

    >>> from pyvista import examples
    >>> import pyvista as pv
    >>> pl = pv.Plotter()
    >>> image_path = examples.planets.download_milkyway_sky_background(
    ...     load=False
    ... )
    >>> pl.add_background_image(image_path)
    >>> pl.show()

    """
    ...

