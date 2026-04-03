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
from .linalg import dagger, trace, projector

def rho_from_ket(ket: np.ndarray) -> np.ndarray:
    """Return density matrix rho = |psi><psi|."""
    return projector(ket)

def fidelity_pure(ket: np.ndarray, rho: np.ndarray) -> float:
    """Fidelity between pure state |psi> and density matrix rho:
        F = <psi| rho |psi>
    """
    ket = ket.reshape((-1,1))
    val = (dagger(ket) @ rho @ ket).item()
    return float(np.real(val))

def partial_trace_two_qubits(rho: np.ndarray, keep: int) -> np.ndarray:
    """Partial trace of a 2-qubit density matrix (4x4).

    keep = 0 keeps the first qubit (trace out second).
    keep = 1 keeps the second qubit (trace out first).

    Returns a 2x2 density matrix.
    """
    if rho.shape != (4,4):
        raise ValueError("rho must be 4x4 for two qubits")
    if keep not in (0,1):
        raise ValueError("keep must be 0 or 1")

    # Index mapping: |ab> where a,b in {0,1}. Flatten ordering: 00,01,10,11.
    # Trace out second qubit:
    #   (rho_A)_{a,a'} = sum_b rho_{ab, a'b}
    # Trace out first qubit:
    #   (rho_B)_{b,b'} = sum_a rho_{ab, ab'}
    out = np.zeros((2,2), dtype=complex)

    if keep == 0:
        for a in (0,1):
            for ap in (0,1):
                s = 0.0+0.0j
                for b in (0,1):
                    i = 2*a + b
                    j = 2*ap + b
                    s += rho[i,j]
                out[a,ap] = s
    else:
        for b in (0,1):
            for bp in (0,1):
                s = 0.0+0.0j
                for a in (0,1):
                    i = 2*a + b
                    j = 2*a + bp
                    s += rho[i,j]
                out[b,bp] = s

    # normalize numerical drift
    tr = trace(out)
    if abs(tr) > 0:
        out = out / tr
    return out
