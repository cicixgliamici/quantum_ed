"""Quantum-Ed: a minimal, educational quantum computing toolkit.

Design goals:
- explicit math (NumPy-based)
- small functions
- testable behavior
"""

from .states import ket0, ket1, normalize, bloch_vector, state_from_bloch
from .gates import I, X, Y, Z, H, S, T, CNOT, kron_n
from .measurement import measure_comp_basis, probs_comp_basis
from .channels import depolarize_rho, dephase_rho
