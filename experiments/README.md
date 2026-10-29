# Cross-ecosystem quantum experiments

This directory is the meeting point between quantum theory and its expression
in different programming ecosystems. Experiments are grouped by concept first,
then by implementation. This makes equivalent programs easy to compare without
mixing portfolio examples with the installable Python package in `src/`.

<!-- experiment-catalog:start -->

| Experiment | Theory | Implementations | Expected result |
| --- | --- | --- | --- |
| [Bell-state experiment](bell-state/README.md) | [Quantum Entanglement](../docs/04-entanglement/README.md) | NumPy, Qiskit, PennyLane, Q#, OpenQASM 3 | Only 00 and 11 occur, with equal ideal probabilities. |
| [Bernstein-Vazirani experiment](bernstein-vazirani/README.md) | [Bernstein-Vazirani algorithm](../docs/10-quantum-algorithms/bernstein-vazirani.md) | NumPy, Qiskit, PennyLane, Q#, OpenQASM 3 | The hidden string 101 is recovered deterministically. |
| [Deutsch-Jozsa experiment](deutsch-jozsa/README.md) | [Deutsch-Jozsa algorithm](../docs/10-quantum-algorithms/deutsch-jozsa.md) | NumPy, Qiskit, PennyLane, Q#, OpenQASM 3 | The selected oracle is classified as balanced. |
| [Entanglement-swapping experiment](entanglement-swapping/README.md) | [Entanglement swapping](../docs/11-quantum-networks/entanglement-swapping.md) | NumPy, Qiskit, PennyLane, Q#, OpenQASM 3 | Each Bob outcome has probability 1/4; outcome-dependent corrections give Alice and Charlie Phi-plus, with P(00)=P(11)=1/2. |
| [Grover-search experiment](grover-search/README.md) | [Grover's Search Algorithm & Amplitude Amplification](../docs/10-quantum-algorithms/grover-search.md) | NumPy, Qiskit, PennyLane, Q#, OpenQASM 3 | The marked state 11 is recovered deterministically in the ideal two-qubit case. |
| [Quantum Fourier transform experiment](quantum-fourier-transform/README.md) | [Quantum Fourier Transform (QFT)](../docs/10-quantum-algorithms/quantum-fourier-transform.md) | NumPy, Qiskit, PennyLane, Q#, OpenQASM 3 | The QFT of basis state 001 has uniform measurement probabilities and phase-encoded input information. |
| [Quantum phase estimation experiment](quantum-phase-estimation/README.md) | [Quantum phase estimation](../docs/10-quantum-algorithms/quantum-phase-estimation.md) | NumPy, Qiskit, PennyLane, Q#, OpenQASM 3 | Estimating the phase of the T gate on state 1 yields phase 1/8 (state 001) with probability 1. |
| [Quantum-teleportation experiment](quantum-teleportation/README.md) | [Quantum Teleportation](../docs/04-entanglement/quantum-teleportation.md) | NumPy, Qiskit, PennyLane, Q#, OpenQASM 3 | Bob's target qubit is measured as 1 deterministically. |
| [Superdense-coding experiment](superdense-coding/README.md) | [Superdense Coding](../docs/04-entanglement/superdense-coding.md) | NumPy, Qiskit, PennyLane, Q#, OpenQASM 3 | The message 10 is decoded deterministically. |
| [Variational quantum eigensolver experiment](variational-quantum-eigensolver/README.md) | [Variational Quantum Eigensolver (VQE)](../docs/10-quantum-algorithms/variational-quantum-eigensolver.md) | NumPy, Qiskit, PennyLane, Q#, OpenQASM 3 | The RY ansatz converges to theta pi and ground-state energy -1 for Hamiltonian Z. |

<!-- experiment-catalog:end -->

For VQE, the Python versions evaluate and optimize the objective. The Q# and
OpenQASM programs prepare the optimal ansatz without implementing an optimizer.
The [validation protocol](../docs/reference/experiment-validation.md) states
which outputs and full states are checked for each experiment.

## Ecosystem roles

- NumPy entrypoints and `quantum_ed` expose the underlying linear algebra.
- Qiskit demonstrates an SDK workflow with circuit construction and sampling.
- Q# demonstrates operations, allocation, measurement, and qubit lifetime.
- OpenQASM 3 exposes a portable circuit-level representation.
- PennyLane exposes differentiable circuits and mixed-state simulation.

Install the optional Qiskit dependency with:

```bash
python -m pip install -e ".[showcase]"
```

Install and validate PennyLane experiments with:

```bash
python -m pip install -e ".[pennylane]"
python tools/validate_pennylane.py
```

Each experiment README defines its purpose, expected result, bit-ordering
convention, implementation links, and execution instructions.

## Experiment contract

Scientific checks execute all five ecosystems against common analytical
references, with explicit wire ordering, relative-phase checks, and statistical
sampling bounds. See the [validation protocol](../docs/reference/experiment-validation.md).

```bash
python tools/validate_experiments.py --ecosystem numpy qiskit pennylane openqasm qsharp
```

Every experiment contains an `experiment.json` manifest conforming to
[`schema.json`](schema.json). The manifest declares its theory page, expected
result, category, and one entrypoint for each supported ecosystem. Validate all
contracts and local documentation links from the repository root:

```bash
python tools/verify_repository.py
```
