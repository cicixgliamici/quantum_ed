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
| [Quantum teleportation](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/quantum-teleportation) | State transfer | Default input `1`; full-state checks also use complex superpositions |
| [Deutsch-Jozsa](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/deutsch-jozsa) | Query complexity | Oracle is classified as balanced |
| [Bernstein-Vazirani](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/bernstein-vazirani) | Hidden strings | Secret `101` is recovered |
| [Grover search](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/grover-search) | Amplitude amplification | Marked state `11` is recovered |
| [Quantum Fourier transform](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/quantum-fourier-transform) | Phase representation | Complex amplitudes match the analytical Fourier transform |
| [Quantum phase estimation](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/quantum-phase-estimation) | Eigenphase extraction | Numerical phase bits `001` represent the T-gate phase 1/8 |
| [Variational quantum eigensolver](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/variational-quantum-eigensolver) | Hybrid optimization | Ground energy is `-1` |

Every experiment has a machine-readable contract. The
[scientific validation protocol](reference/experiment-validation.md) describes
which distributions and full states are checked. CI executes all five
ecosystems, including Q# and imported OpenQASM, against shared references.
The static VQE programs prepare the optimal ansatz; the Python versions also
evaluate the objective and run an optimizer.
