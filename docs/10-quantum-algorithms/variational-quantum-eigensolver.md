# Variational Quantum Eigensolver (VQE)

The **Variational Quantum Eigensolver (VQE)** is the flagship hybrid quantum-classical algorithm designed for the Noisy Intermediate-Scale Quantum (NISQ) era. Introduced by Alberto Peruzzo and collaborators in 2014, VQE calculates the ground-state energy of a quantum Hamiltonian (such as a molecular system in quantum chemistry or a spin lattice in condensed matter physics) using shallow, error-resilient quantum circuits.

---

## 1. The NISQ Dilemma & Hybrid Algorithms

Fault-tolerant quantum algorithms such as Quantum Phase Estimation (QPE) achieve exponential speedups for quantum simulation, but they require deep circuits with thousands of coherent entangling gates and full quantum error correction.

In contrast, VQE addresses the NISQ constraint by dividing the computational workload between a quantum processor and a classical computer:

- **Quantum Processor:** Prepares a parameterized trial state $|\psi(\vec{\theta})\rangle$ (the **ansatz**) using a short circuit and measures expectation values of Hamiltonian terms.
- **Classical Optimizer:** Processes the measured energies, computes gradients or descent directions, and iteratively updates the parameter vector $\vec{\theta}$ to minimize energy.

```text
       ┌────────────────────────────────────────────────────────┐
       │                 Quantum Coprocessor                    │
       │                                                        │
       │   |00...0⟩ ───[ Ansatz U(θ) ]───[ Measure H ] ──> ⟨H⟩  │
       └───────────────────────────┬────────────────────────────┘
                                   │
                         Energy E(θ) / Gradients
                                   │
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │                 Classical Optimizer                    │
       │                                                        │
       │     Updates θ_{t+1} = θ_t - η ∇E(θ_t)                  │
       │     (COBYLA, SPSA, Adam, Gradient Descent)             │
       └────────────────────────────────────────────────────────┘
```

---

## 2. The Rayleigh-Ritz Variational Principle

VQE relies on the foundational **variational principle of quantum mechanics**.

Let $H$ be an arbitrary time-independent Hermitian Hamiltonian with unknown ground-state energy $E_0$ and corresponding ground state $|\psi_0\rangle$:

$$
H |\psi_0\rangle = E_0 |\psi_0\rangle
$$

Because $H$ is Hermitian, its eigenstates $\{|E_k\rangle\}$ form an orthonormal basis with real eigenvalues $E_0 \le E_1 \le E_2 \le \dots$.

For **any** normalized quantum trial state $|\psi\rangle$, the expectation value of $H$ is strictly lower-bounded by $E_0$:

$$
\langle H \rangle_\psi = \langle \psi | H | \psi \rangle \ge E_0
$$

### Proof

Expand $|\psi\rangle$ in the energy eigenbasis: $|\psi\rangle = \sum_k c_k |E_k\rangle$ with $\sum_k |c_k|^2 = 1$:

$$
\langle \psi | H | \psi \rangle = \sum_k |c_k|^2 E_k \ge \sum_k |c_k|^2 E_0 = E_0 \sum_k |c_k|^2 = E_0
$$

Equality holds if and only if $|\psi\rangle$ lies entirely in the ground-state eigenspace.

Therefore, by constructing a parameterized quantum circuit $U(\vec{\theta})$ that prepares state $|\psi(\vec{\theta})\rangle = U(\vec{\theta})|0\rangle$, finding the ground state is transformed into an unconstrained classical optimization problem:

$$
E_0 \le \min_{\vec{\theta}} \langle \psi(\vec{\theta}) | H | \psi(\vec{\theta}) \rangle
$$

---

## 3. Pauli String Decomposition

Quantum hardware cannot measure an arbitrary matrix $H$ directly in a single operation. Instead, any $n$-qubit Hamiltonian is decomposed into a linear combination of tensor products of Pauli matrices (**Pauli strings**):

$$
H = \sum_{i=1}^M c_i P_i, \qquad c_i \in \mathbb{R}, \quad P_i \in \{I, X, Y, Z\}^{\otimes n}
$$

By the linearity of quantum expectation values:

