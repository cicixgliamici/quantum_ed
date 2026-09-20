"""Apply quantum phase estimation with PennyLane."""

import numpy as np
import pennylane as qml

DEVICE = qml.device("default.qubit", wires=4)


@qml.qnode(DEVICE)
def probabilities():
    """Return analytic probabilities for the counting register in QPE."""
    # Target qubit (wire 3) prepared in |1>
    qml.PauliX(wires=3)

    # Counting register (wires 0, 1, 2) initialized in uniform superposition
    qml.Hadamard(wires=0)
    qml.Hadamard(wires=1)
    qml.Hadamard(wires=2)

    # Controlled-U^(2^j) operations
    qml.ControlledPhaseShift(np.pi / 4.0, wires=[0, 3])
    qml.ControlledPhaseShift(np.pi / 2.0, wires=[1, 3])
    qml.ControlledPhaseShift(np.pi, wires=[2, 3])

    # Inverse QFT on counting register
    qml.SWAP(wires=[0, 2])
    qml.Hadamard(wires=0)
    qml.ControlledPhaseShift(-np.pi / 2.0, wires=[1, 0])
    qml.ControlledPhaseShift(-np.pi / 4.0, wires=[2, 0])
    qml.Hadamard(wires=1)
    qml.ControlledPhaseShift(-np.pi / 2.0, wires=[2, 1])
    qml.Hadamard(wires=2)

    return qml.probs(wires=[0, 1, 2])


if __name__ == "__main__":
    print(probabilities())
