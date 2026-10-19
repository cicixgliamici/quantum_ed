"""Density-matrix utilities (intro level).

We introduce density matrices to support:
- mixed states
- partial trace
- simple entanglement experiments
- noise channels acting on rho

This module intentionally stays minimal and educational.
"""

from __future__ import annotations

import numpy as np

from .linalg import dagger, projector
from ._validation import density_matrix, finite_array, state_vector


def rho_from_ket(ket: np.ndarray) -> np.ndarray:
    """Return rho = |psi><psi| from a normalized qubit column vector.

    Reject unnormalized inputs rather than silently changing their scale.
    """
    ket = state_vector(ket, normalized=True)
    return projector(ket)


def fidelity_pure(ket: np.ndarray, rho: np.ndarray) -> float:
    """Fidelity between pure state |psi> and density matrix rho.

    F = <psi| rho |psi>. The ket must be normalized; a flat vector is
    accepted here for compatibility, as well as the usual column vector.
    """
    ket = finite_array(ket, "ket")
    # Preserve the existing flat-vector convenience without flattening matrices.
    if ket.ndim == 1:
        ket = ket.reshape((-1, 1))
    ket = state_vector(ket, normalized=True)
    rho = density_matrix(rho, dimension=ket.shape[0])
    val = (dagger(ket) @ rho @ ket).item()
    return float(np.real(val))


def trace_distance(rho: np.ndarray, sigma: np.ndarray) -> float:
    """Trace distance between two density matrices.

    D(rho, sigma) = 1/2 * ||rho - sigma||_1

    For Hermitian rho - sigma, this equals half the sum of the absolute
    eigenvalues of rho - sigma.
    """
    rho = density_matrix(rho)
    sigma = density_matrix(sigma, dimension=rho.shape[0])
    delta = rho - sigma
    eigvals = np.linalg.eigvalsh(delta)
    return 0.5 * float(np.sum(np.abs(eigvals)))


def partial_trace_two_qubits(rho: np.ndarray, keep: int) -> np.ndarray:
    """Partial trace of a 2-qubit density matrix (4x4).

    keep = 0 keeps the first qubit (trace out second).
    keep = 1 keeps the second qubit (trace out first).

    Returns a 2x2 density matrix. Input must be physical and trace one;
    neither input nor output is automatically renormalized.
    """
    rho = density_matrix(rho, dimension=4)
    if keep not in (0, 1):
        raise ValueError("keep must be 0 or 1")

    out = np.zeros((2, 2), dtype=complex)

    if keep == 0:
        for a in (0, 1):
            for ap in (0, 1):
                s = 0.0 + 0.0j
                for b in (0, 1):
                    i = 2 * a + b
                    j = 2 * ap + b
                    s += rho[i, j]
                out[a, ap] = s
    else:
        for b in (0, 1):
            for bp in (0, 1):
                s = 0.0 + 0.0j
                for a in (0, 1):
                    i = 2 * a + b
                    j = 2 * a + bp
                    s += rho[i, j]
                out[b, bp] = s

    # Partial trace preserves trace; rescaling here would hide invalid inputs.
    return out