$$
E(\vec{\theta}) = \langle \psi(\vec{\theta}) | H | \psi(\vec{\theta}) \rangle = \sum_{i=1}^M c_i \langle \psi(\vec{\theta}) | P_i | \psi(\vec{\theta}) \rangle
$$

### Measuring Pauli Observables

Each Pauli string $P_i$ is measured independently on the quantum device:

1. **$Z$-basis:** Measured directly in the standard computational basis.
2. **$X$-basis:** Apply a Hadamard gate $H$ before measurement ($H Z H = X$).
3. **$Y$-basis:** Apply $S^\dagger H$ before measurement ($S^\dagger H Z H S = Y$).

The classical computer sums the weighted measurement results to compute the total energy $E(\vec{\theta})$.

---

## 4. Ansatz Architectures & Barren Plateaus

The choice of parameterized circuit (ansatz) is the primary determinant of VQE accuracy and convergence.

### 1. Hardware-Efficient Ansatz (HEA)

Composed of repeating layers of single-qubit rotations ($R_y, R_z$) and native two-qubit entangling gates (such as CNOT or CZ between physically connected qubits).

- **Advantage:** Minimal circuit depth tailored to hardware coupling graphs; low gate error.
- **Disadvantage:** Lacks physical problem symmetry; highly vulnerable to optimization traps.

### 2. Physically-Motivated Ansatz (UCCSD)

Used in quantum chemistry. The **Unitary Coupled Cluster Singles and Doubles** ansatz models electronic excitations from occupied molecular orbitals to unoccupied orbitals:

$$
U(\vec{\theta}) = \exp(T(\vec{\theta}) - T^\dagger(\vec{\theta}))
$$

- **Advantage:** Preserves total electron number and spin symmetries; systematically approaches chemical accuracy ($1\ \text{kcal/mol}$).
- **Disadvantage:** Requires deep circuits when compiled into standard gates via Trotterization.

### The Barren Plateau Phenomenon

In 2018, McClean et al. proved that for deep, randomly initialized parameterized quantum circuits, the variance of the energy gradient vanishes exponentially with the number of qubits $n$:

$$
\operatorname{Var}\left( \frac{\partial E}{\partial \theta_k} \right) \in O\left( \frac{1}{2^n} \right)
$$

This causes gradient-based optimizers to stall because the cost landscape becomes featureless and flat everywhere.

**Mitigation strategies include:**
- Using shallow, hardware-efficient layouts
- Local cost functions rather than global observables
- Identity initialization (starting near $\vec{\theta} = \vec{0}$)
- Symmetry-preserving and problem-tailored ansaetze

---

## 5. The Parameter-Shift Rule for Exact Gradients

In classical neural networks, gradients are computed efficiently using automatic differentiation (backpropagation). On a quantum computer, measuring intermediate states collapses the wave function, ruling out backpropagation.

Numerical finite differences $\frac{E(\theta + \epsilon) - E(\theta)}{\epsilon}$ fail on quantum hardware because quantum measurement has intrinsic shot noise, which dominates when $\epsilon$ is small.

The solution is the **Parameter-Shift Rule** (Mitarai et al., 2018; Schuld et al., 2019):

For any quantum gate generated by a Pauli operator $G = e^{-i \theta P / 2}$ with $P^2 = I$ (e.g. $R_x(\theta), R_y(\theta), R_z(\theta)$), the **exact analytical gradient** is given by:

$$
\frac{\partial E}{\partial \theta} = \frac{E\left(\theta + \frac{\pi}{2}\right) - E\left(\theta - \frac{\pi}{2}\right)}{2}
$$

### Mathematical Derivation

Let $U(\theta) = V e^{-i \theta P / 2} W$. The expectation value is:

$$
E(\theta) = \langle 0 | W^\dagger e^{i \theta P / 2} V^\dagger H V e^{-i \theta P / 2} W | 0 \rangle
$$

Define the operator $O \equiv V^\dagger H V$. Using Euler's formula $e^{-i \theta P / 2} = \cos(\theta/2)I - i\sin(\theta/2)P$:

