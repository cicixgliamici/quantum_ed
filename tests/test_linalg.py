import numpy as np

from quantum_ed.states import ket0
from quantum_ed.gates import H
from quantum_ed.linalg import dagger, is_unitary, projector, trace, kron


def test_dagger_of_column_vector():
    v = np.array([[1 + 2j], [3 - 1j]], dtype=complex)
    out = dagger(v)
    expected = np.array([[1 - 2j, 3 + 1j]], dtype=complex)
    assert np.allclose(out, expected)


def test_is_unitary_accepts_hadamard():
    assert is_unitary(H)


def test_is_unitary_rejects_non_unitary_matrix():
    a = np.array([[1.0, 1.0], [0.0, 1.0]], dtype=complex)
    assert not is_unitary(a)


def test_projector_of_ket0():
    out = projector(ket0())
    expected = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    assert np.allclose(out, expected)


def test_trace_of_identity():
    a = np.eye(2, dtype=complex)
    assert np.isclose(trace(a), 2.0)


def test_kron_of_basis_vectors():
    a = np.array([[1.0], [0.0]], dtype=complex)
    b = np.array([[0.0], [1.0]], dtype=complex)
    out = kron(a, b)
    expected = np.array([[0.0], [1.0], [0.0], [0.0]], dtype=complex)
    assert np.allclose(out, expected)
