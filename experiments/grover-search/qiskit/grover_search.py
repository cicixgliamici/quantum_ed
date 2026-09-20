"""Find the marked state 11 with one Grover iteration in Qiskit."""

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler


def build_circuit() -> QuantumCircuit:
    """Build the two-qubit search circuit."""
    circuit = QuantumCircuit(2)
    circuit.h(range(2))
    circuit.cz(0, 1)
    circuit.h(range(2))
    circuit.x(range(2))
    circuit.cz(0, 1)
    circuit.x(range(2))
    circuit.h(range(2))
    circuit.measure_all()
    return circuit


def search(shots: int = 128) -> dict[str, int]:
    """Return reproducible counts for the marked item."""
    result = StatevectorSampler(seed=42).run([build_circuit()], shots=shots).result()
    return result[0].data.meas.get_counts()


if __name__ == "__main__":
    print(search())
