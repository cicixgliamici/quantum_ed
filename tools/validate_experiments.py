"""Validate declared experiments against common, phase-aware references."""

from __future__ import annotations

import argparse
from collections import Counter

import numpy as np

from experiment_checks import (
    ABSOLUTE_TOLERANCE, EXPECTED_PROBABILITIES, REPOSITORY_ROOT, SHOTS,
    assert_probabilities, assert_sampled_counts, assert_state_equivalent,
    assert_teleported_state, assert_swapped_state, circuit_probabilities, expected_qft, load_module,
    manifests, probabilities_dict, qiskit_wire_state, sample_circuit,
    teleportation_inputs,
)


def validate_energy(module) -> float:
    """Check the objective away from its optimum, then the optimizer result."""
    for angle in [0.0, 0.37, np.pi / 2, np.pi, 4.1]:
        if not np.isclose(module.energy(angle), np.cos(angle),
                          atol=ABSOLUTE_TOLERANCE, rtol=0):
            raise AssertionError(f"VQE energy differs from cos(theta) at {angle}")
    _, energy = module.optimize()
    # Gradient descent is approximate, unlike the exact grid-search optimum.
    if not np.isfinite(energy) or abs(energy + 1) > 1e-3:
        raise AssertionError(f"VQE did not reach ground energy: {energy}")
    return energy


def numpy_probabilities(name: str, module) -> dict[str, float]:
    """Adapt the existing educational entrypoints to wire-order labels."""
    if name == "bell-state":
        return module.measurement_probabilities()
    if name == "superdense-coding":
        return probabilities_dict(np.abs(module.decoded_state().ravel()) ** 2)
    if name == "quantum-teleportation":
        return module.target_probabilities()
    if name == "quantum-fourier-transform":
        return probabilities_dict(np.abs(module.transformed_state()) ** 2)
    if name == "quantum-phase-estimation":
        # NumPy's analytical inverse DFT labels integer phase bits, not wires.
        return {label[::-1]: value for label, value in module.estimate_phase().items()}
    if name == "variational-quantum-eigensolver":
        energy = validate_energy(module)
        # For Z, energy = p0 - p1 and normalization fixes both probabilities.
        return {"0": (1 + energy) / 2, "1": (1 - energy) / 2}
    return probabilities_dict(module.final_probabilities())


def validate_python_states(name: str, module, ecosystem: str) -> None:
    """Inspect information that measurement probabilities cannot reveal."""
    if name == "entanglement-swapping":
        actual = (qiskit_wire_state(module.build_circuit()) if ecosystem == "qiskit"
                  else module.swapped_state())
        assert_swapped_state(actual)
    if name == "quantum-fourier-transform":
        for input_value in range(8):
            if ecosystem == "qiskit":
                actual = qiskit_wire_state(module.build_circuit(input_value))
            else:
                actual = module.transformed_state(input_value)
            assert_state_equivalent(actual, expected_qft(input_value))
    if name == "quantum-teleportation":
        for _, _, message in teleportation_inputs():
            if ecosystem == "qiskit":
                actual = qiskit_wire_state(module.build_circuit(message))
            else:
                actual = module.teleported_state(message)
            assert_teleported_state(actual, message)


def validate_python(manifest: dict, ecosystem: str) -> None:
    """Compare Python implementations with the same analytical references."""
    name = manifest["name"]
    module = load_module(manifest["implementations"][ecosystem])
    if ecosystem == "numpy":
        actual = numpy_probabilities(name, module)
    elif name == "variational-quantum-eigensolver":
        validate_energy(module)
        return
    elif ecosystem == "qiskit":
        circuit = module.build_circuit()
        actual = circuit_probabilities(circuit, name)
        assert_sampled_counts(sample_circuit(circuit, name), EXPECTED_PROBABILITIES[name])
    else:
        function = module.target_probabilities if name == "quantum-teleportation" else module.probabilities
        actual = probabilities_dict(function())
    assert_probabilities(actual, EXPECTED_PROBABILITIES[name])
    validate_python_states(name, module, ecosystem)


