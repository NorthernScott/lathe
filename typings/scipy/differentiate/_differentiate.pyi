"""
This type stub file was generated by pyright.
"""

_EERRORINCREASE = ...
def derivative(f, x, *, args=..., tolerances=..., maxiter=..., order=..., initial_step=..., step_factor=..., step_direction=..., preserve_shape=..., callback=...): # -> _RichResult:
    """Evaluate the derivative of a elementwise, real scalar function numerically.

    For each element of the output of `f`, `derivative` approximates the first
    derivative of `f` at the corresponding element of `x` using finite difference
    differentiation.

    This function works elementwise when `x`, `step_direction`, and `args` contain
    (broadcastable) arrays.

    Parameters
    ----------
    f : callable
        The function whose derivative is desired. The signature must be::

            f(xi: ndarray, *argsi) -> ndarray

        where each element of ``xi`` is a finite real number and ``argsi`` is a tuple,
        which may contain an arbitrary number of arrays that are broadcastable with
        ``xi``. `f` must be an elementwise function: each scalar element ``f(xi)[j]``
        must equal ``f(xi[j])`` for valid indices ``j``. It must not mutate the array
        ``xi`` or the arrays in ``argsi``.
    x : float array_like
        Abscissae at which to evaluate the derivative. Must be broadcastable with
        `args` and `step_direction`.
    args : tuple of array_like, optional
        Additional positional array arguments to be passed to `f`. Arrays
        must be broadcastable with one another and the arrays of `init`.
        If the callable for which the root is desired requires arguments that are
        not broadcastable with `x`, wrap that callable with `f` such that `f`
        accepts only `x` and broadcastable ``*args``.
    tolerances : dictionary of floats, optional
        Absolute and relative tolerances. Valid keys of the dictionary are:

        - ``atol`` - absolute tolerance on the derivative
        - ``rtol`` - relative tolerance on the derivative

        Iteration will stop when ``res.error < atol + rtol * abs(res.df)``. The default
        `atol` is the smallest normal number of the appropriate dtype, and
        the default `rtol` is the square root of the precision of the
        appropriate dtype.
    order : int, default: 8
        The (positive integer) order of the finite difference formula to be
        used. Odd integers will be rounded up to the next even integer.
    initial_step : float array_like, default: 0.5
        The (absolute) initial step size for the finite difference derivative
        approximation.
    step_factor : float, default: 2.0
        The factor by which the step size is *reduced* in each iteration; i.e.
        the step size in iteration 1 is ``initial_step/step_factor``. If
        ``step_factor < 1``, subsequent steps will be greater than the initial
        step; this may be useful if steps smaller than some threshold are
        undesirable (e.g. due to subtractive cancellation error).
    maxiter : int, default: 10
        The maximum number of iterations of the algorithm to perform. See
        Notes.
    step_direction : integer array_like
        An array representing the direction of the finite difference steps (for
        use when `x` lies near to the boundary of the domain of the function.)
        Must be broadcastable with `x` and all `args`.
        Where 0 (default), central differences are used; where negative (e.g.
        -1), steps are non-positive; and where positive (e.g. 1), all steps are
        non-negative.
    preserve_shape : bool, default: False
        In the following, "arguments of `f`" refers to the array ``xi`` and
        any arrays within ``argsi``. Let ``shape`` be the broadcasted shape
        of `x` and all elements of `args` (which is conceptually
        distinct from ``xi` and ``argsi`` passed into `f`).

        - When ``preserve_shape=False`` (default), `f` must accept arguments
          of *any* broadcastable shapes.

        - When ``preserve_shape=True``, `f` must accept arguments of shape
          ``shape`` *or* ``shape + (n,)``, where ``(n,)`` is the number of
          abscissae at which the function is being evaluated.

        In either case, for each scalar element ``xi[j]`` within ``xi``, the array
        returned by `f` must include the scalar ``f(xi[j])`` at the same index.
        Consequently, the shape of the output is always the shape of the input
        ``xi``.

        See Examples.
    callback : callable, optional
        An optional user-supplied function to be called before the first
        iteration and after each iteration.
        Called as ``callback(res)``, where ``res`` is a ``_RichResult``
        similar to that returned by `derivative` (but containing the current
        iterate's values of all variables). If `callback` raises a
        ``StopIteration``, the algorithm will terminate immediately and
        `derivative` will return a result. `callback` must not mutate
        `res` or its attributes.

    Returns
    -------
    res : _RichResult
        An object similar to an instance of `scipy.optimize.OptimizeResult` with the
        following attributes. The descriptions are written as though the values will
        be scalars; however, if `f` returns an array, the outputs will be
        arrays of the same shape.

        success : bool array
            ``True`` where the algorithm terminated successfully (status ``0``);
            ``False`` otherwise.
        status : int array
            An integer representing the exit status of the algorithm.

            - ``0`` : The algorithm converged to the specified tolerances.
            - ``-1`` : The error estimate increased, so iteration was terminated.
            - ``-2`` : The maximum number of iterations was reached.
            - ``-3`` : A non-finite value was encountered.
            - ``-4`` : Iteration was terminated by `callback`.
            - ``1`` : The algorithm is proceeding normally (in `callback` only).

        df : float array
            The derivative of `f` at `x`, if the algorithm terminated
            successfully.
        error : float array
            An estimate of the error: the magnitude of the difference between
            the current estimate of the derivative and the estimate in the
            previous iteration.
        nit : int array
            The number of iterations of the algorithm that were performed.
        nfev : int array
            The number of points at which `f` was evaluated.
        x : float array
            The value at which the derivative of `f` was evaluated
            (after broadcasting with `args` and `step_direction`).

    See Also
    --------
    jacobian, hessian

    Notes
    -----
    The implementation was inspired by jacobi [1]_, numdifftools [2]_, and
    DERIVEST [3]_, but the implementation follows the theory of Taylor series
    more straightforwardly (and arguably naively so).
    In the first iteration, the derivative is estimated using a finite
    difference formula of order `order` with maximum step size `initial_step`.
    Each subsequent iteration, the maximum step size is reduced by
    `step_factor`, and the derivative is estimated again until a termination
    condition is reached. The error estimate is the magnitude of the difference
    between the current derivative approximation and that of the previous
    iteration.

    The stencils of the finite difference formulae are designed such that
    abscissae are "nested": after `f` is evaluated at ``order + 1``
    points in the first iteration, `f` is evaluated at only two new points
    in each subsequent iteration; ``order - 1`` previously evaluated function
    values required by the finite difference formula are reused, and two
    function values (evaluations at the points furthest from `x`) are unused.

    Step sizes are absolute. When the step size is small relative to the
    magnitude of `x`, precision is lost; for example, if `x` is ``1e20``, the
    default initial step size of ``0.5`` cannot be resolved. Accordingly,
    consider using larger initial step sizes for large magnitudes of `x`.

    The default tolerances are challenging to satisfy at points where the
    true derivative is exactly zero. If the derivative may be exactly zero,
    consider specifying an absolute tolerance (e.g. ``atol=1e-12``) to
    improve convergence.

    References
    ----------
    .. [1] Hans Dembinski (@HDembinski). jacobi.
           https://github.com/HDembinski/jacobi
    .. [2] Per A. Brodtkorb and John D'Errico. numdifftools.
           https://numdifftools.readthedocs.io/en/latest/
    .. [3] John D'Errico. DERIVEST: Adaptive Robust Numerical Differentiation.
           https://www.mathworks.com/matlabcentral/fileexchange/13490-adaptive-robust-numerical-differentiation
    .. [4] Numerical Differentition. Wikipedia.
           https://en.wikipedia.org/wiki/Numerical_differentiation

    Examples
    --------
    Evaluate the derivative of ``np.exp`` at several points ``x``.

    >>> import numpy as np
    >>> from scipy.differentiate import derivative
    >>> f = np.exp
    >>> df = np.exp  # true derivative
    >>> x = np.linspace(1, 2, 5)
    >>> res = derivative(f, x)
    >>> res.df  # approximation of the derivative
    array([2.71828183, 3.49034296, 4.48168907, 5.75460268, 7.3890561 ])
    >>> res.error  # estimate of the error
    array([7.13740178e-12, 9.16600129e-12, 1.17594823e-11, 1.51061386e-11,
           1.94262384e-11])
    >>> abs(res.df - df(x))  # true error
    array([2.53130850e-14, 3.55271368e-14, 5.77315973e-14, 5.59552404e-14,
           6.92779167e-14])

    Show the convergence of the approximation as the step size is reduced.
    Each iteration, the step size is reduced by `step_factor`, so for
    sufficiently small initial step, each iteration reduces the error by a
    factor of ``1/step_factor**order`` until finite precision arithmetic
    inhibits further improvement.

    >>> import matplotlib.pyplot as plt
    >>> iter = list(range(1, 12))  # maximum iterations
    >>> hfac = 2  # step size reduction per iteration
    >>> hdir = [-1, 0, 1]  # compare left-, central-, and right- steps
    >>> order = 4  # order of differentiation formula
    >>> x = 1
    >>> ref = df(x)
    >>> errors = []  # true error
    >>> for i in iter:
    ...     res = derivative(f, x, maxiter=i, step_factor=hfac,
    ...                      step_direction=hdir, order=order,
    ...                      # prevent early termination
    ...                      tolerances=dict(atol=0, rtol=0))
    ...     errors.append(abs(res.df - ref))
    >>> errors = np.array(errors)
    >>> plt.semilogy(iter, errors[:, 0], label='left differences')
    >>> plt.semilogy(iter, errors[:, 1], label='central differences')
    >>> plt.semilogy(iter, errors[:, 2], label='right differences')
    >>> plt.xlabel('iteration')
    >>> plt.ylabel('error')
    >>> plt.legend()
    >>> plt.show()
    >>> (errors[1, 1] / errors[0, 1], 1 / hfac**order)
    (0.06215223140159822, 0.0625)

    The implementation is vectorized over `x`, `step_direction`, and `args`.
    The function is evaluated once before the first iteration to perform input
    validation and standardization, and once per iteration thereafter.

    >>> def f(x, p):
    ...     f.nit += 1
    ...     return x**p
    >>> f.nit = 0
    >>> def df(x, p):
    ...     return p*x**(p-1)
    >>> x = np.arange(1, 5)
    >>> p = np.arange(1, 6).reshape((-1, 1))
    >>> hdir = np.arange(-1, 2).reshape((-1, 1, 1))
    >>> res = derivative(f, x, args=(p,), step_direction=hdir, maxiter=1)
    >>> np.allclose(res.df, df(x, p))
    True
    >>> res.df.shape
    (3, 5, 4)
    >>> f.nit
    2

    By default, `preserve_shape` is False, and therefore the callable
    `f` may be called with arrays of any broadcastable shapes.
    For example:

    >>> shapes = []
    >>> def f(x, c):
    ...    shape = np.broadcast_shapes(x.shape, c.shape)
    ...    shapes.append(shape)
    ...    return np.sin(c*x)
    >>>
    >>> c = [1, 5, 10, 20]
    >>> res = derivative(f, 0, args=(c,))
    >>> shapes
    [(4,), (4, 8), (4, 2), (3, 2), (2, 2), (1, 2)]

    To understand where these shapes are coming from - and to better
    understand how `derivative` computes accurate results - note that
    higher values of ``c`` correspond with higher frequency sinusoids.
    The higher frequency sinusoids make the function's derivative change
    faster, so more function evaluations are required to achieve the target
    accuracy:

    >>> res.nfev
    array([11, 13, 15, 17], dtype=int32)

    The initial ``shape``, ``(4,)``, corresponds with evaluating the
    function at a single abscissa and all four frequencies; this is used
    for input validation and to determine the size and dtype of the arrays
    that store results. The next shape corresponds with evaluating the
    function at an initial grid of abscissae and all four frequencies.
    Successive calls to the function evaluate the function at two more
    abscissae, increasing the effective order of the approximation by two.
    However, in later function evaluations, the function is evaluated at
    fewer frequencies because the corresponding derivative has already
    converged to the required tolerance. This saves function evaluations to
    improve performance, but it requires the function to accept arguments of
    any shape.

    "Vector-valued" functions are unlikely to satisfy this requirement.
    For example, consider

    >>> def f(x):
    ...    return [x, np.sin(3*x), x+np.sin(10*x), np.sin(20*x)*(x-1)**2]

    This integrand is not compatible with `derivative` as written; for instance,
    the shape of the output will not be the same as the shape of ``x``. Such a
    function *could* be converted to a compatible form with the introduction of
    additional parameters, but this would be inconvenient. In such cases,
    a simpler solution would be to use `preserve_shape`.

    >>> shapes = []
    >>> def f(x):
    ...     shapes.append(x.shape)
    ...     x0, x1, x2, x3 = x
    ...     return [x0, np.sin(3*x1), x2+np.sin(10*x2), np.sin(20*x3)*(x3-1)**2]
    >>>
    >>> x = np.zeros(4)
    >>> res = derivative(f, x, preserve_shape=True)
    >>> shapes
    [(4,), (4, 8), (4, 2), (4, 2), (4, 2), (4, 2)]

    Here, the shape of ``x`` is ``(4,)``. With ``preserve_shape=True``, the
    function may be called with argument ``x`` of shape ``(4,)`` or ``(4, n)``,
    and this is what we observe.

    """
    ...

