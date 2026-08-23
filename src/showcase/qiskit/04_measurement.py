"""
04_measurement.py

Goal
----
Learn how quantum measurement works in Qiskit.

This example introduces:

    - classical bits
    - ClassicalRegister
    - measure()
    - measure_all()
    - shots
    - measurement probabilities
    - measurement in the computational basis
    - multiple classical registers
    - Qiskit bit ordering

Theory
------
A general one-qubit state is:

    |psi> = alpha|0> + beta|1>

with:

    |alpha|^2 + |beta|^2 = 1

A measurement in the computational basis returns:

    0 with probability |alpha|^2
    1 with probability |beta|^2

For example:

    |+> = (|0> + |1>) / sqrt(2)

therefore:

    P(0) = 1/2
    P(1) = 1/2

Measurement converts quantum information into classical information.
"""

from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.primitives import StatevectorSampler


def run_and_show(
    name: str,
    circuit: QuantumCircuit,
    register_name: str,
    shots: int = 1024,
) -> None:
    """Run a measured circuit and print its counts."""

    sampler = StatevectorSampler(seed=42)

    result = sampler.run(
        [circuit],
        shots=shots,
    ).result()

    # Sampler results contain one BitArray for every ClassicalRegister.
    #
    # getattr(...) lets us access the register dynamically:
    #
    #     result[0].data.c
    #     result[0].data.meas
    #
    register = getattr(
        result[0].data,
        register_name,
    )

    counts = register.get_counts()

    print("=" * 70)
    print(name)
    print("=" * 70)

    print("\nCircuit:")
    print(circuit.draw(output="text"))

    print("\nShots:")
    print(shots)

    print("\nCounts:")
    print(counts)

    print()


def example_measure_zero() -> None:
    """
    Measure |0>.

    Since the default qubit state is |0>:

        P(0) = 1

    Therefore every shot should return 0.
    """

    circuit = QuantumCircuit(1, 1)

    circuit.measure(0, 0)

    run_and_show(
        "Measurement of |0>",
        circuit,
        "c",
    )


def example_measure_one() -> None:
    """
    Measure |1>.

    We prepare |1> using X:

        X|0> = |1>

    Therefore:

        P(1) = 1
    """

    circuit = QuantumCircuit(1, 1)

    circuit.x(0)

    circuit.measure(0, 0)

    run_and_show(
        "Measurement of |1>",
        circuit,
        "c",
    )


def example_measure_superposition() -> None:
    """
    Measure the |+> state.

    H prepares:

        |+> =
        (|0> + |1>) / sqrt(2)

    Therefore:

        P(0) = 1/2
        P(1) = 1/2

    With a finite number of shots, counts will normally be close to,
    but not exactly, 50%-50%.
    """

    circuit = QuantumCircuit(1, 1)

    circuit.h(0)

    circuit.measure(0, 0)

    run_and_show(
        "Measurement of |+>",
        circuit,
        "c",
    )


def example_different_shot_counts() -> None:
    """
    Show why the number of shots matters.

    The true probabilities of |+> are exactly:

        P(0) = 0.5
        P(1) = 0.5

    But finite sampling introduces statistical fluctuations.

    Increasing the number of shots generally gives a better estimate
    of the underlying probability distribution.
    """

    for shots in (
        10,
        100,
        1_000,
        10_000,
    ):
        circuit = QuantumCircuit(1, 1)

        circuit.h(0)
        circuit.measure(0, 0)

        run_and_show(
            f"|+> measured with {shots} shots",
            circuit,
            "c",
            shots,
        )


def example_measure_all() -> None:
    """
    Introduce measure_all().

    measure_all() automatically:

        - adds a classical register
        - measures every qubit

    The generated register is normally named:

        meas
    """

    circuit = QuantumCircuit(2)

    circuit.x(0)
    circuit.h(1)

    circuit.measure_all()

    run_and_show(
        "Using measure_all()",
        circuit,
        "meas",
    )


def example_partial_measurement() -> None:
    """
    Measure only selected qubits.

    A quantum circuit may contain more qubits than classical bits.

    Here:

        q0 = |1>
        q1 = |+>

    but only q0 is measured.

    The state of q1 does not appear in the classical output.
    """

    circuit = QuantumCircuit(2, 1)

    circuit.x(0)
    circuit.h(1)

    circuit.measure(0, 0)

    run_and_show(
        "Partial measurement: only q0",
        circuit,
        "c",
    )


def example_multiple_classical_registers() -> None:
    """
    Demonstrate named classical registers.

    Qiskit can store different measurement results in separate
    ClassicalRegister objects.

    This becomes useful in larger circuits and algorithms where
    different groups of measurements have different meanings.
    """

    q = QuantumRegister(
        2,
        "q",
    )

    first = ClassicalRegister(
        1,
        "first",
    )

    second = ClassicalRegister(
        1,
        "second",
    )

    circuit = QuantumCircuit(
        q,
        first,
        second,
    )

    circuit.x(q[0])
    circuit.h(q[1])

    circuit.measure(
        q[0],
        first[0],
    )

    circuit.measure(
        q[1],
        second[0],
    )

    sampler = StatevectorSampler(seed=42)

    result = sampler.run(
        [circuit],
        shots=1024,
    ).result()[0]

    print("=" * 70)
    print("Multiple classical registers")
    print("=" * 70)

    print("\nCircuit:")
    print(circuit.draw(output="text"))

    print("\nRegister 'first':")
    print(
        result.data.first.get_counts()
    )

    print("\nRegister 'second':")
    print(
        result.data.second.get_counts()
    )

    print()


def example_bit_ordering() -> None:
    """
    Demonstrate Qiskit's bit-string ordering.

    Prepare:

        q0 = 1
        q1 = 0
        q2 = 1

    Qiskit normally prints the classical string as:

        c2 c1 c0

    rather than:

        c0 c1 c2

    This is one of the most important conventions to remember
    when reading Qiskit output.
    """

    circuit = QuantumCircuit(
        3,
        3,
    )

    circuit.x(0)
    circuit.x(2)

    circuit.measure(
        range(3),
        range(3),
    )

    run_and_show(
        "Qiskit bit ordering",
        circuit,
        "c",
    )

    print(
        "q0=1, q1=0, q2=1 is displayed as '101'."
    )

    print(
        "In general, Qiskit displays the highest classical bit first."
    )

    print()


def main() -> None:
    """Run all measurement examples."""

    example_measure_zero()
    example_measure_one()

    example_measure_superposition()

    example_different_shot_counts()

    example_measure_all()
    example_partial_measurement()

    example_multiple_classical_registers()

    example_bit_ordering()


if __name__ == "__main__":
    main()
