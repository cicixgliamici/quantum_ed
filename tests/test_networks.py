"""Verify swapping branches, physical states, and the missing-record ensemble."""

import numpy as np
import pytest

from quantum_ed.density import partial_trace_two_qubits, rho_from_ket
from quantum_ed.networks import (
    OUTCOMES, bell_measurement_state, conditional_endpoint_state, endpoint_density, swapped_state,
)
from quantum_ed.states import bell_phi_plus


@pytest.mark.parametrize("outcome", OUTCOMES)
def test_every_outcome_produces_phi_plus_after_classical_corrections(outcome):
    probability, state = conditional_endpoint_state(outcome)
    assert probability == pytest.approx(0.25)
    assert state.shape == (4, 1)
    np.testing.assert_allclose(rho_from_ket(state), rho_from_ket(bell_phi_plus()), atol=1e-12)


@pytest.mark.parametrize("outcome,target", [
    ("00", [1, 0, 0, 1]), ("01", [0, 1, 1, 0]),
    ("10", [1, 0, 0, -1]), ("11", [0, 1, -1, 0]),
])
def test_uncorrected_branches_cover_the_four_distinct_bell_states(outcome, target):
    _, state = conditional_endpoint_state(outcome, corrected=False)
    expected = np.array(target, dtype=complex).reshape(4, 1) / np.sqrt(2)
    np.testing.assert_allclose(rho_from_ket(state), rho_from_ket(expected), atol=1e-12)


def test_missing_record_has_no_usable_endpoint_entanglement():
    density = endpoint_density()
    np.testing.assert_allclose(density, np.eye(4) / 4, atol=1e-12)
    assert np.trace(density) == pytest.approx(1)
    assert np.min(np.linalg.eigvalsh(density)) >= -1e-12
    # Feed-forward changes joint correlations; neither local marginal carries a message.
    for corrected in (False, True):
        for endpoint in (0, 1):
            marginal = partial_trace_two_qubits(endpoint_density(corrected=corrected), keep=endpoint)
            np.testing.assert_allclose(marginal, np.eye(2) / 2, atol=1e-12)


def test_deferred_measurement_and_measured_ensembles_agree():
    for corrected in (False, True):
        state = swapped_state(corrected=corrected).reshape(2, 2, 2, 2)
        # Group endpoints against Bob's two wires to trace out his outcome register.
        endpoint_by_bob = state.transpose(0, 3, 1, 2).reshape(4, 4)
        reduced = endpoint_by_bob @ endpoint_by_bob.conj().T
        np.testing.assert_allclose(reduced, endpoint_density(corrected=corrected), atol=1e-12)
    np.testing.assert_allclose(swapped_state(corrected=False), bell_measurement_state(), atol=1e-12)


@pytest.mark.parametrize("outcome", ["", "0", "000", "02", " 00", 0, None, [0, 0]])
def test_outcome_labels_must_name_exactly_two_bob_bits(outcome):
    with pytest.raises(ValueError, match="outcome"):
        conditional_endpoint_state(outcome)


@pytest.mark.parametrize("corrected", [None, "yes", 1])
def test_correction_selection_is_explicit(corrected):
    with pytest.raises(ValueError, match="boolean"):
        conditional_endpoint_state("00", corrected=corrected)
