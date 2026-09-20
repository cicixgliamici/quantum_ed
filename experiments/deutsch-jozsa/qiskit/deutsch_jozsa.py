"""Run a three-input Deutsch-Jozsa experiment with Qiskit."""

import sys

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

INPUT_COUNT = 3
OUTPUT_QUBIT = INPUT_COUNT


def configure_console() -> None:
    """Allow Qiskit's Unicode circuit drawing on Windows terminals."""
    # Qiskit uses box-drawing characters that are unavailable in cp1252.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def apply_balanced_oracle(circuit: QuantumCircuit) -> None:
    """Apply the balanced oracle f(x) = x_0."""
    # A single dependency is enough to make exactly half the outputs one.
    circuit.cx(0, OUTPUT_QUBIT)


def build_circuit() -> QuantumCircuit:
    """Build a measured Deutsch-Jozsa circuit."""
    circuit = QuantumCircuit(INPUT_COUNT + 1, INPUT_COUNT)

    # Preparing the output as |1> makes the following H produce |->.
    circuit.x(OUTPUT_QUBIT)

    # The input Hadamards query all basis inputs in superposition.
    circuit.h(range(INPUT_COUNT + 1))

    # With the output in |->, the oracle writes f(x) into the phase.
    apply_balanced_oracle(circuit)

    # These Hadamards turn relative phases into computational-basis bits.
    circuit.h(range(INPUT_COUNT))

    # The output qubit is not measured because it contains no classification.
    circuit.measure(range(INPUT_COUNT), range(INPUT_COUNT))
    return circuit


def classify_function(shots: int = 128) -> tuple[str, dict[str, int]]:
    """Return the classification and sampled counts."""
    # StatevectorSampler provides local, credential-free ideal simulation.
    sampler = StatevectorSampler(seed=42)
    result = sampler.run([build_circuit()], shots=shots).result()
    counts = result[0].data.c.get_counts()

    # The promise makes the all-zero test sufficient for classification.
    classification = "constant" if set(counts) == {"0" * INPUT_COUNT} else "balanced"
    return classification, counts


def main() -> None:
    """Print the circuit, counts, and inferred oracle class."""
    configure_console()
    circuit = build_circuit()
    classification, counts = classify_function()
    print(circuit.draw(output="text"))
    print(counts)
    print(f"Oracle classification: {classification}")


if __name__ == "__main__":
    main()
