# Variational quantum eigensolver experiment

This minimal VQE solves the Hamiltonian $H=Z$ with the ansatz
$R_Y(\theta)|0\rangle$. Its exact energy is $\cos\theta$, so the ground state
occurs at $\theta=\pi$ with energy $-1$.

- [NumPy](numpy/vqe.py) and [Qiskit](qiskit/vqe.py) use inspectable grid search.
- [PennyLane](pennylane/vqe.py) uses a differentiable QNode and parameter-shift.
- [Q#](qsharp/VQEAnsatz.qs) and [OpenQASM 3](openqasm/vqe_ansatz.qasm) represent
  the circuit at the classically optimized parameter.

Read the [workflow explanation](../../docs/10-quantum-algorithms/variational-quantum-eigensolver.md).
