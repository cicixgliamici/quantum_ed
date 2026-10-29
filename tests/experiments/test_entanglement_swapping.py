"""Compare independent SDK preparations and reject invisible phase mistakes."""

import numpy as np
import pytest

from tools.experiment_checks import assert_swapped_state, load_module, qiskit_wire_state


@pytest.mark.parametrize("ecosystem", ["numpy", "qiskit", "pennylane"])
def test_independent_preparations_preserve_every_corrected_branch(ecosystem):
    if ecosystem != "numpy":
        pytest.importorskip(ecosystem)
    module = load_module(f"experiments/entanglement-swapping/{ecosystem}/entanglement_swapping.py")
    state = (qiskit_wire_state(module.build_circuit()) if ecosystem == "qiskit"
             else module.swapped_state())
    assert_swapped_state(state)


@pytest.mark.parametrize("ecosystem", ["qiskit", "pennylane"])
def test_uncorrected_sdk_state_leaves_endpoints_maximally_mixed(ecosystem):
    pytest.importorskip(ecosystem)
    module = load_module(f"experiments/entanglement-swapping/{ecosystem}/entanglement_swapping.py")
    state = (qiskit_wire_state(module.build_circuit(corrected=False)) if ecosystem == "qiskit"
             else module.swapped_state(corrected=False))
    amplitudes = np.asarray(state).reshape(2, 2, 2, 2).transpose(0, 3, 1, 2).reshape(4, 4)
    np.testing.assert_allclose(amplitudes @ amplitudes.conj().T, np.eye(4) / 4, atol=1e-12)


def test_phase_sensitive_check_rejects_omitted_phase_correction():
    from quantum_ed.networks import swapped_state

    state = swapped_state().reshape(2, 2, 2, 2)
    incorrect = state.copy()
    # Only Bob's phase-bit=1 branches acquire a wrong relative endpoint phase.
    incorrect[1, 1, :, 1] *= -1
    np.testing.assert_allclose(np.abs(state) ** 2, np.abs(incorrect) ** 2)
    with pytest.raises(AssertionError, match="global phase"):
        assert_swapped_state(incorrect)


def test_branch_check_rejects_dropping_three_measurement_outcomes():
    from quantum_ed.networks import swapped_state

    state = swapped_state().reshape(2, 2, 2, 2)
    postselected = np.zeros_like(state)
    postselected[:, 0, 0, :] = 2 * state[:, 0, 0, :]
    with pytest.raises(AssertionError, match="probability 1/4"):
        assert_swapped_state(postselected)
