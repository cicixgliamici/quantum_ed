"""Model superdense coding with explicit NumPy operators."""

import numpy as np

from quantum_ed.gates import CNOT, H, I, X, Z, apply, kron_n
from quantum_ed.states import ket0

MESSAGE = "10"


def encoding_gate(message: str) -> np.ndarray:
    """Return Alice's phase-and-flip encoding gate."""
    if len(message) != 2 or set(message) - {"0", "1"}:
        raise ValueError("message must contain exactly two binary digits")
    phase_bit, flip_bit = message
    phase_gate = Z if phase_bit == "1" else I
    flip_gate = X if flip_bit == "1" else I
    return phase_gate @ flip_gate


def decoded_state(message: str = MESSAGE) -> np.ndarray:
    """Return the ideal decoded computational-basis state."""
    state = kron_n(ket0(), ket0())
    state = apply(kron_n(H, I), state)
    state = apply(CNOT, state)
    state = apply(kron_n(encoding_gate(message), I), state)
    state = apply(CNOT, state)
    return apply(kron_n(H, I), state)


def decode_message(message: str = MESSAGE) -> str:
    """Return the most probable computational-basis label."""
    probabilities = np.abs(decoded_state(message).reshape(-1)) ** 2
    return f"{int(np.argmax(probabilities)):02b}"


def main() -> None:
    """Print the decoded message."""
    print(f"Decoded message: {decode_message()}")


if __name__ == "__main__":
    main()
