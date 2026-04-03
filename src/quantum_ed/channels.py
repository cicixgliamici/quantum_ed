"""Simple quantum noise channels using density matrices.

We keep this minimal:
- depolarizing channel
- dephasing channel

We represent states as density matrices rho (2x2) for 1 qubit.
"""

from __future__ import annotations
import numpy as np

def is_density_matrix(rho: np.ndarray, atol: float = 1e-10) -> bool:
    if rho.shape != (2,2):
        return False
    # Hermitian
    if not np.allclose(rho, np.conjugate(rho).T, atol=atol):
        return False
    # Trace 1
    if not np.allclose(np.trace(rho), 1.0, atol=atol):
        return False
    # PSD check: eigenvalues >= -atol
    ev = np.linalg.eigvalsh(rho)
    return np.all(ev >= -atol)

def depolarize_rho(rho: np.ndarray, p: float) -> np.ndarray:
    """Depolarizing channel: rho -> (1-p) rho + p I/2."""
    if not (0.0 <= p <= 1.0):
        raise ValueError("p must be in [0,1]")
    I2 = np.eye(2, dtype=complex)
    return (1.0 - p) * rho + p * (I2 / 2.0)

def dephase_rho(rho: np.ndarray, p: float) -> np.ndarray:
    """Dephasing channel: kill off-diagonal terms with strength p.

    A common simple form:
      rho' = [[rho00, (1-p)rho01],
              [(1-p)rho10, rho11]]
    """
    if not (0.0 <= p <= 1.0):
        raise ValueError("p must be in [0,1]")
    out = rho.copy().astype(complex)
    out[0,1] *= (1.0 - p)
    out[1,0] *= (1.0 - p)
    return out
