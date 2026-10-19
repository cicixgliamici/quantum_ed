"""Apply the three-qubit QFT with explicit PennyLane gates."""

import numpy as np
import pennylane as qml

DEVICE = qml.device("default.qubit", wires=3)


def prepare_qft(input_value: int = 1):
    """Queue the QFT using logical basis labels in wire order q0 q1 q2."""
    if not isinstance(input_value, int) or not 0 <= input_value < 8:
        raise ValueError("input_value must be an integer in [0, 7]")
    for wire, bit in enumerate(f"{input_value:03b}"):
        if bit == "1":
            qml.PauliX(wires=wire)
    qml.Hadamard(wires=0)
    qml.ControlledPhaseShift(np.pi / 2.0, wires=[1, 0])
    qml.ControlledPhaseShift(np.pi / 4.0, wires=[2, 0])
    qml.Hadamard(wires=1)
    qml.ControlledPhaseShift(np.pi / 2.0, wires=[2, 1])
    qml.Hadamard(wires=2)
    qml.SWAP(wires=[0, 2])


@qml.qnode(DEVICE)
def probabilities(input_value: int = 1):
    """Return computational-basis probabilities after the shared circuit."""
    prepare_qft(input_value)
    return qml.probs(wires=[0, 1, 2])


@qml.qnode(DEVICE)
def transformed_state(input_value: int = 1):
    """Expose phases as well as magnitudes for differential validation."""
    prepare_qft(input_value)
    return qml.state()


if __name__ == "__main__":
    print(probabilities())
