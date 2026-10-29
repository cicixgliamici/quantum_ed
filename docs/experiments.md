# Cross-ecosystem experiments

Each experiment starts from one quantum concept and implements the same expected
result in multiple layers:

1. NumPy exposes the state-vector mathematics.
2. Qiskit demonstrates a Python SDK and sampling workflow.
3. Q# demonstrates quantum operations and qubit lifetime.
4. OpenQASM 3 exposes the portable circuit representation.
5. PennyLane exposes differentiable and mixed-state workflows where applicable.

<!-- experiment-catalog:start -->

| Experiment | Theory | Implementations | Expected result |
| --- | --- | --- | --- |
| [Bell-state experiment](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/bell-state) | [Quantum Entanglement](04-entanglement/README.md) | NumPy, Qiskit, PennyLane, Q#, OpenQASM 3 | Only 00 and 11 occur, with equal ideal probabilities. |
| [Bernstein-Vazirani experiment](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/bernstein-vazirani) | [Bernstein-Vazirani algorithm](10-quantum-algorithms/bernstein-vazirani.md) | NumPy, Qiskit, PennyLane, Q#, OpenQASM 3 | The hidden string 101 is recovered deterministically. |
| [Deutsch-Jozsa experiment](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/deutsch-jozsa) | [Deutsch-Jozsa algorithm](10-quantum-algorithms/deutsch-jozsa.md) | NumPy, Qiskit, PennyLane, Q#, OpenQASM 3 | The selected oracle is classified as balanced. |
| [Entanglement-swapping experiment](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/entanglement-swapping) | [Entanglement swapping](11-quantum-networks/entanglement-swapping.md) | NumPy, Qiskit, PennyLane, Q#, OpenQASM 3 | Each Bob outcome has probability 1/4; outcome-dependent corrections give Alice and Charlie Phi-plus, with P(00)=P(11)=1/2. |
| [Grover-search experiment](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/grover-search) | [Grover's Search Algorithm & Amplitude Amplification](10-quantum-algorithms/grover-search.md) | NumPy, Qiskit, PennyLane, Q#, OpenQASM 3 | The marked state 11 is recovered deterministically in the ideal two-qubit case. |
| [Quantum Fourier transform experiment](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/quantum-fourier-transform) | [Quantum Fourier Transform (QFT)](10-quantum-algorithms/quantum-fourier-transform.md) | NumPy, Qiskit, PennyLane, Q#, OpenQASM 3 | The QFT of basis state 001 has uniform measurement probabilities and phase-encoded input information. |
| [Quantum phase estimation experiment](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/quantum-phase-estimation) | [Quantum phase estimation](10-quantum-algorithms/quantum-phase-estimation.md) | NumPy, Qiskit, PennyLane, Q#, OpenQASM 3 | Estimating the phase of the T gate on state 1 yields phase 1/8 (state 001) with probability 1. |
| [Quantum-teleportation experiment](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/quantum-teleportation) | [Quantum Teleportation](04-entanglement/quantum-teleportation.md) | NumPy, Qiskit, PennyLane, Q#, OpenQASM 3 | Bob's target qubit is measured as 1 deterministically. |
| [Superdense-coding experiment](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/superdense-coding) | [Superdense Coding](04-entanglement/superdense-coding.md) | NumPy, Qiskit, PennyLane, Q#, OpenQASM 3 | The message 10 is decoded deterministically. |
| [Variational quantum eigensolver experiment](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/variational-quantum-eigensolver) | [Variational Quantum Eigensolver (VQE)](10-quantum-algorithms/variational-quantum-eigensolver.md) | NumPy, Qiskit, PennyLane, Q#, OpenQASM 3 | The RY ansatz converges to theta pi and ground-state energy -1 for Hamiltonian Z. |

<!-- experiment-catalog:end -->

Every experiment has a machine-readable contract. The
[scientific validation protocol](reference/experiment-validation.md) describes
which distributions and full states are checked. CI executes all five
ecosystems, including Q# and imported OpenQASM, against shared references.
The static VQE programs prepare the optimal ansatz; the Python versions also
evaluate the objective and run an optimizer.