$$
e^{i \theta P / 2} O e^{-i \theta P / 2} = \cos^2(\theta/2) O + \sin^2(\theta/2) P O P + i \sin(\theta/2)\cos(\theta/2) [P, O]
$$

Using double-angle trigonometric identities:

$$
= \frac{1}{2}(O + P O P) + \frac{\cos\theta}{2}(O - P O P) + \frac{\sin\theta}{2} i [P, O]
$$

Taking the derivative with respect to $\theta$:

$$
\frac{d}{d\theta} \left( e^{i \theta P / 2} O e^{-i \theta P / 2} \right) = -\frac{\sin\theta}{2}(O - P O P) + \frac{\cos\theta}{2} i [P, O]
$$

Evaluating the difference with shifts of $\pm \pi/2$:

$$
\frac{E(\theta + \pi/2) - E(\theta - \pi/2)}{2} = -\frac{\sin\theta}{2}(O - P O P) + \frac{\cos\theta}{2} i [P, O] = \frac{\partial E}{\partial \theta}
$$

This remarkable formula allows evaluating exact analytic gradients on real quantum computers by measuring two macroscopic shifts of $\pm \pi/2$, completely avoiding finite-difference instabilities!

---

## 6. The Repository Showcase Instance

The repository implements the smallest non-trivial, analytically solvable VQE problem:

### Hamiltonian and Ansatz

$$
H = Z = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}, \qquad |\psi(\theta)\rangle = R_y(\theta)|0\rangle
$$

The rotation gate $R_y(\theta)$ is:

$$
R_y(\theta) = \begin{bmatrix} \cos(\theta/2) & -\sin(\theta/2) \\ \sin(\theta/2) & \cos(\theta/2) \end{bmatrix}
$$

Acting on $|0\rangle$:

$$
|\psi(\theta)\rangle = \cos(\theta/2)|0\rangle + \sin(\theta/2)|1\rangle
$$

### Cost Function & Ground State

Compute the energy expectation value:

$$
E(\theta) = \langle \psi(\theta) | Z | \psi(\theta) \rangle = \cos^2(\theta/2) - \sin^2(\theta/2) = \cos\theta
$$

- For $\theta = 0$: $E(0) = \cos(0) = +1$ (excited state $|0\rangle$).
- For $\theta = \pi$: $E(\pi) = \cos(\pi) = -1$ (exact ground state $|1\rangle$).

The global minimum is $E_0 = -1$ at $\theta^* = \pi$.

### Parameter-Shift Verification

Compute the gradient using parameter-shift:

$$
\frac{\partial E}{\partial \theta} = \frac{\cos(\theta + \pi/2) - \cos(\theta - \pi/2)}{2} = \frac{-\sin\theta - \sin\theta}{2} = -\sin\theta
$$

At $\theta = \pi$: $\frac{\partial E}{\partial \theta} = -\sin(\pi) = 0$, confirming that $\theta^* = \pi$ is an exact stationary point.

---

## 7. Python Implementation with NumPy & PennyLane

### NumPy Grid Search & Analytic Optimization

```python
import numpy as np

def energy(theta: float) -> float:
    # State: [cos(theta/2), sin(theta/2)]
    psi = np.array([np.cos(theta / 2.0), np.sin(theta / 2.0)])
    Z = np.diag([1.0, -1.0])
    return float(psi @ Z @ psi)

def grad_param_shift(theta: float) -> float:
    return 0.5 * (energy(theta + np.pi / 2.0) - energy(theta - np.pi / 2.0))

# Gradient descent optimization
theta = 0.1  # initial guess
eta = 0.2    # learning rate

for step in range(30):
    g = grad_param_shift(theta)
    theta -= eta * g

print(f"Optimized theta: {theta:.4f} (target: {np.pi:.4f})")
print(f"Calculated Ground Energy: {energy(theta):.4f} (target: -1.0000)")
```

### PennyLane QNode Implementation

```python
import pennylane as qml

dev = qml.device("default.qubit", wires=1)

@qml.qnode(dev, diff_method="parameter-shift")
def circuit(theta):
    qml.RY(theta, wires=0)
    return qml.expval(qml.PauliZ(0))

opt = qml.GradientDescentOptimizer(stepsize=0.4)
theta = 0.2

for _ in range(25):
    theta, cost = opt.step_and_cost(circuit, theta)

print(f"PennyLane optimized theta: {theta:.4f}, Energy: {cost:.4f}")
```

