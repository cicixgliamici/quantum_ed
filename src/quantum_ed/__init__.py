"""Quantum-Ed: a minimal, educational quantum computing toolkit.

Design goals:
- explicit math (NumPy-based)
- small functions
- testable behavior
"""

from .states import (
    StateVector,
    basis_00,
    basis_01,
    basis_10,
    basis_11,
    bell_phi_minus,
    bell_phi_plus,
    bell_psi_minus,
    bell_psi_plus,
    bloch_vector,
    ket0,
    ket1,
    normalize,
    state_from_bloch,
)
from .gates import I, X, Y, Z, H, S, T, CNOT, kron_n
from .measurement import measure_comp_basis, probs_comp_basis
from .channels import (
    amplitude_damp_rho,
    bit_flip_rho,
    dephase_rho,
    depolarize_rho,
    phase_flip_rho,
)
from .density import fidelity_pure, partial_trace_two_qubits, rho_from_ket, trace_distance

__all__ = [
    "StateVector",
    "ket0",
    "ket1",
    "basis_00",
    "basis_01",
    "basis_10",
    "basis_11",
    "bell_phi_plus",
    "bell_phi_minus",
    "bell_psi_plus",
    "bell_psi_minus",
    "normalize",
    "bloch_vector",
    "state_from_bloch",
    "I",
    "X",
    "Y",
    "Z",
    "H",
    "S",
    "T",
    "CNOT",
    "kron_n",
    "measure_comp_basis",
    "probs_comp_basis",
    "depolarize_rho",
    "dephase_rho",
    "bit_flip_rho",
    "phase_flip_rho",
    "amplitude_damp_rho",
    "rho_from_ket",
    "partial_trace_two_qubits",
    "fidelity_pure",
    "trace_distance",
]
