"""
08_parameterized_circuits.py

Goal
----
Learn how to build reusable parameterized quantum circuits.

This example introduces:

    - Parameter
    - ParameterVector
    - symbolic gate parameters
    - assign_parameters()
    - parameter expressions
    - reusable circuit templates
    - parameter sweeps

Parameterized circuits are fundamental for:

    - variational quantum algorithms
    - VQE
    - QAOA
    - quantum machine learning
    - optimization
    - reusable quantum circuit ansatzes

Theory
------
Instead of constructing one fixed circuit:

    Ry(pi/2)

we can construct a symbolic circuit:

    Ry(theta)

and choose theta later.

Conceptually:

    circuit(theta)

is a family of quantum circuits rather than one single circuit.
"""

from math import pi

from qiskit import QuantumCircuit
from qiskit.circuit import Parameter, ParameterVector
from qiskit.quantum_info import Statevector


def separator(title: str) -> None:
    """Print a section separator."""

    print("=" * 70)
    print(title)
    print("=" * 70)
    print()


def show_bound_state(
    circuit: QuantumCircuit,
) -> None:
    """Print the exact state produced by a fully bound circuit."""

    state = Statevector.from_instruction(
        circuit
    )

    print("Statevector:")
    print(state)

    print("\nProbabilities:")
    print(
        state.probabilities_dict()
    )

    print()


def example_single_parameter() -> None:
    """
    Create the symbolic circuit:

        Ry(theta)|0>

    At this point theta has no numerical value.
    """

    theta = Parameter("theta")

    circuit = QuantumCircuit(1)

    circuit.ry(theta, 0)

    separator("Single symbolic parameter")

    print("Circuit:")
    print(
        circuit.draw(output="text")
    )

    print("\nParameters:")
    print(
        circuit.parameters
    )

    print("\nNumber of parameters:")
    print(
        circuit.num_parameters
    )

    print()


def example_assign_parameter() -> None:
    """
    Assign a numerical value to a symbolic parameter.

    Start from:

        Ry(theta)

    then choose:

        theta = pi/2

    Since:

        Ry(pi/2)|0>
            =
        (|0> + |1>) / sqrt(2)

    measurement probabilities are 50%-50%.
    """

    theta = Parameter("theta")

    circuit = QuantumCircuit(1)

    circuit.ry(theta, 0)

    # assign_parameters() returns a new circuit by default.
    bound_circuit = circuit.assign_parameters(
        {
            theta: pi / 2,
        }
    )

    separator("Assign theta = pi/2")

    print("Symbolic circuit:")
    print(
        circuit.draw(output="text")
    )

    print("\nBound circuit:")
    print(
        bound_circuit.draw(output="text")
    )

    print()

    show_bound_state(
        bound_circuit
    )


def example_reuse_template() -> None:
    """
    A parameterized circuit can be reused with many values.

    We build Ry(theta) once and evaluate it for:

        theta = 0
        theta = pi/4
        theta = pi/2
        theta = pi
    """

    theta = Parameter("theta")

    template = QuantumCircuit(1)

    template.ry(theta, 0)

    separator("Reuse one circuit template")

    for angle in (
        0,
        pi / 4,
        pi / 2,
        pi,
    ):
        circuit = template.assign_parameters(
            {
                theta: angle,
            }
        )

        state = Statevector.from_instruction(
            circuit
        )

        print(
            f"theta = {angle:.4f}"
        )

        print(
            state.probabilities_dict()
        )

        print()


def example_multiple_parameters() -> None:
    """
    A circuit may contain multiple independent parameters.

    Example:

        Rx(alpha)
        Ry(beta)
        Rz(gamma)

    All parameters must be bound before the circuit can be converted
    into a concrete Statevector.
    """

    alpha = Parameter("alpha")
    beta = Parameter("beta")
    gamma = Parameter("gamma")

    circuit = QuantumCircuit(1)

    circuit.rx(alpha, 0)
    circuit.ry(beta, 0)
    circuit.rz(gamma, 0)

    separator("Multiple parameters")

    print("Parameterized circuit:")
    print(
        circuit.draw(output="text")
    )

    print("\nParameters:")
    print(
        circuit.parameters
    )

    bound_circuit = circuit.assign_parameters(
        {
            alpha: pi / 3,
            beta: pi / 4,
            gamma: pi / 5,
        }
    )

    print("\nBound circuit:")
    print(
        bound_circuit.draw(output="text")
    )

    print()

    show_bound_state(
        bound_circuit
    )


