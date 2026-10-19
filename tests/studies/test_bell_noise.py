"""Check channel conventions, analytical predictions, and entanglement conclusions."""

import numpy as np
import pytest

from quantum_ed.channels import amplitude_damp_rho, dephase_rho, depolarize_rho
from quantum_ed.density import rho_from_ket
from quantum_ed.states import bell_phi_plus, normalize
from studies.bell_noise.metrics import measure_state, negativity, partial_transpose
from studies.bell_noise.numpy_model import CHANNELS, kraus_operators, noisy_bell_state
from studies.bell_noise.run_study import build_summary, collect_results
from studies.bell_noise.theory import DEPOLARIZING_THRESHOLD, predicted_metrics, predicted_state

PROBABILITIES = [0.0, 0.17, DEPOLARIZING_THRESHOLD, 0.5, 0.83, 1.0]


@pytest.mark.parametrize("channel", CHANNELS)
@pytest.mark.parametrize("probability", PROBABILITIES)
def test_local_channels_are_trace_preserving(channel, probability):
    operators = kraus_operators(channel, probability)
    completeness = sum(operator.conj().T @ operator for operator in operators)
    assert np.allclose(completeness, np.eye(2), atol=1e-12, rtol=0)


@pytest.mark.parametrize("channel,function", [
    ("dephasing", dephase_rho), ("depolarizing", depolarize_rho),
    ("amplitude_damping", amplitude_damp_rho),
])
@pytest.mark.parametrize("probability", [0.0, 0.23, 0.75, 1.0])
def test_kraus_conventions_match_core_channels_on_a_complex_input(channel, function, probability):
    state = rho_from_ket(normalize(np.array([[1.0], [0.3 + 0.7j]])))
    operators = kraus_operators(channel, probability)
    actual = sum(operator @ state @ operator.conj().T for operator in operators)
    assert np.allclose(actual, function(state, probability), atol=1e-12, rtol=0)


@pytest.mark.parametrize("channel", CHANNELS)
@pytest.mark.parametrize("probability", PROBABILITIES)
def test_numpy_states_and_metrics_match_independent_theory(channel, probability):
    state = noisy_bell_state(channel, probability)
    assert np.allclose(state, predicted_state(channel, probability), atol=1e-12, rtol=0)
    assert measure_state(state) == pytest.approx(predicted_metrics(channel, probability), abs=1e-12)


@pytest.mark.parametrize("channel", CHANNELS)
@pytest.mark.parametrize("probability", PROBABILITIES)
def test_pennylane_full_matrices_match_numpy_after_parameter_conversion(channel, probability):
    pytest.importorskip("pennylane")
    from studies.bell_noise.pennylane_model import noisy_bell_state as sdk_state

    actual = np.asarray(sdk_state(channel, probability))
    assert np.allclose(actual, noisy_bell_state(channel, probability), atol=1e-10, rtol=0)
    assert measure_state(actual) == pytest.approx(predicted_metrics(channel, probability), abs=1e-10)


def test_partial_transpose_preserves_alice_and_transposes_bob():
    alice = rho_from_ket(normalize(np.array([[1], [0.2j]])))
    bob = rho_from_ket(normalize(np.array([[1], [0.6 + 0.4j]])))
    product = np.kron(alice, bob)
    assert np.allclose(partial_transpose(product), np.kron(alice, bob.T))
    assert negativity(product) == pytest.approx(0, abs=1e-12)


def test_bell_partial_transpose_has_one_negative_eigenvalue():
    spectrum = np.linalg.eigvalsh(partial_transpose(rho_from_ket(bell_phi_plus())))
    assert spectrum == pytest.approx([-0.5, 0.5, 0.5, 0.5])


def test_nonmaximal_entanglement_has_the_expected_negativity():
    angle = 0.37
    state = np.array([[np.cos(angle)], [0], [0], [np.sin(angle)]])
    assert negativity(rho_from_ket(state)) == pytest.approx(np.cos(angle) * np.sin(angle))


def test_dephasing_keeps_z_probabilities_while_destroying_entanglement():
    ideal = noisy_bell_state("dephasing", 0)
    dephased = noisy_bell_state("dephasing", 1)
    assert np.diag(dephased) == pytest.approx(np.diag(ideal))
    assert negativity(ideal) == pytest.approx(0.5)
    assert negativity(dephased) == pytest.approx(0, abs=1e-12)
    assert measure_state(dephased)["xx"] == pytest.approx(0)
    assert measure_state(dephased)["zz"] == pytest.approx(1)


def test_depolarizing_separability_threshold_is_not_a_grid_artifact():
    below = negativity(noisy_bell_state("depolarizing", DEPOLARIZING_THRESHOLD - 1e-6))
    at = negativity(noisy_bell_state("depolarizing", DEPOLARIZING_THRESHOLD))
    above = negativity(noisy_bell_state("depolarizing", DEPOLARIZING_THRESHOLD + 1e-6))
    assert below > 1e-7
    assert at == pytest.approx(0, abs=1e-12)
    assert above == pytest.approx(0, abs=1e-12)


def test_amplitude_damping_can_restore_purity_without_entanglement():
    midpoint = measure_state(noisy_bell_state("amplitude_damping", 0.5))
    endpoint = measure_state(noisy_bell_state("amplitude_damping", 1))
    assert midpoint["purity"] == pytest.approx(0.5625)
    assert endpoint["purity"] == pytest.approx(1)
    assert endpoint["negativity"] == pytest.approx(0)
    assert endpoint["fidelity"] == pytest.approx(0.5)


def test_numpy_only_summary_does_not_claim_cross_framework_validation():
    rows = collect_results(points=5, include_pennylane=False)
    summary = build_summary(rows, points=5)
    assert len(rows) == 15
    assert summary["models"] == ["numpy"]
    assert summary["framework_matrix_max_abs_error"] is None
    assert summary["depolarizing_transition"]["grid_last_entangled"] == 0.25
    assert summary["depolarizing_transition"]["grid_first_numerically_separable"] == 0.5


@pytest.mark.parametrize("probability", [-0.1, 1.1, np.nan, np.inf, 1j])
def test_study_rejects_invalid_noise_strengths(probability):
    with pytest.raises(ValueError):
        noisy_bell_state("dephasing", probability)


def test_study_rejects_unknown_channels():
    with pytest.raises(ValueError, match="channel"):
        noisy_bell_state("unknown", 0.5)
