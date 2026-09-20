"""Decode all superdense-coding messages with PennyLane."""

import pennylane as qml

DEVICE = qml.device("default.qubit", wires=2)


@qml.qnode(DEVICE)
def probabilities(message: str = "10"):
    """Return decoded basis probabilities for one two-bit message."""
    if len(message) != 2 or set(message) - {"0", "1"}:
        raise ValueError("message must contain exactly two binary digits")
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    if message[0] == "1":
        qml.PauliZ(wires=0)
    if message[1] == "1":
        qml.PauliX(wires=0)
    qml.CNOT(wires=[0, 1])
    qml.Hadamard(wires=0)
    return qml.probs(wires=[0, 1])


if __name__ == "__main__":
    print(probabilities())
