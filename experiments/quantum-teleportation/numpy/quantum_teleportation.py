"""Teleport the state |1> with explicit three-qubit NumPy operators."""

import numpy as np

from quantum_ed.gates import CNOT, H, I, X, apply, kron_n
from quantum_ed.states import ket0


def nonadjacent_cz() -> np.ndarray:
    """Return CZ between the first and third qubits in basis order q0 q1 q2."""
    diagonal = np.ones(8, dtype=complex)
    for basis_index in range(8):
        bits = f"{basis_index:03b}"
        if bits[0] == bits[2] == "1":
            diagonal[basis_index] = -1.0
    return np.diag(diagonal)


def teleported_state() -> np.ndarray:
    """Return the three-qubit state after coherent teleportation corrections."""
    state = kron_n(ket0(), ket0(), ket0())

    # Qubit 0 holds |1>; qubits 1 and 2 become the shared Bell pair.
    state = apply(kron_n(X, I, I), state)
    state = apply(kron_n(I, H, I), state)
    state = apply(kron_n(I, CNOT), state)

    # These operations form the sender's Bell-basis interaction.
    state = apply(kron_n(CNOT, I), state)
    state = apply(kron_n(H, I, I), state)

    # Coherent controls defer measurement while preserving the protocol result.
    state = apply(kron_n(I, CNOT), state)
    return apply(nonadjacent_cz(), state)


def target_probabilities() -> dict[str, float]:
    """Return the marginal probabilities of Bob's target qubit."""
    probabilities = np.abs(teleported_state().reshape(-1)) ** 2
    return {
        "0": float(sum(probabilities[0::2])),
        "1": float(sum(probabilities[1::2])),
    }


def main() -> None:
    """Print Bob's ideal measurement probabilities."""
    print(target_probabilities())


if __name__ == "__main__":
    main()
