"""Compare simple one-qubit noise channels on the same input state."""

import numpy as np

from quantum_ed.channels import (
    amplitude_damp_rho,
    bit_flip_rho,
    dephase_rho,
    depolarize_rho,
    phase_flip_rho,
)
from quantum_ed.density import fidelity_pure, rho_from_ket, trace_distance
from quantum_ed.gates import H, apply
from quantum_ed.states import ket0, normalize


def ket_plus() -> np.ndarray:
    return normalize(apply(H, ket0()))


def main() -> None:
    psi = ket_plus()
    rho = rho_from_ket(psi)
    p = 0.4

    channels = {
        "depolarizing": depolarize_rho(rho, p),
        "dephasing": dephase_rho(rho, p),
        "bit-flip": bit_flip_rho(rho, p),
        "phase-flip": phase_flip_rho(rho, p),
        "amplitude-damping": amplitude_damp_rho(rho, p),
    }

    np.set_printoptions(precision=3, suppress=True)

    print("Reference state: |+><+|")
    print(rho)
    print()

    for name, out in channels.items():
        print(f"{name} (p={p}):")
        print(out)
        print(f"  fidelity to |+>: {fidelity_pure(psi, out):.3f}")
        print(f"  trace distance from input: {trace_distance(rho, out):.3f}")
        print()


if __name__ == "__main__":
    main()
