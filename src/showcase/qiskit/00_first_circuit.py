"""
00_first_circuit.py

Goal
----
Learn the basic structure of a Qiskit program:

1. create a quantum circuit
2. apply quantum gates
3. add measurements
4. execute the circuit with a Sampler
5. inspect the measurement results

Circuit
-------

We start from the default one-qubit state:

    |0>

Then we apply an X gate:

    X|0> = |1>

Therefore, after measurement, we expect to obtain:

    "1"

with probability 1.
"""

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler


def build_circuit() -> QuantumCircuit:
    """
    Build the simplest possible measured quantum circuit.

    QuantumCircuit(1, 1) creates:

    - 1 quantum bit
    - 1 classical bit

    Quantum bits store quantum states.
    Classical bits store measurement results.
    """

    circuit = QuantumCircuit(1, 1)

    # Apply the Pauli-X gate to qubit 0.
    #
    # The X gate is the quantum analogue of the classical NOT gate:
    #
    #     X|0> = |1>
    #     X|1> = |0>
    #
    circuit.x(0)

    # Measure qubit 0 and store the result in classical bit 0.
    #
    # The syntax is:
    #
    #     measure(qubit, classical_bit)
    #
    circuit.measure(0, 0)

    return circuit


def run_circuit(shots: int = 1024) -> dict[str, int]:
    """
    Execute the circuit using Qiskit's StatevectorSampler.

    'shots' is the number of repeated measurements.

    Even though this circuit is deterministic, quantum programs are
    normally executed many times to estimate outcome probabilities.
    """

    circuit = build_circuit()

    # StatevectorSampler simulates the circuit locally.
    #
    # A fixed seed makes the example reproducible.
    sampler = StatevectorSampler(seed=42)

    # Sampler.run expects a collection of circuits.
    #
    # Here we run only one circuit.
    job = sampler.run(
        [circuit],
        shots=shots,
    )

    # Obtain the final result object.
    result = job.result()

    # The classical register created by QuantumCircuit(1, 1)
    # is named "c" by default.
    #
    # get_counts() returns something like:
    #
    #     {"1": 1024}
    #
    counts = result[0].data.c.get_counts()

    return counts


def main() -> None:
    """Build, display, execute, and inspect the circuit."""

    circuit = build_circuit()

    print("Quantum circuit:")
    print()
    print(circuit.draw(output="text"))

    print()
    print("Measurement counts:")

    counts = run_circuit()
    print(counts)


if __name__ == "__main__":
    main()
