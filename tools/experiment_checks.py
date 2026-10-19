"""Shared scientific checks, independent of optional quantum SDK imports."""

from __future__ import annotations

import importlib.util
import json
from math import log, sqrt
from pathlib import Path
from types import ModuleType

import numpy as np

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
ABSOLUTE_TOLERANCE = 1e-10
SHOTS = 4096
FAILURE_PROBABILITY = 1e-6

# Every label follows increasing output wire index, including QPE's 100.
# QPE's numerical phase label is its reverse, 001, because wire 0 has weight 1.
EXPECTED_PROBABILITIES = {
    "bell-state": {"00": 0.5, "11": 0.5},
    "superdense-coding": {"10": 1.0},
    "quantum-teleportation": {"1": 1.0},
    "deutsch-jozsa": {"100": 1.0},
    "bernstein-vazirani": {"101": 1.0},
    "grover-search": {"11": 1.0},
    "quantum-fourier-transform": {f"{index:03b}": 0.125 for index in range(8)},
    "quantum-phase-estimation": {"100": 1.0},
    "variational-quantum-eigensolver": {"1": 1.0},
}


def manifests() -> list[dict]:
    """Use the same declared entrypoints as repository structure validation."""
    paths = sorted((REPOSITORY_ROOT / "experiments").glob("*/experiment.json"))
    return [json.loads(path.read_text(encoding="utf-8")) for path in paths]


def load_module(relative_path: str) -> ModuleType:
    """Load an experiment without making example folders Python packages."""
    path = REPOSITORY_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise ValueError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def probabilities_dict(values: np.ndarray) -> dict[str, float]:
    """Label a probability array in its already-canonical tensor order."""
    values = np.asarray(values).ravel()
    width = (len(values) - 1).bit_length()
    return {f"{index:0{width}b}": float(value) for index, value in enumerate(values)}


def assert_probabilities(actual: dict[str, float], expected: dict[str, float]) -> None:
    """Compare full distributions, including unexpected nonzero outcomes."""
    values = np.array(list(actual.values()))
    if not np.all(np.isfinite(values)) or np.any(values < -ABSOLUTE_TOLERANCE):
        raise AssertionError("Probabilities must be finite and nonnegative")
    if not np.isclose(sum(actual.values()), 1, atol=ABSOLUTE_TOLERANCE, rtol=0):
        raise AssertionError("Probabilities must sum to one")
    for label in actual.keys() | expected.keys():
        if not np.isclose(actual.get(label, 0), expected.get(label, 0),
                          atol=ABSOLUTE_TOLERANCE, rtol=0):
            raise AssertionError(f"Probability mismatch for {label}: {actual.get(label, 0)} != {expected.get(label, 0)}")


def assert_sampled_counts(counts: dict[str, int], expected: dict[str, float]) -> None:
    """Use a simultaneous Hoeffding bound for finite-shot sampling.

    The union bound covers every expected outcome in this distribution.
    Impossible outcomes are rejected separately, without statistical slack.
    """
    if sum(counts.values()) != SHOTS or any(count < 0 for count in counts.values()):
        raise AssertionError(f"Expected exactly {SHOTS} samples")
    if any(count and expected.get(label, 0) == 0 for label, count in counts.items()):
        raise AssertionError(f"Observed an impossible outcome: {counts}")
    bound = sqrt(log(2 * len(expected) / FAILURE_PROBABILITY) / (2 * SHOTS))
    for label, probability in expected.items():
        if abs(counts.get(label, 0) / SHOTS - probability) > bound:
            raise AssertionError(f"Sampling mismatch for {label}; absolute bound={bound:.5f}")


def assert_state_equivalent(actual: np.ndarray, expected: np.ndarray) -> None:
    """Permit a global phase but require every relative phase and unit norm."""
    actual = np.asarray(actual, dtype=complex).ravel()
    expected = np.asarray(expected, dtype=complex).ravel()
    if actual.shape != expected.shape or not np.all(np.isfinite(actual)):
        raise AssertionError("State vectors must have matching dimensions and finite values")
    if not np.isclose(np.linalg.norm(actual), 1, atol=ABSOLUTE_TOLERANCE, rtol=0):
        raise AssertionError("State must have unit norm")
    pivot = int(np.argmax(np.abs(expected)))
    phase = actual[pivot] / expected[pivot]
    if not np.isclose(abs(phase), 1, atol=ABSOLUTE_TOLERANCE, rtol=0):
        raise AssertionError("State amplitudes differ")
    if not np.allclose(actual, phase * expected, atol=ABSOLUTE_TOLERANCE, rtol=0):
        raise AssertionError("State vectors differ beyond a global phase")