def validate_openqasm(manifest: dict) -> None:
    """Execute imported circuits and verify phase-sensitive static programs."""
    from qiskit import QuantumCircuit, qasm3

    name = manifest["name"]
    source = REPOSITORY_ROOT / manifest["implementations"]["openqasm"]
    circuit = qasm3.load(str(source))
    assert_probabilities(circuit_probabilities(circuit, name), EXPECTED_PROBABILITIES[name])
    assert_sampled_counts(sample_circuit(circuit, name), EXPECTED_PROBABILITIES[name])
    if name == "quantum-fourier-transform":
        assert_state_equivalent(qiskit_wire_state(circuit), expected_qft())
    if name == "entanglement-swapping":
        assert_swapped_state(qiskit_wire_state(circuit))
    if name == "quantum-teleportation":
        # Inspect the actual imported protocol, rather than a Python copy of it.
        protocol = next(item.operation for item in circuit.data if item.operation.name == "teleport")
        for _, _, message in teleportation_inputs():
            diagnostic = QuantumCircuit(3)
            diagnostic.prepare_state(message.ravel(), 0)
            diagnostic.append(protocol, range(3))
            assert_teleported_state(qiskit_wire_state(diagnostic), message)


def qsharp_counts(results: list) -> dict[str, int]:
    """Q# Result arrays and tuples preserve their explicit element order."""
    labels = []
    for result in results:
        bits = result if isinstance(result, (tuple, list)) else [result]
        if any(str(bit) not in ("Zero", "One") for bit in bits):
            raise AssertionError(f"Unexpected Q# result: {result!r}")
        labels.append("".join("1" if str(bit) == "One" else "0" for bit in bits))
    return dict(Counter(labels))


def validate_qsharp_states(name: str, qsharp) -> None:
    """Inspect shared Q# preparations before their terminal measurements."""
    if name not in {"quantum-fourier-transform", "quantum-teleportation", "entanglement-swapping"}:
        return
    width = 4 if name == "entanglement-swapping" else 3
    qsharp.eval(f"use diagnostics = Qubit[{width}];")
    try:
        if name == "entanglement-swapping":
            qsharp.eval("PrepareSwapping(diagnostics);")
            assert_swapped_state(qsharp.dump_machine().as_dense_state())
        elif name == "quantum-fourier-transform":
            for input_value in range(8):
                qsharp.eval(f"PrepareQft({input_value}, diagnostics);")
                assert_state_equivalent(qsharp.dump_machine().as_dense_state(), expected_qft(input_value))
                qsharp.eval("ResetAll(diagnostics);")
        else:
            for theta, phi, message in teleportation_inputs():
                qsharp.eval(f"PrepareTeleportation({float(theta)}, {float(phi)}, diagnostics);")
                assert_teleported_state(qsharp.dump_machine().as_dense_state(), message)
                qsharp.eval("ResetAll(diagnostics);")
    finally:
        qsharp.eval("ResetAll(diagnostics);")


def validate_qsharp(manifest: dict) -> None:
    """Run actual entrypoints as well as compiling them."""
    import os

    os.environ.setdefault("QDK_PYTHON_TELEMETRY", "none")
    from qdk import qsharp

    name = manifest["name"]
    source = REPOSITORY_ROOT / manifest["implementations"]["qsharp"]
    # Each source defines Main; isolated contexts prevent symbol collisions.
    qsharp.init()
    qsharp.eval(source.read_text(encoding="utf-8"))
    counts = qsharp_counts(qsharp.run("Main()", shots=SHOTS, seed=42))
    assert_sampled_counts(counts, EXPECTED_PROBABILITIES[name])
    validate_qsharp_states(name, qsharp)


def validate_ecosystem(ecosystem: str) -> int:
    """Fail with the concept and ecosystem responsible for a mismatch."""
    validators = {"qsharp": validate_qsharp, "openqasm": validate_openqasm}
    for manifest in manifests():
        name = manifest["name"]
        try:
            if ecosystem in validators:
                validators[ecosystem](manifest)
            else:
                validate_python(manifest, ecosystem)
        except Exception as error:
            print(f"FAILED {ecosystem}/{name}: {error}")
            return 1
        print(f"Validated {ecosystem}/{name}")
    return 0


def main() -> int:
    """Allow separate CI jobs or one complete local equivalence check."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ecosystem", nargs="+", default=["numpy"],
                        choices=["numpy", "qiskit", "pennylane", "openqasm", "qsharp"])
    arguments = parser.parse_args()
    for ecosystem in arguments.ecosystem:
        if validate_ecosystem(ecosystem):
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
