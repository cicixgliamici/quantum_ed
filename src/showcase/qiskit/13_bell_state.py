"""
13_bell_state.py

Goal
----
Prepare, inspect, and measure the Bell state |Phi+> with Qiskit.

This example connects four views of the same computation:

1. the mathematical state
2. the quantum circuit
3. the statevector
4. repeated measurement outcomes

Theory
------
The two-qubit register starts in:

    |00>

After applying H to qubit 0:

    (|00> + |10>) / sqrt(2)

After applying CX(0, 1):

    |Phi+> = (|00> + |11>) / sqrt(2)

The qubits are now entangled.

Expected measurements:

    P(00) = 1/2
    P(11) = 1/2
"""

import sys

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Statevector


def configure_console() -> None:
    """Allow Qiskit's Unicode circuit drawing on Windows terminals."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def prepare_bell_circuit() -> QuantumCircuit:
    """Return an unmeasured circuit preparing |Phi+>."""
    circuit = QuantumCircuit(2)

    # Initial state:
    #
    #     |00>
    #
    # H on q0 creates:
    #
    #     (|00> + |10>) / sqrt(2)
    #
    circuit.h(0)

    # Controlled-X entangles the two qubits:
    #
    #     |00> -> |00>
    #     |10> -> |11>
    #
    # Final state:
    #
    #     (|00> + |11>) / sqrt(2)
    #
    circuit.cx(0, 1)

    return circuit


def inspect_state() -> Statevector:
    """Return the exact ideal statevector before measurement."""
    circuit = prepare_bell_circuit()

    return Statevector.from_instruction(circuit)


def build_measured_circuit() -> QuantumCircuit:
    """Return the Bell-state circuit with measurements."""
    circuit = prepare_bell_circuit()

    # measure_all() automatically creates a classical register
    # named "meas".
    circuit.measure_all()

    return circuit


def sample_bell_circuit(shots: int = 1024) -> dict[str, int]:
    """Sample the Bell circuit using ideal statevector simulation."""
    circuit = build_measured_circuit()

    sampler = StatevectorSampler(seed=42)

    result = sampler.run(
        [circuit],
        shots=shots,
    ).result()

    return result[0].data.meas.get_counts()


def main() -> None:
    """Display circuit, statevector, probabilities, and measurements."""
    configure_console()

    circuit = prepare_bell_circuit()
    state = inspect_state()
    counts = sample_bell_circuit()

    print("Bell-state preparation circuit:")
    print()
    print(circuit.draw(output="text"))

    print("\nStatevector:")
    print(state)

    print("\nExact probabilities:")
    print(state.probabilities_dict())

    print("\nMeasurement counts:")
    print(counts)

    print("\nExpected outcomes: only 00 and 11, approximately 50% each.")


if __name__ == "__main__":
    main()
