"""Teleport |1> coherently with PennyLane."""

import pennylane as qml

DEVICE = qml.device("default.qubit", wires=3)


@qml.qnode(DEVICE)
def target_probabilities():
    """Return Bob's analytic target probabilities."""
    qml.PauliX(wires=0)
    qml.Hadamard(wires=1)
    qml.CNOT(wires=[1, 2])
    qml.CNOT(wires=[0, 1])
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[1, 2])
    qml.CZ(wires=[0, 2])
    return qml.probs(wires=2)


if __name__ == "__main__":
    print(target_probabilities())
