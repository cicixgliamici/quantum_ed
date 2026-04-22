import numpy as np

from quantum_ed.linalg import dagger
from quantum_ed.states import bell_phi_plus, basis_00, basis_01, basis_10, basis_11


def test_bell_state_has_expected_vector() -> None:
    bell = bell_phi_plus()
    expected = (1 / np.sqrt(2)) * np.array([[1], [0], [0], [1]], dtype=complex)
    assert np.allclose(bell, expected)


def test_bell_state_is_normalized() -> None:
    bell = bell_phi_plus()
    norm = (dagger(bell) @ bell).item()
    assert np.isclose(norm, 1.0)


def test_bell_state_measurement_probabilities() -> None:
    bell = bell_phi_plus()
    probs = np.abs(bell.flatten()) ** 2

    assert np.isclose(probs[0], 0.5)
    assert np.isclose(probs[1], 0.0)
    assert np.isclose(probs[2], 0.0)
    assert np.isclose(probs[3], 0.5)


def test_basis_states_are_orthonormal() -> None:
    basis = [basis_00(), basis_01(), basis_10(), basis_11()]

    for i, left in enumerate(basis):
        for j, right in enumerate(basis):
            overlap = (dagger(left) @ right).item()
            expected = 1.0 if i == j else 0.0
            assert np.isclose(overlap, expected)
