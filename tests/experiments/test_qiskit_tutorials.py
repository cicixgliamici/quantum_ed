"""Keep the relocated tutorial explanations aligned with Qiskit's ket order."""

import importlib.util
from pathlib import Path

import numpy as np
import pytest

pytest.importorskip("qiskit")
from qiskit.quantum_info import Statevector

EXAMPLES_ROOT = Path(__file__).resolve().parents[2] / "examples/qiskit"


def load_tutorial(filename):
    """Load numbered lesson filenames without turning tutorials into packages."""
    specification = importlib.util.spec_from_file_location("qiskit_tutorial", EXAMPLES_ROOT / filename)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


@pytest.mark.parametrize("function,expected", [
    ("example_cnot_control_one", [0, 0, 0, 1]),
    ("example_cnot_superposition", np.array([1, 0, 0, 1]) / np.sqrt(2)),
    ("example_swap", [0, 0, 1, 0]),
])
def test_multiqubit_tutorial_states_match_displayed_kets(monkeypatch, function, expected):
    tutorial = load_tutorial("03_multi_qubit_gates.py")
    observed = []
    monkeypatch.setattr(tutorial, "show_state", lambda name, circuit: observed.append(
        Statevector.from_instruction(circuit).data
    ))
    getattr(tutorial, function)()
    np.testing.assert_allclose(observed[0], expected, atol=1e-12)


def test_measurement_example_uses_an_asymmetric_bit_pattern(monkeypatch, capsys):
    tutorial = load_tutorial("04_measurement.py")
    observed = []
    # Inspect the prepared state directly; sampling adds no evidence about ordering.
    monkeypatch.setattr(tutorial, "run_and_show", lambda name, circuit, register: observed.append(
        Statevector.from_instruction(circuit.remove_final_measurements(inplace=False)).probabilities_dict()
    ))
    tutorial.example_bit_ordering()
    assert observed == [{"001": 1.0}]
    assert "'001'" in capsys.readouterr().out
