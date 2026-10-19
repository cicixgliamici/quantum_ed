# Variational Quantum Eigensolver (VQE)

The **Variational Quantum Eigensolver (VQE)** estimates a Hamiltonian's ground
energy by optimizing a parameterized trial state. A quantum device estimates
expectation values and a classical optimizer changes the parameters.
[Peruzzo et al.](https://arxiv.org/abs/1304.3061) proposed and demonstrated this
hybrid approach. Circuit depth, accuracy, noise sensitivity, and optimization
cost depend on the problem and ansatz; VQE has no general guarantee of noise
resilience or quantum advantage.

---

## 1. The NISQ Dilemma & Hybrid Algorithms

Phase estimation uses controlled unitary powers to estimate eigenphases.
Large, accurate instances can require substantial coherent evolution and error
correction, while small examples can run without it. Neither QPE nor VQE
automatically implies an exponential advantage for an unspecified simulation
task; precision, input preparation, implementation cost, and classical methods
must be included in the comparison.

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

The ansatz minimum equals E0 only if the family can represent a ground state.
A classical optimizer need not find that minimum. The variational bound applies
to the exact expectation of a physical state; a noisy finite-sample estimate
or a mitigated estimator can fall below it due to estimation error.

---

## 3. Pauli String Decomposition

A practical approach for gate-based devices is to decompose an n-qubit
Hamiltonian into tensor products of Pauli matrices (**Pauli strings**):

$$
H = \sum_{i=1}^M c_i P_i, \qquad c_i \in \mathbb{R}, \quad P_i \in \{I, X, Y, Z\}^{\otimes n}
$$

By the linearity of quantum expectation values:

$$
E(\vec{\theta}) = \langle \psi(\vec{\theta}) | H | \psi(\vec{\theta}) \rangle = \sum_{i=1}^M c_i \langle \psi(\vec{\theta}) | P_i | \psi(\vec{\theta}) \rangle
$$

### Measuring Pauli Observables

Pauli terms may be estimated separately; compatible terms can sometimes be
grouped into shared measurement settings. For an individual qubit:

1. **$Z$-basis:** Measured directly in the standard computational basis.
2. **$X$-basis:** Apply a Hadamard gate $H$ before measurement ($H Z H = X$).
3. **$Y$-basis:** Apply $S^\dagger$ first, then H. The total basis-change
   operator is $B=HS^\dagger$, so $B^\dagger ZB=SHZHS^\dagger=Y$.

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

- **Advantage:** Number-conserving excitations and appropriate restrictions can
  encode physical symmetries. Truncating to singles and doubles does not
  guarantee a specified chemical accuracy for every system.
- **Disadvantage:** Requires deep circuits when compiled into standard gates via Trotterization.

### The Barren Plateau Phenomenon

[McClean et al. (2018)](https://arxiv.org/abs/1803.11173) establish exponentially
small gradient variance for the random-circuit ensembles and assumptions they
study. A schematic scaling in such a regime is:

$$
\operatorname{Var}\left( \frac{\partial E}{\partial \theta_k} \right) \in O\left( \frac{1}{2^n} \right)
$$

This can make typical gradients difficult to resolve. It does not mean every
ansatz has the same scaling, or that the cost function is literally constant
everywhere. Depth, initialization distribution, and observable all matter.

**Mitigation strategies include:**
- Using shallow, hardware-efficient layouts
- Local cost functions rather than global observables
- Structured near-identity initialization when the ansatz permits it; setting
  every parameter to zero does not by itself guarantee the identity circuit
- Symmetry-preserving and problem-tailored ansaetze

---

## 5. The Parameter-Shift Rule for Exact Gradients

Classical simulators can differentiate through state evolution. A hardware
device does not expose its state amplitudes for classical backpropagation;
gradients must instead be obtained through suitable measurement procedures.

Finite differences remain possible, but dividing noisy estimates by a small
epsilon amplifies sampling error and introduces a truncation-error tradeoff.

For appropriate gates, the **Parameter-Shift Rule** avoids this small-step
tradeoff: see [Mitarai et al.](https://arxiv.org/abs/1803.00745) and
[Schuld et al.](https://arxiv.org/abs/1811.11184).

For a single parameter occurrence in a gate $G=e^{-i\theta P/2}$ with
Hermitian $P^2=I$, with all other gates fixed, the exact expectation satisfies:

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

Define $A(\theta)=e^{i\theta P/2}Oe^{-i\theta P/2}$. At the operator level:

$$
\frac{A(\theta+\pi/2)-A(\theta-\pi/2)}2
=-\frac{\sin\theta}{2}(O-POP)+\frac{i\cos\theta}{2}[P,O]
=\frac{dA}{d\theta}.
$$

Taking the expectation in $W|0\rangle$ gives the scalar energy-gradient
formula above. Finite-shot evaluations still have statistical uncertainty.
If a shared parameter appears in several gates, differentiate each occurrence
and sum its contribution; the two-evaluation formula is not automatically
valid for the entire shared-parameter circuit.

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

### NumPy Parameter-Shift Optimization

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
from pennylane import numpy as pnp

dev = qml.device("default.qubit", wires=1)

@qml.qnode(dev, diff_method="parameter-shift")
def circuit(theta):
    qml.RY(theta, wires=0)
    return qml.expval(qml.PauliZ(0))

opt = qml.GradientDescentOptimizer(stepsize=0.4)
theta = pnp.array(0.2, requires_grad=True)

for _ in range(25):
    theta, cost = opt.step_and_cost(circuit, theta)

# step_and_cost returns the cost before its update; evaluate the final point.
final_energy = float(circuit(theta))
print(f"PennyLane optimized theta: {float(theta):.4f}, Energy: {final_energy:.4f}")
```

---

## 8. Multi-Ecosystem Showcase

The $H = Z$ VQE instance is implemented across all five ecosystems:

The Python versions evaluate and optimize the energy. Q# and OpenQASM expose
the optimal ansatz preparation only; they do not implement a classical
optimization loop. This is an educational instance, not an advantage claim.

- [NumPy Implementation](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/variational-quantum-eigensolver/numpy/vqe.py)
- [Qiskit Circuit](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/variational-quantum-eigensolver/qiskit/vqe.py)
- [PennyLane QNode](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/variational-quantum-eigensolver/pennylane/vqe.py)
- [Q# Program](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/variational-quantum-eigensolver/qsharp/VQEAnsatz.qs)
- [OpenQASM 3](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/variational-quantum-eigensolver/openqasm/vqe_ansatz.qasm)

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
A suitable Ry trial state can reach $E_0=-\sqrt2$, below the energy of the
particular basis state `00`. This tiny example is also solved by ordinary
classical matrix diagonalization, so this comparison is not quantum advantage.

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
