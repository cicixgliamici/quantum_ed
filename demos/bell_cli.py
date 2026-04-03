"""Create a Bell state from scratch and print amplitudes."""

import numpy as np
from quantum_ed.states import ket0
from quantum_ed.gates import H, CNOT, kron_n, apply

def main():
    # |00>
    psi = kron_n(ket0(), ket0())
    # (H ⊗ I)|00>
    psi = apply(kron_n(H, np.eye(2, dtype=complex)), psi)
    # CNOT (control=first qubit)
    psi = apply(CNOT, psi)

    print("Bell state |Phi+> amplitudes (|00>,|01>,|10>,|11>):")
    for i, amp in enumerate(psi.flatten()):
        print(f"{i:02b}: {amp}")

if __name__ == "__main__":
    main()
