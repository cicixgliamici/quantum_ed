# Variational quantum eigensolver

VQE is a hybrid algorithm. A quantum circuit prepares a parameterized state and
measures a Hamiltonian expectation; a classical optimizer updates the parameters.

The repository uses the smallest complete example:

$$H=Z, \qquad |\psi(\theta)\rangle=R_Y(\theta)|0\rangle.$$

The cost is

$$E(\theta)=\langle\psi(\theta)|Z|\psi(\theta)\rangle=\cos\theta.$$

Its minimum is $E(\pi)=-1$, corresponding to the ground state $|1\rangle$.
The example is intentionally analytically solvable: reviewers can verify every
optimization result instead of treating VQE as a black box.

PennyLane demonstrates parameter-shift differentiation. NumPy and Qiskit use a
visible grid search. Q# and OpenQASM express the optimized ansatz because a
static quantum program does not itself define the outer classical optimizer.

See the [experiment](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/variational-quantum-eigensolver).
