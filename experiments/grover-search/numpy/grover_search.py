"""Find the marked two-bit state 11 with NumPy Grover operators."""

import numpy as np


def final_probabilities() -> np.ndarray:
    """Return probabilities after one optimal Grover iteration."""
    uniform_state = np.ones(4, dtype=complex) / 2.0
    oracle = np.diag([1.0, 1.0, 1.0, -1.0])
    diffusion = 2.0 * np.outer(uniform_state, uniform_state) - np.eye(4)
    return np.abs(diffusion @ oracle @ uniform_state) ** 2


if __name__ == "__main__":
    print({f"{index:02b}": value for index, value in enumerate(final_probabilities())})