def example_parameter_expression() -> None:
    """
    Parameters may appear inside symbolic mathematical expressions.

    For example:

        Ry(2 * theta)

    Setting:

        theta = pi/4

    produces:

        Ry(pi/2)
    """

    theta = Parameter("theta")

    circuit = QuantumCircuit(1)

    circuit.ry(
        2 * theta,
        0,
    )

    separator("Parameter expressions")

    print("Symbolic circuit:")
    print(
        circuit.draw(output="text")
    )

    bound_circuit = circuit.assign_parameters(
        {
            theta: pi / 4,
        }
    )

    print("\nAfter theta = pi/4:")
    print(
        bound_circuit.draw(output="text")
    )

    print()

    show_bound_state(
        bound_circuit
    )


def example_parameter_vector() -> None:
    """
    ParameterVector creates several related parameters at once.

    Instead of manually writing:

        theta_0
        theta_1
        theta_2

    we create:

        theta = ParameterVector("theta", 3)

    This is useful for larger parameterized circuits.
    """

    theta = ParameterVector(
        "theta",
        3,
    )

    circuit = QuantumCircuit(1)

    circuit.rx(theta[0], 0)
    circuit.ry(theta[1], 0)
    circuit.rz(theta[2], 0)

    separator("ParameterVector")

    print("Circuit:")
    print(
        circuit.draw(output="text")
    )

    print("\nParameter vector:")
    print(theta)

    print("\nIndividual parameters:")

    for parameter in theta:
        print(parameter)

    bound_circuit = circuit.assign_parameters(
        {
            theta: [
                pi / 3,
                pi / 4,
                pi / 5,
            ]
        }
    )

    print("\nBound circuit:")
    print(
        bound_circuit.draw(output="text")
    )

    print()

    show_bound_state(
        bound_circuit
    )


def example_two_qubit_ansatz() -> None:
    """
    Build a tiny parameterized two-qubit ansatz.

    Structure:

        Ry(theta_0) on q0
        Ry(theta_1) on q1
        CX(0, 1)

    The rotation parameters control the local states,
    while CX can generate entanglement.

    This circuit pattern resembles the building blocks used in
    variational quantum algorithms.
    """

    theta = ParameterVector(
        "theta",
        2,
    )

    circuit = QuantumCircuit(2)

    circuit.ry(
        theta[0],
        0,
    )

    circuit.ry(
        theta[1],
        1,
    )

    circuit.cx(
        0,
        1,
    )

    separator("Simple parameterized ansatz")

    print("Template:")
    print(
        circuit.draw(output="text")
    )

    bound_circuit = circuit.assign_parameters(
        {
            theta: [
                pi / 2,
                pi / 3,
            ]
        }
    )

    print("\nBound circuit:")
    print(
        bound_circuit.draw(output="text")
    )

    print()

    show_bound_state(
        bound_circuit
    )


def example_inplace_assignment() -> None:
    """
    assign_parameters() normally returns a new circuit.

    With:

        inplace=True

    the original circuit itself is modified.

    For educational code, returning a new circuit is often clearer,
    but both approaches are useful.
    """

    theta = Parameter("theta")

    circuit = QuantumCircuit(1)

    circuit.rx(
        theta,
        0,
    )

    separator("In-place assignment")

    print("Before:")
    print(
        circuit.parameters
    )

    circuit.assign_parameters(
        {
            theta: pi,
        },
        inplace=True,
    )

    print("\nAfter:")
    print(
        circuit.parameters
    )

    print()

    show_bound_state(
        circuit
    )


def main() -> None:
    """Run all parameterized-circuit examples."""

    example_single_parameter()

    example_assign_parameter()

    example_reuse_template()

    example_multiple_parameters()

    example_parameter_expression()

    example_parameter_vector()

    example_two_qubit_ansatz()

    example_inplace_assignment()


if __name__ == "__main__":
    main()
