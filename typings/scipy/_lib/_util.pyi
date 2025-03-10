"""
This type stub file was generated by pyright.
"""

import numpy as np
from typing import TypeAlias, TypeVar
from numpy.exceptions import AxisError, ComplexWarning, DTypePromotionError, VisibleDeprecationWarning
from numpy import AxisError, ComplexWarning, VisibleDeprecationWarning
from numpy.random import Generator as Generator

AxisError: type[Exception]
ComplexWarning: type[Warning]
VisibleDeprecationWarning: type[Warning]
if np.lib.NumpyVersion(np.__version__) >= '1.25.0':
    ...
else:
    DTypePromotionError = ...
np_long: type
np_ulong: type
if np.lib.NumpyVersion(np.__version__) >= "2.0.0.dev0":
    ...
else:
    np_long = ...
    np_ulong = ...
IntNumber = int | np.integer
DecimalNumber = float | np.floating | np.integer
copy_if_needed: bool | None
if np.lib.NumpyVersion(np.__version__) >= "2.0.0":
    copy_if_needed = ...
else:
    copy_if_needed = ...
    copy_if_needed = ...
_RNG: TypeAlias = np.random.Generator | np.random.RandomState
SeedType: TypeAlias = IntNumber | _RNG | None
GeneratorType = TypeVar("GeneratorType", bound=_RNG)
def float_factorial(n: int) -> float:
    """Compute the factorial and return as a float

    Returns infinity when result is too large for a double
    """
    ...

_rng_desc = ...
def check_random_state(seed): # -> RandomState | Generator:
    """Turn `seed` into a `np.random.RandomState` instance.

    Parameters
    ----------
    seed : {None, int, `numpy.random.Generator`, `numpy.random.RandomState`}, optional
        If `seed` is None (or `np.random`), the `numpy.random.RandomState`
        singleton is used.
        If `seed` is an int, a new ``RandomState`` instance is used,
        seeded with `seed`.
        If `seed` is already a ``Generator`` or ``RandomState`` instance then
        that instance is used.

    Returns
    -------
    seed : {`numpy.random.Generator`, `numpy.random.RandomState`}
        Random number generator.

    """
    ...

FullArgSpec = ...
def getfullargspec_no_self(func): # -> FullArgSpec:
    """inspect.getfullargspec replacement using inspect.signature.

    If func is a bound method, do not list the 'self' parameter.

    Parameters
    ----------
    func : callable
        A callable to inspect

    Returns
    -------
    fullargspec : FullArgSpec(args, varargs, varkw, defaults, kwonlyargs,
                              kwonlydefaults, annotations)

        NOTE: if the first argument of `func` is self, it is *not*, I repeat
        *not*, included in fullargspec.args.
        This is done for consistency between inspect.getargspec() under
        Python 2.x, and inspect.signature() under Python 3.x.

    """
    ...

class _FunctionWrapper:
    """
    Object to wrap user's function, allowing picklability
    """
    def __init__(self, f, args) -> None:
        ...
    
    def __call__(self, x):
        ...
    


class MapWrapper:
    """
    Parallelisation wrapper for working with map-like callables, such as
    `multiprocessing.Pool.map`.

    Parameters
    ----------
    pool : int or map-like callable
        If `pool` is an integer, then it specifies the number of threads to
        use for parallelization. If ``int(pool) == 1``, then no parallel
        processing is used and the map builtin is used.
        If ``pool == -1``, then the pool will utilize all available CPUs.
        If `pool` is a map-like callable that follows the same
        calling sequence as the built-in map function, then this callable is
        used for parallelization.
    """
    def __init__(self, pool=...) -> None:
        ...
    
    def __enter__(self): # -> Self:
        ...
    
    def terminate(self): # -> None:
        ...
    
    def join(self): # -> None:
        ...
    
    def close(self): # -> None:
        ...
    
    def __exit__(self, exc_type, exc_value, traceback): # -> None:
        ...
    
    def __call__(self, func, iterable): # -> map[Any] | list[Any]:
        ...
    


def rng_integers(gen, low, high=..., size=..., dtype=..., endpoint=...):
    """
    Return random integers from low (inclusive) to high (exclusive), or if
    endpoint=True, low (inclusive) to high (inclusive). Replaces
    `RandomState.randint` (with endpoint=False) and
    `RandomState.random_integers` (with endpoint=True).

    Return random integers from the "discrete uniform" distribution of the
    specified dtype. If high is None (the default), then results are from
    0 to low.

    Parameters
    ----------
    gen : {None, np.random.RandomState, np.random.Generator}
        Random number generator. If None, then the np.random.RandomState
        singleton is used.
    low : int or array-like of ints
        Lowest (signed) integers to be drawn from the distribution (unless
        high=None, in which case this parameter is 0 and this value is used
        for high).
    high : int or array-like of ints
        If provided, one above the largest (signed) integer to be drawn from
        the distribution (see above for behavior if high=None). If array-like,
        must contain integer values.
    size : array-like of ints, optional
        Output shape. If the given shape is, e.g., (m, n, k), then m * n * k
        samples are drawn. Default is None, in which case a single value is
        returned.
    dtype : {str, dtype}, optional
        Desired dtype of the result. All dtypes are determined by their name,
        i.e., 'int64', 'int', etc, so byteorder is not available and a specific
        precision may have different C types depending on the platform.
        The default value is 'int64'.
    endpoint : bool, optional
        If True, sample from the interval [low, high] instead of the default
        [low, high) Defaults to False.

    Returns
    -------
    out: int or ndarray of ints
        size-shaped array of random integers from the appropriate distribution,
        or a single such random int if size not provided.
    """
    ...

def normalize_axis_index(axis, ndim):
    ...

class _RichResult(dict):
    """ Container for multiple outputs with pretty-printing """
    def __getattr__(self, name):
        ...
    
    __setattr__ = ...
    __delattr__ = ...
    def __repr__(self): # -> LiteralString | str:
        ...
    
    def __dir__(self): # -> list[Any]:
        ...
    


