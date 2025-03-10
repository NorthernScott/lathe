"""
This type stub file was generated by pyright.
"""

def milp(c, *, integrality=..., bounds=..., constraints=..., options=...): # -> OptimizeResult:
    r"""
    Mixed-integer linear programming

    Solves problems of the following form:

    .. math::

        \min_x \ & c^T x \\
        \mbox{such that} \ & b_l \leq A x \leq b_u,\\
        & l \leq x \leq u, \\
        & x_i \in \mathbb{Z}, i \in X_i

    where :math:`x` is a vector of decision variables;
    :math:`c`, :math:`b_l`, :math:`b_u`, :math:`l`, and :math:`u` are vectors;
    :math:`A` is a matrix, and :math:`X_i` is the set of indices of
    decision variables that must be integral. (In this context, a
    variable that can assume only integer values is said to be "integral";
    it has an "integrality" constraint.)

    Alternatively, that's:

    minimize::

        c @ x

    such that::

        b_l <= A @ x <= b_u
        l <= x <= u
        Specified elements of x must be integers

    By default, ``l = 0`` and ``u = np.inf`` unless specified with
    ``bounds``.

    Parameters
    ----------
    c : 1D dense array_like
        The coefficients of the linear objective function to be minimized.
        `c` is converted to a double precision array before the problem is
        solved.
    integrality : 1D dense array_like, optional
        Indicates the type of integrality constraint on each decision variable.

        ``0`` : Continuous variable; no integrality constraint.

        ``1`` : Integer variable; decision variable must be an integer
        within `bounds`.

        ``2`` : Semi-continuous variable; decision variable must be within
        `bounds` or take value ``0``.

        ``3`` : Semi-integer variable; decision variable must be an integer
        within `bounds` or take value ``0``.

        By default, all variables are continuous. `integrality` is converted
        to an array of integers before the problem is solved.

    bounds : scipy.optimize.Bounds, optional
        Bounds on the decision variables. Lower and upper bounds are converted
        to double precision arrays before the problem is solved. The
        ``keep_feasible`` parameter of the `Bounds` object is ignored. If
        not specified, all decision variables are constrained to be
        non-negative.
    constraints : sequence of scipy.optimize.LinearConstraint, optional
        Linear constraints of the optimization problem. Arguments may be
        one of the following:

        1. A single `LinearConstraint` object
        2. A single tuple that can be converted to a `LinearConstraint` object
           as ``LinearConstraint(*constraints)``
        3. A sequence composed entirely of objects of type 1. and 2.

        Before the problem is solved, all values are converted to double
        precision, and the matrices of constraint coefficients are converted to
        instances of `scipy.sparse.csc_array`. The ``keep_feasible`` parameter
        of `LinearConstraint` objects is ignored.
    options : dict, optional
        A dictionary of solver options. The following keys are recognized.

        disp : bool (default: ``False``)
            Set to ``True`` if indicators of optimization status are to be
            printed to the console during optimization.
        node_limit : int, optional
            The maximum number of nodes (linear program relaxations) to solve
            before stopping. Default is no maximum number of nodes.
        presolve : bool (default: ``True``)
            Presolve attempts to identify trivial infeasibilities,
            identify trivial unboundedness, and simplify the problem before
            sending it to the main solver.
        time_limit : float, optional
            The maximum number of seconds allotted to solve the problem.
            Default is no time limit.
        mip_rel_gap : float, optional
            Termination criterion for MIP solver: solver will terminate when
            the gap between the primal objective value and the dual objective
            bound, scaled by the primal objective value, is <= mip_rel_gap.

    Returns
    -------
    res : OptimizeResult
        An instance of :class:`scipy.optimize.OptimizeResult`. The object
        is guaranteed to have the following attributes.

        status : int
            An integer representing the exit status of the algorithm.

            ``0`` : Optimal solution found.

            ``1`` : Iteration or time limit reached.

            ``2`` : Problem is infeasible.

            ``3`` : Problem is unbounded.

            ``4`` : Other; see message for details.

        success : bool
            ``True`` when an optimal solution is found and ``False`` otherwise.

        message : str
            A string descriptor of the exit status of the algorithm.

        The following attributes will also be present, but the values may be
        ``None``, depending on the solution status.

        x : ndarray
            The values of the decision variables that minimize the
            objective function while satisfying the constraints.
        fun : float
            The optimal value of the objective function ``c @ x``.
        mip_node_count : int
            The number of subproblems or "nodes" solved by the MILP solver.
        mip_dual_bound : float
            The MILP solver's final estimate of the lower bound on the optimal
            solution.
        mip_gap : float
            The difference between the primal objective value and the dual
            objective bound, scaled by the primal objective value.

    Notes
    -----
    `milp` is a wrapper of the HiGHS linear optimization software [1]_. The
    algorithm is deterministic, and it typically finds the global optimum of
    moderately challenging mixed-integer linear programs (when it exists).

    References
    ----------
    .. [1] Huangfu, Q., Galabova, I., Feldmeier, M., and Hall, J. A. J.
           "HiGHS - high performance software for linear optimization."
           https://highs.dev/
    .. [2] Huangfu, Q. and Hall, J. A. J. "Parallelizing the dual revised
           simplex method." Mathematical Programming Computation, 10 (1),
           119-142, 2018. DOI: 10.1007/s12532-017-0130-5

    Examples
    --------
    Consider the problem at
    https://en.wikipedia.org/wiki/Integer_programming#Example, which is
    expressed as a maximization problem of two variables. Since `milp` requires
    that the problem be expressed as a minimization problem, the objective
    function coefficients on the decision variables are:

    >>> import numpy as np
    >>> c = -np.array([0, 1])

    Note the negative sign: we maximize the original objective function
    by minimizing the negative of the objective function.

    We collect the coefficients of the constraints into arrays like:

    >>> A = np.array([[-1, 1], [3, 2], [2, 3]])
    >>> b_u = np.array([1, 12, 12])
    >>> b_l = np.full_like(b_u, -np.inf, dtype=float)

    Because there is no lower limit on these constraints, we have defined a
    variable ``b_l`` full of values representing negative infinity. This may
    be unfamiliar to users of `scipy.optimize.linprog`, which only accepts
    "less than" (or "upper bound") inequality constraints of the form
    ``A_ub @ x <= b_u``. By accepting both ``b_l`` and ``b_u`` of constraints
    ``b_l <= A_ub @ x <= b_u``, `milp` makes it easy to specify "greater than"
    inequality constraints, "less than" inequality constraints, and equality
    constraints concisely.

    These arrays are collected into a single `LinearConstraint` object like:

    >>> from scipy.optimize import LinearConstraint
    >>> constraints = LinearConstraint(A, b_l, b_u)

    The non-negativity bounds on the decision variables are enforced by
    default, so we do not need to provide an argument for `bounds`.

    Finally, the problem states that both decision variables must be integers:

    >>> integrality = np.ones_like(c)

    We solve the problem like:

    >>> from scipy.optimize import milp
    >>> res = milp(c=c, constraints=constraints, integrality=integrality)
    >>> res.x
    [2.0, 2.0]

    Note that had we solved the relaxed problem (without integrality
    constraints):

    >>> res = milp(c=c, constraints=constraints)  # OR:
    >>> # from scipy.optimize import linprog; res = linprog(c, A, b_u)
    >>> res.x
    [1.8, 2.8]

    we would not have obtained the correct solution by rounding to the nearest
    integers.

    Other examples are given :ref:`in the tutorial <tutorial-optimize_milp>`.

    """
    ...

