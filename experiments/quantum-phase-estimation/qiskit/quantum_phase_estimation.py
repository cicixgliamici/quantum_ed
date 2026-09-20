"""Apply quantum phase estimation with Qiskit."""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler


def build_circuit() -> QuantumCircuit:
    """Build a 4-qubit QPE circuit for the T gate on eigenstate |1>."""
    circuit = QuantumCircuit(4, 3)
    # Target qubit 3 in |1>
    circuit.x(3)

    # Counting qubits 0, 1, 2 in uniform superposition
    circuit.h([0, 1, 2])

    # Controlled-U^(2^j) operations
    circuit.cp(np.pi / 4.0, 0, 3)
    circuit.cp(np.pi / 2.0, 1, 3)
    circuit.cp(np.pi, 2, 3)

    # Inverse QFT on counting qubits 0, 1, 2
    circuit.swap(0, 2)
    circuit.h(0)
    circuit.cp(-np.pi / 2.0, 1, 0)
    circuit.cp(-np.pi / 4.0, 2, 0)
    circuit.h(1)
    circuit.cp(-np.pi / 2.0, 2, 1)
    circuit.h(2)

    circuit.measure([0, 1, 2], [0, 1, 2])
    return circuit


def sample(shots: int = 1_024) -> dict[str, int]:
    """Sample the QPE output distribution reproducibly."""
    result = StatevectorSampler(seed=42).run([build_circuit()], shots=shots).result()
    return result[0].data.c.get_counts()


if __name__ == "__main__":
    print(sample())
