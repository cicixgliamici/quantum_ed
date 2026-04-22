"""Simple quantum noise channels using density matrices.

We keep this minimal:
- depolarizing channel
- dephasing channel
- bit-flip channel
- phase-flip channel
- amplitude-damping channel

We represent states as density matrices rho (2x2) for 1 qubit.
"""

from __future__ import annotations

import numpy as np

from .gates import X, Z


def _validate_probability(p: float) -> None:
    if not (0.0 <= p <= 1.0):
        raise ValueError("p must be in [0,1]")


def is_density_matrix(rho: np.ndarray, atol: float = 1e-10) -> bool:
    if rho.shape != (2, 2):
        return False
    if not np.allclose(rho, np.conjugate(rho).T, atol=atol):
        return False
    if not np.allclose(np.trace(rho), 1.0, atol=atol):
        return False
    ev = np.linalg.eigvalsh(rho)
    return np.all(ev >= -atol)


def depolarize_rho(rho: np.ndarray, p: float) -> np.ndarray:
    """Depolarizing channel: rho -> (1-p) rho + p I/2."""
    _validate_probability(p)
    i2 = np.eye(2, dtype=complex)
    return (1.0 - p) * rho + p * (i2 / 2.0)


def dephase_rho(rho: np.ndarray, p: float) -> np.ndarray:
    """Dephasing channel: kill off-diagonal terms with strength p.

    A common simple form:
      rho' = [[rho00, (1-p)rho01],
              [(1-p)rho10, rho11]]
    """
    _validate_probability(p)
    out = rho.copy().astype(complex)
    out[0, 1] *= (1.0 - p)
    out[1, 0] *= (1.0 - p)
    return out


def bit_flip_rho(rho: np.ndarray, p: float) -> np.ndarray:
    """Bit-flip channel: rho -> (1-p) rho + p X rho X."""
    _validate_probability(p)
    return (1.0 - p) * rho + p * (X @ rho @ X)


def phase_flip_rho(rho: np.ndarray, p: float) -> np.ndarray:
    """Phase-flip channel: rho -> (1-p) rho + p Z rho Z."""
    _validate_probability(p)
    return (1.0 - p) * rho + p * (Z @ rho @ Z)


def amplitude_damp_rho(rho: np.ndarray, p: float) -> np.ndarray:
    """Amplitude-damping channel with decay probability p.

    This models energy relaxation from |1> to |0>.
    """
    _validate_probability(p)
    k0 = np.array([[1.0, 0.0], [0.0, np.sqrt(1.0 - p)]], dtype=complex)
    k1 = np.array([[0.0, np.sqrt(p)], [0.0, 0.0]], dtype=complex)
    return k0 @ rho @ np.conjugate(k0).T + k1 @ rho @ np.conjugate(k1).T
