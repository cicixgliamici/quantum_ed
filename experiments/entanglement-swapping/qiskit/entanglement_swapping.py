"""Prepare two links and perform swapping with deferred corrections in Qiskit."""

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler


def build_circuit(corrected: bool = True) -> QuantumCircuit:
    """Use wires A=0, Bob-left=1, Bob-right=2, C=3; measure only endpoints."""
    circuit = QuantumCircuit(4, 2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.h(2)
    circuit.cx(2, 3)
    # Bob's Bell measurement is expressed as a basis change before readout.
    circuit.cx(1, 2)
    circuit.h(1)
    if corrected:
        # Coherent controls stand in for the two classical messages in simulation.
        circuit.cx(2, 3)
        circuit.cz(1, 3)
    circuit.measure(0, 0)
    circuit.measure(3, 1)
    return circuit


if __name__ == "__main__":
    result = StatevectorSampler(seed=42).run([build_circuit()], shots=1024).result()[0]
    print(result.data.c.get_counts())
