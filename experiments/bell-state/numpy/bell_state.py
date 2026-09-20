"""Prepare the Bell state directly from its NumPy matrix representation."""

import numpy as np

from quantum_ed.gates import CNOT, H, apply, kron_n
from quantum_ed.states import ket0


def bell_state() -> np.ndarray:
    """Return Phi-plus as a state vector."""
    initial_state = kron_n(ket0(), ket0())
    superposition = apply(kron_n(H, np.eye(2, dtype=complex)), initial_state)
    return apply(CNOT, superposition)


def measurement_probabilities() -> dict[str, float]:
    """Return computational-basis probabilities in documented basis order."""
    probabilities = np.abs(bell_state().reshape(-1)) ** 2
    return {f"{index:02b}": float(value) for index, value in enumerate(probabilities)}


def main() -> None:
    """Print the state and ideal measurement probabilities."""
    print(bell_state())
    print(measurement_probabilities())


if __name__ == "__main__":
    main()
