import numpy as np

from quantum_ed.states import ket0, ket1, normalize
from quantum_ed.gates import H, apply
from quantum_ed.density import rho_from_ket
from quantum_ed.channels import (
    amplitude_damp_rho,
    bit_flip_rho,
    dephase_rho,
    depolarize_rho,
    is_density_matrix,
    phase_flip_rho,
)


def ket_plus():
    return normalize(apply(H, ket0()))


def test_is_density_matrix_accepts_valid_pure_state():
    rho = rho_from_ket(ket0())
    assert is_density_matrix(rho)


def test_is_density_matrix_rejects_wrong_shape():
    rho = np.eye(4, dtype=complex)
    assert not is_density_matrix(rho)


def test_is_density_matrix_rejects_bad_trace():
    rho = np.array([[2.0, 0.0], [0.0, 0.0]], dtype=complex)
    assert not is_density_matrix(rho)


def test_depolarize_with_p_zero_keeps_state():
    rho = rho_from_ket(ket0())
    out = depolarize_rho(rho, 0.0)
    assert np.allclose(out, rho)


def test_depolarize_with_p_one_gives_maximally_mixed_state():
    rho = rho_from_ket(ket0())
    out = depolarize_rho(rho, 1.0)
    expected = 0.5 * np.eye(2, dtype=complex)
    assert np.allclose(out, expected)


def test_dephase_with_p_one_kills_off_diagonal_terms():
    rho = rho_from_ket(ket_plus())
    out = dephase_rho(rho, 1.0)
    expected = np.array([[0.5, 0.0], [0.0, 0.5]], dtype=complex)
    assert np.allclose(out, expected)


def test_dephase_preserves_diagonal_entries():
    rho = rho_from_ket(ket_plus())
    out = dephase_rho(rho, 0.7)
    assert np.allclose(np.diag(out), np.diag(rho))


def test_bit_flip_maps_zero_to_one_at_full_probability():
    rho = rho_from_ket(ket0())
    out = bit_flip_rho(rho, 1.0)
    assert np.allclose(out, rho_from_ket(ket1()))


def test_phase_flip_keeps_basis_state_zero_unchanged():
    rho = rho_from_ket(ket0())
    out = phase_flip_rho(rho, 1.0)
    assert np.allclose(out, rho)


def test_phase_flip_kills_plus_coherence_at_half_probability():
    rho = rho_from_ket(ket_plus())
    out = phase_flip_rho(rho, 0.5)
    expected = np.array([[0.5, 0.0], [0.0, 0.5]], dtype=complex)
    assert np.allclose(out, expected)


def test_amplitude_damping_maps_excited_state_to_ground_at_full_probability():
    rho = rho_from_ket(ket1())
    out = amplitude_damp_rho(rho, 1.0)
    assert np.allclose(out, rho_from_ket(ket0()))


def test_amplitude_damping_leaves_ground_state_unchanged():
    rho = rho_from_ket(ket0())
    out = amplitude_damp_rho(rho, 0.8)
    assert np.allclose(out, rho)


def test_new_channels_preserve_density_matrix_structure():
    rho = rho_from_ket(ket_plus())

    for out in (
        bit_flip_rho(rho, 0.25),
        phase_flip_rho(rho, 0.25),
        amplitude_damp_rho(rho, 0.25),
    ):
        assert is_density_matrix(out)


def test_depolarize_rejects_invalid_probability():
    rho = rho_from_ket(ket0())

    try:
        depolarize_rho(rho, 1.5)
        assert False, "Expected ValueError for invalid p"
    except ValueError:
        pass


def test_dephase_rejects_invalid_probability():
    rho = rho_from_ket(ket0())

    try:
        dephase_rho(rho, -0.1)
        assert False, "Expected ValueError for invalid p"
    except ValueError:
        pass


def test_new_channels_reject_invalid_probability():
    rho = rho_from_ket(ket0())

    for fn in (bit_flip_rho, phase_flip_rho, amplitude_damp_rho):
        try:
            fn(rho, 1.5)
            assert False, "Expected ValueError for invalid p"
        except ValueError:
            pass
