"""
This type stub file was generated by pyright.
"""

CrosstabResult = ...
def crosstab(*args, levels=..., sparse=...): # -> _:
    """
    Return table of counts for each possible unique combination in ``*args``.

    When ``len(args) > 1``, the array computed by this function is
    often referred to as a *contingency table* [1]_.

    The arguments must be sequences with the same length.  The second return
    value, `count`, is an integer array with ``len(args)`` dimensions.  If
    `levels` is None, the shape of `count` is ``(n0, n1, ...)``, where ``nk``
    is the number of unique elements in ``args[k]``.

    Parameters
    ----------
    *args : sequences
        A sequence of sequences whose unique aligned elements are to be
        counted.  The sequences in args must all be the same length.
    levels : sequence, optional
        If `levels` is given, it must be a sequence that is the same length as
        `args`.  Each element in `levels` is either a sequence or None.  If it
        is a sequence, it gives the values in the corresponding sequence in
        `args` that are to be counted.  If any value in the sequences in `args`
        does not occur in the corresponding sequence in `levels`, that value
        is ignored and not counted in the returned array `count`.  The default
        value of `levels` for ``args[i]`` is ``np.unique(args[i])``
    sparse : bool, optional
        If True, return a sparse matrix.  The matrix will be an instance of
        the `scipy.sparse.coo_matrix` class.  Because SciPy's sparse matrices
        must be 2-d, only two input sequences are allowed when `sparse` is
        True.  Default is False.

    Returns
    -------
    res : CrosstabResult
        An object containing the following attributes:

        elements : tuple of numpy.ndarrays.
            Tuple of length ``len(args)`` containing the arrays of elements
            that are counted in `count`.  These can be interpreted as the
            labels of the corresponding dimensions of `count`. If `levels` was
            given, then if ``levels[i]`` is not None, ``elements[i]`` will
            hold the values given in ``levels[i]``.
        count : numpy.ndarray or scipy.sparse.coo_matrix
            Counts of the unique elements in ``zip(*args)``, stored in an
            array. Also known as a *contingency table* when ``len(args) > 1``.

    See Also
    --------
    numpy.unique

    Notes
    -----
    .. versionadded:: 1.7.0

    References
    ----------
    .. [1] "Contingency table", http://en.wikipedia.org/wiki/Contingency_table

    Examples
    --------
    >>> from scipy.stats.contingency import crosstab

    Given the lists `a` and `x`, create a contingency table that counts the
    frequencies of the corresponding pairs.

    >>> a = ['A', 'B', 'A', 'A', 'B', 'B', 'A', 'A', 'B', 'B']
    >>> x = ['X', 'X', 'X', 'Y', 'Z', 'Z', 'Y', 'Y', 'Z', 'Z']
    >>> res = crosstab(a, x)
    >>> avals, xvals = res.elements
    >>> avals
    array(['A', 'B'], dtype='<U1')
    >>> xvals
    array(['X', 'Y', 'Z'], dtype='<U1')
    >>> res.count
    array([[2, 3, 0],
           [1, 0, 4]])

    So ``('A', 'X')`` occurs twice, ``('A', 'Y')`` occurs three times, etc.

    Higher dimensional contingency tables can be created.

    >>> p = [0, 0, 0, 0, 1, 1, 1, 0, 0, 1]
    >>> res = crosstab(a, x, p)
    >>> res.count
    array([[[2, 0],
            [2, 1],
            [0, 0]],
           [[1, 0],
            [0, 0],
            [1, 3]]])
    >>> res.count.shape
    (2, 3, 2)

    The values to be counted can be set by using the `levels` argument.
    It allows the elements of interest in each input sequence to be
    given explicitly instead finding the unique elements of the sequence.

    For example, suppose one of the arguments is an array containing the
    answers to a survey question, with integer values 1 to 4.  Even if the
    value 1 does not occur in the data, we want an entry for it in the table.

    >>> q1 = [2, 3, 3, 2, 4, 4, 2, 3, 4, 4, 4, 3, 3, 3, 4]  # 1 does not occur.
    >>> q2 = [4, 4, 2, 2, 2, 4, 1, 1, 2, 2, 4, 2, 2, 2, 4]  # 3 does not occur.
    >>> options = [1, 2, 3, 4]
    >>> res = crosstab(q1, q2, levels=(options, options))
    >>> res.count
    array([[0, 0, 0, 0],
           [1, 1, 0, 1],
           [1, 4, 0, 1],
           [0, 3, 0, 3]])

    If `levels` is given, but an element of `levels` is None, the unique values
    of the corresponding argument are used. For example,

    >>> res = crosstab(q1, q2, levels=(None, options))
    >>> res.elements
    [array([2, 3, 4]), [1, 2, 3, 4]]
    >>> res.count
    array([[1, 1, 0, 1],
           [1, 4, 0, 1],
           [0, 3, 0, 3]])

    If we want to ignore the pairs where 4 occurs in ``q2``, we can
    give just the values [1, 2] to `levels`, and the 4 will be ignored:

    >>> res = crosstab(q1, q2, levels=(None, [1, 2]))
    >>> res.elements
    [array([2, 3, 4]), [1, 2]]
    >>> res.count
    array([[1, 1],
           [1, 4],
           [0, 3]])

    Finally, let's repeat the first example, but return a sparse matrix:

    >>> res = crosstab(a, x, sparse=True)
    >>> res.count
    <COOrdinate sparse matrix of dtype 'int64'
        with 4 stored elements and shape (2, 3)>
    >>> res.count.toarray()
    array([[2, 3, 0],
           [1, 0, 4]])

    """
    ...

