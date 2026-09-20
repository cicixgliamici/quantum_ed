"""Recover the secret 101 with PennyLane."""

import pennylane as qml

SECRET = "101"
ANCILLA = len(SECRET)
DEVICE = qml.device("default.qubit", wires=len(SECRET) + 1)


@qml.qnode(DEVICE)
def probabilities():
    """Return the final input-register probabilities."""
    qml.PauliX(wires=ANCILLA)
    for wire in range(len(SECRET) + 1):
        qml.Hadamard(wires=wire)
    for wire, bit in enumerate(SECRET):
        if bit == "1":
            qml.CNOT(wires=[wire, ANCILLA])
    for wire in range(len(SECRET)):
        qml.Hadamard(wires=wire)
    return qml.probs(wires=range(len(SECRET)))


if __name__ == "__main__":
    print(probabilities())
