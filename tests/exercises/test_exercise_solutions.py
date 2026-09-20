"""Verify the mathematical properties documented by the exercises."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import numpy as np
import pytest

from quantum_ed.density import partial_trace_two_qubits, rho_from_ket

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def load_solution(relative_path: str, module_name: str) -> ModuleType:
    """Load a reference solution from its concept-first exercise directory."""
    path = REPOSITORY_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load exercise solution from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


NORMALIZATION = load_solution("exercises/01-normalize-state/solution.py", "normalization_solution")
BELL = load_solution("exercises/02-prepare-bell-state/solution.py", "bell_solution")
NOISE = load_solution("exercises/03-validate-noise-channel/solution.py", "noise_solution")


def test_normalization_preserves_relative_amplitudes() -> None:
    state = NORMALIZATION.normalize_state(np.array([1.0, 1.0j]))

    assert state.shape == (2, 1)
    assert np.isclose(np.linalg.norm(state), 1.0)
    assert np.isclose(state[1, 0] / state[0, 0], 1.0j)


def test_normalization_rejects_zero() -> None:
    with pytest.raises(ValueError, match="zero vector"):
        NORMALIZATION.normalize_state(np.zeros(2))


def test_bell_state_has_expected_probabilities_and_marginals() -> None:
    state = BELL.prepare_bell_state()
    probabilities = np.abs(state.reshape(-1)) ** 2
    reduced_state = partial_trace_two_qubits(rho_from_ket(state), keep=0)

    assert np.allclose(probabilities, [0.5, 0.0, 0.0, 0.5])
    assert np.allclose(reduced_state, 0.5 * np.eye(2))


@pytest.mark.parametrize("probability", [0.0, 0.25, 0.5, 1.0])
def test_amplitude_damping_has_expected_populations(probability: float) -> None:
    state = NOISE.damp_excited_state(probability)

    assert np.allclose(np.diag(state), [probability, 1.0 - probability])
