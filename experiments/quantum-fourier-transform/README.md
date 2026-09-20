# Quantum Fourier transform experiment

The three-qubit QFT maps basis state `001` to amplitudes with equal magnitude
and input-dependent phases. Measurement is uniform, so the NumPy state vector
is important for inspecting information hidden from computational-basis counts.

Implementations: [NumPy](numpy/quantum_fourier_transform.py),
[Qiskit](qiskit/quantum_fourier_transform.py), [Q#](qsharp/QuantumFourierTransform.qs),
[OpenQASM 3](openqasm/quantum_fourier_transform.qasm), and
[PennyLane](pennylane/quantum_fourier_transform.py).

Read the [derivation](../../docs/10-quantum-algorithms/quantum-fourier-transform.md).
