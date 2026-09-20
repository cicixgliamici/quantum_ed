"""Minimize the one-qubit Hamiltonian Z with a NumPy variational ansatz."""

import numpy as np

from quantum_ed.gates import Z, ry
from quantum_ed.states import ket0


def energy(theta: float) -> float:
    """Return the expectation of Z after applying RY(theta) to |0>."""
    state = ry(theta) @ ket0()
    return float(np.real((state.conj().T @ Z @ state).item()))


def optimize(grid_size: int = 361) -> tuple[float, float]:
    """Return the best angle and energy from a transparent grid search."""
    angles = np.linspace(0.0, 2.0 * np.pi, grid_size)
    energies = np.array([energy(angle) for angle in angles])
    best_index = int(np.argmin(energies))
    return float(angles[best_index]), float(energies[best_index])


if __name__ == "__main__":
    print(optimize())
