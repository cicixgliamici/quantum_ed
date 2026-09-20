"""Classify a balanced phase oracle with explicit NumPy vectors."""

import numpy as np

INPUT_COUNT = 3


def hadamard_register(qubit_count: int) -> np.ndarray:
    """Return the normalized Hadamard transform for a full register."""
    dimension = 2**qubit_count
    rows = np.arange(dimension)[:, None]
    columns = np.arange(dimension)[None, :]
    parity = np.zeros((dimension, dimension), dtype=int)
    for bit in range(qubit_count):
        parity ^= ((rows >> bit) & 1) * ((columns >> bit) & 1)
    return ((-1.0) ** parity) / np.sqrt(dimension)


def balanced_oracle_phases(qubit_count: int) -> np.ndarray:
    """Return phases for the balanced function f(x)=x_0."""
    values = np.arange(2**qubit_count)
    return (-1.0) ** (values & 1)


def final_probabilities() -> np.ndarray:
    """Return the ideal measurement distribution after interference."""
    transform = hadamard_register(INPUT_COUNT)
    zero_state = np.eye(2**INPUT_COUNT, dtype=complex)[:, 0]
    uniform_state = transform @ zero_state
    phased_state = balanced_oracle_phases(INPUT_COUNT) * uniform_state
    return np.abs(transform @ phased_state) ** 2


def classify_function() -> str:
    """Classify the oracle from its all-zero outcome probability."""
    return "constant" if np.isclose(final_probabilities()[0], 1.0) else "balanced"


def main() -> None:
    """Print the oracle classification."""
    print(f"Oracle classification: {classify_function()}")


if __name__ == "__main__":
    main()
