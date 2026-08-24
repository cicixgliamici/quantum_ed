"""
09_sampler.py

Goal
----
Learn how Qiskit's StatevectorSampler primitive works.

This example introduces:

    - StatevectorSampler
    - Primitive V2
    - shots
    - jobs
    - PrimitiveResult
    - SamplerPubResult
    - DataBin
    - BitArray
    - get_counts()
    - get_bitstrings()
    - multiple circuits
    - Sampler PUBs
    - parameterized PUBs
    - parameter sweeps

Concept
-------
Sampler answers a question of the form:

    "If I measure this circuit repeatedly,
     which classical bit strings do I obtain?"

StatevectorSampler uses exact statevector simulation internally,
then samples measurement outcomes from that state.

It therefore produces classical samples, not the raw quantum
statevector.
"""

from math import pi

from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.primitives import StatevectorSampler


def separator(title: str) -> None:
    """Print a section separator."""

    print("=" * 70)
    print(title)
    print("=" * 70)
    print()


def example_basic_sampler() -> None:
    """
    Run the smallest useful Sampler experiment.

    Prepare:

        |+>

    and measure it.

    Expected:

        approximately 50% 0
        approximately 50% 1
    """

    circuit = QuantumCircuit(1)

    circuit.h(0)
    circuit.measure_all()

    sampler = StatevectorSampler(
        seed=42
    )

    job = sampler.run(
        [circuit],
        shots=1024,
    )

    result = job.result()

    counts = (
        result[0]
        .data
        .meas
        .get_counts()
    )

    separator("Basic StatevectorSampler")

    print("Circuit:")
    print(
        circuit.draw(output="text")
    )

    print("\nCounts:")
    print(counts)

    print()


def example_result_structure() -> None:
    """
    Inspect the result hierarchy.

    Conceptually:

        PrimitiveResult
            |
            +-- result[0]
                  |
                  +-- data
                       |
                       +-- meas
                            |
                            +-- BitArray

    Understanding this hierarchy explains expressions such as:

        result[0].data.meas.get_counts()
    """

    circuit = QuantumCircuit(1)

    circuit.h(0)
    circuit.measure_all()

    sampler = StatevectorSampler(
        seed=42
    )

    result = sampler.run(
        [circuit],
        shots=10,
    ).result()

    pub_result = result[0]

    data = pub_result.data

    bit_array = data.meas

    separator("Sampler result structure")

    print("PrimitiveResult:")
    print(result)

    print("\nFirst PUB result:")
    print(pub_result)

    print("\nDataBin:")
    print(data)

    print("\nBitArray:")
    print(bit_array)

    print("\nNumber of bits:")
    print(
        bit_array.num_bits
    )

    print("\nNumber of shots:")
    print(
        bit_array.num_shots
    )

    print()


def example_bitstrings() -> None:
    """
    BitArray can return the individual measurement results.

    get_bitstrings() preserves the sequence of shots.

    Example:

        [
            "0",
            "1",
            "1",
            "0",
            ...
        ]

    get_counts() instead groups identical outcomes.
    """

    circuit = QuantumCircuit(1)

    circuit.h(0)
    circuit.measure_all()

    sampler = StatevectorSampler(
        seed=42
    )

    result = sampler.run(
        [circuit],
        shots=10,
    ).result()[0]

    bit_array = result.data.meas

    separator("Bitstrings versus counts")

    print("Individual shots:")
    print(
        bit_array.get_bitstrings()
    )

    print("\nGrouped counts:")
    print(
        bit_array.get_counts()
    )

    print()


def example_default_shots() -> None:
    """
    StatevectorSampler can define a default number of shots.

    If run() does not receive shots explicitly, default_shots is used.
    """

    circuit = QuantumCircuit(1)

    circuit.h(0)
    circuit.measure_all()

    sampler = StatevectorSampler(
        default_shots=256,
        seed=42,
    )

    result = sampler.run(
        [circuit]
    ).result()[0]

    separator("Default shots")

    print("Number of shots:")
    print(
        result.data.meas.num_shots
    )

    print("\nCounts:")
    print(
        result.data.meas.get_counts()
    )

    print()


def example_multiple_circuits() -> None:
    """
    One Sampler job can contain multiple circuits.

    Here we execute:

        circuit 0 -> |0>
        circuit 1 -> |1>
        circuit 2 -> |+>

    Each circuit corresponds to one PUB result.
    """

    zero = QuantumCircuit(1)
    zero.measure_all()

    one = QuantumCircuit(1)
    one.x(0)
    one.measure_all()

    plus = QuantumCircuit(1)
    plus.h(0)
    plus.measure_all()

    sampler = StatevectorSampler(
        seed=42
    )

    result = sampler.run(
        [
            zero,
            one,
            plus,
        ],
        shots=100,
    ).result()

    separator("Multiple circuits")

    for index, pub_result in enumerate(
        result
    ):
        print(
            f"Circuit {index}:"
        )

        print(
            pub_result
            .data
            .meas
            .get_counts()
        )

        print()


