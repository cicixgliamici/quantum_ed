# Quantum phase estimation experiment

Quantum phase estimation (QPE) extracts the eigenphase $\theta$ of a unitary $U$
acting on an eigenstate $|\psi\rangle$ such that $U|\psi\rangle = e^{2\pi i \theta}|\psi\rangle$.

This experiment implements a 4-qubit instance:
- **Target qubit (qubit 3):** prepared in $|1\rangle$.
- **Unitary:** $U = T$, with eigenstate $|1\rangle$ and eigenvalue $e^{i\pi/4} = e^{2\pi i (1/8)}$, so $\theta = 1/8 = 0.001_2$.
- **Counting qubits (qubits 0, 1, 2):** $m = 3$ qubits providing exact representation $2^3 \times (1/8) = 1$.
- **Expected measurement on counting register:** `001` with probability $1.0$.

Here `001` denotes numerical phase bits, as displayed by Qiskit and returned
by the NumPy analytical inverse DFT. In increasing wire order `q0 q1 q2`,
the result is `100`: wire 0 has binary weight one in this circuit. PennyLane
therefore places probability one at array index 4, and Q# returns
`[One, Zero, Zero]`. The shared validator converts these conventions explicitly.

Implementations: [NumPy](numpy/quantum_phase_estimation.py),
[Qiskit](qiskit/quantum_phase_estimation.py), [Q#](qsharp/QuantumPhaseEstimation.qs),
[OpenQASM 3](openqasm/quantum_phase_estimation.qasm), and
[PennyLane](pennylane/quantum_phase_estimation.py).

Read the [theory and derivation](../../docs/10-quantum-algorithms/quantum-phase-estimation.md).
