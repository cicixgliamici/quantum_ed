"""Verify differentiable and noisy PennyLane workflows."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import numpy as np
import pytest

pytest.importorskip("pennylane")

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def load_module(relative_path: str, name: str) -> ModuleType:
    """Load a standalone PennyLane experiment or study."""
    path = REPOSITORY_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load PennyLane source from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GROVER = load_module("experiments/grover-search/pennylane/grover_search.py", "pl_grover")
QFT = load_module(
    "experiments/quantum-fourier-transform/pennylane/quantum_fourier_transform.py",
    "pl_qft",
)
QPE = load_module(
    "experiments/quantum-phase-estimation/pennylane/quantum_phase_estimation.py",
    "pl_qpe",
)
VQE = load_module("experiments/variational-quantum-eigensolver/pennylane/vqe.py", "pl_vqe")
NOISE = load_module("studies/ideal-vs-noisy/pennylane_model.py", "pl_noise")


def test_pennylane_grover_finds_marked_state() -> None:
    assert GROVER.probabilities() == pytest.approx([0.0, 0.0, 0.0, 1.0])


def test_pennylane_qft_has_uniform_probabilities() -> None:
    assert QFT.probabilities() == pytest.approx(np.full(8, 1.0 / 8.0))


def test_pennylane_qpe_estimates_phase() -> None:
    probs = QPE.probabilities()
    expected = np.zeros(8)
    expected[4] = 1.0
    assert probs == pytest.approx(expected)


def test_pennylane_vqe_converges_to_ground_energy() -> None:
    _, energy = VQE.optimize()

    assert energy < -0.999


@pytest.mark.parametrize("probability", [0.0, 0.1, 0.25, 0.5])
def test_pennylane_noise_matches_bit_flip_probability(probability: float) -> None:
    assert NOISE.probabilities(probability) == pytest.approx([1.0 - probability, probability])
