import numpy as np

from quantum_ed.states import ket0, normalize
from quantum_ed.gates import H, apply
from quantum_ed.density import rho_from_ket
from quantum_ed.channels import is_density_matrix, depolarize_rho, dephase_rho


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
