"""Exercise public API boundaries that previously allowed misleading results."""

import numpy as np
import pytest

from quantum_ed.channels import (
    amplitude_damp_rho, bit_flip_rho, dephase_rho, depolarize_rho,
    is_density_matrix, phase_flip_rho,
)
from quantum_ed.density import (
    fidelity_pure, partial_trace_two_qubits, rho_from_ket, trace_distance,
)
from quantum_ed.gates import H, apply, rx, ry, rz
from quantum_ed.measurement import measure_comp_basis, probs_comp_basis
from quantum_ed.states import basis_00, bloch_vector, ket0, normalize, state_from_bloch


CHANNELS = [amplitude_damp_rho, bit_flip_rho, dephase_rho, depolarize_rho, phase_flip_rho]
SINGLE_QUBIT_FUNCTIONS = [bloch_vector, probs_comp_basis, measure_comp_basis]
INVALID_DENSITIES = [
    np.eye(2),  # Trace two.
    np.diag([1.1, -0.1]),  # Trace one alone does not imply a physical state.
    np.array([[0.5, 0.2], [0.0, 0.5]]),  # Non-Hermitian.
    np.array([[np.nan, 0.0], [0.0, 1.0]]),
    np.array([[1.0, np.inf], [0.0, 0.0]]),
    np.ones((2, 1)),
    np.eye(4) / 4,
]


@pytest.mark.parametrize("function", SINGLE_QUBIT_FUNCTIONS)
def test_single_qubit_operations_reject_registers(function):
    # In particular, |00> must not be mistaken for a single-qubit |0>.
    with pytest.raises(ValueError, match="shape"):
        function(basis_00())


@pytest.mark.parametrize("ket", [np.ones(2), np.ones((1, 2)), np.ones((3, 1)), np.empty((0, 1))])
def test_normalize_rejects_unsupported_shapes(ket):
    with pytest.raises(ValueError, match="column vector"):
        normalize(ket)


@pytest.mark.parametrize("value", [np.nan, np.inf, -np.inf])
@pytest.mark.parametrize("function", [normalize, bloch_vector, probs_comp_basis, measure_comp_basis, rho_from_ket])
def test_state_operations_reject_nonfinite_amplitudes(function, value):
    with pytest.raises(ValueError, match="finite"):
        function(np.array([[value], [1.0]]))


@pytest.mark.parametrize("function", [normalize, *SINGLE_QUBIT_FUNCTIONS])
def test_state_operations_reject_zero_vectors(function):
    with pytest.raises(ValueError, match="near-zero"):
        function(np.zeros((2, 1)))


@pytest.mark.parametrize("scale", [1e308, 1e-300])
def test_normalize_handles_extreme_finite_scales(scale):
    # Complex components also exercise overflow-safe magnitude calculation.
    ket = np.array([[scale * (1 + 1j)], [scale * (1 - 1j)]])
    with np.errstate(over="raise", invalid="raise", divide="raise"):
        result = normalize(ket, atol=0)
    assert np.allclose(result, np.array([[1 + 1j], [1 - 1j]]) / 2)


def test_normalize_accepts_minimum_signed_integer_amplitude():
    ket = np.array([[np.iinfo(np.int64).min], [0]], dtype=np.int64)
    assert np.allclose(normalize(ket), -ket0())


@pytest.mark.parametrize("atol", [-1.0, np.nan, np.inf, [0.0]])
def test_normalize_rejects_invalid_tolerances(atol):
    with pytest.raises(ValueError, match="atol"):
        normalize(ket0(), atol=atol)


def test_zero_tolerance_still_rejects_zero_norm():
    with pytest.raises(ValueError, match="near-zero"):
        normalize(np.zeros((2, 1)), atol=0)


def test_single_qubit_normalization_is_explicit_and_does_not_mutate_input():
    ket = np.array([[3.0], [4.0]])
    original = ket.copy()
    assert probs_comp_basis(ket) == pytest.approx((0.36, 0.64))
    assert np.linalg.norm(bloch_vector(ket)) == pytest.approx(1)
    measure_comp_basis(ket, rng=np.random.default_rng(1))
    assert np.array_equal(ket, original)