def example_pub_specific_shots() -> None:
    """
    A Sampler Primitive Unified Bloc (PUB) can specify:

        circuit
        parameter values
        shots

    Therefore different experiments can use different numbers
    of measurements in one job.
    """

    zero = QuantumCircuit(1)
    zero.measure_all()

    plus = QuantumCircuit(1)
    plus.h(0)
    plus.measure_all()

    sampler = StatevectorSampler(
        seed=42
    )

    pubs = [
        (
            zero,
            None,
            10,
        ),
        (
            plus,
            None,
            1000,
        ),
    ]

    result = sampler.run(
        pubs
    ).result()

    separator("PUB-specific shots")

    print("First circuit:")
    print(
        result[0]
        .data
        .meas
        .get_counts()
    )

    print(
        "Shots:",
        result[0].data.meas.num_shots,
    )

    print("\nSecond circuit:")
    print(
        result[1]
        .data
        .meas
        .get_counts()
    )

    print(
        "Shots:",
        result[1].data.meas.num_shots,
    )

    print()


def example_parameterized_pub() -> None:
    """
    Sampler can bind parameters directly.

    Build:

        Ry(theta)|0>

    without manually calling assign_parameters().

    The PUB contains:

        (circuit, parameter_values)

    Parameter values are supplied in the circuit's parameter order.
    """

    theta = Parameter(
        "theta"
    )

    circuit = QuantumCircuit(1)

    circuit.ry(
        theta,
        0,
    )

    circuit.measure_all()

    sampler = StatevectorSampler(
        seed=42
    )

    parameter_values = [
        [pi / 2],
    ]

    pub = (
        circuit,
        parameter_values,
    )

    result = sampler.run(
        [pub],
        shots=1000,
    ).result()[0]

    separator("Parameterized Sampler PUB")

    print("Circuit:")
    print(
        circuit.draw(output="text")
    )

    print("\ntheta = pi/2")

    print("\nCounts:")
    print(
        result.data.meas.get_counts()
    )

    print()


def example_parameter_sweep() -> None:
    """
    Evaluate one parameterized circuit at several parameter values.

    Circuit:

        Ry(theta)|0>

    Sweep:

        theta = 0
        theta = pi/2
        theta = pi

    Expected behaviour:

        theta = 0
            -> |0>

        theta = pi/2
            -> 50%-50%

        theta = pi
            -> |1>
    """

    theta = Parameter(
        "theta"
    )

    circuit = QuantumCircuit(1)

    circuit.ry(
        theta,
        0,
    )

    circuit.measure_all()

    parameter_values = [
        [0],
        [pi / 2],
        [pi],
    ]

    sampler = StatevectorSampler(
        seed=42
    )

    result = sampler.run(
        [
            (
                circuit,
                parameter_values,
            )
        ],
        shots=1000,
    ).result()[0]

    separator("Parameter sweep")

    angles = [
        0,
        pi / 2,
        pi,
    ]

    for index, angle in enumerate(
        angles
    ):
        print(
            f"theta = {angle:.4f}"
        )

        # The BitArray has one entry for every
        # parameter set in the sweep.
        counts = (
            result
            .data
            .meas
            .get_counts(index)
        )

        print(counts)

        print()


def example_two_qubit_sampler() -> None:
    """
    Sample a Bell state.

    Prepare:

        (|00> + |11>) / sqrt(2)

    Expected counts:

        00 -> approximately 50%
        11 -> approximately 50%
    """

    circuit = QuantumCircuit(2)

    circuit.h(0)
    circuit.cx(0, 1)

    circuit.measure_all()

    sampler = StatevectorSampler(
        seed=42
    )

    result = sampler.run(
        [circuit],
        shots=1024,
    ).result()[0]

    separator("Sampler with Bell state")

    print("Circuit:")
    print(
        circuit.draw(output="text")
    )

    print("\nCounts:")
    print(
        result.data.meas.get_counts()
    )

    print()


def main() -> None:
    """Run all StatevectorSampler examples."""

    example_basic_sampler()

    example_result_structure()

    example_bitstrings()

    example_default_shots()

    example_multiple_circuits()

    example_pub_specific_shots()

    example_parameterized_pub()

    example_parameter_sweep()

    example_two_qubit_sampler()


if __name__ == "__main__":
    main()
