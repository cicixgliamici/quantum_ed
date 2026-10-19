"""Classify f(x)=x_0 with a three-input Deutsch-Jozsa circuit."""

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler


def build_circuit() -> QuantumCircuit:
    """Return a measured circuit; wire zero defines x_0."""
    circuit = QuantumCircuit(4, 3)
    circuit.x(3)
    circuit.h(range(4))
    circuit.cx(0, 3)
    circuit.h(range(3))
    circuit.measure(range(3), range(3))
    return circuit


def classify_function(shots: int = 128) -> tuple[str, dict[str, int]]:
    """Classify from the absence or presence of the all-zero outcome."""
    result = StatevectorSampler(seed=42).run([build_circuit()], shots=shots).result()
    counts = result[0].data.c.get_counts()
    return ("constant" if counts.get("000", 0) == shots else "balanced"), counts


if __name__ == "__main__":
    print(classify_function())
