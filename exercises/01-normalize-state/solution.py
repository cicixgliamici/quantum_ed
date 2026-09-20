"""Reference solution for state-vector normalization."""

import numpy as np


def normalize_state(vector: np.ndarray) -> np.ndarray:
    """Return a normalized complex column vector."""
    column = np.asarray(vector, dtype=complex).reshape(-1, 1)
    norm = np.linalg.norm(column)
    if np.isclose(norm, 0.0):
        raise ValueError("cannot normalize the zero vector")
    return column / norm
