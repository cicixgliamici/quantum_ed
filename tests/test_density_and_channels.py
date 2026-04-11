import numpy as np

from quantum_ed.states import ket0, ket1, normalize
from quantum_ed.gates import H, CNOT, kron_n, apply
from quantum_ed.density import rho_from_ket, partial_trace_two_qubits, fidelity_pure
from quantum_ed.channels import is_density_matrix, depolarize_rho, dephase_rho


def ket_plus() -> np.ndarray:
    return normalize(H @ ket0())


def bell_phi_plus() -> np.ndarray:
    psi = kron_n(ket0(), ket0())
    psi = apply(kron_n(H, np.eye(2, dtype=complex)), psi)
    psi = apply(CNOT, psi)
    return normalize(psi)


def test_rho_from_ket_for_zero_state():
    rho = rho_from_ket(ket0())
    expected = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    assert np.allclose(rho, expected)


def test_density_matrix_checker_accepts_valid_pure_state():
    rho = rho_from_ket(ket_plus())
    assert is_density_matrix(rho)


def test_density_matrix_checker_rejects_bad_trace():
    rho = np.array([[2.0, 0.0], [0.0, 0.0]], dtype=complex)
    assert not is_density_matrix(rho)


def test_depolarize_preserves_density_matrix_structure():
    rho = rho_from_ket(ket0())
    out = depolarize_rho(rho, 0.3)

    assert is_density_matrix(out)
    assert np.allclose(np.trace(out), 1.0)


def test_depolarize_at_one_gives_maximally_mixed_state():
    rho = rho_from_ket(ket0())
    out = depolarize_rho(rho, 1.0)
    expected = 0.5 * np.eye(2, dtype=complex)

    assert np.allclose(out, expected)


def test_dephase_kills_off_diagonal_terms_at_one():
    rho = rho_from_ket(ket_plus())
    out = dephase_rho(rho, 1.0)

    expected = np.array([[0.5, 0.0], [0.0, 0.5]], dtype=complex)
    assert np.allclose(out, expected)


def test_dephase_preserves_populations():
    rho = rho_from_ket(ket_plus())
    out = dephase_rho(rho, 0.7)

    assert np.allclose(np.diag(out), np.diag(rho))


def test_fidelity_pure_is_one_for_same_state():
    psi = ket_plus()
    rho = rho_from_ket(psi)

    assert np.isclose(fidelity_pure(psi, rho), 1.0)


def test_partial_trace_of_bell_state_is_maximally_mixed():
    psi_ab = bell_phi_plus()
    rho_ab = rho_from_ket(psi_ab)

    rho_a = partial_trace_two_qubits(rho_ab, keep=0)
    rho_b = partial_trace_two_qubits(rho_ab, keep=1)

    expected = 0.5 * np.eye(2, dtype=complex)

    assert np.allclose(rho_a, expected)
    assert np.allclose(rho_b, expected)


def test_partial_trace_returns_density_matrix():
    psi_ab = bell_phi_plus()
    rho_ab = rho_from_ket(psi_ab)

    rho_a = partial_trace_two_qubits(rho_ab, keep=0)
    rho_b = partial_trace_two_qubits(rho_ab, keep=1)

    assert is_density_matrix(rho_a)
    assert is_density_matrix(rho_b)
