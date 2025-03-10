"""
This type stub file was generated by pyright.
"""

import numpy as np

EPS = np.finfo(float).eps
class Interpolation:
    """
    Interpolation set.

    This class stores a base point around which the models are expanded and the
    interpolation points. The coordinates of the interpolation points are
    relative to the base point.
    """
    def __init__(self, pb, options) -> None:
        """
        Initialize the interpolation set.

        Parameters
        ----------
        pb : `cobyqa.problem.Problem`
            Problem to be solved.
        options : dict
            Options of the solver.
        """
        ...
    
    @property
    def n(self): # -> Any:
        """
        Number of variables.

        Returns
        -------
        int
            Number of variables.
        """
        ...
    
    @property
    def npt(self):
        """
        Number of interpolation points.

        Returns
        -------
        int
            Number of interpolation points.
        """
        ...
    
    @property
    def xpt(self): # -> NDArray[float64]:
        """
        Interpolation points.

        Returns
        -------
        `numpy.ndarray`, shape (n, npt)
            Interpolation points.
        """
        ...
    
    @xpt.setter
    def xpt(self, xpt): # -> None:
        """
        Set the interpolation points.

        Parameters
        ----------
        xpt : `numpy.ndarray`, shape (n, npt)
            New interpolation points.
        """
        ...
    
    @property
    def x_base(self): # -> NDArray[Any]:
        """
        Base point around which the models are expanded.

        Returns
        -------
        `numpy.ndarray`, shape (n,)
            Base point around which the models are expanded.
        """
        ...
    
    @x_base.setter
    def x_base(self, x_base): # -> None:
        """
        Set the base point around which the models are expanded.

        Parameters
        ----------
        x_base : `numpy.ndarray`, shape (n,)
            New base point around which the models are expanded.
        """
        ...
    
    def point(self, k): # -> NDArray[floating[Any]]:
        """
        Get the `k`-th interpolation point.

        The return point is relative to the origin.

        Parameters
        ----------
        k : int
            Index of the interpolation point.

        Returns
        -------
        `numpy.ndarray`, shape (n,)
            `k`-th interpolation point.
        """
        ...
    


_cache = ...
def build_system(interpolation): # -> tuple[None, None, None] | tuple[NDArray[float64], NDArray[float64], tuple[Any, Any]]:
    """
    Build the left-hand side matrix of the interpolation system. The
    matrix below stores W * diag(right_scaling),
    where W is the theoretical matrix of the interpolation system. The
    right scaling matrices is chosen to keep the elements in
    the matrix well-balanced.

    Parameters
    ----------
    interpolation : `cobyqa.models.Interpolation`
        Interpolation set.
    """
    ...

