"""
This type stub file was generated by pyright.
"""

from typing import TYPE_CHECKING
from pyvista.plotting import _vtk
from pyvista.core._typing_core import NumpyArray

"""Image regression module."""
if TYPE_CHECKING:
    ...
def remove_alpha(img): # -> DataSet | pyvista_ndarray | None:
    """Remove the alpha channel from a ``vtk.vtkImageData``.

    Parameters
    ----------
    img : vtk.vtkImageData
        The input image data with an alpha channel.

    Returns
    -------
    pyvista.ImageData
        The output image data with the alpha channel removed.

    """
    ...

def wrap_image_array(arr): # -> DataSet | pyvista_ndarray | None:
    """Wrap a numpy array as a pyvista.ImageData.

    Parameters
    ----------
    arr : np.ndarray
        A numpy array of shape (X, Y, (3 or 4)) and dtype ``np.uint8``. For
        example, an array of shape ``(768, 1024, 3)``.

    Raises
    ------
    ValueError
        If the input array does not have 3 dimensions, the third dimension of
        the input array is not 3 or 4, or the input array is not of type
        ``np.uint8``.

    Returns
    -------
    pyvista.ImageData
        A PyVista ImageData object with the wrapped array data.

    """
    ...

def run_image_filter(imfilter: _vtk.vtkWindowToImageFilter) -> NumpyArray[float]:
    """Run a ``vtkWindowToImageFilter`` and get output as array.

    Parameters
    ----------
    imfilter : _vtk.vtkWindowToImageFilter
        The ``vtkWindowToImageFilter`` instance to be processed.

    Notes
    -----
    An empty array will be returned if an image cannot be extracted.

    Returns
    -------
    numpy.ndarray
        An array containing the filtered image data. The shape of the array
        is given by (height, width, -1) where height and width are the
        dimensions of the image.

    """
    ...

def image_from_window(render_window, as_vtk=..., ignore_alpha=..., scale=...): # -> DataSet | pyvista_ndarray | NumpyArray | None:
    """Extract the image from the render window as an array.

    Parameters
    ----------
    render_window : vtk.vtkRenderWindow
        The render window to extract the image from.

    as_vtk : bool, default: False
        If set to True, the image will be returned as a VTK object.

    ignore_alpha : bool, default: False
        If set to True, the image will be returned in RGB format,
        otherwise, it will be returned in RGBA format.

    scale : int, default: 1
        The scaling factor of the extracted image. The default value is 1
        which means that no scaling is applied.

    Returns
    -------
    ndarray | vtk.vtkImageData
        The image as an array or as a VTK object depending on the ``as_vtk`` parameter.

    """
    ...

def compare_images(im1, im2, threshold=..., use_vtk=...): # -> float | Any:
    """Compare two different images of the same size.

    Parameters
    ----------
    im1 : str | numpy.ndarray | vtkRenderWindow | vtkImageData
        Render window, numpy array representing the output of a render
        window, or ``vtkImageData``.

    im2 : str | numpy.ndarray | vtkRenderWindow | vtkImageData
        Render window, numpy array representing the output of a render
        window, or ``vtkImageData``.

    threshold : int, default: 1
        Threshold tolerance for pixel differences.  This should be
        greater than 0, otherwise it will always return an error, even
        on identical images.

    use_vtk : bool, default: True
        When disabled, computes the mean pixel error over the entire
        image using numpy.  The difference between pixel is calculated
        for each RGB channel, summed, and then divided by the number
        of pixels.  This is faster than using
        ``vtk.vtkImageDifference`` but potentially less accurate.

    Returns
    -------
    float
        Total error between the images if using ``use_vtk=True``, and
        the mean pixel error when ``use_vtk=False``.

    Examples
    --------
    Compare two active plotters.

    >>> import pyvista as pv
    >>> pl1 = pv.Plotter()
    >>> _ = pl1.add_mesh(pv.Sphere(), smooth_shading=True)
    >>> pl2 = pv.Plotter()
    >>> _ = pl2.add_mesh(pv.Sphere(), smooth_shading=False)
    >>> error = pv.compare_images(pl1, pl2)

    Compare images from file.

    >>> import pyvista as pv
    >>> img1 = pv.read('img1.png')  # doctest:+SKIP
    >>> img2 = pv.read('img2.png')  # doctest:+SKIP
    >>> pv.compare_images(img1, img2)  # doctest:+SKIP

    """
    ...

