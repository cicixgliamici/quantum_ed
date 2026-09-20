"""Classify a balanced oracle with PennyLane."""

import pennylane as qml

INPUT_COUNT = 3
ANCILLA = 3
DEVICE = qml.device("default.qubit", wires=4)


@qml.qnode(DEVICE)
def probabilities():
    """Return the final input-register probabilities."""
    qml.PauliX(wires=ANCILLA)
    for wire in range(4):
        qml.Hadamard(wires=wire)
    qml.CNOT(wires=[0, ANCILLA])
    for wire in range(INPUT_COUNT):
        qml.Hadamard(wires=wire)
    return qml.probs(wires=range(INPUT_COUNT))


if __name__ == "__main__":
    print(probabilities())