class Quadratic:
    """
    Quadratic model.

    This class stores the Hessian matrix of the quadratic model using the
    implicit/explicit representation designed by Powell for NEWUOA [1]_.

    References
    ----------
    .. [1] M. J. D. Powell. The NEWUOA software for unconstrained optimization
       without derivatives. In G. Di Pillo and M. Roma, editors, *Large-Scale
       Nonlinear Optimization*, volume 83 of Nonconvex Optim. Appl., pages
       255--297. Springer, Boston, MA, USA, 2006. `doi:10.1007/0-387-30065-1_16
       <https://doi.org/10.1007/0-387-30065-1_16>`_.
    """
    def __init__(self, interpolation, values, debug) -> None:
        """
        Initialize the quadratic model.

        Parameters
        ----------
        interpolation : `cobyqa.models.Interpolation`
            Interpolation set.
        values : `numpy.ndarray`, shape (npt,)
            Values of the interpolated function at the interpolation points.
        debug : bool
            Whether to make debugging tests during the execution.

        Raises
        ------
        `numpy.linalg.LinAlgError`
            If the interpolation system is ill-defined.
        """
        ...
    
    def __call__(self, x, interpolation):
        """
        Evaluate the quadratic model at a given point.

        Parameters
        ----------
        x : `numpy.ndarray`, shape (n,)
            Point at which the quadratic model is evaluated.
        interpolation : `cobyqa.models.Interpolation`
            Interpolation set.

        Returns
        -------
        float
            Value of the quadratic model at `x`.
        """
        ...
    
    @property
    def n(self):
        """
        Number of variables.

        Returns
        -------
        int
            Number of variables.
        """
        ...
    
    @property
    def npt(self):
        """
        Number of interpolation points used to define the quadratic model.

        Returns
        -------
        int
            Number of interpolation points used to define the quadratic model.
        """
        ...
    
    def grad(self, x, interpolation):
        """
        Evaluate the gradient of the quadratic model at a given point.

        Parameters
        ----------
        x : `numpy.ndarray`, shape (n,)
            Point at which the gradient of the quadratic model is evaluated.
        interpolation : `cobyqa.models.Interpolation`
            Interpolation set.

        Returns
        -------
        `numpy.ndarray`, shape (n,)
            Gradient of the quadratic model at `x`.
        """
        ...
    
    def hess(self, interpolation):
        """
        Evaluate the Hessian matrix of the quadratic model.

        Parameters
        ----------
        interpolation : `cobyqa.models.Interpolation`
            Interpolation set.

        Returns
        -------
        `numpy.ndarray`, shape (n, n)
            Hessian matrix of the quadratic model.
        """
        ...
    
    def hess_prod(self, v, interpolation):
        """
        Evaluate the right product of the Hessian matrix of the quadratic model
        with a given vector.

        Parameters
        ----------
        v : `numpy.ndarray`, shape (n,)
            Vector with which the Hessian matrix of the quadratic model is
            multiplied from the right.
        interpolation : `cobyqa.models.Interpolation`
            Interpolation set.

        Returns
        -------
        `numpy.ndarray`, shape (n,)
            Right product of the Hessian matrix of the quadratic model with
            `v`.
        """
        ...
    
    def curv(self, v, interpolation):
        """
        Evaluate the curvature of the quadratic model along a given direction.

        Parameters
        ----------
        v : `numpy.ndarray`, shape (n,)
            Direction along which the curvature of the quadratic model is
            evaluated.
        interpolation : `cobyqa.models.Interpolation`
            Interpolation set.

        Returns
        -------
        float
            Curvature of the quadratic model along `v`.
        """
        ...
    
    def update(self, interpolation, k_new, dir_old, values_diff): # -> Any:
        """
        Update the quadratic model.

        This method applies the derivative-free symmetric Broyden update to the
        quadratic model. The `knew`-th interpolation point must be updated
        before calling this method.

        Parameters
        ----------
        interpolation : `cobyqa.models.Interpolation`
            Updated interpolation set.
        k_new : int
            Index of the updated interpolation point.
        dir_old : `numpy.ndarray`, shape (n,)
            Value of ``interpolation.xpt[:, k_new]`` before the update.
        values_diff : `numpy.ndarray`, shape (npt,)
            Differences between the values of the interpolated nonlinear
            function and the previous quadratic model at the updated
            interpolation points.

        Raises
        ------
        `numpy.linalg.LinAlgError`
            If the interpolation system is ill-defined.
        """
        ...
    
    def shift_x_base(self, interpolation, new_x_base): # -> None:
        """
        Shift the point around which the quadratic model is defined.

        Parameters
        ----------
        interpolation : `cobyqa.models.Interpolation`
            Previous interpolation set.
        new_x_base : `numpy.ndarray`, shape (n,)
            Point that will replace ``interpolation.x_base``.
        """
        ...
    
    @staticmethod
    def solve_systems(interpolation, rhs): # -> tuple[Any, Any]:
        """
        Solve the interpolation systems.

        Parameters
        ----------
        interpolation : `cobyqa.models.Interpolation`
            Interpolation set.
        rhs : `numpy.ndarray`, shape (npt + n + 1, m)
            Right-hand side vectors of the ``m`` interpolation systems.

        Returns
        -------
        `numpy.ndarray`, shape (npt + n + 1, m)
            Solutions of the interpolation systems.
        `numpy.ndarray`, shape (m, )
            Whether the interpolation systems are ill-conditioned.

        Raises
        ------
        `numpy.linalg.LinAlgError`
            If the interpolation systems are ill-defined.
        """
        ...
    


