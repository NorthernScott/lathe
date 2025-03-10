"""
This type stub file was generated by pyright.
"""

from typing import TYPE_CHECKING
from . import _vtk
from .prop3d import Prop3D
from ._property import Property
from .mapper import _BaseMapper

"""
This type stub file was generated by pyright.
"""
if TYPE_CHECKING:
    ...
class Volume(Prop3D, _vtk.vtkVolume):
    """Wrapper class for VTK volume.

    This class represents a volume in a rendered scene. It inherits
    functions related to the volume's position, orientation and origin
    from Prop3D.

    """
    def __init__(self) -> None:
        """Initialize volume."""
        ...
    
    @property
    def mapper(self) -> _BaseMapper:
        """Return or set the mapper of the volume.

        Examples
        --------
        Add a volume to a :class:`pyvista.Plotter` and get its mapper.

        >>> import pyvista as pv
        >>> vol = pv.ImageData(dimensions=(10, 10, 10))
        >>> vol['scalars'] = 255 - vol.z * 25
        >>> pl = pv.Plotter()
        >>> actor = pl.add_volume(vol)
        >>> actor.mapper.bounds
        (0.0, 9.0, 0.0, 9.0, 0.0, 9.0)
        """
        ...
    
    @mapper.setter
    def mapper(self, obj):
        ...
    
    @property
    def prop(self):
        """Return or set the property of this actor.

        Examples
        --------
        Create an volume and get its properties.

        >>> import pyvista as pv
        >>> vol = pv.ImageData(dimensions=(10, 10, 10))
        >>> vol['scalars'] = 255 - vol.z * 25
        >>> pl = pv.Plotter()
        >>> actor = pl.add_volume(vol)
        >>> actor.prop.GetShade()
        0

        """
        ...
    
    @prop.setter
    def prop(self, obj: Property):
        ...
    


