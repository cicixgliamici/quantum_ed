"""
20_deutsch_jozsa.py

Goal
----
Use the Deutsch-Jozsa algorithm to determine whether a promised Boolean
function is constant or balanced.

Theory
------
We have:

    f : {0,1}^n -> {0,1}

with the promise that f is either:

- constant
- balanced

The oracle acts as:

    U_f |x>|y> = |x>|y xor f(x)>

If the output qubit is prepared in |->:

    |-> = (|0> - |1>) / sqrt(2)

then phase kickback gives:

    U_f |x>|-> = (-1)^f(x) |x>|->

After the final Hadamards:

- measurement 000...0 means constant
- any other result means balanced

This example uses:

    n = 3
    f(x) = x_0

which is balanced.
"""

import sys

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler


INPUT_COUNT = 3
OUTPUT_QUBIT = INPUT_COUNT


def configure_console() -> None:
    """Allow Qiskit's Unicode circuit drawing on Windows terminals."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def apply_balanced_oracle(circuit: QuantumCircuit) -> None:
    """
    Apply the balanced oracle:

        f(x0, x1, x2) = x0

    The output qubit is flipped exactly when x0 = 1.
    """

    circuit.cx(0, OUTPUT_QUBIT)


def build_circuit() -> QuantumCircuit:
    """Build the complete Deutsch-Jozsa circuit."""
    circuit = QuantumCircuit(
        INPUT_COUNT + 1,
        INPUT_COUNT,
    )

    # ------------------------------------------------------------
    # 1. Prepare the output qubit in |1>
    # ------------------------------------------------------------

    circuit.x(OUTPUT_QUBIT)

    # ------------------------------------------------------------
    # 2. Apply Hadamard to every qubit
    # ------------------------------------------------------------
    #
    # Inputs:
    #
    #     |0...0> -> uniform superposition
    #
    # Output:
    #
    #     |1> -> |->
    #
    circuit.h(range(INPUT_COUNT + 1))

    # ------------------------------------------------------------
    # 3. Query the oracle
    # ------------------------------------------------------------
    #
    # Because the output is |->, the oracle information is
    # transferred into the phase:
    #
    #     (-1)^f(x)
    #
    apply_balanced_oracle(circuit)

    # ------------------------------------------------------------
    # 4. Interference
    # ------------------------------------------------------------
    #
    # The final Hadamards convert relative phase information
    # into computational-basis information.
    #
    circuit.h(range(INPUT_COUNT))

    # ------------------------------------------------------------
    # 5. Measure only the input register
    # ------------------------------------------------------------

    circuit.measure(
        range(INPUT_COUNT),
        range(INPUT_COUNT),
    )

    return circuit


def classify_function(
    shots: int = 128,
) -> tuple[str, dict[str, int]]:
    """Execute the circuit and classify the oracle."""
    sampler = StatevectorSampler(seed=42)

    result = sampler.run(
        [build_circuit()],
        shots=shots,
    ).result()

    counts = result[0].data.c.get_counts()

    all_zero = "0" * INPUT_COUNT

    # Ideal Deutsch-Jozsa decision rule:
    #
    #     000...0 -> constant
    #     otherwise -> balanced
    #
    classification = (
        "constant"
        if set(counts) == {all_zero}
        else "balanced"
    )

    return classification, counts


def main() -> None:
    """Display circuit, results, and classification."""
    configure_console()

    circuit = build_circuit()
    classification, counts = classify_function()

    print("Deutsch-Jozsa circuit:")
    print()
    print(circuit.draw(output="text"))

    print("\nMeasurement counts:")
    print(counts)

    print("\nClassification:")
    print(classification)

    print("\nExpected result for f(x) = x0: balanced")


if __name__ == "__main__":
    main()
