"""Evaluate a one-qubit variational energy with Qiskit statevectors."""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector

HAMILTONIAN = SparsePauliOp.from_list([("Z", 1.0)])


def energy(theta: float) -> float:
    """Return the exact expectation of Z for the RY ansatz."""
    circuit = QuantumCircuit(1)
    circuit.ry(theta, 0)
    state = Statevector.from_instruction(circuit)
    return float(np.real(state.expectation_value(HAMILTONIAN)))


def optimize(grid_size: int = 361) -> tuple[float, float]:
    """Use a visible grid search so optimizer behavior is inspectable."""
    angles = np.linspace(0.0, 2.0 * np.pi, grid_size)
    energies = np.array([energy(angle) for angle in angles])
    best_index = int(np.argmin(energies))
    return float(angles[best_index]), float(energies[best_index])


if __name__ == "__main__":
    print(optimize())
