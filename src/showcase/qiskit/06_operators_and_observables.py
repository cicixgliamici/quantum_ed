"""
06_operators_and_observables.py

Goal
----
Learn how Qiskit represents quantum operators and observables.

This example introduces:

    - Operator
    - matrices of quantum gates
    - operator composition
    - SparsePauliOp
    - Pauli observables
    - expectation values
    - multi-qubit observables

Theory
------
A quantum gate is represented mathematically by a unitary operator U.

For example:

    X = [0 1]
        [1 0]

An observable is represented by a Hermitian operator.

Common observables are the Pauli operators:

    X, Y, Z

The expectation value of an observable A in state |psi> is:

    <A> = <psi| A |psi>

This number represents the average value obtained by repeatedly
measuring the observable on identically prepared states.
"""

import numpy as np

from qiskit import QuantumCircuit
from qiskit.quantum_info import (
    Operator,
    SparsePauliOp,
    Statevector,
)


def separator(title: str) -> None:
    """Print a simple section separator."""

    print("=" * 70)
    print(title)
    print("=" * 70)
    print()


def example_operator_from_matrix() -> None:
    """
    Create an Operator directly from a matrix.

    The Pauli-X matrix is:

        X = [0 1]
            [1 0]

    It maps:

        |0> -> |1>
        |1> -> |0>
    """

    x_matrix = np.array(
        [
            [0, 1],
            [1, 0],
        ],
        dtype=complex,
    )

    x_operator = Operator(x_matrix)

    separator("Operator from matrix")

    print("X operator:")
    print(x_operator)

    print("\nMatrix data:")
    print(x_operator.data)

    print()


def example_operator_from_circuit() -> None:
    """
    Convert a QuantumCircuit into its equivalent unitary Operator.

    A circuit containing only unitary gates represents one
    overall unitary transformation.
    """

    circuit = QuantumCircuit(1)

    circuit.h(0)

    operator = Operator(circuit)

    separator("Operator from QuantumCircuit")

    print("Circuit:")
    print(circuit.draw(output="text"))

    print("\nEquivalent matrix:")
    print(operator.data)

    print()


def example_operator_composition() -> None:
    """
    Compose quantum operators.

    Consider:

        H X H

    Since:

        H X H = Z

    the resulting matrix should be equivalent to the Pauli-Z gate.

    Operator composition follows matrix multiplication rules,
    so the order of operations matters.
    """

    h = Operator(
        np.array(
            [
                [1, 1],
                [1, -1],
            ],
            dtype=complex,
        )
        / np.sqrt(2)
    )

    x = Operator(
        [
            [0, 1],
            [1, 0],
        ]
    )

    # compose() follows operator-composition conventions.
    #
    # Here we use explicit matrix multiplication to make the
    # mathematical order immediately visible:
    #
    #     H X H
    #
    result_matrix = h.data @ x.data @ h.data

    result = Operator(result_matrix)

    separator("Operator composition: H X H")

    print("Result:")
    print(result.data)

    print(
        "\nExpected: Pauli-Z, up to numerical floating-point error."
    )

    print()


def example_sparse_pauli_operator() -> None:
    """
    Introduce SparsePauliOp.

    SparsePauliOp represents operators as linear combinations
    of Pauli strings.

    For example:

        A = 2 Z + 0.5 X

    can be represented without manually constructing the matrix.
    """

    observable = SparsePauliOp.from_list(
        [
            ("Z", 2.0),
            ("X", 0.5),
        ]
    )

    separator("SparsePauliOp")

    print("Observable:")
    print(observable)

    print("\nPauli terms:")
    print(observable.paulis)

    print("\nCoefficients:")
    print(observable.coeffs)

    print("\nEquivalent matrix:")
    print(
        observable.to_matrix()
    )

    print()