@pytest.mark.parametrize("channel", CHANNELS)
@pytest.mark.parametrize("rho", INVALID_DENSITIES)
def test_channels_reject_nonphysical_or_wrong_size_states(channel, rho):
    with pytest.raises(ValueError):
        channel(rho, 0.5)


@pytest.mark.parametrize("channel", CHANNELS)
@pytest.mark.parametrize("probability", [-0.1, 1.1, np.nan, np.inf, 0.5j, np.array([0.5])])
def test_channels_reject_invalid_probabilities(channel, probability):
    with pytest.raises(ValueError, match="p"):
        channel(rho_from_ket(ket0()), probability)


@pytest.mark.parametrize("rho", INVALID_DENSITIES)
def test_density_predicate_returns_false_for_invalid_states(rho):
    assert not is_density_matrix(rho)


def test_density_validation_uses_absolute_tolerance():
    assert is_density_matrix(np.diag([1 + 1e-12, -1e-12]))
    assert not is_density_matrix(np.diag([1.0, 1e-6]))


@pytest.mark.parametrize("channel", CHANNELS)
def test_channels_preserve_physical_mixed_states_without_mutating_input(channel):
    rho = np.array([[0.6, 0.1j], [-0.1j, 0.4]])
    original = rho.copy()
    for probability in [0.0, 0.4, 1.0]:
        assert is_density_matrix(channel(rho, probability))
    assert np.array_equal(rho, original)


def test_density_operations_require_normalized_kets():
    with pytest.raises(ValueError, match="normalized"):
        rho_from_ket(2 * ket0())
    with pytest.raises(ValueError, match="normalized"):
        fidelity_pure(2 * ket0(), rho_from_ket(ket0()))


def test_fidelity_keeps_flat_vector_support_but_rejects_matrix_inputs():
    assert fidelity_pure(ket0().ravel(), rho_from_ket(ket0())) == pytest.approx(1)
    with pytest.raises(ValueError, match="column vector"):
        fidelity_pure(np.eye(2) / np.sqrt(2), np.eye(4) / 4)


@pytest.mark.parametrize("rho", INVALID_DENSITIES[:-1])
def test_density_metrics_reject_invalid_states(rho):
    with pytest.raises(ValueError):
        fidelity_pure(ket0(), rho)
    with pytest.raises(ValueError):
        trace_distance(rho_from_ket(ket0()), rho)


def test_density_metrics_reject_dimension_mismatches():
    with pytest.raises(ValueError, match="shape"):
        fidelity_pure(ket0(), np.eye(4) / 4)
    with pytest.raises(ValueError, match="shape"):
        trace_distance(np.eye(2) / 2, np.eye(4) / 4)


def test_partial_trace_rejects_unnormalized_input_instead_of_repairing_it():
    with pytest.raises(ValueError, match="trace one"):
        partial_trace_two_qubits(np.eye(4), keep=0)


@pytest.mark.parametrize("keep", [0, 1])
def test_partial_trace_preserves_a_mixed_state_trace(keep):
    result = partial_trace_two_qubits(np.diag([0.1, 0.2, 0.3, 0.4]), keep)
    expected = [0.3, 0.7] if keep == 0 else [0.4, 0.6]
    assert np.allclose(result, np.diag(expected))
    assert np.trace(result) == pytest.approx(1)


@pytest.mark.parametrize("operator", [np.ones((2, 1)), np.eye(4), np.full((2, 2), np.nan)])
def test_apply_rejects_incompatible_or_nonfinite_operators(operator):
    with pytest.raises(ValueError):
        apply(operator, ket0())


def test_apply_does_not_normalize_or_require_unitarity():
    # Observables/projectors remain usable as ordinary linear operators.
    assert np.allclose(apply(2 * H, ket0()), 2 * H @ ket0())


@pytest.mark.parametrize("angle", [np.nan, np.inf, 1j, [0.5]])
@pytest.mark.parametrize("rotation", [rx, ry, rz])
def test_rotations_reject_invalid_angles(rotation, angle):
    with pytest.raises(ValueError, match="theta"):
        rotation(angle)


@pytest.mark.parametrize("angles", [(np.nan, 0), (0, np.inf), ([0], 0), (0, 1j)])
def test_bloch_state_rejects_invalid_angles(angles):
    with pytest.raises(ValueError):
        state_from_bloch(*angles)
