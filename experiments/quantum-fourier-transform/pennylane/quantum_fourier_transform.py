"""Apply the three-qubit QFT with explicit PennyLane gates."""

import numpy as np
import pennylane as qml

DEVICE = qml.device("default.qubit", wires=3)


@qml.qnode(DEVICE)
def probabilities():
    """Return analytic probabilities for the QFT of basis state 001."""
    qml.PauliX(wires=0)
    qml.Hadamard(wires=0)
    qml.ControlledPhaseShift(np.pi / 2.0, wires=[1, 0])
    qml.ControlledPhaseShift(np.pi / 4.0, wires=[2, 0])
    qml.Hadamard(wires=1)
    qml.ControlledPhaseShift(np.pi / 2.0, wires=[2, 1])
    qml.Hadamard(wires=2)
    qml.SWAP(wires=[0, 2])
    return qml.probs(wires=[0, 1, 2])


if __name__ == "__main__":
    print(probabilities())
