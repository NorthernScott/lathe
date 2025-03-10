"""
This type stub file was generated by pyright.
"""

_tukeylambda_var_pc = ...
_tukeylambda_var_qc = ...
_tukeylambda_var_p = ...
_tukeylambda_var_q = ...
def tukeylambda_variance(lam): # -> NDArray[floating[_64Bit]]:
    """Variance of the Tukey Lambda distribution.

    Parameters
    ----------
    lam : array_like
        The lambda values at which to compute the variance.

    Returns
    -------
    v : ndarray
        The variance.  For lam < -0.5, the variance is not defined, so
        np.nan is returned.  For lam = 0.5, np.inf is returned.

    Notes
    -----
    In an interval around lambda=0, this function uses the [4,4] Pade
    approximation to compute the variance.  Otherwise it uses the standard
    formula (https://en.wikipedia.org/wiki/Tukey_lambda_distribution).  The
    Pade approximation is used because the standard formula has a removable
    discontinuity at lambda = 0, and does not produce accurate numerical
    results near lambda = 0.
    """
    ...

_tukeylambda_kurt_pc = ...
_tukeylambda_kurt_qc = ...
_tukeylambda_kurt_p = ...
_tukeylambda_kurt_q = ...
def tukeylambda_kurtosis(lam): # -> NDArray[floating[_64Bit]]:
    """Kurtosis of the Tukey Lambda distribution.

    Parameters
    ----------
    lam : array_like
        The lambda values at which to compute the variance.

    Returns
    -------
    v : ndarray
        The variance.  For lam < -0.25, the variance is not defined, so
        np.nan is returned.  For lam = 0.25, np.inf is returned.

    """
    ...

