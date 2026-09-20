"""Compute bit-flip-noisy outcomes with PennyLane default.mixed."""

import pennylane as qml

DEVICE = qml.device("default.mixed", wires=1)


@qml.qnode(DEVICE)
def probabilities(error_probability: float):
    """Return measurement probabilities after bit-flip noise on |0>."""
    qml.BitFlip(error_probability, wires=0)
    return qml.probs(wires=0)


if __name__ == "__main__":
    for probability in (0.0, 0.1, 0.25, 0.5):
        print(probability, probabilities(probability))
