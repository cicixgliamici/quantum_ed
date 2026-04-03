"""Linear algebra helpers for QC.

We keep utilities explicit and small so that notebooks remain clean and
the math is inspectable.

All vectors are column vectors (shape (n,1)) unless stated otherwise.
"""

from __future__ import annotations
import numpy as np

ComplexArray = np.ndarray

def dagger(a: ComplexArray) -> ComplexArray:
    """Conjugate transpose."""
    return np.conjugate(a).T

def is_square(a: ComplexArray) -> bool:
    return a.ndim == 2 and a.shape[0] == a.shape[1]

def is_unitary(u: ComplexArray, atol: float = 1e-10) -> bool:
    """Check U†U = I."""
    if not is_square(u):
        return False
    n = u.shape[0]
    return np.allclose(dagger(u) @ u, np.eye(n, dtype=complex), atol=atol)

def projector(ket: ComplexArray) -> ComplexArray:
    """Return |psi><psi| for a normalized state ket."""
    return ket @ dagger(ket)

def trace(a: ComplexArray) -> complex:
    """Trace of a square matrix."""
    return np.trace(a)

def kron(*mats: ComplexArray) -> ComplexArray:
    """Kronecker product of multiple matrices/vectors."""
    out = mats[0]
    for m in mats[1:]:
        out = np.kron(out, m)
    return out
