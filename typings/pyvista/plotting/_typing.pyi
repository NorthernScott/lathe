"""
This type stub file was generated by pyright.
"""

from typing import Dict, Sequence, TYPE_CHECKING, Tuple, Union
from pyvista.core._typing_core import NumpyArray
from . import _vtk
from .plotting.charts import Chart2D, ChartBox, ChartMPL, ChartPie
from .plotting.colors import Color

"""Type aliases for type hints."""
if TYPE_CHECKING:
    ...
ColorLike = Union[Tuple[int, int, int], Tuple[int, int, int, int], Tuple[float, float, float], Tuple[float, float, float, float], Sequence[int], Sequence[float], NumpyArray[float], Dict[str, Union[int, float, str]], str, "Color", _vtk.vtkColor3ub,]
Chart = Union["Chart2D", "ChartBox", "ChartPie", "ChartMPL"]
