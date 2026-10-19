"""Prepare and sample a Bell pair with Qiskit."""

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler


def build_circuit() -> QuantumCircuit:
    """Return a measured Phi-plus preparation."""
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure_all()
    return circuit


def sample(shots: int = 1024) -> dict[str, int]:
    """Use a fixed seed so the example can be reproduced."""
    result = StatevectorSampler(seed=42).run([build_circuit()], shots=shots).result()
    return result[0].data.meas.get_counts()


if __name__ == "__main__":
    print(sample())
