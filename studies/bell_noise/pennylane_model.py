"""Simulate the same channels with PennyLane's built-in mixed-state engine."""

import pennylane as qml

from .numpy_model import validate_parameters

DEVICE = qml.device("default.mixed", wires=2, shots=None)


@qml.qnode(DEVICE)
def noisy_bell_state(channel: str, probability: float):
    """Return the joint density matrix with explicit SDK parameter conversion."""
    probability = validate_parameters(channel, probability)
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    for wire in (0, 1):
        if channel == "dephasing":
            # PennyLane uses sqrt(1-gamma); this study uses coherence factor 1-p.
            qml.PhaseDamping(probability * (2 - probability), wires=wire)
        elif channel == "depolarizing":
            # Total Pauli-error probability equals 3p/4, not p.
            qml.DepolarizingChannel(3 * probability / 4, wires=wire)
        else:
            qml.AmplitudeDamping(probability, wires=wire)
    return qml.density_matrix(wires=[0, 1])
