"""Recover a secret whose characters follow increasing wire index."""

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler


def build_circuit(secret: str = "101") -> QuantumCircuit:
    """Keep logical bit order explicit rather than relying on printed counts."""
    if not secret or set(secret) - {"0", "1"}:
        raise ValueError("secret must be a nonempty binary string")
    input_count = len(secret)
    circuit = QuantumCircuit(input_count + 1, input_count)
    circuit.x(input_count)
    circuit.h(range(input_count + 1))
    for wire, bit in enumerate(secret):
        if bit == "1":
            circuit.cx(wire, input_count)
    circuit.h(range(input_count))
    circuit.measure(range(input_count), range(input_count))
    return circuit


def recover_secret(secret: str = "101", shots: int = 128) -> tuple[str, dict[str, int]]:
    """Reverse Qiskit's displayed classical order to recover wire-order bits."""
    result = StatevectorSampler(seed=42).run([build_circuit(secret)], shots=shots).result()
    counts = result[0].data.c.get_counts()
    return max(counts, key=counts.get)[::-1], counts


if __name__ == "__main__":
    print(recover_secret())
