import numpy as np
from quantum_ed.states import ket0
from quantum_ed.gates import H, CNOT, kron_n, apply
from quantum_ed.density import rho_from_ket, partial_trace_two_qubits, fidelity_pure

def bell_phi_plus():
    # |00>
    psi = kron_n(ket0(), ket0())
    psi = apply(kron_n(H, np.eye(2, dtype=complex)), psi)
    psi = apply(CNOT, psi)
    return psi

def test_partial_trace_bell_is_maximally_mixed():
    psi = bell_phi_plus()
    rho = rho_from_ket(psi)
    rhoA = partial_trace_two_qubits(rho, keep=0)
    rhoB = partial_trace_two_qubits(rho, keep=1)
    I2 = np.eye(2, dtype=complex)/2.0
    assert np.allclose(rhoA, I2, atol=1e-10)
    assert np.allclose(rhoB, I2, atol=1e-10)

def test_fidelity_pure():
    psi = bell_phi_plus()
    rho = rho_from_ket(psi)
    assert abs(fidelity_pure(psi, rho) - 1.0) < 1e-10
