"""
This type stub file was generated by pyright.
"""

from numpy.linalg._linalg import cholesky as cholesky, cond as cond, cross as cross, det as det, diagonal as diagonal, eig as eig, eigh as eigh, eigvals as eigvals, eigvalsh as eigvalsh, inv as inv, lstsq as lstsq, matmul as matmul, matrix_norm as matrix_norm, matrix_power as matrix_power, matrix_rank as matrix_rank, multi_dot as multi_dot, norm as norm, outer as outer, pinv as pinv, qr as qr, slogdet as slogdet, solve as solve, svd as svd, svdvals as svdvals, tensorinv as tensorinv, tensorsolve as tensorsolve, trace as trace, vector_norm as vector_norm
from numpy._core.fromnumeric import matrix_transpose as matrix_transpose
from numpy._core.numeric import tensordot as tensordot, vecdot as vecdot
from numpy._pytesttester import PytestTester

__all__: list[str]
test: PytestTester
class LinAlgError(Exception):
    ...


