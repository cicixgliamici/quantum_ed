"""
02_rotation_gates.py

Goal
----
Learn the most important parameterized single-qubit rotation gates:

    Rx(theta)
    Ry(theta)
    Rz(theta)

These gates rotate a qubit around the x, y, and z axes of the Bloch sphere.

Unlike gates such as X, H, or Z, rotation gates accept a continuous angle.

This example also introduces:

    - angles in radians
    - circuit parameters
    - Parameter
    - assign_parameters
    - the relation between rotations and Pauli gates

Theory
------

The three rotation gates are:

    Rx(theta) = exp(-i theta X / 2)

    Ry(theta) = exp(-i theta Y / 2)

    Rz(theta) = exp(-i theta Z / 2)

For theta = pi:

    Rx(pi) ~ X
    Ry(pi) ~ Y
    Rz(pi) ~ Z

where "~" means equality up to a global phase.

Global phase does not affect measurement probabilities.
"""

from math import pi

from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.quantum_info import Statevector


def show_state(
    name: str,
    circuit: QuantumCircuit,
) -> None:
    """
    Display a circuit together with its exact statevector
    and computational-basis probabilities.
    """

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


def example_rx() -> None:
    """
    Rotate |0> around the x axis by pi/2.

    The general action is:

        Rx(theta)|0>
            =
        cos(theta/2)|0>
        - i sin(theta/2)|1>

    For theta = pi/2:

        Rx(pi/2)|0>
            =
        1/sqrt(2)|0>
        - i/sqrt(2)|1>

    Measurement probabilities are therefore:

        P(0) = 1/2
        P(1) = 1/2
    """

    circuit = QuantumCircuit(1)

    circuit.rx(pi / 2, 0)

    show_state(
        "Rx(pi/2) applied to |0>",
        circuit,
    )


def example_ry() -> None:
    """
    Rotate |0> around the y axis by pi/2.

    The general action is:

        Ry(theta)|0>
            =
        cos(theta/2)|0>
        +
        sin(theta/2)|1>

    Therefore:

        Ry(pi/2)|0>
            =
        (|0> + |1>) / sqrt(2)

    This is the same state produced by H|0>.
    """

    circuit = QuantumCircuit(1)

    circuit.ry(pi / 2, 0)

    show_state(
        "Ry(pi/2) applied to |0>",
        circuit,
    )


def example_rz() -> None:
    """
    Demonstrate a rotation around the z axis.

    Applying Rz directly to |0> changes only a global phase,
    which is physically unobservable.

    To make the relative phase visible, first create:

        |+> = (|0> + |1>) / sqrt(2)

    using H.

    Then apply Rz(pi/2).
    """

    circuit = QuantumCircuit(1)

    circuit.h(0)

    circuit.rz(pi / 2, 0)

    show_state(
        "H followed by Rz(pi/2)",
        circuit,
    )


def example_full_rotation() -> None:
    """
    A rotation by 2*pi returns the Bloch vector to its original position.

    At the statevector level, however:

        Rx(2*pi) = -I

    so the state gains a global phase of -1.

    This does not change any measurement probability.
    """

    circuit = QuantumCircuit(1)

    circuit.rx(2 * pi, 0)

    show_state(
        "Rx(2*pi): same physical state up to global phase",
        circuit,
    )


def example_rx_pi_vs_x() -> None:
    """
    Compare Rx(pi) with the X gate.

    Mathematically:

        Rx(pi) = -i X

    They differ only by a global phase.

    Therefore they have exactly the same measurement statistics.
    """

    rotation_circuit = QuantumCircuit(1)
    rotation_circuit.rx(pi, 0)

    x_circuit = QuantumCircuit(1)
    x_circuit.x(0)

    print("=" * 70)
    print("Rx(pi) compared with X")
    print("=" * 70)

    print("\nRx(pi) state:")
    print(
        Statevector.from_instruction(
            rotation_circuit
        )
    )

    print("\nX state:")
    print(
        Statevector.from_instruction(
            x_circuit
        )
    )

    print(
        "\nThe vectors differ by a global phase, "
        "but represent the same physical measurement behaviour."
    )

    print()


def example_parameterized_circuit() -> None:
    """
    Introduce symbolic circuit parameters.

    Parameter lets us construct a circuit before choosing the
    numerical value of an angle.

    This is fundamental for:

        - variational algorithms
        - VQE
        - QAOA
        - optimization
        - reusable circuit templates
    """

    theta = Parameter("theta")

    circuit = QuantumCircuit(1)

    # theta is symbolic here.
    circuit.ry(theta, 0)

    print("=" * 70)
    print("Parameterized circuit")
    print("=" * 70)

    print("\nBefore assigning theta:")
    print(circuit.draw(output="text"))

    # Substitute theta = pi/2.
    bound_circuit = circuit.assign_parameters(
        {
            theta: pi / 2,
        }
    )

    print("\nAfter assigning theta = pi/2:")
    print(bound_circuit.draw(output="text"))

    state = Statevector.from_instruction(
        bound_circuit
    )

    print("\nStatevector:")
    print(state)

    print("\nProbabilities:")
    print(state.probabilities_dict())

    print()


def example_multiple_rotations() -> None:
    """
    Combine multiple rotations.

    Single-qubit operations generally do NOT commute.

    For example:

        Rx(a) Ry(b)

    is generally different from:

        Ry(b) Rx(a)

    Order therefore matters in a quantum circuit.
    """

    circuit = QuantumCircuit(1)

    circuit.rx(pi / 3, 0)
    circuit.ry(pi / 4, 0)
    circuit.rz(pi / 5, 0)

    show_state(
        "Composition: Rx(pi/3), Ry(pi/4), Rz(pi/5)",
        circuit,
    )


def main() -> None:
    """Run all rotation-gate examples."""

    example_rx()
    example_ry()
    example_rz()

    example_full_rotation()
    example_rx_pi_vs_x()

    example_parameterized_circuit()

    example_multiple_rotations()


if __name__ == "__main__":
    main()
