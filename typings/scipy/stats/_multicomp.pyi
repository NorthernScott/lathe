"""
This type stub file was generated by pyright.
"""

import numpy as np
import numpy.typing as npt
from dataclasses import dataclass
from typing import Literal, TYPE_CHECKING
from scipy.stats._common import ConfidenceInterval
from scipy._lib._util import DecimalNumber, SeedType, _transition_to_rng

if TYPE_CHECKING:
    ...
__all__ = ['dunnett']
@dataclass
class DunnettResult:
    """Result object returned by `scipy.stats.dunnett`.

    Attributes
    ----------
    statistic : float ndarray
        The computed statistic of the test for each comparison. The element
        at index ``i`` is the statistic for the comparison between
        groups ``i`` and the control.
    pvalue : float ndarray
        The computed p-value of the test for each comparison. The element
        at index ``i`` is the p-value for the comparison between
        group ``i`` and the control.
    """
    statistic: np.ndarray
    pvalue: np.ndarray
    _alternative: Literal['two-sided', 'less', 'greater'] = ...
    _rho: np.ndarray = ...
    _df: int = ...
    _std: float = ...
    _mean_samples: np.ndarray = ...
    _mean_control: np.ndarray = ...
    _n_samples: np.ndarray = ...
    _n_control: int = ...
    _rng: SeedType = ...
    _ci: ConfidenceInterval | None = ...
    _ci_cl: DecimalNumber | None = ...
    def __str__(self) -> str:
        ...
    
    def confidence_interval(self, confidence_level: DecimalNumber = ...) -> ConfidenceInterval:
        """Compute the confidence interval for the specified confidence level.

        Parameters
        ----------
        confidence_level : float, optional
            Confidence level for the computed confidence interval.
            Default is .95.

        Returns
        -------
        ci : ``ConfidenceInterval`` object
            The object has attributes ``low`` and ``high`` that hold the
            lower and upper bounds of the confidence intervals for each
            comparison. The high and low values are accessible for each
            comparison at index ``i`` for each group ``i``.

        """
        ...
    


@_transition_to_rng('random_state', replace_doc=False)
def dunnett(*samples: npt.ArrayLike, control: npt.ArrayLike, alternative: Literal['two-sided', 'less', 'greater'] = ..., rng: SeedType = ...) -> DunnettResult:
    """Dunnett's test: multiple comparisons of means against a control group.

    This is an implementation of Dunnett's original, single-step test as
    described in [1]_.

    Parameters
    ----------
    sample1, sample2, ... : 1D array_like
        The sample measurements for each experimental group.
    control : 1D array_like
        The sample measurements for the control group.
    alternative : {'two-sided', 'less', 'greater'}, optional
        Defines the alternative hypothesis.

        The null hypothesis is that the means of the distributions underlying
        the samples and control are equal. The following alternative
        hypotheses are available (default is 'two-sided'):

        * 'two-sided': the means of the distributions underlying the samples
          and control are unequal.
        * 'less': the means of the distributions underlying the samples
          are less than the mean of the distribution underlying the control.
        * 'greater': the means of the distributions underlying the
          samples are greater than the mean of the distribution underlying
          the control.
    rng : `numpy.random.Generator`, optional
        Pseudorandom number generator state. When `rng` is None, a new
        `numpy.random.Generator` is created using entropy from the
        operating system. Types other than `numpy.random.Generator` are
        passed to `numpy.random.default_rng` to instantiate a ``Generator``.

        .. versionchanged:: 1.15.0

            As part of the `SPEC-007 <https://scientific-python.org/specs/spec-0007/>`_
            transition from use of `numpy.random.RandomState` to
            `numpy.random.Generator`, this keyword was changed from `random_state` to
            `rng`. For an interim period, both keywords will continue to work, although
            only one may be specified at a time. After the interim period, function
            calls using the `random_state` keyword will emit warnings. Following a
            deprecation period, the `random_state` keyword will be removed.

    Returns
    -------
    res : `~scipy.stats._result_classes.DunnettResult`
        An object containing attributes:

        statistic : float ndarray
            The computed statistic of the test for each comparison. The element
            at index ``i`` is the statistic for the comparison between
            groups ``i`` and the control.
        pvalue : float ndarray
            The computed p-value of the test for each comparison. The element
            at index ``i`` is the p-value for the comparison between
            group ``i`` and the control.

        And the following method:

        confidence_interval(confidence_level=0.95) :
            Compute the difference in means of the groups
            with the control +- the allowance.

    See Also
    --------
    tukey_hsd : performs pairwise comparison of means.
    :ref:`hypothesis_dunnett` : Extended example

    Notes
    -----
    Like the independent-sample t-test, Dunnett's test [1]_ is used to make
    inferences about the means of distributions from which samples were drawn.
    However, when multiple t-tests are performed at a fixed significance level,
    the "family-wise error rate" - the probability of incorrectly rejecting the
    null hypothesis in at least one test - will exceed the significance level.
    Dunnett's test is designed to perform multiple comparisons while
    controlling the family-wise error rate.

    Dunnett's test compares the means of multiple experimental groups
    against a single control group. Tukey's Honestly Significant Difference Test
    is another multiple-comparison test that controls the family-wise error
    rate, but `tukey_hsd` performs *all* pairwise comparisons between groups.
    When pairwise comparisons between experimental groups are not needed,
    Dunnett's test is preferable due to its higher power.

    The use of this test relies on several assumptions.

    1. The observations are independent within and among groups.
    2. The observations within each group are normally distributed.
    3. The distributions from which the samples are drawn have the same finite
       variance.

    References
    ----------
    .. [1] Dunnett, Charles W. (1955) "A Multiple Comparison Procedure for
           Comparing Several Treatments with a Control." Journal of the American
           Statistical Association, 50:272, 1096-1121,
           :doi:`10.1080/01621459.1955.10501294`
    .. [2] Thomson, M. L., & Short, M. D. (1969). Mucociliary function in
           health, chronic obstructive airway disease, and asbestosis. Journal
           of applied physiology, 26(5), 535-539.
           :doi:`10.1152/jappl.1969.26.5.535`

    Examples
    --------
    We'll use data from [2]_, Table 1. The null hypothesis is that the means of
    the distributions underlying the samples and control are equal.

    First, we test that the means of the distributions underlying the samples
    and control are unequal (``alternative='two-sided'``, the default).

    >>> import numpy as np
    >>> from scipy.stats import dunnett
    >>> samples = [[3.8, 2.7, 4.0, 2.4], [2.8, 3.4, 3.7, 2.2, 2.0]]
    >>> control = [2.9, 3.0, 2.5, 2.6, 3.2]
    >>> res = dunnett(*samples, control=control)
    >>> res.statistic
    array([ 0.90874545, -0.05007117])
    >>> res.pvalue
    array([0.58325114, 0.99819341])

    Now, we test that the means of the distributions underlying the samples are
    greater than the mean of the distribution underlying the control.

    >>> res = dunnett(*samples, control=control, alternative='greater')
    >>> res.statistic
    array([ 0.90874545, -0.05007117])
    >>> res.pvalue
    array([0.30230596, 0.69115597])

    For a more detailed example, see :ref:`hypothesis_dunnett`.
    """
    ...

