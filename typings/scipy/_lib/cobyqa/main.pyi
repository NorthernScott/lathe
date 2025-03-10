"""
This type stub file was generated by pyright.
"""

def minimize(fun, x0, args=..., bounds=..., constraints=..., callback=..., options=..., **kwargs):
    r"""
    Minimize a scalar function using the COBYQA method.

    The Constrained Optimization BY Quadratic Approximations (COBYQA) method is
    a derivative-free optimization method designed to solve general nonlinear
    optimization problems. A complete description of COBYQA is given in [3]_.

    Parameters
    ----------
    fun : {callable, None}
        Objective function to be minimized.

            ``fun(x, *args) -> float``

        where ``x`` is an array with shape (n,) and `args` is a tuple. If `fun`
        is ``None``, the objective function is assumed to be the zero function,
        resulting in a feasibility problem.
    x0 : array_like, shape (n,)
        Initial guess.
    args : tuple, optional
        Extra arguments passed to the objective function.
    bounds : {`scipy.optimize.Bounds`, array_like, shape (n, 2)}, optional
        Bound constraints of the problem. It can be one of the cases below.

        #. An instance of `scipy.optimize.Bounds`. For the time being, the
           argument ``keep_feasible`` is disregarded, and all the constraints
           are considered unrelaxable and will be enforced.
        #. An array with shape (n, 2). The bound constraints for ``x[i]`` are
           ``bounds[i][0] <= x[i] <= bounds[i][1]``. Set ``bounds[i][0]`` to
           :math:`-\infty` if there is no lower bound, and set ``bounds[i][1]``
           to :math:`\infty` if there is no upper bound.

        The COBYQA method always respect the bound constraints.
    constraints : {Constraint, list}, optional
        General constraints of the problem. It can be one of the cases below.

        #. An instance of `scipy.optimize.LinearConstraint`. The argument
           ``keep_feasible`` is disregarded.
        #. An instance of `scipy.optimize.NonlinearConstraint`. The arguments
           ``jac``, ``hess``, ``keep_feasible``, ``finite_diff_rel_step``, and
           ``finite_diff_jac_sparsity`` are disregarded.

        #. A list, each of whose elements are described in the cases above.

    callback : callable, optional
        A callback executed at each objective function evaluation. The method
        terminates if a ``StopIteration`` exception is raised by the callback
        function. Its signature can be one of the following:

            ``callback(intermediate_result)``

        where ``intermediate_result`` is a keyword parameter that contains an
        instance of `scipy.optimize.OptimizeResult`, with attributes ``x``
        and ``fun``, being the point at which the objective function is
        evaluated and the value of the objective function, respectively. The
        name of the parameter must be ``intermediate_result`` for the callback
        to be passed an instance of `scipy.optimize.OptimizeResult`.

        Alternatively, the callback function can have the signature:

            ``callback(xk)``

        where ``xk`` is the point at which the objective function is evaluated.
        Introspection is used to determine which of the signatures to invoke.
    options : dict, optional
        Options passed to the solver. Accepted keys are:

            disp : bool, optional
                Whether to print information about the optimization procedure.
                Default is ``False``.
            maxfev : int, optional
                Maximum number of function evaluations. Default is ``500 * n``.
            maxiter : int, optional
                Maximum number of iterations. Default is ``1000 * n``.
            target : float, optional
                Target on the objective function value. The optimization
                procedure is terminated when the objective function value of a
                feasible point is less than or equal to this target. Default is
                ``-numpy.inf``.
            feasibility_tol : float, optional
                Tolerance on the constraint violation. If the maximum
                constraint violation at a point is less than or equal to this
                tolerance, the point is considered feasible. Default is
                ``numpy.sqrt(numpy.finfo(float).eps)``.
            radius_init : float, optional
                Initial trust-region radius. Typically, this value should be in
                the order of one tenth of the greatest expected change to `x0`.
                Default is ``1.0``.
            radius_final : float, optional
                Final trust-region radius. It should indicate the accuracy
                required in the final values of the variables. Default is
                ``1e-6``.
            nb_points : int, optional
                Number of interpolation points used to build the quadratic
                models of the objective and constraint functions. Default is
                ``2 * n + 1``.
            scale : bool, optional
                Whether to scale the variables according to the bounds. Default
                is ``False``.
            filter_size : int, optional
                Maximum number of points in the filter. The filter is used to
                select the best point returned by the optimization procedure.
                Default is ``sys.maxsize``.
            store_history : bool, optional
                Whether to store the history of the function evaluations.
                Default is ``False``.
            history_size : int, optional
                Maximum number of function evaluations to store in the history.
                Default is ``sys.maxsize``.
            debug : bool, optional
                Whether to perform additional checks during the optimization
                procedure. This option should be used only for debugging
                purposes and is highly discouraged to general users. Default is
                ``False``.

        Other constants (from the keyword arguments) are described below. They
        are not intended to be changed by general users. They should only be
        changed by users with a deep understanding of the algorithm, who want
        to experiment with different settings.

    Returns
    -------
    `scipy.optimize.OptimizeResult`
        Result of the optimization procedure, with the following fields:

            message : str
                Description of the cause of the termination.
            success : bool
                Whether the optimization procedure terminated successfully.
            status : int
                Termination status of the optimization procedure.
            x : `numpy.ndarray`, shape (n,)
                Solution point.
            fun : float
                Objective function value at the solution point.
            maxcv : float
                Maximum constraint violation at the solution point.
            nfev : int
                Number of function evaluations.
            nit : int
                Number of iterations.

        If ``store_history`` is True, the result also has the following fields:

            fun_history : `numpy.ndarray`, shape (nfev,)
                History of the objective function values.
            maxcv_history : `numpy.ndarray`, shape (nfev,)
                History of the maximum constraint violations.

        A description of the termination statuses is given below.

        .. list-table::
            :widths: 25 75
            :header-rows: 1

            * - Exit status
              - Description
            * - 0
              - The lower bound for the trust-region radius has been reached.
            * - 1
              - The target objective function value has been reached.
            * - 2
              - All variables are fixed by the bound constraints.
            * - 3
              - The callback requested to stop the optimization procedure.
            * - 4
              - The feasibility problem received has been solved successfully.
            * - 5
              - The maximum number of function evaluations has been exceeded.
            * - 6
              - The maximum number of iterations has been exceeded.
            * - -1
              - The bound constraints are infeasible.
            * - -2
              - A linear algebra error occurred.

    Other Parameters
    ----------------
    decrease_radius_factor : float, optional
        Factor by which the trust-region radius is reduced when the reduction
        ratio is low or negative. Default is ``0.5``.
    increase_radius_factor : float, optional
        Factor by which the trust-region radius is increased when the reduction
        ratio is large. Default is ``numpy.sqrt(2.0)``.
    increase_radius_threshold : float, optional
        Threshold that controls the increase of the trust-region radius when
        the reduction ratio is large. Default is ``2.0``.
    decrease_radius_threshold : float, optional
        Threshold used to determine whether the trust-region radius should be
        reduced to the resolution. Default is ``1.4``.
    decrease_resolution_factor : float, optional
        Factor by which the resolution is reduced when the current value is far
        from its final value. Default is ``0.1``.
    large_resolution_threshold : float, optional
        Threshold used to determine whether the resolution is far from its
        final value. Default is ``250.0``.
    moderate_resolution_threshold : float, optional
        Threshold used to determine whether the resolution is close to its
        final value. Default is ``16.0``.
    low_ratio : float, optional
        Threshold used to determine whether the reduction ratio is low. Default
        is ``0.1``.
    high_ratio : float, optional
        Threshold used to determine whether the reduction ratio is high.
        Default is ``0.7``.
    very_low_ratio : float, optional
        Threshold used to determine whether the reduction ratio is very low.
        This is used to determine whether the models should be reset. Default
        is ``0.01``.
    penalty_increase_threshold : float, optional
        Threshold used to determine whether the penalty parameter should be
        increased. Default is ``1.5``.
    penalty_increase_factor : float, optional
        Factor by which the penalty parameter is increased. Default is ``2.0``.
    short_step_threshold : float, optional
        Factor used to determine whether the trial step is too short. Default
        is ``0.5``.
    low_radius_factor : float, optional
        Factor used to determine which interpolation point should be removed
        from the interpolation set at each iteration. Default is ``0.1``.
    byrd_omojokun_factor : float, optional
        Factor by which the trust-region radius is reduced for the computations
        of the normal step in the Byrd-Omojokun composite-step approach.
        Default is ``0.8``.
    threshold_ratio_constraints : float, optional
        Threshold used to determine which constraints should be taken into
        account when decreasing the penalty parameter. Default is ``2.0``.
    large_shift_factor : float, optional
        Factor used to determine whether the point around which the quadratic
        models are built should be updated. Default is ``10.0``.
    large_gradient_factor : float, optional
        Factor used to determine whether the models should be reset. Default is
        ``10.0``.
    resolution_factor : float, optional
        Factor by which the resolution is decreased. Default is ``2.0``.
    improve_tcg : bool, optional
        Whether to improve the steps computed by the truncated conjugate
        gradient method when the trust-region boundary is reached. Default is
        ``True``.

    References
    ----------
    .. [1] J. Nocedal and S. J. Wright. *Numerical Optimization*. Springer Ser.
       Oper. Res. Financ. Eng. Springer, New York, NY, USA, second edition,
       2006. `doi:10.1007/978-0-387-40065-5
       <https://doi.org/10.1007/978-0-387-40065-5>`_.
    .. [2] M. J. D. Powell. A direct search optimization method that models the
       objective and constraint functions by linear interpolation. In S. Gomez
       and J.-P. Hennart, editors, *Advances in Optimization and Numerical
       Analysis*, volume 275 of Math. Appl., pages 51--67. Springer, Dordrecht,
       Netherlands, 1994. `doi:10.1007/978-94-015-8330-5_4
       <https://doi.org/10.1007/978-94-015-8330-5_4>`_.
    .. [3] T. M. Ragonneau. *Model-Based Derivative-Free Optimization Methods
       and Software*. PhD thesis, Department of Applied Mathematics, The Hong
       Kong Polytechnic University, Hong Kong, China, 2022. URL:
       https://theses.lib.polyu.edu.hk/handle/200/12294.

    Examples
    --------
    To demonstrate how to use `minimize`, we first minimize the Rosenbrock
    function implemented in `scipy.optimize` in an unconstrained setting.

    .. testsetup::

        import numpy as np
        np.set_printoptions(precision=3, suppress=True)

    >>> from cobyqa import minimize
    >>> from scipy.optimize import rosen

    To solve the problem using COBYQA, run:

    >>> x0 = [1.3, 0.7, 0.8, 1.9, 1.2]
    >>> res = minimize(rosen, x0)
    >>> res.x
    array([1., 1., 1., 1., 1.])

    To see how bound and constraints are handled using `minimize`, we solve
    Example 16.4 of [1]_, defined as

    .. math::

        \begin{aligned}
            \min_{x \in \mathbb{R}^2}   & \quad (x_1 - 1)^2 + (x_2 - 2.5)^2\\
            \text{s.t.}                 & \quad -x_1 + 2x_2 \le 2,\\
                                        & \quad x_1 + 2x_2 \le 6,\\
                                        & \quad x_1 - 2x_2 \le 2,\\
                                        & \quad x_1 \ge 0,\\
                                        & \quad x_2 \ge 0.
        \end{aligned}

    >>> import numpy as np
    >>> from scipy.optimize import Bounds, LinearConstraint

    Its objective function can be implemented as:

    >>> def fun(x):
    ...     return (x[0] - 1.0)**2 + (x[1] - 2.5)**2

    This problem can be solved using `minimize` as:

    >>> x0 = [2.0, 0.0]
    >>> bounds = Bounds([0.0, 0.0], np.inf)
    >>> constraints = LinearConstraint([
    ...     [-1.0, 2.0],
    ...     [1.0, 2.0],
    ...     [1.0, -2.0],
    ... ], -np.inf, [2.0, 6.0, 2.0])
    >>> res = minimize(fun, x0, bounds=bounds, constraints=constraints)
    >>> res.x
    array([1.4, 1.7])

    To see how nonlinear constraints are handled, we solve Problem (F) of [2]_,
    defined as

    .. math::

        \begin{aligned}
            \min_{x \in \mathbb{R}^2}   & \quad -x_1 - x_2\\
            \text{s.t.}                 & \quad x_1^2 - x_2 \le 0,\\
                                        & \quad x_1^2 + x_2^2 \le 1.
        \end{aligned}

    >>> from scipy.optimize import NonlinearConstraint

    Its objective and constraint functions can be implemented as:

    >>> def fun(x):
    ...     return -x[0] - x[1]
    >>>
    >>> def cub(x):
    ...     return [x[0]**2 - x[1], x[0]**2 + x[1]**2]

    This problem can be solved using `minimize` as:

    >>> x0 = [1.0, 1.0]
    >>> constraints = NonlinearConstraint(cub, -np.inf, [0.0, 1.0])
    >>> res = minimize(fun, x0, constraints=constraints)
    >>> res.x
    array([0.707, 0.707])

    Finally, to see how to supply linear and nonlinear constraints
    simultaneously, we solve Problem (G) of [2]_, defined as

    .. math::

        \begin{aligned}
            \min_{x \in \mathbb{R}^3}   & \quad x_3\\
            \text{s.t.}                 & \quad 5x_1 - x_2 + x_3 \ge 0,\\
                                        & \quad -5x_1 - x_2 + x_3 \ge 0,\\
                                        & \quad x_1^2 + x_2^2 + 4x_2 \le x_3.
        \end{aligned}

    Its objective and nonlinear constraint functions can be implemented as:

    >>> def fun(x):
    ...     return x[2]
    >>>
    >>> def cub(x):
    ...     return x[0]**2 + x[1]**2 + 4.0*x[1] - x[2]

    This problem can be solved using `minimize` as:

    >>> x0 = [1.0, 1.0, 1.0]
    >>> constraints = [
    ...     LinearConstraint(
    ...         [[5.0, -1.0, 1.0], [-5.0, -1.0, 1.0]],
    ...         [0.0, 0.0],
    ...         np.inf,
    ...     ),
    ...     NonlinearConstraint(cub, -np.inf, 0.0),
    ... ]
    >>> res = minimize(fun, x0, constraints=constraints)
    >>> res.x
    array([ 0., -3., -3.])
    """
    ...

