"""Execute reviewed examples and check the scientific distinctions they teach."""

import importlib.util
from pathlib import Path
import re

import numpy as np
import pytest

from quantum_ed.density import fidelity_pure, rho_from_ket, trace_distance
from quantum_ed.gates import H, S, Y, Z, ry
from quantum_ed.states import ket0, normalize

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
REVIEWED_PAGES = [
    "docs/04-entanglement/quantum-teleportation.md",
    "docs/06-density-matrices/README.md",
    "docs/07-noise-and-channels/README.md",
    "docs/07-noise-and-channels/FIDELITY.md",
    "docs/07-noise-and-channels/ideal-vs-noisy.md",
    "docs/08-hardware/README.md",
    "docs/10-quantum-algorithms/variational-quantum-eigensolver.md",
]


def documentation_examples():
    """Take executable examples from the actual pages, not copied test versions."""
    examples = []
    for document in REVIEWED_PAGES:
        text = (REPOSITORY_ROOT / document).read_text(encoding="utf-8")
        for index, source in enumerate(re.findall(r"```python\s*\n(.*?)```", text, re.DOTALL)):
            examples.append(pytest.param(document, index, source, id=f"{document}:{index}"))
    return examples


@pytest.mark.parametrize("document,index,source", documentation_examples())
def test_reviewed_python_example_runs(document, index, source):
    if "import pennylane" in source and importlib.util.find_spec("pennylane") is None:
        pytest.skip("This documented example requires the optional PennyLane dependency")
    exec(compile(source, f"{document}:python-{index}", "exec"), {"__name__": "__main__"})


def test_one_pure_state_does_not_imply_the_pure_pair_trace_distance_identity():
    pure = rho_from_ket(ket0())
    mixed = np.eye(2) / 2
    fidelity = fidelity_pure(ket0(), mixed)
    distance = trace_distance(pure, mixed)
    assert fidelity == pytest.approx(0.5)
    assert distance == pytest.approx(0.5)
    assert distance < np.sqrt(1 - fidelity)


def test_y_basis_measurement_uses_s_adjoint_before_hadamard():
    change_basis = H @ S.conj().T
    assert np.allclose(change_basis.conj().T @ Z @ change_basis, Y, atol=1e-12, rtol=0)
    plus_i = normalize(np.array([[1], [1j]]))
    measured_state = change_basis @ plus_i
    assert np.abs(measured_state.ravel()) ** 2 == pytest.approx([1, 0], abs=1e-12, rel=0)


def controlled_not_matrix(qubit_count: int, control: int, target: int) -> np.ndarray:
    """Build the logical permutation independently of any routing construction."""
    matrix = np.zeros((2**qubit_count, 2**qubit_count))
    for source in range(2**qubit_count):
        control_is_one = source & (1 << (qubit_count - control - 1))
        destination = source ^ (1 << (qubit_count - target - 1)) if control_is_one else source
        matrix[destination, source] = 1
    return matrix


@pytest.mark.parametrize("distance,expected_count", [(1, 1), (2, 7), (3, 13)])
def test_layout_restoring_swap_route_matches_the_full_logical_unitary(distance, expected_count):
    swaps = [(wire, wire + 1) for wire in range(distance - 1)]
    operations = []
    for first, second in swaps:
        operations.extend([(first, second), (second, first), (first, second)])
    operations.append((distance - 1, distance))
    for first, second in reversed(swaps):
        operations.extend([(first, second), (second, first), (first, second)])
    actual = np.eye(2 ** (distance + 1))
    for control, target in operations:
        assert abs(control - target) == 1
        actual = controlled_not_matrix(distance + 1, control, target) @ actual
    assert len(operations) == expected_count
    assert np.array_equal(actual, controlled_not_matrix(distance + 1, 0, distance))


@pytest.mark.parametrize("phase", [0.125, 0.17, 0.37, 0.499, 0.99])
def test_qpe_distribution_and_nearest_phase_bound(phase):
    dimension = 8
    labels = np.arange(dimension)
    # Sum over the numerical k register, independently of gate decompositions.
    amplitudes = np.exp(2j * np.pi * labels[:, None] * (phase - labels[None, :] / dimension)).mean(axis=0)
    probabilities = np.abs(amplitudes) ** 2
    assert probabilities.sum() == pytest.approx(1, abs=1e-12, rel=0)
    nearest = int(np.floor(dimension * phase + 0.5)) % dimension
    assert probabilities[nearest] >= 4 / np.pi**2 - 1e-12
    if phase == 0.125:
        assert probabilities == pytest.approx([0, 1, 0, 0, 0, 0, 0, 0], abs=1e-12, rel=0)


def test_shifting_a_shared_parameter_is_not_the_single_occurrence_rule():
    def energy(angle):
        state = ry(angle) @ ry(angle) @ ket0()
        return float((state.conj().T @ Z @ state).item().real)

    angle = 0.37
    incorrect_shared_shift = (energy(angle + np.pi / 2) - energy(angle - np.pi / 2)) / 2
    actual_derivative = -2 * np.sin(2 * angle)
    assert incorrect_shared_shift == pytest.approx(0, abs=1e-12)
    assert not np.isclose(incorrect_shared_shift, actual_derivative)
