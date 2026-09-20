"""Apply the three-qubit quantum Fourier transform with NumPy."""

import numpy as np


def qft_matrix(qubit_count: int) -> np.ndarray:
    """Return the unitary discrete Fourier transform matrix."""
    dimension = 2**qubit_count
    indices = np.arange(dimension)
    roots = np.exp(2.0j * np.pi * np.outer(indices, indices) / dimension)
    return roots / np.sqrt(dimension)


def transformed_state(input_value: int = 1, qubit_count: int = 3) -> np.ndarray:
    """Transform one computational-basis input state."""
    state = np.eye(2**qubit_count, dtype=complex)[:, input_value]
    return qft_matrix(qubit_count) @ state


if __name__ == "__main__":
    print(np.abs(transformed_state()) ** 2)
