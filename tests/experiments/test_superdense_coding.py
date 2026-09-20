"""Verify every logical message supported by the Qiskit experiment."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

pytest.importorskip("qiskit")

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SOURCE = REPOSITORY_ROOT / "experiments/superdense-coding/qiskit/superdense_coding.py"


def load_experiment() -> ModuleType:
    """Load the standalone experiment without making it an installed package."""
    spec = importlib.util.spec_from_file_location("superdense_coding", SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load experiment from {SOURCE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


EXPERIMENT = load_experiment()


@pytest.mark.parametrize("message", ["00", "01", "10", "11"])
def test_every_message_is_decoded_deterministically(message: str) -> None:
    decoded, counts = EXPERIMENT.decode_message(message, shots=32)

    assert decoded == message
    assert counts == {message: 32}


@pytest.mark.parametrize("message", ["", "1", "101", "2a"])
def test_invalid_messages_are_rejected(message: str) -> None:
    with pytest.raises(ValueError, match="exactly two binary digits"):
        EXPERIMENT.build_circuit(message)
