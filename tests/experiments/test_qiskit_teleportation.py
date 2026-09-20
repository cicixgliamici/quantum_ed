"""Verify the optional Qiskit teleportation experiment."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

pytest.importorskip("qiskit")

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SOURCE = REPOSITORY_ROOT / "experiments/quantum-teleportation/qiskit/quantum_teleportation.py"


def test_target_is_one_for_every_shot() -> None:
    """Ensure Bob deterministically receives the prepared state |1>."""
    spec = importlib.util.spec_from_file_location("qiskit_teleportation", SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load experiment from {SOURCE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert module.sample_target(shots=32) == {"1": 32}
