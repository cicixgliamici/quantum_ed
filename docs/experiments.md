# Cross-ecosystem experiments

Each experiment starts from one quantum concept and implements the same expected
result in multiple layers:

1. NumPy exposes the state-vector mathematics.
2. Qiskit demonstrates a Python SDK and sampling workflow.
3. Q# demonstrates quantum operations and qubit lifetime.
4. OpenQASM 3 exposes the portable circuit representation.
5. PennyLane exposes differentiable and mixed-state workflows where applicable.

| Experiment | Concept | Expected result |
| --- | --- | --- |
| [Bell state](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/bell-state) | Entanglement | Only `00` and `11` |
| [Superdense coding](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/superdense-coding) | Communication capacity | Message `10` is decoded |
| [Quantum teleportation](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/quantum-teleportation) | State transfer | Bob receives `1` |
| [Deutsch-Jozsa](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/deutsch-jozsa) | Query complexity | Oracle is classified as balanced |
| [Bernstein-Vazirani](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/bernstein-vazirani) | Hidden strings | Secret `101` is recovered |
| [Grover search](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/grover-search) | Amplitude amplification | Marked state `11` is recovered |
| [Quantum Fourier transform](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/quantum-fourier-transform) | Phase representation | Output magnitudes are uniform |
| [Variational quantum eigensolver](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/variational-quantum-eigensolver) | Hybrid optimization | Ground energy is `-1` |

Every experiment has a machine-readable contract. CI executes NumPy and Qiskit,
parses OpenQASM, and compiles Q#.
