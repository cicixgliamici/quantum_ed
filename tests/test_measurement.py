import numpy as np

from quantum_ed.states import ket0, ket1, normalize
from quantum_ed.gates import H, apply
from quantum_ed.measurement import probs_comp_basis, measure_comp_basis


def ket_plus():
    return normalize(apply(H, ket0()))


def test_probs_comp_basis_of_ket0():
    p0, p1 = probs_comp_basis(ket0())
    assert np.isclose(p0, 1.0)
    assert np.isclose(p1, 0.0)


def test_probs_comp_basis_of_ket1():
    p0, p1 = probs_comp_basis(ket1())
    assert np.isclose(p0, 0.0)
    assert np.isclose(p1, 1.0)


def test_probs_comp_basis_of_plus_state():
    p0, p1 = probs_comp_basis(ket_plus())
    assert np.isclose(p0, 0.5)
    assert np.isclose(p1, 0.5)


def test_measurement_of_ket0_is_deterministically_zero():
    rng = np.random.default_rng(123)
    outcome, post = measure_comp_basis(ket0(), rng=rng)

    assert outcome == 0
    assert np.allclose(post, ket0())


def test_measurement_of_ket1_is_deterministically_one():
    rng = np.random.default_rng(123)
    outcome, post = measure_comp_basis(ket1(), rng=rng)

    assert outcome == 1
    assert np.allclose(post, ket1())


def test_measurement_post_state_matches_outcome():
    rng = np.random.default_rng(0)
    outcome, post = measure_comp_basis(ket_plus(), rng=rng)

    if outcome == 0:
        assert np.allclose(post, ket0())
    else:
        assert np.allclose(post, ket1())
