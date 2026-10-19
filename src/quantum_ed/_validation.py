"""Shared input contracts for the small, qubit-based public API."""

from __future__ import annotations

from numbers import Real

import numpy as np


def finite_array(value: np.ndarray, name: str) -> np.ndarray:
    """Require numeric entries before calling NumPy's numerical routines."""
    array = np.asarray(value)
    if array.dtype.kind not in "iufc" or not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite numeric values")
    return array


def real_scalar(value: float, name: str) -> float:
    """Reject arrays and complex values even when NumPy could coerce them."""
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a finite real scalar")
    if not np.isfinite(value):
        raise ValueError(f"{name} must be a finite real scalar")
    return float(value)


def tolerance(value: float) -> float:
    """Keep absolute tolerances finite and nonnegative."""
    value = real_scalar(value, "atol")
    if value < 0:
        raise ValueError("atol must be nonnegative")
    return value


def is_qubit_dimension(size: int) -> bool:
    """A register has at least one qubit and a power-of-two dimension."""
    return size >= 2 and (size & (size - 1)) == 0


def state_vector(
    ket: np.ndarray, dimension: int | None = None, *, normalized: bool = False
) -> np.ndarray:
    """Require column vectors so row/flat inputs cannot silently broadcast."""
    ket = finite_array(ket, "ket")
    if ket.ndim != 2 or ket.shape[1] != 1 or not is_qubit_dimension(ket.shape[0]):
        raise ValueError("ket must be a column vector with shape (2**n, 1), n >= 1")
    if dimension is not None and ket.shape[0] != dimension:
        raise ValueError(f"ket must have shape ({dimension}, 1)")
    if normalized and not np.isclose(np.linalg.norm(ket), 1.0, atol=1e-10, rtol=0):
        raise ValueError("ket must be normalized; call normalize explicitly")
    return ket


def density_matrix(
    rho: np.ndarray, dimension: int | None = None, *, atol: float = 1e-10
) -> np.ndarray:
    """Validate physical states without repairing or renormalizing them."""
    atol = tolerance(atol)
    rho = finite_array(rho, "rho")
    if rho.ndim != 2 or rho.shape[0] != rho.shape[1] or not is_qubit_dimension(rho.shape[0]):
        raise ValueError("rho must be a square matrix with dimension 2**n, n >= 1")
    if dimension is not None and rho.shape[0] != dimension:
        raise ValueError(f"rho must have shape ({dimension}, {dimension})")
    # Relative tolerance is disabled so the documented absolute bound is exact.
    if not np.allclose(rho, rho.conj().T, atol=atol, rtol=0):
        raise ValueError("rho must be Hermitian")
    if not np.isclose(np.trace(rho), 1.0, atol=atol, rtol=0):
        raise ValueError("rho must have trace one")
    if np.min(np.linalg.eigvalsh(rho)) < -atol:
        raise ValueError("rho must be positive semidefinite")
    return rho
