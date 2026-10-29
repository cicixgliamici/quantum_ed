"""
01_single_qubit_gates.py

Goal
----
Learn the most important single-qubit gates in Qiskit:

    X
    Y
    Z
    H
    S
    T

The example also introduces Statevector, which lets us inspect the
quantum state produced by a circuit before measurement.

General one-qubit state
-----------------------

A qubit can be written as:

    |psi> = alpha|0> + beta|1>

where:

    |alpha|^2 + |beta|^2 = 1

The statevector representation is therefore:

    [alpha, beta]
"""

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def show_state(name: str, circuit: QuantumCircuit) -> None:
    """
    Print a circuit and the statevector it produces from |0>.

    Statevector.from_instruction(circuit) simulates the unitary
    operations in the circuit without performing measurements.
    """

    state = Statevector.from_instruction(circuit)

    print("=" * 60)
    print(name)
    print("=" * 60)

    print("\nCircuit:")
    print(circuit.draw(output="text"))

    print("Statevector:")
    print(state)

    print("\nProbabilities:")
    print(state.probabilities_dict())

    print()


def example_x_gate() -> None:
    """
    Pauli-X gate.

    Matrix:

        X = [0 1]
            [1 0]

    Action:

        X|0> = |1>
        X|1> = |0>

    It behaves similarly to a classical NOT gate.
    """

    circuit = QuantumCircuit(1)

    circuit.x(0)

    show_state("Pauli-X gate", circuit)


def example_y_gate() -> None:
    """
    Pauli-Y gate.

    Matrix:

        Y = [0 -i]
            [i  0]

    Action on |0>:

        Y|0> = i|1>

    The global phase i does not change measurement probabilities.
    """

    circuit = QuantumCircuit(1)

    circuit.y(0)

    show_state("Pauli-Y gate", circuit)


def example_z_gate() -> None:
    """
    Pauli-Z gate.

    Matrix:

        Z = [1  0]
            [0 -1]

    Action:

        Z|0> =  |0>
        Z|1> = -|1>

    Notice that applying Z directly to |0> appears to do nothing.

    Z is a PHASE gate, not a bit-flip gate.
    """

    circuit = QuantumCircuit(1)

    circuit.z(0)

    show_state("Pauli-Z gate", circuit)


def example_h_gate() -> None:
    """
    Hadamard gate.

    Matrix:

             1
        H = ---- [1  1]
            sqrt2 [1 -1]

    Action:

        H|0> = (|0> + |1>) / sqrt(2)

        H|1> = (|0> - |1>) / sqrt(2)

    H creates superposition and is one of the most important
    gates in quantum algorithms.
    """

    circuit = QuantumCircuit(1)

    circuit.h(0)

    show_state("Hadamard gate", circuit)


def example_z_phase() -> None:
    """
    Demonstrate why Z matters when the qubit is in superposition.

    Start:

        |0>

    After H:

        (|0> + |1>) / sqrt(2)

    After Z:

        (|0> - |1>) / sqrt(2)

    The measurement probabilities remain 50%-50%, but the relative
    phase between |0> and |1> changes.
    """

    circuit = QuantumCircuit(1)

    circuit.h(0)
    circuit.z(0)

    show_state("H followed by Z", circuit)


def example_s_gate() -> None:
    """
    S gate.

    Matrix:

        S = [1 0]
            [0 i]

    It introduces a phase of pi/2 on the |1> component.

    To make the phase visible we first create a superposition.
    """

    circuit = QuantumCircuit(1)

    circuit.h(0)
    circuit.s(0)

    show_state("H followed by S", circuit)


def example_t_gate() -> None:
    """
    T gate.

    Matrix:

        T = [1        0       ]
            [0  exp(i*pi/4)]

    It introduces a phase of pi/4 on the |1> component.

    T is especially important because Clifford gates plus T form
    a universal gate set for quantum computation.
    """

    circuit = QuantumCircuit(1)

    circuit.h(0)
    circuit.t(0)

    show_state("H followed by T", circuit)


def example_double_hadamard() -> None:
    """
    Demonstrate that applying H twice gives the identity:

        H^2 = I

    Therefore:

        H H |0> = |0>
    """

    circuit = QuantumCircuit(1)

    circuit.h(0)
    circuit.h(0)

    show_state("Two Hadamard gates: H^2 = I", circuit)


def main() -> None:
    """Run all single-qubit gate examples."""

    example_x_gate()
    example_y_gate()
    example_z_gate()

    example_h_gate()

    example_z_phase()
    example_s_gate()
    example_t_gate()

    example_double_hadamard()


if __name__ == "__main__":
    main()