def jacobian(f, x, *, tolerances=..., maxiter=..., order=..., initial_step=..., step_factor=..., step_direction=...): # -> _RichResult:
    r"""Evaluate the Jacobian of a function numerically.

    Parameters
    ----------
    f : callable
        The function whose Jacobian is desired. The signature must be::

            f(xi: ndarray) -> ndarray

        where each element of ``xi`` is a finite real. If the function to be
        differentiated accepts additional arguments, wrap it (e.g. using
        `functools.partial` or ``lambda``) and pass the wrapped callable
        into `jacobian`. `f` must not mutate the array ``xi``. See Notes
        regarding vectorization and the dimensionality of the input and output.
    x : float array_like
        Points at which to evaluate the Jacobian. Must have at least one dimension.
        See Notes regarding the dimensionality and vectorization.
    tolerances : dictionary of floats, optional
        Absolute and relative tolerances. Valid keys of the dictionary are:

        - ``atol`` - absolute tolerance on the derivative
        - ``rtol`` - relative tolerance on the derivative

        Iteration will stop when ``res.error < atol + rtol * abs(res.df)``. The default
        `atol` is the smallest normal number of the appropriate dtype, and
        the default `rtol` is the square root of the precision of the
        appropriate dtype.
    maxiter : int, default: 10
        The maximum number of iterations of the algorithm to perform. See
        Notes.
    order : int, default: 8
        The (positive integer) order of the finite difference formula to be
        used. Odd integers will be rounded up to the next even integer.
    initial_step : float array_like, default: 0.5
        The (absolute) initial step size for the finite difference derivative
        approximation. Must be broadcastable with `x` and `step_direction`.
    step_factor : float, default: 2.0
        The factor by which the step size is *reduced* in each iteration; i.e.
        the step size in iteration 1 is ``initial_step/step_factor``. If
        ``step_factor < 1``, subsequent steps will be greater than the initial
        step; this may be useful if steps smaller than some threshold are
        undesirable (e.g. due to subtractive cancellation error).
    step_direction : integer array_like
        An array representing the direction of the finite difference steps (e.g.
        for use when `x` lies near to the boundary of the domain of the function.)
        Must be broadcastable with `x` and `initial_step`.
        Where 0 (default), central differences are used; where negative (e.g.
        -1), steps are non-positive; and where positive (e.g. 1), all steps are
        non-negative.

    Returns
    -------
    res : _RichResult
        An object similar to an instance of `scipy.optimize.OptimizeResult` with the
        following attributes. The descriptions are written as though the values will
        be scalars; however, if `f` returns an array, the outputs will be
        arrays of the same shape.

        success : bool array
            ``True`` where the algorithm terminated successfully (status ``0``);
            ``False`` otherwise.
        status : int array
            An integer representing the exit status of the algorithm.

            - ``0`` : The algorithm converged to the specified tolerances.
            - ``-1`` : The error estimate increased, so iteration was terminated.
            - ``-2`` : The maximum number of iterations was reached.
            - ``-3`` : A non-finite value was encountered.

        df : float array
            The Jacobian of `f` at `x`, if the algorithm terminated
            successfully.
        error : float array
            An estimate of the error: the magnitude of the difference between
            the current estimate of the Jacobian and the estimate in the
            previous iteration.
        nit : int array
            The number of iterations of the algorithm that were performed.
        nfev : int array
            The number of points at which `f` was evaluated.

        Each element of an attribute is associated with the corresponding
        element of `df`. For instance, element ``i`` of `nfev` is the
        number of points at which `f` was evaluated for the sake of
        computing element ``i`` of `df`.

    See Also
    --------
    derivative, hessian

    Notes
    -----
    Suppose we wish to evaluate the Jacobian of a function
    :math:`f: \mathbf{R}^m \rightarrow \mathbf{R}^n`. Assign to variables
    ``m`` and ``n`` the positive integer values of :math:`m` and :math:`n`,
    respectively, and let ``...`` represent an arbitrary tuple of integers.
    If we wish to evaluate the Jacobian at a single point, then:

    - argument `x` must be an array of shape ``(m,)``
    - argument `f` must be vectorized to accept an array of shape ``(m, ...)``.
      The first axis represents the :math:`m` inputs of :math:`f`; the remainder
      are for evaluating the function at multiple points in a single call.
    - argument `f` must return an array of shape ``(n, ...)``. The first
      axis represents the :math:`n` outputs of :math:`f`; the remainder
      are for the result of evaluating the function at multiple points.
    - attribute ``df`` of the result object will be an array of shape ``(n, m)``,
      the Jacobian.

    This function is also vectorized in the sense that the Jacobian can be
    evaluated at ``k`` points in a single call. In this case, `x` would be an
    array of shape ``(m, k)``, `f` would accept an array of shape
    ``(m, k, ...)`` and return an array of shape ``(n, k, ...)``, and the ``df``
    attribute of the result would have shape ``(n, m, k)``.

    Suppose the desired callable ``f_not_vectorized`` is not vectorized; it can
    only accept an array of shape ``(m,)``. A simple solution to satisfy the required
    interface is to wrap ``f_not_vectorized`` as follows::

        def f(x):
            return np.apply_along_axis(f_not_vectorized, axis=0, arr=x)

    Alternatively, suppose the desired callable ``f_vec_q`` is vectorized, but
    only for 2-D arrays of shape ``(m, q)``. To satisfy the required interface,
    consider::

        def f(x):
            m, batch = x.shape[0], x.shape[1:]  # x.shape is (m, ...)
            x = np.reshape(x, (m, -1))  # `-1` is short for q = prod(batch)
            res = f_vec_q(x)  # pass shape (m, q) to function
            n = res.shape[0]
            return np.reshape(res, (n,) + batch)  # return shape (n, ...)

    Then pass the wrapped callable ``f`` as the first argument of `jacobian`.

    References
    ----------
    .. [1] Jacobian matrix and determinant, *Wikipedia*,
           https://en.wikipedia.org/wiki/Jacobian_matrix_and_determinant

    Examples
    --------
    The Rosenbrock function maps from :math:`\mathbf{R}^m \rightarrow \mathbf{R}`;
    the SciPy implementation `scipy.optimize.rosen` is vectorized to accept an
    array of shape ``(m, p)`` and return an array of shape ``p``. Suppose we wish
    to evaluate the Jacobian (AKA the gradient because the function returns a scalar)
    at ``[0.5, 0.5, 0.5]``.

    >>> import numpy as np
    >>> from scipy.differentiate import jacobian
    >>> from scipy.optimize import rosen, rosen_der
    >>> m = 3
    >>> x = np.full(m, 0.5)
    >>> res = jacobian(rosen, x)
    >>> ref = rosen_der(x)  # reference value of the gradient
    >>> res.df, ref
    (array([-51.,  -1.,  50.]), array([-51.,  -1.,  50.]))

    As an example of a function with multiple outputs, consider Example 4
    from [1]_.

    >>> def f(x):
    ...     x1, x2, x3 = x
    ...     return [x1, 5*x3, 4*x2**2 - 2*x3, x3*np.sin(x1)]

    The true Jacobian is given by:

    >>> def df(x):
    ...         x1, x2, x3 = x
    ...         one = np.ones_like(x1)
    ...         return [[one, 0*one, 0*one],
    ...                 [0*one, 0*one, 5*one],
    ...                 [0*one, 8*x2, -2*one],
    ...                 [x3*np.cos(x1), 0*one, np.sin(x1)]]

    Evaluate the Jacobian at an arbitrary point.

    >>> rng = np.random.default_rng(389252938452)
    >>> x = rng.random(size=3)
    >>> res = jacobian(f, x)
    >>> ref = df(x)
    >>> res.df.shape == (4, 3)
    True
    >>> np.allclose(res.df, ref)
    True

    Evaluate the Jacobian at 10 arbitrary points in a single call.

    >>> x = rng.random(size=(3, 10))
    >>> res = jacobian(f, x)
    >>> ref = df(x)
    >>> res.df.shape == (4, 3, 10)
    True
    >>> np.allclose(res.df, ref)
    True

    """
    ...

