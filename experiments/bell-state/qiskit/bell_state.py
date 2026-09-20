"""Create and sample a Bell state with Qiskit."""

import sys

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler


def configure_console() -> None:
    """Allow Qiskit's Unicode circuit drawing on Windows terminals."""
    # Qiskit uses box-drawing characters that are unavailable in cp1252.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def build_bell_circuit() -> QuantumCircuit:
    """Return a measured circuit that prepares the Bell state Phi-plus."""
    circuit = QuantumCircuit(2)

    # H creates an equal superposition on the control qubit.
    circuit.h(0)

    # CNOT correlates the target with the control, producing Phi-plus.
    circuit.cx(0, 1)

    # Measurements are required because Sampler returns classical outcomes.
    circuit.measure_all()
    return circuit


def sample_bell_circuit(shots: int = 1_024) -> dict[str, int]:
    """Sample the Bell circuit with a deterministic simulator seed."""
    # A fixed seed keeps documentation and review runs reproducible.
    sampler = StatevectorSampler(seed=42)
    result = sampler.run([build_bell_circuit()], shots=shots).result()

    # measure_all names its generated classical register "meas".
    return result[0].data.meas.get_counts()


def main() -> None:
    """Print the circuit and its measurement counts."""
    configure_console()
    circuit = build_bell_circuit()
    print(circuit.draw(output="text"))
    print(sample_bell_circuit())


if __name__ == "__main__":
    main()
