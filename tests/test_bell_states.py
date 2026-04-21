import numpy as np


def ket0() -> np.ndarray:
    return np.array([1, 0], dtype=complex)


def ket1() -> np.ndarray:
    return np.array([0, 1], dtype=complex)


def hadamard() -> np.ndarray:
    return (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)


def identity() -> np.ndarray:
    return np.eye(2, dtype=complex)


def cnot() -> np.ndarray:
    return np.array(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0],
        ],
        dtype=complex,
    )


def kron(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.kron(a, b)


def bell_phi_plus() -> np.ndarray:
    psi0 = kron(ket0(), ket0())
    psi1 = kron(hadamard(), identity()) @ psi0
    return cnot() @ psi1


def test_bell_state_has_expected_vector() -> None:
    bell = bell_phi_plus()
    expected = (1 / np.sqrt(2)) * np.array([1, 0, 0, 1], dtype=complex)
    assert np.allclose(bell, expected)


def test_bell_state_is_normalized() -> None:
    bell = bell_phi_plus()
    norm = np.vdot(bell, bell)
    assert np.isclose(norm, 1.0)


def test_bell_state_measurement_probabilities() -> None:
    bell = bell_phi_plus()
    probs = np.abs(bell) ** 2

    assert np.isclose(probs[0], 0.5)
    assert np.isclose(probs[1], 0.0)
    assert np.isclose(probs[2], 0.0)
    assert np.isclose(probs[3], 0.5)


def test_basis_states_are_orthonormal() -> None:
    zero = ket0()
    one = ket1()

    assert np.isclose(np.vdot(zero, zero), 1.0)
    assert np.isclose(np.vdot(one, one), 1.0)
    assert np.isclose(np.vdot(zero, one), 0.0)
