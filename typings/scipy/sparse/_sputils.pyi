"""
This type stub file was generated by pyright.
"""

import numpy as np
import scipy.sparse as sp
from typing import Any, Literal, Union

""" Utility functions for sparse matrix module
"""
__all__ = ['upcast', 'getdtype', 'getdata', 'isscalarlike', 'isintlike', 'isshape', 'issequence', 'isdense', 'ismatrix', 'get_sum_dtype', 'broadcast_shapes']
supported_dtypes = ...
_upcast_memo = ...
def upcast(*args):
    """Returns the nearest supported sparse dtype for the
    combination of one or more types.

    upcast(t0, t1, ..., tn) -> T  where T is a supported dtype

    Examples
    --------
    >>> from scipy.sparse._sputils import upcast
    >>> upcast('int32')
    <class 'numpy.int32'>
    >>> upcast('bool')
    <class 'numpy.bool'>
    >>> upcast('int32','float32')
    <class 'numpy.float64'>
    >>> upcast('bool',complex,float)
    <class 'numpy.complex128'>

    """
    ...

def upcast_char(*args):
    """Same as `upcast` but taking dtype.char as input (faster)."""
    ...

def upcast_scalar(dtype, scalar):
    """Determine data type for binary operation between an array of
    type `dtype` and a scalar.
    """
    ...

def downcast_intp_index(arr):
    """
    Down-cast index array to np.intp dtype if it is of a larger dtype.

    Raise an error if the array contains a value that is too large for
    intp.
    """
    ...

def to_native(A): # -> NDArray[Any]:
    """
    Ensure that the data type of the NumPy array `A` has native byte order.

    `A` must be a NumPy array.  If the data type of `A` does not have native
    byte order, a copy of `A` with a native byte order is returned. Otherwise
    `A` is returned.
    """
    ...

def getdtype(dtype, a=..., default=...): # -> dtype[Any]:
    """Form a supported numpy dtype based on input arguments.

    Returns a valid ``numpy.dtype`` from `dtype` if not None,
    or else ``a.dtype`` if possible, or else the given `default`
    if not None, or else raise a ``TypeError``.

    The resulting ``dtype`` must be in ``supported_dtypes``:
        bool_, int8, uint8, int16, uint16, int32, uint32,
        int64, uint64, longlong, ulonglong, float32, float64,
        longdouble, complex64, complex128, clongdouble
    """
    ...

def getdata(obj, dtype=..., copy=...) -> np.ndarray:
    """
    This is a wrapper of `np.array(obj, dtype=dtype, copy=copy)`
    that will generate a warning if the result is an object array.
    """
    ...

def safely_cast_index_arrays(A, idx_dtype=..., msg=...): # -> tuple[Any, Any] | tuple[Any, ...]:
    """Safely cast sparse array indices to `idx_dtype`.

    Check the shape of `A` to determine if it is safe to cast its index
    arrays to dtype `idx_dtype`. If any dimension in shape is larger than
    fits in the dtype, casting is unsafe so raise ``ValueError``.
    If safe, cast the index arrays to `idx_dtype` and return the result
    without changing the input `A`. The caller can assign results to `A`
    attributes if desired or use the recast index arrays directly.

    Unless downcasting is needed, the original index arrays are returned.
    You can test e.g. ``A.indptr is new_indptr`` to see if downcasting occurred.

    .. versionadded:: 1.15.0

    Parameters
    ----------
    A : sparse array or matrix
        The array for which index arrays should be downcast.
    idx_dtype : dtype
        Desired dtype. Should be an integer dtype (default: ``np.int32``).
        Most of scipy.sparse uses either int64 or int32.
    msg : string, optional
        A string to be added to the end of the ValueError message
        if the array shape is too big to fit in `idx_dtype`.
        The error message is ``f"<index> values too large for {msg}"``
        It should indicate why the downcasting is needed, e.g. "SuperLU",
        and defaults to f"dtype {idx_dtype}".

    Returns
    -------
    idx_arrays : ndarray or tuple of ndarrays
        Based on ``A.format``, index arrays are returned after casting to `idx_dtype`.
        For CSC/CSR, returns ``(indices, indptr)``.
        For COO, returns ``coords``.
        For DIA, returns ``offsets``.
        For BSR, returns ``(indices, indptr)``.

    Raises
    ------
    ValueError
        If the array has shape that would not fit in the new dtype, or if
        the sparse format does not use index arrays.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import sparse
    >>> data = [3]
    >>> coords = (np.array([3]), np.array([1]))  # Note: int64 arrays
    >>> A = sparse.coo_array((data, coords))
    >>> A.coords[0].dtype
    dtype('int64')

    >>> # rescast after construction, raising exception if shape too big
    >>> coords = sparse.safely_cast_index_arrays(A, np.int32)
    >>> A.coords[0] is coords[0]  # False if casting is needed
    False
    >>> A.coords = coords  # set the index dtype of A
    >>> A.coords[0].dtype
    dtype('int32')
    """
    ...

