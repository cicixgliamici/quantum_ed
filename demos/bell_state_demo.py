"""
Small CLI demo:
- build a Bell state
- convert it to a density matrix
- partial trace one qubit
- show that each subsystem is maximally mixed
"""

import numpy as np

from quantum_ed.states import ket0, normalize
from quantum_ed.gates import H, CNOT, kron_n, apply
from quantum_ed.density import rho_from_ket, partial_trace_two_qubits


def main() -> None:
    psi = kron_n(ket0(), ket0())
    psi = apply(kron_n(H, np.eye(2, dtype=complex)), psi)
    psi = apply(CNOT, psi)
    psi = normalize(psi)

    rho_ab = rho_from_ket(psi)
    rho_a = partial_trace_two_qubits(rho_ab, keep=0)
    rho_b = partial_trace_two_qubits(rho_ab, keep=1)

    np.set_printoptions(precision=3, suppress=True)

    print("Bell state |Phi+> density matrix:")
    print(rho_ab)
    print()

    print("Reduced state of qubit A:")
    print(rho_a)
    print()

    print("Reduced state of qubit B:")
    print(rho_b)
    print()

    print("Expected reduced state = I / 2:")
    print(0.5 * np.eye(2, dtype=complex))


if __name__ == "__main__":
    main()
