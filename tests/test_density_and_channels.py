import numpy as np

from quantum_ed.states import ket0, ket1, normalize
from quantum_ed.gates import H, CNOT, kron_n, apply
from quantum_ed.density import (
    fidelity_pure,
    partial_trace_two_qubits,
    rho_from_ket,
    trace_distance,
)
from quantum_ed.channels import (
    amplitude_damp_rho,
    bit_flip_rho,
    dephase_rho,
    depolarize_rho,
    is_density_matrix,
    phase_flip_rho,
)


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


def test_bit_flip_on_zero_state_matches_one_state():
    rho = rho_from_ket(ket0())
    out = bit_flip_rho(rho, 1.0)
    expected = rho_from_ket(ket1())
    assert np.allclose(out, expected)


def test_phase_flip_reduces_fidelity_of_plus_state():
    psi = ket_plus()
    rho = rho_from_ket(psi)
    out = phase_flip_rho(rho, 0.5)

    assert np.isclose(fidelity_pure(psi, out), 0.5)


def test_amplitude_damping_reduces_excited_state_population():
    rho = rho_from_ket(ket1())
    out = amplitude_damp_rho(rho, 0.4)

    expected = np.array([[0.4, 0.0], [0.0, 0.6]], dtype=complex)
    assert np.allclose(out, expected)


def test_new_channels_keep_trace_one():
    rho = rho_from_ket(ket_plus())

    for out in (
        bit_flip_rho(rho, 0.2),
        phase_flip_rho(rho, 0.2),
        amplitude_damp_rho(rho, 0.2),
    ):
        assert np.allclose(np.trace(out), 1.0)


def test_dephasing_increases_trace_distance_from_plus_state():
    psi = ket_plus()
    rho = rho_from_ket(psi)
    out = dephase_rho(rho, 1.0)

    assert np.isclose(trace_distance(rho, out), 0.5)
