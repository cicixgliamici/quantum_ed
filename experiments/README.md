# Cross-ecosystem quantum experiments

This directory is the meeting point between quantum theory and its expression
in different programming ecosystems. Experiments are grouped by concept first,
then by implementation. This makes equivalent programs easy to compare without
mixing portfolio examples with the installable Python package in `src/`.

| Experiment | Theory | Implementations | Expected result |
| --- | --- | --- | --- |
| [Bell state](bell-state/README.md) | Entanglement | NumPy, Qiskit, Q#, OpenQASM 3 | Only `00` and `11`, with equal ideal probabilities |
| [Superdense coding](superdense-coding/README.md) | Entanglement-assisted communication | NumPy, Qiskit, Q#, OpenQASM 3 | The message `10` is decoded deterministically |
| [Quantum teleportation](quantum-teleportation/README.md) | Quantum communication | NumPy, Qiskit, Q#, OpenQASM 3 | Bob recovers the state `1` deterministically |
| [Deutsch-Jozsa](deutsch-jozsa/README.md) | Query algorithms | NumPy, Qiskit, Q#, OpenQASM 3 | The selected oracle is classified as balanced |
| [Bernstein-Vazirani](bernstein-vazirani/README.md) | Query algorithms | NumPy, Qiskit, Q#, OpenQASM 3 | The hidden string `101` is recovered |
| [Grover search](grover-search/README.md) | Search algorithms | Five ecosystems | The marked state `11` is recovered |
| [Quantum Fourier transform](quantum-fourier-transform/README.md) | Algorithmic primitives | Five ecosystems | Output magnitudes are uniform |
| [Quantum phase estimation](quantum-phase-estimation/README.md) | Algorithmic primitives | Five ecosystems | The phase 1/8 of the T gate is estimated deterministically as `001` |
| [Variational quantum eigensolver](variational-quantum-eigensolver/README.md) | Hybrid algorithms | Five ecosystems | Ground energy is `-1` |

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

Every experiment contains an `experiment.json` manifest conforming to
[`schema.json`](schema.json). The manifest declares its theory page, expected
result, category, and one entrypoint for each supported ecosystem. Validate all
contracts and local documentation links from the repository root:

```bash
python tools/verify_repository.py
```
