"""Express the same four-wire swapping protocol independently in PennyLane."""

import pennylane as qml

DEVICE = qml.device("default.qubit", wires=4)


def prepare_swapping(corrected: bool = True) -> None:
    """Prepare two links, change Bob's measurement basis, and defer corrections."""
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    qml.Hadamard(wires=2)
    qml.CNOT(wires=[2, 3])
    qml.CNOT(wires=[1, 2])
    qml.Hadamard(wires=1)
    if corrected:
        # These quantum controls reproduce feed-forward only inside the simulator.
        qml.CNOT(wires=[2, 3])
        qml.CZ(wires=[1, 3])


@qml.qnode(DEVICE)
def swapped_state(corrected: bool = True):
    """Expose all amplitudes so validation checks each of Bob's outcome branches."""
    prepare_swapping(corrected)
    return qml.state()


@qml.qnode(DEVICE)
def probabilities():
    """Read Alice and Charlie in increasing output-wire order."""
    prepare_swapping()
    return qml.probs(wires=[0, 3])


if __name__ == "__main__":
    print(probabilities())
