"""
This type stub file was generated by pyright.
"""

import numpy as np
import dask.array as da
from ..._internal import get_xp
from numpy import bool_ as bool
from typing import Optional, TYPE_CHECKING, Union
from ...common._typing import Array, Device, Dtype, NestedSequence, SupportsBufferProtocol

if TYPE_CHECKING:
    ...
isdtype = ...
unstack = ...
astype = ...
arange = ...
eye = ...
linspace = ...
eye = ...
UniqueAllResult = ...
UniqueCountsResult = ...
UniqueInverseResult = ...
unique_all = ...
unique_counts = ...
unique_inverse = ...
unique_values = ...
permute_dims = ...
std = ...
var = ...
cumulative_sum = ...
empty = ...
empty_like = ...
full = ...
full_like = ...
ones = ...
ones_like = ...
zeros = ...
zeros_like = ...
reshape = ...
matrix_transpose = ...
vecdot = ...
nonzero = ...
ceil = ...
floor = ...
trunc = ...
matmul = ...
tensordot = ...
sign = ...
def asarray(obj: Union[Array, bool, int, float, NestedSequence[bool | int | float], SupportsBufferProtocol,], /, *, dtype: Optional[Dtype] = ..., device: Optional[Device] = ..., copy: Optional[Union[bool, np._CopyMode]] = ..., **kwargs) -> Array:
    """
    Array API compatibility wrapper for asarray().

    See the corresponding documentation in the array library and/or the array API
    specification for more details.
    """
    ...

@get_xp(da)
def clip(x: Array, /, min: Optional[Union[int, float, Array]] = ..., max: Optional[Union[int, float, Array]] = ..., *, xp) -> Array:
    ...

_da_unsupported = ...
_common_aliases = ...
__all__ = _common_aliases + ['__array_namespace_info__', 'asarray', 'acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'bitwise_left_shift', 'bitwise_invert', 'bitwise_right_shift', 'concat', 'pow', 'iinfo', 'finfo', 'can_cast', 'result_type', 'bool', 'float32', 'float64', 'int8', 'int16', 'int32', 'int64', 'uint8', 'uint16', 'uint32', 'uint64', 'complex64', 'complex128', 'iinfo', 'finfo', 'can_cast', 'result_type']
_all_ignore = ...
