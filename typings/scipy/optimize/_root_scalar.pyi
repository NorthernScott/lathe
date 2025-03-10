"""
This type stub file was generated by pyright.
"""

"""
Unified interfaces to root finding algorithms for real or complex
scalar functions.

Functions
---------
- root : find a root of a scalar function.
"""
__all__ = ['root_scalar']
ROOT_SCALAR_METHODS = ...
class MemoizeDer:
    """Decorator that caches the value and derivative(s) of function each
    time it is called.

    This is a simplistic memoizer that calls and caches a single value
    of ``f(x, *args)``.
    It assumes that `args` does not change between invocations.
    It supports the use case of a root-finder where `args` is fixed,
    `x` changes, and only rarely, if at all, does x assume the same value
    more than once."""
    def __init__(self, fun) -> None:
        ...
    
    def __call__(self, x, *args):
        r"""Calculate f or use cached value if available"""
        ...
    
    def fprime(self, x, *args):
        r"""Calculate f' or use a cached value if available"""
        ...
    
    def fprime2(self, x, *args):
        r"""Calculate f'' or use a cached value if available"""
        ...
    
    def ncalls(self): # -> int:
        ...
    


def root_scalar(f, args=..., method=..., bracket=..., fprime=..., fprime2=..., x0=..., x1=..., xtol=..., rtol=..., maxiter=..., options=...):
    """
    Find a root of a scalar function.

    Parameters
    ----------
    f : callable
        A function to find a root of.

        Suppose the callable has signature ``f0(x, *my_args, **my_kwargs)``, where
        ``my_args`` and ``my_kwargs`` are required positional and keyword arguments.
        Rather than passing ``f0`` as the callable, wrap it to accept
        only ``x``; e.g., pass ``fun=lambda x: f0(x, *my_args, **my_kwargs)`` as the
        callable, where ``my_args`` (tuple) and ``my_kwargs`` (dict) have been
        gathered before invoking this function.
    args : tuple, optional
        Extra arguments passed to the objective function and its derivative(s).
    method : str, optional
        Type of solver.  Should be one of

        - 'bisect'    :ref:`(see here) <optimize.root_scalar-bisect>`
        - 'brentq'    :ref:`(see here) <optimize.root_scalar-brentq>`
        - 'brenth'    :ref:`(see here) <optimize.root_scalar-brenth>`
        - 'ridder'    :ref:`(see here) <optimize.root_scalar-ridder>`
        - 'toms748'    :ref:`(see here) <optimize.root_scalar-toms748>`
        - 'newton'    :ref:`(see here) <optimize.root_scalar-newton>`
        - 'secant'    :ref:`(see here) <optimize.root_scalar-secant>`
        - 'halley'    :ref:`(see here) <optimize.root_scalar-halley>`

    bracket: A sequence of 2 floats, optional
        An interval bracketing a root.  ``f(x, *args)`` must have different
        signs at the two endpoints.
    x0 : float, optional
        Initial guess.
    x1 : float, optional
        A second guess.
    fprime : bool or callable, optional
        If `fprime` is a boolean and is True, `f` is assumed to return the
        value of the objective function and of the derivative.
        `fprime` can also be a callable returning the derivative of `f`. In
        this case, it must accept the same arguments as `f`.
    fprime2 : bool or callable, optional
        If `fprime2` is a boolean and is True, `f` is assumed to return the
        value of the objective function and of the
        first and second derivatives.
        `fprime2` can also be a callable returning the second derivative of `f`.
        In this case, it must accept the same arguments as `f`.
    xtol : float, optional
        Tolerance (absolute) for termination.
    rtol : float, optional
        Tolerance (relative) for termination.
    maxiter : int, optional
        Maximum number of iterations.
    options : dict, optional
        A dictionary of solver options. E.g., ``k``, see
        :obj:`show_options()` for details.

    Returns
    -------
    sol : RootResults
        The solution represented as a ``RootResults`` object.
        Important attributes are: ``root`` the solution , ``converged`` a
        boolean flag indicating if the algorithm exited successfully and
        ``flag`` which describes the cause of the termination. See
        `RootResults` for a description of other attributes.

    See also
    --------
    show_options : Additional options accepted by the solvers
    root : Find a root of a vector function.

    Notes
    -----
    This section describes the available solvers that can be selected by the
    'method' parameter.

    The default is to use the best method available for the situation
    presented.
    If a bracket is provided, it may use one of the bracketing methods.
    If a derivative and an initial value are specified, it may
    select one of the derivative-based methods.
    If no method is judged applicable, it will raise an Exception.

    Arguments for each method are as follows (x=required, o=optional).

    +-----------------------------------------------+---+------+---------+----+----+--------+---------+------+------+---------+---------+
    |                    method                     | f | args | bracket | x0 | x1 | fprime | fprime2 | xtol | rtol | maxiter | options |
    +===============================================+===+======+=========+====+====+========+=========+======+======+=========+=========+
    | :ref:`bisect <optimize.root_scalar-bisect>`   | x |  o   |    x    |    |    |        |         |  o   |  o   |    o    |   o     |
    +-----------------------------------------------+---+------+---------+----+----+--------+---------+------+------+---------+---------+
    | :ref:`brentq <optimize.root_scalar-brentq>`   | x |  o   |    x    |    |    |        |         |  o   |  o   |    o    |   o     |
    +-----------------------------------------------+---+------+---------+----+----+--------+---------+------+------+---------+---------+
    | :ref:`brenth <optimize.root_scalar-brenth>`   | x |  o   |    x    |    |    |        |         |  o   |  o   |    o    |   o     |
    +-----------------------------------------------+---+------+---------+----+----+--------+---------+------+------+---------+---------+
    | :ref:`ridder <optimize.root_scalar-ridder>`   | x |  o   |    x    |    |    |        |         |  o   |  o   |    o    |   o     |
    +-----------------------------------------------+---+------+---------+----+----+--------+---------+------+------+---------+---------+
    | :ref:`toms748 <optimize.root_scalar-toms748>` | x |  o   |    x    |    |    |        |         |  o   |  o   |    o    |   o     |
    +-----------------------------------------------+---+------+---------+----+----+--------+---------+------+------+---------+---------+
    | :ref:`secant <optimize.root_scalar-secant>`   | x |  o   |         | x  | o  |        |         |  o   |  o   |    o    |   o     |
    +-----------------------------------------------+---+------+---------+----+----+--------+---------+------+------+---------+---------+
    | :ref:`newton <optimize.root_scalar-newton>`   | x |  o   |         | x  |    |   o    |         |  o   |  o   |    o    |   o     |
    +-----------------------------------------------+---+------+---------+----+----+--------+---------+------+------+---------+---------+
    | :ref:`halley <optimize.root_scalar-halley>`   | x |  o   |         | x  |    |   x    |    x    |  o   |  o   |    o    |   o     |
    +-----------------------------------------------+---+------+---------+----+----+--------+---------+------+------+---------+---------+

    Examples
    --------

    Find the root of a simple cubic

    >>> from scipy import optimize
    >>> def f(x):
    ...     return (x**3 - 1)  # only one real root at x = 1

    >>> def fprime(x):
    ...     return 3*x**2

    The `brentq` method takes as input a bracket

    >>> sol = optimize.root_scalar(f, bracket=[0, 3], method='brentq')
    >>> sol.root, sol.iterations, sol.function_calls
    (1.0, 10, 11)

    The `newton` method takes as input a single point and uses the
    derivative(s).

    >>> sol = optimize.root_scalar(f, x0=0.2, fprime=fprime, method='newton')
    >>> sol.root, sol.iterations, sol.function_calls
    (1.0, 11, 22)

    The function can provide the value and derivative(s) in a single call.

    >>> def f_p_pp(x):
    ...     return (x**3 - 1), 3*x**2, 6*x

    >>> sol = optimize.root_scalar(
    ...     f_p_pp, x0=0.2, fprime=True, method='newton'
    ... )
    >>> sol.root, sol.iterations, sol.function_calls
    (1.0, 11, 11)

    >>> sol = optimize.root_scalar(
    ...     f_p_pp, x0=0.2, fprime=True, fprime2=True, method='halley'
    ... )
    >>> sol.root, sol.iterations, sol.function_calls
    (1.0, 7, 8)


    """
    ...

