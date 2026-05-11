import numpy as np

from quantum_ed.gates import CNOT, CZ, H, I, S, SWAP, T, X, Y, Z, apply, kron_n, rx, ry, rz
from quantum_ed.linalg import is_unitary
from quantum_ed.states import basis_00, basis_01, basis_10, basis_11, bell_phi_plus, ket0, ket1


def test_basic_gates_are_unitary() -> None:
    for gate in [I, X, Y, Z, H, S, T, CNOT, CZ, SWAP, rx(0.3), ry(0.3), rz(0.3)]:
        assert is_unitary(gate)


def test_pauli_gates_square_to_identity() -> None:
    for gate in [X, Y, Z]:
        assert np.allclose(gate @ gate, I)


def test_hadamard_square_is_identity() -> None:
    assert np.allclose(H @ H, I)


def test_phase_gate_relations() -> None:
    assert np.allclose(S @ S, Z)
    assert np.allclose(T @ T, S)


def test_x_flips_computational_basis_states() -> None:
    assert np.allclose(apply(X, ket0()), ket1())
    assert np.allclose(apply(X, ket1()), ket0())


def test_z_flips_phase_of_one_state() -> None:
    assert np.allclose(apply(Z, ket0()), ket0())
    assert np.allclose(apply(Z, ket1()), -ket1())


def test_hadamard_creates_plus_state() -> None:
    expected = (1 / np.sqrt(2)) * np.array([[1], [1]], dtype=complex)
    assert np.allclose(apply(H, ket0()), expected)


def test_cnot_truth_table() -> None:
    assert np.allclose(apply(CNOT, basis_00()), basis_00())
    assert np.allclose(apply(CNOT, basis_01()), basis_01())
    assert np.allclose(apply(CNOT, basis_10()), basis_11())
    assert np.allclose(apply(CNOT, basis_11()), basis_10())


def test_cz_flips_only_11_phase() -> None:
    assert np.allclose(apply(CZ, basis_00()), basis_00())
    assert np.allclose(apply(CZ, basis_01()), basis_01())
    assert np.allclose(apply(CZ, basis_10()), basis_10())
    assert np.allclose(apply(CZ, basis_11()), -basis_11())


def test_swap_exchanges_two_qubits() -> None:
    assert np.allclose(apply(SWAP, basis_00()), basis_00())
    assert np.allclose(apply(SWAP, basis_01()), basis_10())
    assert np.allclose(apply(SWAP, basis_10()), basis_01())
    assert np.allclose(apply(SWAP, basis_11()), basis_11())


def test_bell_state_from_h_and_cnot() -> None:
    state = basis_00()
    state = apply(kron_n(H, I), state)
    state = apply(CNOT, state)

    assert np.allclose(state, bell_phi_plus())


def test_rotations_at_zero_are_identity() -> None:
    assert np.allclose(rx(0.0), I)
    assert np.allclose(ry(0.0), I)
    assert np.allclose(rz(0.0), I)
