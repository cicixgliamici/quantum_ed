"""Recover a Bernstein-Vazirani secret with explicit NumPy vectors."""

import numpy as np

SECRET = "101"


def hadamard_register(qubit_count: int) -> np.ndarray:
    """Return the normalized Hadamard transform for a full register."""
    dimension = 2**qubit_count
    matrix = np.empty((dimension, dimension), dtype=float)
    for row in range(dimension):
        for column in range(dimension):
            parity = (row & column).bit_count() % 2
            matrix[row, column] = (-1.0) ** parity
    return matrix / np.sqrt(dimension)


def oracle_phases(secret: str) -> np.ndarray:
    """Return phases produced by the hidden inner-product oracle."""
    secret_value = int(secret, 2)
    return np.array(
        [(-1.0) ** ((value & secret_value).bit_count() % 2) for value in range(2 ** len(secret))]
    )


def recover_secret(secret: str = SECRET) -> str:
    """Recover the secret from the final ideal measurement distribution."""
    transform = hadamard_register(len(secret))
    zero_state = np.eye(2 ** len(secret), dtype=complex)[:, 0]
    final_state = transform @ (oracle_phases(secret) * (transform @ zero_state))
    return f"{int(np.argmax(np.abs(final_state) ** 2)):0{len(secret)}b}"


def main() -> None:
    """Print the recovered secret."""
    print(f"Recovered secret: {recover_secret()}")


if __name__ == "__main__":
    main()
