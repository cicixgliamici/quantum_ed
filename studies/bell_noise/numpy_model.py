"""Apply independent local Kraus channels to an explicitly prepared Bell pair."""

import numpy as np

from quantum_ed._validation import real_scalar
from quantum_ed.gates import CNOT, H, I, X, Y, Z, apply, kron_n
from quantum_ed.density import rho_from_ket
from quantum_ed.states import basis_00

CHANNELS = ("dephasing", "depolarizing", "amplitude_damping")


def validate_parameters(channel: str, probability: float) -> float:
    """Share parameter contracts, but not physical evolution, with the SDK model."""
    if channel not in CHANNELS:
        raise ValueError(f"channel must be one of {CHANNELS}")
    probability = real_scalar(probability, "probability")
    if not 0 <= probability <= 1:
        raise ValueError("probability must be in [0, 1]")
    return probability


def ideal_bell_state() -> np.ndarray:
    """Prepare Phi-plus through gates rather than assuming the final matrix."""
    state = apply(kron_n(H, I), basis_00())
    return rho_from_ket(apply(CNOT, state))


def kraus_operators(channel: str, probability: float) -> tuple[np.ndarray, ...]:
    """Use a full-dephasing/mixing/decay strength p, each ranging from 0 to 1."""
    probability = validate_parameters(channel, probability)
    if channel == "dephasing":
        # Projectors scale off-diagonal entries by (1-p), not sqrt(1-p).
        return (np.sqrt(1 - probability) * I,
                np.sqrt(probability) * np.diag([1, 0]),
                np.sqrt(probability) * np.diag([0, 1]))
    if channel == "depolarizing":
        # The Pauli sum gives (1-p)rho + p I/2 for trace-one rho.
        return (np.sqrt(1 - 3 * probability / 4) * I,
                *(np.sqrt(probability / 4) * gate for gate in (X, Y, Z)))
    return (np.diag([1, np.sqrt(1 - probability)]),
            np.array([[0, np.sqrt(probability)], [0, 0]]))


def noisy_bell_state(channel: str, probability: float) -> np.ndarray:
    """Apply E_p tensor E_p once after ideal preparation, in q0 q1 order."""
    operators = kraus_operators(channel, probability)
    state = ideal_bell_state()
    for wire in (0, 1):
        # Independent channels act on one tensor factor at a time.
        local_operators = [np.kron(operator, I) if wire == 0 else np.kron(I, operator)
                           for operator in operators]
        state = sum(operator @ state @ operator.conj().T for operator in local_operators)
    return state
