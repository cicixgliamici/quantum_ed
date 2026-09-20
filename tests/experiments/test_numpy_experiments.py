"""Verify the mathematical outcomes of NumPy experiment implementations."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import numpy as np
import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def load_experiment(experiment: str, filename: str) -> ModuleType:
    """Load one standalone NumPy experiment by concept name."""
    path = REPOSITORY_ROOT / "experiments" / experiment / "numpy" / filename
    spec = importlib.util.spec_from_file_location(f"numpy_{experiment}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load experiment from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BELL = load_experiment("bell-state", "bell_state.py")
DENSE = load_experiment("superdense-coding", "superdense_coding.py")
DEUTSCH_JOZSA = load_experiment("deutsch-jozsa", "deutsch_jozsa.py")
BERNSTEIN_VAZIRANI = load_experiment("bernstein-vazirani", "bernstein_vazirani.py")
TELEPORTATION = load_experiment("quantum-teleportation", "quantum_teleportation.py")
GROVER = load_experiment("grover-search", "grover_search.py")
QFT = load_experiment("quantum-fourier-transform", "quantum_fourier_transform.py")
QPE = load_experiment("quantum-phase-estimation", "quantum_phase_estimation.py")
VQE = load_experiment("variational-quantum-eigensolver", "vqe.py")


def test_bell_state_has_only_correlated_outcomes() -> None:
    probabilities = BELL.measurement_probabilities()

    assert probabilities == pytest.approx({"00": 0.5, "01": 0.0, "10": 0.0, "11": 0.5})


@pytest.mark.parametrize("message", ["00", "01", "10", "11"])
def test_superdense_coding_decodes_every_message(message: str) -> None:
    assert DENSE.decode_message(message) == message


def test_deutsch_jozsa_classifies_balanced_oracle() -> None:
    assert DEUTSCH_JOZSA.classify_function() == "balanced"


@pytest.mark.parametrize("secret", ["0", "1", "001", "101", "111"])
def test_bernstein_vazirani_recovers_secret(secret: str) -> None:
    assert BERNSTEIN_VAZIRANI.recover_secret(secret) == secret


def test_teleportation_recovers_one_on_target() -> None:
    probabilities = TELEPORTATION.target_probabilities()

    assert probabilities == pytest.approx({"0": 0.0, "1": 1.0})
    assert np.isclose(np.linalg.norm(TELEPORTATION.teleported_state()), 1.0)


def test_grover_amplifies_marked_state_exactly() -> None:
    assert GROVER.final_probabilities() == pytest.approx([0.0, 0.0, 0.0, 1.0])


def test_qft_is_unitary_and_has_uniform_output_magnitudes() -> None:
    transform = QFT.qft_matrix(3)
    probabilities = np.abs(QFT.transformed_state()) ** 2

    assert np.allclose(transform.conj().T @ transform, np.eye(8))
    assert np.allclose(probabilities, np.full(8, 1.0 / 8.0))


def test_numpy_vqe_reaches_known_ground_energy() -> None:
    theta, energy = VQE.optimize()

    assert theta == pytest.approx(np.pi)
    assert energy == pytest.approx(-1.0)


def test_qpe_estimates_t_gate_phase_exactly() -> None:
    probs = QPE.estimate_phase()
    assert probs["001"] == pytest.approx(1.0)
    for state, p in probs.items():
        if state != "001":
            assert p == pytest.approx(0.0, abs=1e-10)

