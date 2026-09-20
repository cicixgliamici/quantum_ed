"""Optimize a differentiable one-qubit VQE objective with PennyLane."""

import pennylane as qml
from pennylane import numpy as np

DEVICE = qml.device("default.qubit", wires=1)


@qml.qnode(DEVICE, diff_method="parameter-shift")
def energy(theta):
    """Return the expectation of the Hamiltonian Z."""
    qml.RY(theta, wires=0)
    return qml.expval(qml.PauliZ(0))


def optimize(steps: int = 50) -> tuple[float, float]:
    """Minimize the QNode with gradient descent from a fixed initial angle."""
    theta = np.array(0.2, requires_grad=True)
    optimizer = qml.GradientDescentOptimizer(stepsize=0.2)
    for _ in range(steps):
        theta = optimizer.step(energy, theta)
    return float(theta), float(energy(theta))


if __name__ == "__main__":
    print(optimize())
