"""Reference solution for preparing Phi-plus from gates."""

import numpy as np

from quantum_ed.gates import CNOT, H, apply, kron_n
from quantum_ed.states import ket0


def prepare_bell_state() -> np.ndarray:
    """Prepare Phi-plus from |00> with H and CNOT."""
    initial_state = kron_n(ket0(), ket0())
    superposition = apply(kron_n(H, np.eye(2, dtype=complex)), initial_state)
    return apply(CNOT, superposition)
