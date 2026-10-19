"""Closed-form predictions independent of the simulated Kraus sums."""

import numpy as np

from .numpy_model import validate_parameters

DEPOLARIZING_THRESHOLD = 1 - 1 / np.sqrt(3)


def predicted_state(channel: str, probability: float) -> np.ndarray:
    """Return the analytical matrix for Phi-plus under E_p tensor E_p."""
    p = validate_parameters(channel, probability)
    if channel == "depolarizing":
        weight = (1 - p) ** 2
        bell = np.array([[1, 0, 0, 1], [0, 0, 0, 0],
                         [0, 0, 0, 0], [1, 0, 0, 1]], dtype=complex) / 2
        return weight * bell + (1 - weight) * np.eye(4) / 4
    if channel == "dephasing":
        state = np.diag([0.5, 0, 0, 0.5]).astype(complex)
        state[0, 3] = state[3, 0] = (1 - p) ** 2 / 2
        return state
    state = np.diag([1 + p**2, p * (1 - p), p * (1 - p), (1 - p)**2]) / 2
    state[0, 3] = state[3, 0] = (1 - p) / 2
    return state.astype(complex)


def predicted_metrics(channel: str, probability: float) -> dict[str, float]:
    """Predict metrics without using the numerical metric implementation."""
    p = validate_parameters(channel, probability)
    remaining = 1 - p
    if channel == "dephasing":
        return {"fidelity": (1 + remaining**2) / 2, "negativity": remaining**2 / 2,
                "purity": (1 + remaining**4) / 2, "xx": remaining**2, "zz": 1.0}
    if channel == "depolarizing":
        return {"fidelity": (1 + 3 * remaining**2) / 4,
                "negativity": max(0.0, (3 * remaining**2 - 1) / 4),
                "purity": (1 + 3 * remaining**4) / 4,
                "xx": remaining**2, "zz": remaining**2}
    return {"fidelity": 1 - p + p**2 / 2, "negativity": remaining**2 / 2,
            "purity": 1 - 2*p + 3*p**2 - 2*p**3 + p**4,
            "xx": remaining, "zz": 1 - 2*p + 2*p**2}