class Models:
    """
    Models for a nonlinear optimization problem.
    """
    def __init__(self, pb, options, penalty) -> None:
        """
        Initialize the models.

        Parameters
        ----------
        pb : `cobyqa.problem.Problem`
            Problem to be solved.
        options : dict
            Options of the solver.
        penalty : float
            Penalty parameter used to select the point in the filter to forward
            to the callback function.

        Raises
        ------
        `cobyqa.utils.MaxEvalError`
            If the maximum number of evaluations is reached.
        `cobyqa.utils.TargetSuccess`
            If a nearly feasible point has been found with an objective
            function value below the target.
        `cobyqa.utils.FeasibleSuccess`
            If a feasible point has been found for a feasibility problem.
        `numpy.linalg.LinAlgError`
            If the interpolation system is ill-defined.
        """
        ...
    
    @property
    def n(self): # -> Any:
        """
        Dimension of the problem.

        Returns
        -------
        int
            Dimension of the problem.
        """
        ...
    
    @property
    def npt(self):
        """
        Number of interpolation points.

        Returns
        -------
        int
            Number of interpolation points.
        """
        ...
    
    @property
    def m_nonlinear_ub(self): # -> Any:
        """
        Number of nonlinear inequality constraints.

        Returns
        -------
        int
            Number of nonlinear inequality constraints.
        """
        ...
    
    @property
    def m_nonlinear_eq(self): # -> Any:
        """
        Number of nonlinear equality constraints.

        Returns
        -------
        int
            Number of nonlinear equality constraints.
        """
        ...
    
    @property
    def interpolation(self): # -> Interpolation:
        """
        Interpolation set.

        Returns
        -------
        `cobyqa.models.Interpolation`
            Interpolation set.
        """
        ...
    
    @property
    def fun_val(self): # -> NDArray[Any]:
        """
        Values of the objective function at the interpolation points.

        Returns
        -------
        `numpy.ndarray`, shape (npt,)
            Values of the objective function at the interpolation points.
        """
        ...
    
    @property
    def cub_val(self): # -> NDArray[Any]:
        """
        Values of the nonlinear inequality constraint functions at the
        interpolation points.

        Returns
        -------
        `numpy.ndarray`, shape (npt, m_nonlinear_ub)
            Values of the nonlinear inequality constraint functions at the
            interpolation points.
        """
        ...
    
    @property
    def ceq_val(self): # -> NDArray[Any]:
        """
        Values of the nonlinear equality constraint functions at the
        interpolation points.

        Returns
        -------
        `numpy.ndarray`, shape (npt, m_nonlinear_eq)
            Values of the nonlinear equality constraint functions at the
            interpolation points.
        """
        ...
    
    def fun(self, x):
        """
        Evaluate the quadratic model of the objective function at a given
        point.

        Parameters
        ----------
        x : `numpy.ndarray`, shape (n,)
            Point at which to evaluate the quadratic model of the objective
            function.

        Returns
        -------
        float
            Value of the quadratic model of the objective function at `x`.
        """
        ...
    
    def fun_grad(self, x):
        """
        Evaluate the gradient of the quadratic model of the objective function
        at a given point.

        Parameters
        ----------
        x : `numpy.ndarray`, shape (n,)
            Point at which to evaluate the gradient of the quadratic model of
            the objective function.

        Returns
        -------
        `numpy.ndarray`, shape (n,)
            Gradient of the quadratic model of the objective function at `x`.
        """
        ...
    
    def fun_hess(self):
        """
        Evaluate the Hessian matrix of the quadratic model of the objective
        function.

        Returns
        -------
        `numpy.ndarray`, shape (n, n)
            Hessian matrix of the quadratic model of the objective function.
        """
        ...
    
    def fun_hess_prod(self, v):
        """
        Evaluate the right product of the Hessian matrix of the quadratic model
        of the objective function with a given vector.

        Parameters
        ----------
        v : `numpy.ndarray`, shape (n,)
            Vector with which the Hessian matrix of the quadratic model of the
            objective function is multiplied from the right.

        Returns
        -------
        `numpy.ndarray`, shape (n,)
            Right product of the Hessian matrix of the quadratic model of the
            objective function with `v`.
        """
        ...
    
    def fun_curv(self, v):
        """
        Evaluate the curvature of the quadratic model of the objective function
        along a given direction.

        Parameters
        ----------
        v : `numpy.ndarray`, shape (n,)
            Direction along which the curvature of the quadratic model of the
            objective function is evaluated.

        Returns
        -------
        float
            Curvature of the quadratic model of the objective function along
            `v`.
        """
        ...
    
    def fun_alt_grad(self, x):
        """
        Evaluate the gradient of the alternative quadratic model of the
        objective function at a given point.

        Parameters
        ----------
        x : `numpy.ndarray`, shape (n,)
            Point at which to evaluate the gradient of the alternative
            quadratic model of the objective function.

        Returns
        -------
        `numpy.ndarray`, shape (n,)
            Gradient of the alternative quadratic model of the objective
            function at `x`.

        Raises
        ------
        `numpy.linalg.LinAlgError`
            If the interpolation system is ill-defined.
        """
        ...
    
    def cub(self, x, mask=...): # -> NDArray[Any]:
        """
        Evaluate the quadratic models of the nonlinear inequality functions at
        a given point.

        Parameters
        ----------
        x : `numpy.ndarray`, shape (n,)
            Point at which to evaluate the quadratic models of the nonlinear
            inequality functions.
        mask : `numpy.ndarray`, shape (m_nonlinear_ub,), optional
            Mask of the quadratic models to consider.

        Returns
        -------
        `numpy.ndarray`
            Values of the quadratic model of the nonlinear inequality
            functions.
        """
        ...
    
    def cub_grad(self, x, mask=...): # -> NDArray[Any]:
        """
        Evaluate the gradients of the quadratic models of the nonlinear
        inequality functions at a given point.

        Parameters
        ----------
        x : `numpy.ndarray`, shape (n,)
            Point at which to evaluate the gradients of the quadratic models of
            the nonlinear inequality functions.
        mask : `numpy.ndarray`, shape (m_nonlinear_eq,), optional
            Mask of the quadratic models to consider.

        Returns
        -------
        `numpy.ndarray`
            Gradients of the quadratic model of the nonlinear inequality
            functions.
        """
        ...
    
    def cub_hess(self, mask=...): # -> NDArray[Any]:
        """
        Evaluate the Hessian matrices of the quadratic models of the nonlinear
        inequality functions.

        Parameters
        ----------
        mask : `numpy.ndarray`, shape (m_nonlinear_ub,), optional
            Mask of the quadratic models to consider.

        Returns
        -------
        `numpy.ndarray`
            Hessian matrices of the quadratic models of the nonlinear
            inequality functions.
        """
        ...
    
    def cub_hess_prod(self, v, mask=...): # -> NDArray[Any]:
        """
        Evaluate the right product of the Hessian matrices of the quadratic
        models of the nonlinear inequality functions with a given vector.

        Parameters
        ----------
        v : `numpy.ndarray`, shape (n,)
            Vector with which the Hessian matrices of the quadratic models of
            the nonlinear inequality functions are multiplied from the right.
        mask : `numpy.ndarray`, shape (m_nonlinear_ub,), optional
            Mask of the quadratic models to consider.

        Returns
        -------
        `numpy.ndarray`
            Right products of the Hessian matrices of the quadratic models of
            the nonlinear inequality functions with `v`.
        """
        ...
    
    def cub_curv(self, v, mask=...): # -> NDArray[Any]:
        """
        Evaluate the curvature of the quadratic models of the nonlinear
        inequality functions along a given direction.

        Parameters
        ----------
        v : `numpy.ndarray`, shape (n,)
            Direction along which the curvature of the quadratic models of the
            nonlinear inequality functions is evaluated.
        mask : `numpy.ndarray`, shape (m_nonlinear_ub,), optional
            Mask of the quadratic models to consider.

        Returns
        -------
        `numpy.ndarray`
            Curvature of the quadratic models of the nonlinear inequality
            functions along `v`.
        """
        ...
    
    def ceq(self, x, mask=...): # -> NDArray[Any]:
        """
        Evaluate the quadratic models of the nonlinear equality functions at a
        given point.

        Parameters
        ----------
        x : `numpy.ndarray`, shape (n,)
            Point at which to evaluate the quadratic models of the nonlinear
            equality functions.
        mask : `numpy.ndarray`, shape (m_nonlinear_eq,), optional
            Mask of the quadratic models to consider.

        Returns
        -------
        `numpy.ndarray`
            Values of the quadratic model of the nonlinear equality functions.
        """
        ...
    
    def ceq_grad(self, x, mask=...): # -> NDArray[Any]:
        """
        Evaluate the gradients of the quadratic models of the nonlinear
        equality functions at a given point.

        Parameters
        ----------
        x : `numpy.ndarray`, shape (n,)
            Point at which to evaluate the gradients of the quadratic models of
            the nonlinear equality functions.
        mask : `numpy.ndarray`, shape (m_nonlinear_eq,), optional
            Mask of the quadratic models to consider.

        Returns
        -------
        `numpy.ndarray`
            Gradients of the quadratic model of the nonlinear equality
            functions.
        """
        ...
    
    def ceq_hess(self, mask=...): # -> NDArray[Any]:
        """
        Evaluate the Hessian matrices of the quadratic models of the nonlinear
        equality functions.

        Parameters
        ----------
        mask : `numpy.ndarray`, shape (m_nonlinear_eq,), optional
            Mask of the quadratic models to consider.

        Returns
        -------
        `numpy.ndarray`
            Hessian matrices of the quadratic models of the nonlinear equality
            functions.
        """
        ...
    
    def ceq_hess_prod(self, v, mask=...): # -> NDArray[Any]:
        """
        Evaluate the right product of the Hessian matrices of the quadratic
        models of the nonlinear equality functions with a given vector.

        Parameters
        ----------
        v : `numpy.ndarray`, shape (n,)
            Vector with which the Hessian matrices of the quadratic models of
            the nonlinear equality functions are multiplied from the right.
        mask : `numpy.ndarray`, shape (m_nonlinear_eq,), optional
            Mask of the quadratic models to consider.

        Returns
        -------
        `numpy.ndarray`
            Right products of the Hessian matrices of the quadratic models of
            the nonlinear equality functions with `v`.
        """
        ...
    
    def ceq_curv(self, v, mask=...): # -> NDArray[Any]:
        """
        Evaluate the curvature of the quadratic models of the nonlinear
        equality functions along a given direction.

        Parameters
        ----------
        v : `numpy.ndarray`, shape (n,)
            Direction along which the curvature of the quadratic models of the
            nonlinear equality functions is evaluated.
        mask : `numpy.ndarray`, shape (m_nonlinear_eq,), optional
            Mask of the quadratic models to consider.

        Returns
        -------
        `numpy.ndarray`
            Curvature of the quadratic models of the nonlinear equality
            functions along `v`.
        """
        ...
    
    def reset_models(self): # -> None:
        """
        Set the quadratic models of the objective function, nonlinear
        inequality constraints, and nonlinear equality constraints to the
        alternative quadratic models.

        Raises
        ------
        `numpy.linalg.LinAlgError`
            If the interpolation system is ill-defined.
        """
        ...
    
    def update_interpolation(self, k_new, x_new, fun_val, cub_val, ceq_val): # -> Any:
        """
        Update the interpolation set.

        This method updates the interpolation set by replacing the `knew`-th
        interpolation point with `xnew`. It also updates the function values
        and the quadratic models.

        Parameters
        ----------
        k_new : int
            Index of the updated interpolation point.
        x_new : `numpy.ndarray`, shape (n,)
            New interpolation point. Its value is interpreted as relative to
            the origin, not the base point.
        fun_val : float
            Value of the objective function at `x_new`.
            Objective function value at `x_new`.
        cub_val : `numpy.ndarray`, shape (m_nonlinear_ub,)
            Values of the nonlinear inequality constraints at `x_new`.
        ceq_val : `numpy.ndarray`, shape (m_nonlinear_eq,)
            Values of the nonlinear equality constraints at `x_new`.

        Raises
        ------
        `numpy.linalg.LinAlgError`
            If the interpolation system is ill-defined.
        """
        ...
    
    def determinants(self, x_new, k_new=...):
        """
        Compute the normalized determinants of the new interpolation systems.

        Parameters
        ----------
        x_new : `numpy.ndarray`, shape (n,)
            New interpolation point. Its value is interpreted as relative to
            the origin, not the base point.
        k_new : int, optional
            Index of the updated interpolation point. If `k_new` is not
            specified, all the possible determinants are computed.

        Returns
        -------
        {float, `numpy.ndarray`, shape (npt,)}
            Determinant(s) of the new interpolation system.

        Raises
        ------
        `numpy.linalg.LinAlgError`
            If the interpolation system is ill-defined.

        Notes
        -----
        The determinants are normalized by the determinant of the current
        interpolation system. For stability reasons, the calculations are done
        using the formula (2.12) in [1]_.

        References
        ----------
        .. [1] M. J. D. Powell. On updating the inverse of a KKT matrix.
           Technical Report DAMTP 2004/NA01, Department of Applied Mathematics
           and Theoretical Physics, University of Cambridge, Cambridge, UK,
           2004.
        """
        ...
    
    def shift_x_base(self, new_x_base, options): # -> None:
        """
        Shift the base point without changing the interpolation set.

        Parameters
        ----------
        new_x_base : `numpy.ndarray`, shape (n,)
            New base point.
        options : dict
            Options of the solver.
        """
        ...
    


