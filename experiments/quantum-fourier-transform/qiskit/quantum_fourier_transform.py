"""Apply a transparent three-qubit QFT circuit with Qiskit."""

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler


def build_circuit(input_value: int = 1) -> QuantumCircuit:
    """Build a measured QFT of the input basis state 001."""
    circuit = QuantumCircuit(3)
    if not isinstance(input_value, int) or not 0 <= input_value < 8:
        raise ValueError("input_value must be an integer in [0, 7]")
    # Logical basis labels use q0 q1 q2, independent of Qiskit's display order.
    for wire, bit in enumerate(f"{input_value:03b}"):
        if bit == "1":
            circuit.x(wire)
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
