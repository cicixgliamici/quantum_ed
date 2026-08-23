"""
21_bernstein_vazirani.py

Goal
----
Recover a hidden bit string with the Bernstein-Vazirani algorithm.

Theory
------
The hidden string is:

    s in {0,1}^n

and the oracle implements:

    f_s(x) = s . x mod 2

where:

    s . x =
        s0*x0 xor
        s1*x1 xor
        ...
        sn*xn

Classically, learning all n secret bits requires n oracle queries
in the standard deterministic strategy.

Bernstein-Vazirani recovers the whole string using one quantum
oracle query.

This example uses:

    SECRET = "101"
"""

import sys

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler


SECRET = "101"

INPUT_COUNT = len(SECRET)
OUTPUT_QUBIT = INPUT_COUNT


def configure_console() -> None:
    """Allow Qiskit's Unicode circuit drawing on Windows terminals."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def apply_secret_oracle(circuit: QuantumCircuit) -> None:
    """
    Encode the hidden string into controlled-X gates.

    For every secret bit equal to 1, add:

        CX(input_qubit, output_qubit)

    Qiskit displays classical bit strings in highest-index-first
    order, so the string is reversed while mapping it to qubit indices.
    """

    for input_qubit, secret_bit in enumerate(reversed(SECRET)):
        if secret_bit == "1":
            circuit.cx(
                input_qubit,
                OUTPUT_QUBIT,
            )


def build_circuit() -> QuantumCircuit:
    """Build the complete Bernstein-Vazirani circuit."""
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
    # Input register becomes:
    #
    #     1/sqrt(2^n) sum_x |x>
    #
    # Output becomes:
    #
    #     |->
    #
    circuit.h(range(INPUT_COUNT + 1))

    # ------------------------------------------------------------
    # 3. Apply the oracle
    # ------------------------------------------------------------
    #
    # Phase kickback produces:
    #
    #     (-1)^(s.x)
    #
    # on every basis component |x>.
    #
    apply_secret_oracle(circuit)

    # ------------------------------------------------------------
    # 4. Apply final Hadamards
    # ------------------------------------------------------------
    #
    # Interference converts the phase pattern into the state:
    #
    #     |s>
    #
    circuit.h(range(INPUT_COUNT))

    # ------------------------------------------------------------
    # 5. Measure the input register
    # ------------------------------------------------------------

    circuit.measure(
        range(INPUT_COUNT),
        range(INPUT_COUNT),
    )

    return circuit


def recover_secret(
    shots: int = 128,
) -> tuple[str, dict[str, int]]:
    """Execute the circuit and recover the hidden string."""
    sampler = StatevectorSampler(seed=42)

    result = sampler.run(
        [build_circuit()],
        shots=shots,
    ).result()

    counts = result[0].data.c.get_counts()

    # In the ideal simulation the answer is deterministic.
    #
    # max(...) is useful because the same post-processing also makes
    # sense when later moving to noisy simulations or real hardware.
    recovered = max(
        counts,
        key=counts.get,
    )

    return recovered, counts


def main() -> None:
    """Display circuit, counts, and recovered secret."""
    configure_console()

    circuit = build_circuit()
    recovered, counts = recover_secret()

    print("Bernstein-Vazirani circuit:")
    print()
    print(circuit.draw(output="text"))

    print("\nMeasurement counts:")
    print(counts)

    print("\nSecret:")
    print(SECRET)

    print("\nRecovered secret:")
    print(recovered)

    print(
        "\nCorrect:",
        recovered == SECRET,
    )


if __name__ == "__main__":
    main()
