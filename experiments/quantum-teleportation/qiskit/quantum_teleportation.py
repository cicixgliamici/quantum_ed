"""Teleport |1> with deferred measurement and Qiskit."""

import sys

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler


def configure_console() -> None:
    """Allow Qiskit's Unicode circuit drawing on Windows terminals."""
    # Qiskit uses box-drawing characters that are unavailable in cp1252.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def build_circuit() -> QuantumCircuit:
    """Build a coherent teleportation circuit for the input state |1>."""
    circuit = QuantumCircuit(3, 1)

    # Qubit 0 is the message; qubits 1 and 2 are Alice and Bob's Bell pair.
    circuit.x(0)
    circuit.h(1)
    circuit.cx(1, 2)
    circuit.barrier()

    # Alice rotates her two qubits into the Bell basis.
    circuit.cx(0, 1)
    circuit.h(0)

    # Deferred measurement replaces classical corrections with coherent controls.
    circuit.cx(1, 2)
    circuit.cz(0, 2)
    circuit.barrier()

    # Only Bob's qubit is measured because it carries the teleported state.
    circuit.measure(2, 0)
    return circuit


def sample_target(shots: int = 128) -> dict[str, int]:
    """Sample Bob's target qubit with a reproducible simulator seed."""
    sampler = StatevectorSampler(seed=42)
    result = sampler.run([build_circuit()], shots=shots).result()
    return result[0].data.c.get_counts()


def main() -> None:
    """Print the circuit and Bob's deterministic result."""
    configure_console()
    print(build_circuit().draw(output="text"))
    print(sample_target())


if __name__ == "__main__":
    main()
