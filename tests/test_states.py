import numpy as np

from quantum_ed.states import ket0, ket1, normalize, bloch_vector, state_from_bloch


def test_ket0_is_correct_basis_vector():
    expected = np.array([[1.0], [0.0]], dtype=complex)
    assert np.allclose(ket0(), expected)


def test_ket1_is_correct_basis_vector():
    expected = np.array([[0.0], [1.0]], dtype=complex)
    assert np.allclose(ket1(), expected)


def test_normalize_returns_unit_vector():
    psi = np.array([[3.0], [4.0]], dtype=complex)
    out = normalize(psi)

    norm_sq = (np.conjugate(out).T @ out).item()
    assert np.isclose(norm_sq, 1.0)


def test_normalize_raises_on_zero_vector():
    psi = np.array([[0.0], [0.0]], dtype=complex)

    try:
        normalize(psi)
        assert False, "Expected ValueError for zero vector"
    except ValueError:
        pass


def test_bloch_vector_of_ket0():
    r = bloch_vector(ket0())
    expected = np.array([0.0, 0.0, 1.0], dtype=float)
    assert np.allclose(r, expected)


def test_bloch_vector_of_ket1():
    r = bloch_vector(ket1())
    expected = np.array([0.0, 0.0, -1.0], dtype=float)
    assert np.allclose(r, expected)


def test_state_from_bloch_north_pole_is_ket0_up_to_phase():
    psi = state_from_bloch(0.0, 0.0)
    expected = ket0()
    assert np.allclose(np.abs(psi), np.abs(expected))


def test_state_from_bloch_south_pole_is_ket1_up_to_phase():
    psi = state_from_bloch(np.pi, 0.0)
    expected = ket1()
    assert np.allclose(np.abs(psi), np.abs(expected))
