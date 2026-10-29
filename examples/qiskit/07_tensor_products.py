"""
07_tensor_products.py

Goal
----
Learn how tensor products construct multi-qubit quantum states.

This example introduces:

    - tensor products
    - Statevector.tensor()
    - Statevector.expand()
    - numpy.kron()
    - multi-qubit basis states
    - subsystem ordering
    - product states
    - product states versus entangled states

Theory
------
If qubit A is in:

    |psi>

and qubit B is in:

    |phi>

the combined system is:

    |psi> tensor |phi>

For example:

    |0> tensor |1> = |01>

The dimensions multiply:

    2 x 2 = 4

so two qubits require four amplitudes.

For n qubits:

    dimension = 2^n
"""

from math import sqrt

import numpy as np

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def separator(title: str) -> None:
    """Print a section separator."""

    print("=" * 70)
    print(title)
    print("=" * 70)
    print()


def example_numpy_tensor_product() -> None:
    """
    Compute a tensor product directly with NumPy.

    Define:

        |0> = [1, 0]
        |1> = [0, 1]

    Then:

        |0> tensor |1>

    gives a four-dimensional vector.
    """

    zero = np.array(
        [1, 0],
        dtype=complex,
    )

    one = np.array(
        [0, 1],
        dtype=complex,
    )

    state = np.kron(
        zero,
        one,
    )

    separator("Tensor product with NumPy")

    print("|0>:")
    print(zero)

    print("\n|1>:")
    print(one)

    print("\n|0> tensor |1>:")
    print(state)

    print()


def example_qiskit_tensor() -> None:
    """
    Use Statevector.tensor().

    Important:

        A.tensor(B)

    returns:

        A tensor B
    """

    zero = Statevector.from_label("0")
    one = Statevector.from_label("1")

    state = zero.tensor(one)

    separator("Statevector.tensor()")

    print("|0> tensor |1>:")
    print(state)

    print("\nProbabilities:")
    print(
        state.probabilities_dict()
    )

    print()


def example_tensor_vs_expand() -> None:
    """
    Compare tensor() and expand().

    Qiskit defines:

        A.tensor(B) = A tensor B

    while:

        A.expand(B) = B tensor A

    The order therefore matters.
    """

    zero = Statevector.from_label("0")
    one = Statevector.from_label("1")

    tensor_result = zero.tensor(one)

    expand_result = zero.expand(one)

    separator("tensor() versus expand()")

    print("zero.tensor(one):")
    print(
        tensor_result.probabilities_dict()
    )

    print("\nzero.expand(one):")
    print(
        expand_result.probabilities_dict()
    )

    print()


def example_two_qubit_basis_states() -> None:
    """
    Display all two-qubit computational basis states.

    The basis is:

        |00>
        |01>
        |10>
        |11>

    Each state is represented by four amplitudes.
    """

    separator("Two-qubit computational basis")

    for label in (
        "00",
        "01",
        "10",
        "11",
    ):
        state = Statevector.from_label(
            label
        )

        print(
            f"|{label}> -> {state.data}"
        )

    print()


def example_qiskit_bit_ordering() -> None:
    """
    Reinforce Qiskit's subsystem ordering.

    In the printed ket:

        |q1 q0>

    q0 is the right-most bit.

    Therefore, if:

        q0 = 1
        q1 = 0

    Qiskit displays:

        |01>

    This convention is essential when reading statevectors and counts.
    """

    circuit = QuantumCircuit(2)

    circuit.x(0)

    state = Statevector.from_instruction(
        circuit
    )

    separator("Qiskit qubit ordering")

    print("Circuit:")
    print(circuit.draw(output="text"))

    print("\nProbabilities:")
    print(
        state.probabilities_dict()
    )

    print(
        "\nq0 = 1 and q1 = 0 is displayed as |01>."
    )

    print()


