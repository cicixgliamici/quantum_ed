"""Prepare Phi-plus with a PennyLane QNode."""

import pennylane as qml

DEVICE = qml.device("default.qubit", wires=2)


@qml.qnode(DEVICE)
def probabilities():
    """Return analytic computational-basis probabilities."""
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    return qml.probs(wires=[0, 1])


if __name__ == "__main__":
    print(probabilities())
