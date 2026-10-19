"""Teleport |1> coherently with PennyLane."""

import pennylane as qml
from quantum_ed.states import ket1, normalize

DEVICE = qml.device("default.qubit", wires=3)


def prepare_teleportation(input_state=None):
    """Queue one shared protocol for both probabilities and state inspection."""
    message = normalize(ket1() if input_state is None else input_state)
    if message.shape != (2, 1):
        raise ValueError("input_state must have shape (2, 1)")
    qml.StatePrep(message.ravel(), wires=0)
    qml.Hadamard(wires=1)
    qml.CNOT(wires=[1, 2])
    qml.CNOT(wires=[0, 1])
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[1, 2])
    qml.CZ(wires=[0, 2])


@qml.qnode(DEVICE)
def target_probabilities(input_state=None):
    """Return Bob's analytic probabilities after normalizing the input."""
    prepare_teleportation(input_state)
    return qml.probs(wires=2)


@qml.qnode(DEVICE)
def teleported_state(input_state=None):
    """Expose the final joint state to verify Bob's relative phase."""
    prepare_teleportation(input_state)
    return qml.state()


if __name__ == "__main__":
    print(target_probabilities())
