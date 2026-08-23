"""
03_multi_qubit_gates.py

Goal
----
Learn the most important multi-qubit gates in Qiskit:

    CX / CNOT
    CZ
    SWAP
    CCX / Toffoli

Multi-qubit gates are essential because they allow qubits to interact.

In particular, controlled gates are fundamental for:

    - entanglement
    - quantum algorithms
    - reversible computation
    - oracles
    - quantum error correction

This file also reinforces the concept of control and target qubits.
"""

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def show_state(
    name: str,
    circuit: QuantumCircuit,
) -> None:
    """Display circuit, statevector, and measurement probabilities."""

    state = Statevector.from_instruction(circuit)

    print("=" * 70)
    print(name)
    print("=" * 70)

    print("\nCircuit:")
    print(circuit.draw(output="text"))

    print("\nStatevector:")
    print(state)

    print("\nProbabilities:")
    print(state.probabilities_dict())

    print()


def example_cnot_control_zero() -> None:
    """
    CNOT with control qubit equal to |0>.

    Initial state:

        |00>

    Apply:

        CX(0, 1)

    Since the control qubit q0 is 0, the target is not flipped.

    Result:

        |00>
    """

    circuit = QuantumCircuit(2)

    circuit.cx(0, 1)

    show_state(
        "CNOT with control = 0",
        circuit,
    )


def example_cnot_control_one() -> None:
    """
    CNOT with control qubit equal to |1>.

    Start:

        |00>

    Apply X to q0:

        |10>

    Then:

        CX(0, 1)

    Since control q0 = 1, q1 is flipped:

        |10> -> |11>
    """

    circuit = QuantumCircuit(2)

    circuit.x(0)

    circuit.cx(0, 1)

    show_state(
        "CNOT with control = 1",
        circuit,
    )


def example_cnot_superposition() -> None:
    """
    Show why CNOT is a quantum operation, not merely a classical conditional.

    Start:

        |00>

    Apply H to q0:

        (|00> + |10>) / sqrt(2)

    Apply CX:

        (|00> + |11>) / sqrt(2)

    This produces the Bell state |Phi+>.

    The qubits are now entangled.
    """

    circuit = QuantumCircuit(2)

    circuit.h(0)

    circuit.cx(0, 1)

    show_state(
        "CNOT acting on a superposition",
        circuit,
    )


def example_cz() -> None:
    """
    Controlled-Z gate.

    CZ applies a phase -1 only to the basis state:

        |11>

    Its action is:

        |00> ->  |00>
        |01> ->  |01>
        |10> ->  |10>
        |11> -> -|11>

    Since this is a phase operation, we create a superposition first
    to make its effect meaningful.
    """

    circuit = QuantumCircuit(2)

    circuit.h(0)
    circuit.h(1)

    # State before CZ:
    #
    #     1/2 (
    #         |00> +
    #         |01> +
    #         |10> +
    #         |11>
    #     )
    #
    circuit.cz(0, 1)

    # State after CZ:
    #
    #     1/2 (
    #         |00> +
    #         |01> +
    #         |10> -
    #         |11>
    #     )
    #
    show_state(
        "Controlled-Z gate",
        circuit,
    )


def example_swap() -> None:
    """
    SWAP exchanges the states of two qubits.

    Start from:

        |10>

    Then:

        SWAP(0,1)

    produces:

        |01>

    Note
    ----
    Qiskit's textual bit-string conventions may appear reversed
    relative to qubit indexing.

    Always distinguish:

        qubit index

    from:

        printed computational-basis string.
    """

    circuit = QuantumCircuit(2)

    # Prepare q0 = 1 and q1 = 0.
    circuit.x(0)

    circuit.swap(0, 1)

    show_state(
        "SWAP gate",
        circuit,
    )


def example_toffoli() -> None:
    """
    Toffoli gate, also called CCX.

    Syntax:

        ccx(control_1, control_2, target)

    The target flips only if BOTH controls are 1.

    It behaves like a reversible classical AND operation.
    """

    circuit = QuantumCircuit(3)

    # Prepare:
    #
    #     q0 = 1
    #     q1 = 1
    #     q2 = 0
    #
    circuit.x(0)
    circuit.x(1)

    # Both controls are 1, so q2 flips.
    circuit.ccx(0, 1, 2)

    show_state(
        "Toffoli / CCX with both controls = 1",
        circuit,
    )


def example_toffoli_inactive() -> None:
    """
    Show a Toffoli where only one control is 1.

    Because both controls are not active, the target is unchanged.
    """

    circuit = QuantumCircuit(3)

    circuit.x(0)

    circuit.ccx(0, 1, 2)

    show_state(
        "Toffoli / CCX with one inactive control",
        circuit,
    )


def example_controlled_phase_equivalence() -> None:
    """
    Show a useful relationship between CZ and CX.

    Hadamard changes between the X and Z bases:

        H X H = Z

    Therefore:

        CZ(0,1)

    is equivalent to:

        H(target)
        CX(control,target)
        H(target)

    This identity appears frequently in circuit transformations.
    """

    circuit = QuantumCircuit(2)

    circuit.h(0)
    circuit.h(1)

    circuit.h(1)
    circuit.cx(0, 1)
    circuit.h(1)

    show_state(
        "CZ implemented using H-CX-H",
        circuit,
    )


def main() -> None:
    """Run all multi-qubit gate examples."""

    example_cnot_control_zero()
    example_cnot_control_one()

    example_cnot_superposition()

    example_cz()

    example_swap()

    example_toffoli()
    example_toffoli_inactive()

    example_controlled_phase_equivalence()


if __name__ == "__main__":
    main()