def hessian(f, x, *, tolerances=..., maxiter=..., order=..., initial_step=..., step_factor=...): # -> _RichResult:
    r"""Evaluate the Hessian of a function numerically.

    Parameters
    ----------
    f : callable
        The function whose Hessian is desired. The signature must be::

            f(xi: ndarray) -> ndarray

        where each element of ``xi`` is a finite real. If the function to be
        differentiated accepts additional arguments, wrap it (e.g. using
        `functools.partial` or ``lambda``) and pass the wrapped callable
        into `hessian`. `f` must not mutate the array ``xi``. See Notes
        regarding vectorization and the dimensionality of the input and output.
    x : float array_like
        Points at which to evaluate the Hessian. Must have at least one dimension.
        See Notes regarding the dimensionality and vectorization.
    tolerances : dictionary of floats, optional
        Absolute and relative tolerances. Valid keys of the dictionary are:

        - ``atol`` - absolute tolerance on the derivative
        - ``rtol`` - relative tolerance on the derivative

        Iteration will stop when ``res.error < atol + rtol * abs(res.df)``. The default
        `atol` is the smallest normal number of the appropriate dtype, and
        the default `rtol` is the square root of the precision of the
        appropriate dtype.
    order : int, default: 8
        The (positive integer) order of the finite difference formula to be
        used. Odd integers will be rounded up to the next even integer.
    initial_step : float, default: 0.5
        The (absolute) initial step size for the finite difference derivative
        approximation.
    step_factor : float, default: 2.0
        The factor by which the step size is *reduced* in each iteration; i.e.
        the step size in iteration 1 is ``initial_step/step_factor``. If
        ``step_factor < 1``, subsequent steps will be greater than the initial
        step; this may be useful if steps smaller than some threshold are
        undesirable (e.g. due to subtractive cancellation error).
    maxiter : int, default: 10
        The maximum number of iterations of the algorithm to perform. See
        Notes.

    Returns
    -------
    res : _RichResult
        An object similar to an instance of `scipy.optimize.OptimizeResult` with the
        following attributes. The descriptions are written as though the values will
        be scalars; however, if `f` returns an array, the outputs will be
        arrays of the same shape.

        success : bool array
            ``True`` where the algorithm terminated successfully (status ``0``);
            ``False`` otherwise.
        status : int array
            An integer representing the exit status of the algorithm.

            - ``0`` : The algorithm converged to the specified tolerances.
            - ``-1`` : The error estimate increased, so iteration was terminated.
            - ``-2`` : The maximum number of iterations was reached.
            - ``-3`` : A non-finite value was encountered.

        ddf : float array
            The Hessian of `f` at `x`, if the algorithm terminated
            successfully.
        error : float array
            An estimate of the error: the magnitude of the difference between
            the current estimate of the Hessian and the estimate in the
            previous iteration.
        nfev : int array
            The number of points at which `f` was evaluated.

        Each element of an attribute is associated with the corresponding
        element of `ddf`. For instance, element ``[i, j]`` of `nfev` is the
        number of points at which `f` was evaluated for the sake of
        computing element ``[i, j]`` of `ddf`.

    See Also
    --------
    derivative, jacobian

    Notes
    -----
    Suppose we wish to evaluate the Hessian of a function
    :math:`f: \mathbf{R}^m \rightarrow \mathbf{R}`, and we assign to variable
    ``m`` the positive integer value of :math:`m`. If we wish to evaluate
    the Hessian at a single point, then:

    - argument `x` must be an array of shape ``(m,)``
    - argument `f` must be vectorized to accept an array of shape
      ``(m, ...)``. The first axis represents the :math:`m` inputs of
      :math:`f`; the remaining axes indicated by ellipses are for evaluating
      the function at several abscissae in a single call.
    - argument `f` must return an array of shape ``(...)``.
    - attribute ``dff`` of the result object will be an array of shape ``(m, m)``,
      the Hessian.

    This function is also vectorized in the sense that the Hessian can be
    evaluated at ``k`` points in a single call. In this case, `x` would be an
    array of shape ``(m, k)``, `f` would accept an array of shape
    ``(m, ...)`` and return an array of shape ``(...)``, and the ``ddf``
    attribute of the result would have shape ``(m, m, k)``. Note that the
    axis associated with the ``k`` points is included within the axes
    denoted by ``(...)``.

    Currently, `hessian` is implemented by nesting calls to `jacobian`.
    All options passed to `hessian` are used for both the inner and outer
    calls with one exception: the `rtol` used in the inner `jacobian` call
    is tightened by a factor of 100 with the expectation that the inner
    error can be ignored. A consequence is that `rtol` should not be set
    less than 100 times the precision of the dtype of `x`; a warning is
    emitted otherwise.

    References
    ----------
    .. [1] Hessian matrix, *Wikipedia*,
           https://en.wikipedia.org/wiki/Hessian_matrix

    Examples
    --------
    The Rosenbrock function maps from :math:`\mathbf{R}^m \rightarrow \mathbf{R}`;
    the SciPy implementation `scipy.optimize.rosen` is vectorized to accept an
    array of shape ``(m, ...)`` and return an array of shape ``...``. Suppose we
    wish to evaluate the Hessian at ``[0.5, 0.5, 0.5]``.

    >>> import numpy as np
    >>> from scipy.differentiate import hessian
    >>> from scipy.optimize import rosen, rosen_hess
    >>> m = 3
    >>> x = np.full(m, 0.5)
    >>> res = hessian(rosen, x)
    >>> ref = rosen_hess(x)  # reference value of the Hessian
    >>> np.allclose(res.ddf, ref)
    True

    `hessian` is vectorized to evaluate the Hessian at multiple points
    in a single call.

    >>> rng = np.random.default_rng(4589245925010)
    >>> x = rng.random((m, 10))
    >>> res = hessian(rosen, x)
    >>> ref = [rosen_hess(xi) for xi in x.T]
    >>> ref = np.moveaxis(ref, 0, -1)
    >>> np.allclose(res.ddf, ref)
    True

    """
    ...

