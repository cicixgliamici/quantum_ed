"""Measure physical states without confusing purity with entanglement."""

import numpy as np

from quantum_ed._validation import density_matrix
from quantum_ed.density import fidelity_pure
from quantum_ed.gates import X, Z
from quantum_ed.states import bell_phi_plus


def partial_transpose(rho: np.ndarray) -> np.ndarray:
    """Transpose Bob's indices: rho[a,b,c,d] becomes rho[a,d,c,b]."""
    rho = density_matrix(rho, dimension=4)
    return rho.reshape(2, 2, 2, 2).transpose(0, 3, 2, 1).reshape(4, 4)


def negativity(rho: np.ndarray) -> float:
    """Sum absolute negative partial-transpose eigenvalues; Bell pairs give 1/2."""
    eigenvalues = np.linalg.eigvalsh(partial_transpose(rho))
    # Keep numerical residuals; interpretation uses the documented tolerance.
    return float(np.sum(np.maximum(-eigenvalues, 0)))


def measure_state(rho: np.ndarray) -> dict[str, float]:
    """Measure full-state metrics and complementary Pauli correlations."""
    rho = density_matrix(rho, dimension=4)
    return {
        "fidelity": fidelity_pure(bell_phi_plus(), rho),
        "negativity": negativity(rho),
        "purity": float(np.trace(rho @ rho).real),
        "xx": float(np.trace(rho @ np.kron(X, X)).real),
        "zz": float(np.trace(rho @ np.kron(Z, Z)).real),
    }
