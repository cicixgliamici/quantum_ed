"""Recover a hidden bit string with Bernstein-Vazirani and Qiskit."""

import sys

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

SECRET = "101"
INPUT_COUNT = len(SECRET)
OUTPUT_QUBIT = INPUT_COUNT


def configure_console() -> None:
    """Allow Qiskit's Unicode circuit drawing on Windows terminals."""
    # Qiskit uses box-drawing characters that are unavailable in cp1252.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def apply_secret_oracle(circuit: QuantumCircuit) -> None:
    """Encode the secret in controlled-X operations."""
    # Qiskit prints classical bits from highest to lowest index.
    for input_qubit, secret_bit in enumerate(reversed(SECRET)):
        if secret_bit == "1":
            circuit.cx(input_qubit, OUTPUT_QUBIT)


def build_circuit() -> QuantumCircuit:
    """Build a measured Bernstein-Vazirani circuit."""
    circuit = QuantumCircuit(INPUT_COUNT + 1, INPUT_COUNT)

    # X followed by H prepares the output qubit in the |-> state.
    circuit.x(OUTPUT_QUBIT)

    # This layer creates a uniform superposition of every possible input.
    circuit.h(range(INPUT_COUNT + 1))

    # Phase kickback encodes the secret without measuring the output qubit.
    apply_secret_oracle(circuit)

    # Interference maps the phase pattern to the basis state |SECRET>.
    circuit.h(range(INPUT_COUNT))
    circuit.measure(range(INPUT_COUNT), range(INPUT_COUNT))
    return circuit


def recover_secret(shots: int = 128) -> tuple[str, dict[str, int]]:
    """Return the most frequent measured string and all counts."""
    # The seed makes the sampled demonstration reproducible.
    sampler = StatevectorSampler(seed=42)
    result = sampler.run([build_circuit()], shots=shots).result()
    counts = result[0].data.c.get_counts()

    # Majority selection also mirrors the post-processing used with noisy data.
    recovered = max(counts, key=counts.get)
    return recovered, counts


def main() -> None:
    """Print the circuit and recovered secret."""
    configure_console()
    circuit = build_circuit()
    recovered, counts = recover_secret()
    print(circuit.draw(output="text"))
    print(counts)
    print(f"Recovered secret: {recovered}")


if __name__ == "__main__":
    main()