def example_z_expectation_zero() -> None:
    """
    Compute <Z> for |0>.

    Since:

        Z|0> = +|0>

    we have:

        <0|Z|0> = +1
    """

    state = Statevector.from_label("0")

    z = SparsePauliOp("Z")

    expectation = state.expectation_value(z)

    separator("<Z> for |0>")

    print("State:")
    print(state)

    print("\nExpectation value:")
    print(expectation)

    print("\nExpected:")
    print(1)

    print()


def example_z_expectation_one() -> None:
    """
    Compute <Z> for |1>.

    Since:

        Z|1> = -|1>

    we obtain:

        <1|Z|1> = -1
    """

    state = Statevector.from_label("1")

    z = SparsePauliOp("Z")

    expectation = state.expectation_value(z)

    separator("<Z> for |1>")

    print("Expectation value:")
    print(expectation)

    print("\nExpected:")
    print(-1)

    print()


def example_z_expectation_plus() -> None:
    """
    Compute <Z> for |+>.

        |+> =
        (|0> + |1>) / sqrt(2)

    Measuring Z gives:

        +1 with probability 1/2
        -1 with probability 1/2

    Therefore:

        <Z> = 0
    """

    state = Statevector.from_label("+")

    z = SparsePauliOp("Z")

    expectation = state.expectation_value(z)

    separator("<Z> for |+>")

    print("State:")
    print(state)

    print("\nExpectation value:")
    print(expectation)

    print("\nExpected:")
    print(0)

    print()


def example_x_expectation_plus() -> None:
    """
    The state |+> is an eigenstate of X:

        X|+> = +|+>

    Therefore:

        <X> = +1
    """

    state = Statevector.from_label("+")

    x = SparsePauliOp("X")

    expectation = state.expectation_value(x)

    separator("<X> for |+>")

    print("Expectation value:")
    print(expectation)

    print("\nExpected:")
    print(1)

    print()


def example_bell_observables() -> None:
    """
    Evaluate observables on the Bell state:

        |Phi+> =
        (|00> + |11>) / sqrt(2)

    The qubits are perfectly correlated in the Z basis.

    Therefore:

        <ZZ> = +1

    The Bell state also has:

        <XX> = +1

    These correlations reveal information that cannot be understood
    by looking at either qubit independently.
    """

    circuit = QuantumCircuit(2)

    circuit.h(0)
    circuit.cx(0, 1)

    state = Statevector.from_instruction(circuit)

    zz = SparsePauliOp("ZZ")
    xx = SparsePauliOp("XX")

    zz_expectation = state.expectation_value(zz)
    xx_expectation = state.expectation_value(xx)

    separator("Bell-state correlations")

    print("Circuit:")
    print(circuit.draw(output="text"))

    print("\nState:")
    print(state)

    print("\n<ZZ>:")
    print(zz_expectation)

    print("\n<XX>:")
    print(xx_expectation)

    print()


def example_hamiltonian() -> None:
    """
    Build a small Hamiltonian.

    Quantum algorithms often work with observables of the form:

        H =
            a I
          + b Z
          + c X

    or, for many qubits, sums of Pauli strings.

    This representation is particularly important for algorithms
    such as VQE.
    """

    hamiltonian = SparsePauliOp.from_list(
        [
            ("I", 0.5),
            ("Z", -1.0),
            ("X", 0.25),
        ]
    )

    state = Statevector.from_label("0")

    energy = state.expectation_value(
        hamiltonian
    )

    separator("Small Hamiltonian")

    print("Hamiltonian:")
    print(hamiltonian)

    print("\nMatrix:")
    print(
        hamiltonian.to_matrix()
    )

    print("\nExpectation value on |0>:")
    print(energy)

    print()


def main() -> None:
    """Run all operator and observable examples."""

    example_operator_from_matrix()
    example_operator_from_circuit()
    example_operator_composition()

    example_sparse_pauli_operator()

    example_z_expectation_zero()
    example_z_expectation_one()
    example_z_expectation_plus()

    example_x_expectation_plus()

    example_bell_observables()

    example_hamiltonian()


if __name__ == "__main__":
    main()
