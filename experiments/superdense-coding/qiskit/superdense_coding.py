"""Transmit two classical bits with superdense coding and Qiskit."""

import sys

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

MESSAGE = "10"


def configure_console() -> None:
    """Allow Qiskit's Unicode circuit drawing on Windows terminals."""
    # Qiskit uses box-drawing characters that are unavailable in cp1252.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def encode_message(circuit: QuantumCircuit, message: str) -> None:
    """Encode a phase bit and a flip bit on Alice's qubit."""
    phase_bit, flip_bit = message

    # Z selects the Bell-state phase, while X selects its parity.
    if phase_bit == "1":
        circuit.z(0)
    if flip_bit == "1":
        circuit.x(0)


def build_circuit(message: str = MESSAGE) -> QuantumCircuit:
    """Build a measured superdense-coding circuit."""
    if len(message) != 2 or set(message) - {"0", "1"}:
        raise ValueError("message must contain exactly two binary digits")

    circuit = QuantumCircuit(2, 2)

    # Alice and Bob first share Phi-plus, which is the communication resource.
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.barrier()

    # Only Alice's qubit is changed and conceptually transmitted to Bob.
    encode_message(circuit, message)
    circuit.barrier()

    # Bob reverses Bell preparation to decode into computational-basis bits.
    circuit.cx(0, 1)
    circuit.h(0)

    # Reverse the classical destinations so displayed strings match MESSAGE.
    circuit.measure(0, 1)
    circuit.measure(1, 0)
    return circuit


def decode_message(message: str = MESSAGE, shots: int = 128) -> tuple[str, dict[str, int]]:
    """Return the decoded message and sampled measurement counts."""
    sampler = StatevectorSampler(seed=42)
    result = sampler.run([build_circuit(message)], shots=shots).result()
    counts = result[0].data.c.get_counts()
    decoded = max(counts, key=counts.get)
    return decoded, counts


def main() -> None:
    """Print the circuit, counts, and decoded message."""
    configure_console()
    decoded, counts = decode_message()
    print(build_circuit().draw(output="text"))
    print(counts)
    print(f"Decoded message: {decoded}")


if __name__ == "__main__":
    main()