def example_product_superposition() -> None:
    """
    Construct:

        |+> tensor |0>

    where:

        |+> =
        (|0> + |1>) / sqrt(2)

    Therefore:

        |+>|0>
        =
        (|00> + |10>) / sqrt(2)

    depending on the chosen subsystem ordering.
    """

    plus = Statevector.from_label("+")
    zero = Statevector.from_label("0")

    state = plus.tensor(zero)

    separator("|+> tensor |0>")

    print("State:")
    print(state)

    print("\nProbabilities:")
    print(
        state.probabilities_dict()
    )

    print()


def example_three_qubit_product_state() -> None:
    """
    Build a three-qubit state using repeated tensor products.

    Example:

        |0> tensor |1> tensor |+>

    Three qubits require:

        2^3 = 8

    amplitudes.
    """

    zero = Statevector.from_label("0")
    one = Statevector.from_label("1")
    plus = Statevector.from_label("+")

    state = (
        zero
        .tensor(one)
        .tensor(plus)
    )

    separator("Three-qubit product state")

    print("State:")
    print(state)

    print("\nNumber of amplitudes:")
    print(
        len(state.data)
    )

    print("\nProbabilities:")
    print(
        state.probabilities_dict()
    )

    print()


def example_same_state_from_circuit() -> None:
    """
    Compare tensor construction with circuit construction.

    Prepare:

        q0 = |+>
        q1 = |0>

    using a circuit.

    In Qiskit's ket convention, this corresponds to:

        |0> tensor |+>

    because the displayed basis order is:

        |q1 q0>
    """

    circuit = QuantumCircuit(2)

    circuit.h(0)

    circuit_state = Statevector.from_instruction(
        circuit
    )

    zero = Statevector.from_label("0")
    plus = Statevector.from_label("+")

    tensor_state = zero.tensor(plus)

    separator("Tensor state versus circuit state")

    print("Circuit:")
    print(circuit.draw(output="text"))

    print("\nCircuit state:")
    print(circuit_state)

    print("\nTensor-product state:")
    print(tensor_state)

    print("\nEquivalent:")
    print(
        circuit_state.equiv(
            tensor_state
        )
    )

    print()


def example_product_vs_entangled() -> None:
    """
    Compare a product state with an entangled state.

    Product state:

        |+> tensor |0>

    can be separated into two individual qubit states.

    Bell state:

        (|00> + |11>) / sqrt(2)

    cannot be written as:

        |psi> tensor |phi>

    for any one-qubit states |psi> and |phi>.

    This is the defining feature of entanglement.
    """

    product_state = Statevector(
        [
            1 / sqrt(2),
            0,
            1 / sqrt(2),
            0,
        ]
    )

    bell_state = Statevector(
        [
            1 / sqrt(2),
            0,
            0,
            1 / sqrt(2),
        ]
    )

    separator("Product state versus Bell state")

    print("Product state:")
    print(product_state)

    print("\nProduct-state probabilities:")
    print(
        product_state.probabilities_dict()
    )

    print("\nBell state:")
    print(bell_state)

    print("\nBell-state probabilities:")
    print(
        bell_state.probabilities_dict()
    )

    print(
        "\nThe Bell state cannot be factored into two "
        "independent one-qubit statevectors."
    )

    print()


def example_dimension_growth() -> None:
    """
    Show why tensor products cause exponential state-space growth.

    Each additional qubit multiplies the state dimension by 2.

        1 qubit  -> 2 amplitudes
        2 qubits -> 4
        3 qubits -> 8
        ...
    """

    separator("Exponential state-space growth")

    for qubits in range(
        1,
        11,
    ):
        dimension = 2 ** qubits

        print(
            f"{qubits:2d} qubits -> "
            f"{dimension:5d}-dimensional state"
        )

    print()


def main() -> None:
    """Run all tensor-product examples."""

    example_numpy_tensor_product()

    example_qiskit_tensor()
    example_tensor_vs_expand()

    example_two_qubit_basis_states()

    example_qiskit_bit_ordering()

    example_product_superposition()
    example_three_qubit_product_state()

    example_same_state_from_circuit()

    example_product_vs_entangled()

    example_dimension_growth()


if __name__ == "__main__":
    main()
