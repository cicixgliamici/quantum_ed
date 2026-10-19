"""Verify scientific equivalence beyond computational-basis probabilities."""

import numpy as np
import pytest

from tools.experiment_checks import (
    SHOTS, assert_probabilities, assert_sampled_counts, assert_state_equivalent,
    assert_teleported_state, expected_qft, load_module, qiskit_wire_state,
    sample_circuit, teleportation_inputs,
)


def experiment_module(name: str, ecosystem: str, filename: str):
    """Optional SDKs are skipped only in jobs where they are not installed."""
    if ecosystem != "numpy":
        pytest.importorskip(ecosystem)
    return load_module(f"experiments/{name}/{ecosystem}/{filename}.py")


@pytest.mark.parametrize("ecosystem", ["numpy", "qiskit", "pennylane"])
@pytest.mark.parametrize("input_value", range(8))
def test_qft_matches_analytical_complex_amplitudes(ecosystem, input_value):
    module = experiment_module("quantum-fourier-transform", ecosystem, "quantum_fourier_transform")
    actual = (qiskit_wire_state(module.build_circuit(input_value)) if ecosystem == "qiskit"
              else module.transformed_state(input_value))
    assert_state_equivalent(actual, expected_qft(input_value))


@pytest.mark.parametrize("ecosystem", ["numpy", "qiskit", "pennylane"])
@pytest.mark.parametrize("theta,phi,message", teleportation_inputs())
def test_teleportation_preserves_bobs_full_state(ecosystem, theta, phi, message):
    module = experiment_module("quantum-teleportation", ecosystem, "quantum_teleportation")
    actual = (qiskit_wire_state(module.build_circuit(message)) if ecosystem == "qiskit"
              else module.teleported_state(message))
    assert_teleported_state(actual, message)


def test_state_comparison_accepts_global_phase_but_rejects_wrong_relative_phases():
    expected = expected_qft(1)
    assert_state_equivalent(np.exp(0.37j) * expected, expected)
    # Both incorrect states have exactly the same measurement probabilities.
    with pytest.raises(AssertionError, match="global phase"):
        assert_state_equivalent(expected_qft(4), expected)
    with pytest.raises(AssertionError, match="global phase"):
        assert_state_equivalent(expected.conj(), expected)


def test_teleportation_check_rejects_phase_loss_even_when_probabilities_match():
    message = np.array([1, 1j]) / np.sqrt(2)
    incorrect_bob = np.array([1, 1]) / np.sqrt(2)
    with pytest.raises(AssertionError, match="Bob"):
        assert_teleported_state(np.kron([1, 0, 0, 0], incorrect_bob), message)


def test_probability_comparison_rejects_extra_outcomes_and_bit_reversal():
    with pytest.raises(AssertionError, match="mismatch"):
        assert_probabilities({"100": 0.9, "001": 0.1}, {"100": 1})
    with pytest.raises(AssertionError, match="mismatch"):
        assert_probabilities({"001": 1}, {"100": 1})


def test_sample_comparison_distinguishes_fluctuation_bias_and_impossible_results():
    expected = {"00": 0.5, "11": 0.5}
    assert_sampled_counts({"00": SHOTS // 2 + 20, "11": SHOTS // 2 - 20}, expected)
    with pytest.raises(AssertionError, match="Sampling mismatch"):
        assert_sampled_counts({"00": SHOTS}, expected)
    with pytest.raises(AssertionError, match="impossible"):
        assert_sampled_counts({"00": SHOTS - 1, "01": 1}, expected)


@pytest.mark.parametrize("secret", ["001", "100", "011", "110"])
def test_bernstein_vazirani_preserves_asymmetric_secret_order(secret):
    module = experiment_module("bernstein-vazirani", "qiskit", "bernstein_vazirani")
    recovered, counts = module.recover_secret(secret, shots=32)
    assert recovered == secret
    assert counts == {secret[::-1]: 32}


def test_deutsch_jozsa_numpy_uses_first_tensor_factor_for_x_zero():
    module = experiment_module("deutsch-jozsa", "numpy", "deutsch_jozsa")
    assert module.final_probabilities() == pytest.approx([0, 0, 0, 0, 1, 0, 0, 0])


@pytest.mark.parametrize("message", ["00", "01", "10", "11"])
def test_superdense_coding_matches_all_messages_in_pennylane(message):
    module = experiment_module("superdense-coding", "pennylane", "superdense_coding")
    expected = np.zeros(4)
    expected[int(message, 2)] = 1
    assert module.probabilities(message) == pytest.approx(expected)


def test_sampler_groups_loose_classical_bits_without_changing_destinations():
    qiskit = pytest.importorskip("qiskit")
    # Scalar OpenQASM outputs import as loose bits; samplers need a register.
    circuit = qiskit.QuantumCircuit(3)
    circuit.add_bits([qiskit.circuit.Clbit()])
    circuit.x(2)
    circuit.measure(2, 0)
    assert sample_circuit(circuit, "quantum-teleportation") == {"1": SHOTS}
    assert not circuit.cregs
