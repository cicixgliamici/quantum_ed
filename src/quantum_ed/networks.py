"""Ideal entanglement swapping in tensor order Alice, Bob-left, Bob-right, Charlie.

States use column vectors. The model assumes two available perfect Bell pairs,
ideal local gates, and a complete Bell measurement; it does not model link loss.
"""

import numpy as np

from .density import rho_from_ket
from .gates import CNOT, H, I, X, Z, apply, kron_n
from .states import bell_phi_plus

OUTCOMES = ("00", "01", "10", "11")


def bell_measurement_state() -> np.ndarray:
    """Return the four-qubit state after Bob's CNOT and Hadamard, before readout."""
    links = kron_n(bell_phi_plus(), bell_phi_plus())
    # Bob holds the middle two tensor factors, one from each independent link.
    interacted = apply(kron_n(I, CNOT, I), links)
    return apply(kron_n(I, H, I, I), interacted)


def conditional_endpoint_state(outcome: str, *, corrected: bool = True) -> tuple[float, np.ndarray]:
    """Return the branch probability and normalized Alice-Charlie column vector.

    The outcome is Bob-left followed by Bob-right, encoding phase then bit flip.
    Correcting Charlie applies X for the second bit, then Z for the first bit.
    """
    if not isinstance(outcome, str) or outcome not in OUTCOMES:
        raise ValueError("outcome must be one of 00, 01, 10, 11 in Bob's wire order")
    if not isinstance(corrected, bool):
        raise ValueError("corrected must be a boolean")
    phase_bit, flip_bit = (int(bit) for bit in outcome)
    amplitudes = bell_measurement_state().reshape(2, 2, 2, 2)
    branch = amplitudes[:, phase_bit, flip_bit, :].reshape(4, 1)
    probability = float(np.vdot(branch, branch).real)
    branch = branch / np.sqrt(probability)
    if corrected:
        correction = (Z if phase_bit else I) @ (X if flip_bit else I)
        branch = apply(kron_n(I, correction), branch)
    return probability, branch


def endpoint_density(*, corrected: bool = False) -> np.ndarray:
    """Average branches, either before feed-forward or after outcome-based corrections."""
    density = np.zeros((4, 4), dtype=complex)
    for outcome in OUTCOMES:
        probability, branch = conditional_endpoint_state(outcome, corrected=corrected)
        density += probability * rho_from_ket(branch)
    return density


def swapped_state(*, corrected: bool = True) -> np.ndarray:
    """Return a coherent deferred-measurement representation for SDK comparisons.

    Bob's two wires retain the outcome record. Quantum controls are a simulator
    representation of feed-forward, not remote gates or faster classical traffic.
    """
    amplitudes = np.zeros((2, 2, 2, 2), dtype=complex)
    for outcome in OUTCOMES:
        probability, branch = conditional_endpoint_state(outcome, corrected=corrected)
        phase_bit, flip_bit = (int(bit) for bit in outcome)
        amplitudes[:, phase_bit, flip_bit, :] = np.sqrt(probability) * branch.reshape(2, 2)
    return amplitudes.reshape(16, 1)