def get_index_dtype(arrays=..., maxval=..., check_contents=...): # -> int64 | int32:
    """
    Based on input (integer) arrays `a`, determine a suitable index data
    type that can hold the data in the arrays.

    Parameters
    ----------
    arrays : tuple of array_like
        Input arrays whose types/contents to check
    maxval : float, optional
        Maximum value needed
    check_contents : bool, optional
        Whether to check the values in the arrays and not just their types.
        Default: False (check only the types)

    Returns
    -------
    dtype : dtype
        Suitable index data type (int32 or int64)

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import sparse
    >>> # select index dtype based on shape
    >>> shape = (3, 3)
    >>> idx_dtype = sparse.get_index_dtype(maxval=max(shape))
    >>> data = [1.1, 3.0, 1.5]
    >>> indices = np.array([0, 1, 0], dtype=idx_dtype)
    >>> indptr = np.array([0, 2, 3, 3], dtype=idx_dtype)
    >>> A = sparse.csr_array((data, indices, indptr), shape=shape)
    >>> A.indptr.dtype
    dtype('int32')

    >>> # select based on larger of existing arrays and shape
    >>> shape = (3, 3)
    >>> idx_dtype = sparse.get_index_dtype(A.indptr, maxval=max(shape))
    >>> idx_dtype
    <class 'numpy.int32'>
    """
    ...

def get_sum_dtype(dtype: np.dtype) -> np.dtype:
    """Mimic numpy's casting for np.sum"""
    ...

def isscalarlike(x) -> bool:
    """Is x either a scalar, an array scalar, or a 0-dim array?"""
    ...

def isintlike(x) -> bool:
    """Is x appropriate as an index into a sparse matrix? Returns True
    if it can be cast safely to a machine int.
    """
    ...

def isshape(x, nonneg=..., *, allow_nd=...) -> bool:
    """Is x a valid tuple of dimensions?

    If nonneg, also checks that the dimensions are non-negative.
    Shapes of length in the tuple allow_nd are allowed.
    """
    ...

def issequence(t) -> bool:
    ...

def ismatrix(t) -> bool:
    ...

def isdense(x) -> bool:
    ...

def validateaxis(axis) -> None:
    ...

def check_shape(args, current_shape=..., *, allow_nd=...) -> tuple[int, ...]:
    """Imitate numpy.matrix handling of shape arguments

    Parameters
    ----------
    args : array_like
        Data structures providing information about the shape of the sparse array.
    current_shape : tuple, optional
        The current shape of the sparse array or matrix.
        If None (default), the current shape will be inferred from args.
    allow_nd : tuple of ints, optional default: (2,)
        If shape does not have a length in the tuple allow_nd an error is raised.

    Returns
    -------
    new_shape: tuple
        The new shape after validation.
    """
    ...

def broadcast_shapes(*shapes): # -> tuple[()] | tuple[Any, ...]:
    """Check if shapes can be broadcast and return resulting shape

    This is similar to the NumPy ``broadcast_shapes`` function but
    does not check memory consequences of the resulting dense matrix.

    Parameters
    ----------
    *shapes : tuple of shape tuples
        The tuple of shapes to be considered for broadcasting.
        Shapes should be tuples of non-negative integers.

    Returns
    -------
    new_shape : tuple of integers
        The shape that results from broadcasting th input shapes.
    """
    ...

def check_reshape_kwargs(kwargs): # -> tuple[Any, Any]:
    """Unpack keyword arguments for reshape function.

    This is useful because keyword arguments after star arguments are not
    allowed in Python 2, but star keyword arguments are. This function unpacks
    'order' and 'copy' from the star keyword arguments (with defaults) and
    throws an error for any remaining.
    """
    ...

def is_pydata_spmatrix(m) -> bool:
    """
    Check whether object is pydata/sparse matrix, avoiding importing the module.
    """
    ...

def convert_pydata_sparse_to_scipy(arg: Any, target_format: None | Literal["csc", "csr"] = ..., accept_fv: Any = ...) -> Union[Any, sp.spmatrix]:
    """
    Convert a pydata/sparse array to scipy sparse matrix,
    pass through anything else.
    """
    ...

def matrix(*args, **kwargs):
    ...

def asmatrix(data, dtype=...): # -> matrix[Any, Any]:
    ...

