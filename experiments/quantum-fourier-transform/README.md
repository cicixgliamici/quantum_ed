# Quantum Fourier transform experiment

The three-qubit QFT maps basis state `001` to amplitudes with equal magnitude
and input-dependent phases. Measurement is uniform, so the NumPy state vector
is important for inspecting information hidden from computational-basis counts.

Logical labels use wire order `q0 q1 q2`: input `001` prepares wire 2 in
state one in every circuit implementation. Qiskit's state-vector tensor axes
must be reversed before comparison with NumPy or PennyLane. The validators
check complex amplitudes up to a global phase, not just uniform probabilities.

Implementations: [NumPy](numpy/quantum_fourier_transform.py),
[Qiskit](qiskit/quantum_fourier_transform.py), [Q#](qsharp/QuantumFourierTransform.qs),
[OpenQASM 3](openqasm/quantum_fourier_transform.qasm), and
[PennyLane](pennylane/quantum_fourier_transform.py).

Read the [derivation](../../docs/10-quantum-algorithms/quantum-fourier-transform.md).
