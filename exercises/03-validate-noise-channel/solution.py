"""Reference solution for amplitude-damping validation."""

import numpy as np

from quantum_ed.channels import amplitude_damp_rho, is_density_matrix
from quantum_ed.density import rho_from_ket
from quantum_ed.states import ket1


def damp_excited_state(probability: float) -> np.ndarray:
    """Return a validated amplitude-damped excited state."""
    output = amplitude_damp_rho(rho_from_ket(ket1()), probability)
    if not is_density_matrix(output):
        raise ValueError("channel output is not a density matrix")
    return output
