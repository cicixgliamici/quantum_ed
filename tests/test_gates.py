import numpy as np

from quantum_ed.states import ket0, ket1, normalize
from quantum_ed.gates import X, H, CNOT, kron_n, apply
from quantum_ed.linalg import is_unitary


def test_hadamard_is_unitary():
    assert is_unitary(H)


def test_x_maps_ket0_to_ket1():
    out = apply(X, ket0())
    assert np.allclose(out, ket1())


def test_h_maps_ket0_to_plus_state():
    out = apply(H, ket0())
    expected = normalize(np.array([[1.0], [1.0]], dtype=complex))
    assert np.allclose(out, expected)


def test_kron_n_two_basis_states():
    out = kron_n(ket0(), ket1())
    expected = np.array([[0.0], [1.0], [0.0], [0.0]], dtype=complex)
    assert np.allclose(out, expected)


def test_cnot_on_00_leaves_state_unchanged():
    psi = kron_n(ket0(), ket0())
    out = apply(CNOT, psi)
    assert np.allclose(out, psi)


def test_cnot_on_10_flips_second_qubit():
    psi = kron_n(ket1(), ket0())
    out = apply(CNOT, psi)
    expected = kron_n(ket1(), ket1())
    assert np.allclose(out, expected)
