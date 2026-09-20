"""Apply a transparent three-qubit QFT circuit with Qiskit."""

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler


def build_circuit() -> QuantumCircuit:
    """Build a measured QFT of the input basis state 001."""
    circuit = QuantumCircuit(3)
    circuit.x(0)
    circuit.h(0)
    circuit.cp(3.141592653589793 / 2.0, 1, 0)
    circuit.cp(3.141592653589793 / 4.0, 2, 0)
    circuit.h(1)
    circuit.cp(3.141592653589793 / 2.0, 2, 1)
    circuit.h(2)
    circuit.swap(0, 2)
    circuit.measure_all()
    return circuit


def sample(shots: int = 1_024) -> dict[str, int]:
    """Sample the uniform QFT output distribution reproducibly."""
    result = StatevectorSampler(seed=42).run([build_circuit()], shots=shots).result()
    return result[0].data.meas.get_counts()


if __name__ == "__main__":
    print(sample())