---

## 8. Multi-Ecosystem Showcase

The $H = Z$ VQE instance is implemented across all five ecosystems:

- [NumPy Implementation](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/variational-quantum-eigensolver/numpy/variational_quantum_eigensolver.py)
- [Qiskit Circuit](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/variational-quantum-eigensolver/qiskit/variational_quantum_eigensolver.py)
- [PennyLane QNode](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/variational-quantum-eigensolver/pennylane/variational_quantum_eigensolver.py)
- [Q# Program](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/variational-quantum-eigensolver/qsharp/VariationalQuantumEigensolver.qs)
- [OpenQASM 3](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/variational-quantum-eigensolver/openqasm/variational_quantum_eigensolver.qasm)

---

## 9. Worked Exercises

### Exercise 1 — VQE for a 2-Qubit Ising Model
**Problem:**
Consider the 2-qubit transverse-field Ising Hamiltonian:

$$
H = -Z_0 Z_1 - X_0
$$

Compute the expectation value of $H$ for the trial state $|\psi\rangle = |00\rangle$. Is it possible for a different state to have lower energy?

**Solution:**
1. Compute expectation values for $|\psi\rangle = |00\rangle$:

$$
\langle 00 | Z_0 Z_1 | 00 \rangle = (+1)(+1) = 1
$$

$$
\langle 00 | X_0 | 00 \rangle = \langle 0 | X | 0 \rangle \langle 0 | 0 \rangle = 0
$$

2. Total energy for $|00\rangle$:

$$
E(|00\rangle) = - (1) - 0 = -1
$$

3. Matrix representation of $H$:
   In basis $|00\rangle, |01\rangle, |10\rangle, |11\rangle$:

$$
H = \begin{bmatrix}
-1 & 0 & -1 & 0 \\
0 & 1 & 0 & -1 \\
-1 & 0 & 1 & 0 \\
0 & -1 & 0 & -1
\end{bmatrix}
$$

The eigenvalues of $H$ in the invariant subspace $\{|00\rangle, |10\rangle\}$ are roots of $\det \begin{bmatrix} -1-\lambda & -1 \\ -1 & 1-\lambda \end{bmatrix} = \lambda^2 - 1 - 1 = \lambda^2 - 2 = 0 \implies \lambda = \pm\sqrt{2}$.

The true ground state energy is $E_0 = -\sqrt{2} \approx -1.414 < -1$.
A VQE ansatz that introduces superposition with $R_y$ can reach $E_0 = -\sqrt{2}$, strictly outperforming the classical state $|00\rangle$.

---

### Exercise 2 — Parameter-Shift on Multi-Qubit Gates
**Problem:**
Show that the parameter-shift rule applies to a two-qubit rotation gate $R_{zz}(\theta) = \exp(-i \frac{\theta}{2} Z \otimes Z)$.

**Solution:**
Let $P = Z \otimes Z$.
Notice that:

$$
P^2 = (Z \otimes Z)(Z \otimes Z) = Z^2 \otimes Z^2 = I \otimes I = I
$$

Because $P$ is Hermitian and involutory ($P^2 = I$), the operator expansion:

$$
e^{-i \frac{\theta}{2} P} = \cos(\theta/2) I - i \sin(\theta/2) P
$$

holds identically to single-qubit rotations. Therefore, the parameter-shift rule holds without modification:

$$
\frac{\partial \langle H \rangle}{\partial \theta} = \frac{\langle H \rangle(\theta + \pi/2) - \langle H \rangle(\theta - \pi/2)}{2}
$$

---

## 10. Next Steps

- [Quantum Phase Estimation](quantum-phase-estimation.md) — the fault-tolerant alternative for eigenvalue estimation
- [Language Comparison](language-comparison.md) — see how parameter optimization maps across Python, Q#, and OpenQASM
- [Hardware Overview](../08-hardware/README.md) — understand why NISQ processors favor hybrid algorithms
