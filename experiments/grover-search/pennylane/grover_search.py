"""Find the marked state 11 with PennyLane."""

import pennylane as qml

DEVICE = qml.device("default.qubit", wires=2)


@qml.qnode(DEVICE)
def probabilities():
    """Return analytic probabilities after one Grover iteration."""
    for wire in range(2):
        qml.Hadamard(wires=wire)
    qml.CZ(wires=[0, 1])
    for wire in range(2):
        qml.Hadamard(wires=wire)
        qml.PauliX(wires=wire)
    qml.CZ(wires=[0, 1])
    for wire in range(2):
        qml.PauliX(wires=wire)
        qml.Hadamard(wires=wire)
    return qml.probs(wires=[0, 1])


if __name__ == "__main__":
    print(probabilities())
