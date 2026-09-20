"""Apply quantum phase estimation with NumPy."""

import numpy as np


def qft_matrix(qubit_count: int) -> np.ndarray:
    """Return the unitary discrete Fourier transform matrix."""
    dimension = 2**qubit_count
    indices = np.arange(dimension)
    roots = np.exp(2.0j * np.pi * np.outer(indices, indices) / dimension)
    return roots / np.sqrt(dimension)


def estimate_phase() -> dict[str, float]:
    """Run QPE for T gate on target state |1> and return counting probabilities."""
    counting_dim = 8
    # After controlled-U operations, target |1> imparts phase e^(2pi * i * (1/8) * k)
    state = np.exp(2.0j * np.pi * (1.0 / 8.0) * np.arange(counting_dim)) / np.sqrt(counting_dim)

    # Apply inverse QFT: QFT_dag = QFT.conj().T
    inv_qft = qft_matrix(3).conj().T
    final_state = inv_qft @ state

    probabilities = np.abs(final_state) ** 2
    return {f"{idx:03b}": float(prob) for idx, prob in enumerate(probabilities)}


if __name__ == "__main__":
    probs = estimate_phase()
    print("Probabilities:", {k: round(v, 4) for k, v in probs.items()})
