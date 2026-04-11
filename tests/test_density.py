import numpy as np

from quantum_ed.states import ket0, normalize
from quantum_ed.gates import H, CNOT, kron_n, apply
from quantum_ed.density import rho_from_ket, fidelity_pure, partial_trace_two_qubits


def bell_phi_plus() -> np.ndarray:
    psi = kron_n(ket0(), ket0())
    psi = apply(kron_n(H, np.eye(2, dtype=complex)), psi)
    psi = apply(CNOT, psi)
    return normalize(psi)


def test_rho_from_ket0():
    rho = rho_from_ket(ket0())
    expected = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    assert np.allclose(rho, expected)


def test_fidelity_pure_is_one_for_same_state():
    psi = normalize(np.array([[1.0], [1.0]], dtype=complex))
    rho = rho_from_ket(psi)
    assert np.isclose(fidelity_pure(psi, rho), 1.0)


def test_partial_trace_of_bell_state_keep_first_qubit():
    psi_ab = bell_phi_plus()
    rho_ab = rho_from_ket(psi_ab)

    rho_a = partial_trace_two_qubits(rho_ab, keep=0)
    expected = 0.5 * np.eye(2, dtype=complex)

    assert np.allclose(rho_a, expected)


def test_partial_trace_of_bell_state_keep_second_qubit():
    psi_ab = bell_phi_plus()
    rho_ab = rho_from_ket(psi_ab)

    rho_b = partial_trace_two_qubits(rho_ab, keep=1)
    expected = 0.5 * np.eye(2, dtype=complex)

    assert np.allclose(rho_b, expected)


def test_partial_trace_rejects_wrong_shape():
    rho = np.eye(2, dtype=complex)

    try:
        partial_trace_two_qubits(rho, keep=0)
        assert False, "Expected ValueError for wrong matrix shape"
    except ValueError:
        pass