def expected_qft(input_value: int = 1) -> np.ndarray:
    """Use the analytical Fourier column, independently of circuit gates."""
    return np.exp(2j * np.pi * input_value * np.arange(8) / 8) / np.sqrt(8)


def assert_teleported_state(actual: np.ndarray, message: np.ndarray) -> None:
    """Trace out Alice; probabilities alone would miss lost relative phases."""
    amplitudes = np.asarray(actual).reshape(4, 2)
    reduced = amplitudes.T @ amplitudes.conj()
    message = np.asarray(message).ravel()
    expected = np.outer(message, message.conj())
    if not np.allclose(reduced, expected, atol=ABSOLUTE_TOLERANCE, rtol=0):
        raise AssertionError("Bob's density matrix does not reproduce the input state")


def teleportation_inputs() -> list[tuple[float, float, np.ndarray]]:
    """Include both phase-sensitive equatorial states and a generic state."""
    angles = [(0, 0), (np.pi, 0), (np.pi / 2, 0),
              (np.pi / 2, np.pi), (np.pi / 2, np.pi / 2),
              (np.pi / 2, -np.pi / 2), (0.73, -1.12)]
    return [(theta, phi, np.array([[np.cos(theta / 2)],
            [np.exp(1j * phi) * np.sin(theta / 2)]])) for theta, phi in angles]


def qiskit_wire_state(circuit) -> np.ndarray:
    """Reverse Qiskit's tensor axes, not the physical circuit's wire labels."""
    from qiskit.quantum_info import Statevector

    state = Statevector.from_instruction(circuit.remove_final_measurements(inplace=False))
    return state.data.reshape([2] * circuit.num_qubits).transpose().ravel()


def output_wires(name: str) -> list[int]:
    """Ancillas and Alice's qubits are omitted from logical output registers."""
    if name == "quantum-teleportation":
        return [2]
    width = len(next(iter(EXPECTED_PROBABILITIES[name])))
    return list(range(width))


def circuit_probabilities(circuit, name: str) -> dict[str, float]:
    """Marginalize unmeasured wires and compare outputs in wire-index order."""
    from qiskit.quantum_info import Statevector

    wires = output_wires(name)
    state = Statevector.from_instruction(circuit.remove_final_measurements(inplace=False))
    # Qiskit's qargs list places its first entry at the least significant axis.
    return probabilities_dict(state.probabilities(qargs=list(reversed(wires))))


def sample_circuit(circuit, name: str) -> dict[str, int]:
    """Follow actual measurement destinations, including superdense coding."""
    from qiskit.primitives import StatevectorSampler
    from qiskit import ClassicalRegister

    # OpenQASM scalar bits import as loose Clbits. The sampler only reports
    # registered outputs, so group those same bits without changing their mapping.
    if not circuit.cregs:
        circuit = circuit.copy()
        circuit.add_register(ClassicalRegister(bits=circuit.clbits, name="validation_output"))

    destinations = {}
    measuring = False
    for instruction in circuit.data:
        operation = instruction.operation.name
        if operation == "measure":
            measuring = True
            wire = circuit.find_bit(instruction.qubits[0]).index
            destinations[wire] = circuit.find_bit(instruction.clbits[0]).index
        elif measuring and operation != "barrier":
            raise AssertionError("Validator supports terminal measurements only")
    wires = output_wires(name)
    if set(destinations) != set(wires) or len(set(destinations.values())) != len(wires):
        raise AssertionError("Measurements must cover exactly the logical output wires")
    if len(circuit.cregs) != 1:
        raise AssertionError("Expected one classical output register")
    result = StatevectorSampler(seed=42).run([circuit], shots=SHOTS).result()[0]
    raw_counts = getattr(result.data, circuit.cregs[0].name).get_counts()
    counts = {}
    for label, count in raw_counts.items():
        classical_value = int(label, 2)
        logical = "".join(str((classical_value >> destinations[wire]) & 1) for wire in wires)
        counts[logical] = counts.get(logical, 0) + count
    return counts
