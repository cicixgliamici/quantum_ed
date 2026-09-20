"""Compute ideal and bit-flip-noisy outcomes with quantum_ed."""

import numpy as np

from quantum_ed.channels import bit_flip_rho
from quantum_ed.density import rho_from_ket
from quantum_ed.states import ket0


def probabilities(error_probability: float) -> np.ndarray:
    """Return measurement probabilities after bit-flip noise on |0>."""
    noisy_state = bit_flip_rho(rho_from_ket(ket0()), error_probability)
    return np.real(np.diag(noisy_state))


if __name__ == "__main__":
    for probability in (0.0, 0.1, 0.25, 0.5):
        print(probability, probabilities(probability))
