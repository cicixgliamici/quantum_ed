# Measurement in Quantum Mechanics

In classical physics, observing a system is passive: you can measure the position or speed of a ball with arbitrary precision without disturbing its trajectory.

In quantum mechanics, **measurement is active, probabilistic, and fundamentally irreversible**. Measuring a quantum state disturbs it, collapsing a continuous superposition of amplitudes into a single discrete basis state.

---

## 1. The Measurement Postulate (Born Rule)

Quantum measurement is described by the **Measurement Postulate**, formalized by Max Born (1926) and John von Neumann (1932).

### Projective (von Neumann) Measurements
A projective measurement is described by a set of Hermitian operators $\{P_m\}$, called **projectors**, where each index $m$ labels a possible physical measurement outcome.

These operators must satisfy:
1. **Hermiticity:** $P_m^\dagger = P_m$
2. **Idempotence:** $P_m^2 = P_m$
3. **Mutual orthogonality:** $P_m P_{m'} = 0$ for $m \ne m'$
4. **Completeness:**

$$
\sum_m P_m = I
$$

### The Born Probability Rule
Given a normalized quantum state $|\psi\rangle$, the probability of obtaining outcome $m$ is given by the expectation value of the projector $P_m$:

$$
P(m) = \langle \psi | P_m | \psi \rangle = \|P_m |\psi\rangle\|^2
$$

The completeness relation guarantees that the probabilities of all possible outcomes sum to 1:

$$
\sum_m P(m) = \sum_m \langle \psi | P_m | \psi \rangle = \langle \psi | \left(\sum_m P_m\right) | \psi \rangle = \langle \psi | I | \psi \rangle = \langle \psi | \psi \rangle = 1
$$

### State Collapse (Lüders' Rule)
Immediately after obtaining outcome $m$, the state vector **collapses** to the normalized projection onto the eigenspace of $P_m$:

$$
|\psi'\rangle = \frac{P_m |\psi\rangle}{\sqrt{P(m)}} = \frac{P_m |\psi\rangle}{\sqrt{\langle \psi | P_m | \psi \rangle}}
$$

### Repeatability
If the state is measured a second time immediately after collapse in the same basis, the probability of obtaining outcome $m$ again is:

$$
P'(m) = \langle \psi' | P_m | \psi' \rangle = \frac{\langle \psi | P_m^\dagger P_m P_m | \psi \rangle}{P(m)} = \frac{\langle \psi | P_m | \psi \rangle}{P(m)} = \frac{P(m)}{P(m)} = 1
$$

Measurement confirms the state once collapsed; subsequent measurements yield the same outcome deterministically.

---

## 2. Computational Basis Measurement

For a single qubit, the standard measurement occurs in the computational basis $\{|0\rangle, |1\rangle\}$.

The corresponding projectors are:

$$
P_0 = |0\rangle\langle 0| = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix},
\qquad
P_1 = |1\rangle\langle 1| = \begin{pmatrix} 0 & 0 \\ 0 & 1 \end{pmatrix}
$$

For an arbitrary normalized single-qubit state $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$:

### Outcome 0:
- **Probability:**

$$
P(0) = \langle \psi | P_0 | \psi \rangle = \begin{pmatrix} \alpha^* & \beta^* \end{pmatrix} \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix} \begin{pmatrix} \alpha \\ \beta \end{pmatrix} = |\alpha|^2
$$

- **Post-measurement state:**

$$
|\psi'\rangle = \frac{P_0 |\psi\rangle}{\sqrt{P(0)}} = \frac{\alpha|0\rangle}{|\alpha|} = e^{i\arg(\alpha)}|0\rangle \sim |0\rangle
$$

### Outcome 1:
- **Probability:**

$$
P(1) = \langle \psi | P_1 | \psi \rangle = \begin{pmatrix} \alpha^* & \beta^* \end{pmatrix} \begin{pmatrix} 0 & 0 \\ 0 & 1 \end{pmatrix} \begin{pmatrix} \alpha \\ \beta \end{pmatrix} = |\beta|^2
$$

- **Post-measurement state:**

$$
|\psi'\rangle = \frac{P_1 |\psi\rangle}{\sqrt{P(1)}} = \frac{\beta|1\rangle}{|\beta|} = e^{i\arg(\beta)}|1\rangle \sim |1\rangle
$$

---

## 3. Measuring in Non-Computational Bases

Quantum computers physically measure qubits in the computational basis (the $Z$-basis). To measure in any other basis, such as the $X$-basis or $Y$-basis, we perform a **unitary basis rotation** immediately before measurement.

### Measuring in the $X$-Basis $\{|+\rangle, |-\rangle\}$
The eigenstates of the Pauli-X operator are:

$$
|+\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}},
\qquad
|-\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}}
$$

The Hadamard gate $H$ rotates the computational basis into the $X$-basis:

$$
H|0\rangle = |+\rangle, \qquad H|1\rangle = |-\rangle
$$

Because $H = H^\dagger = H^{-1}$, applying $H$ before a computational-basis measurement inverts this mapping:

$$
H|+\rangle = |0\rangle, \qquad H|-\rangle = |1\rangle
$$

Therefore:
1. Apply $H$ to the target qubit.
2. Measure in the computational basis.
3. Reading `0` corresponds to physical outcome $|+\rangle$; reading `1` corresponds to physical outcome $|-\rangle$.

### Measuring in the $Y$-Basis $\{|+i\rangle, |-i\rangle\}$
The eigenstates of the Pauli-Y operator are:

$$
|+i\rangle = \frac{|0\rangle + i|1\rangle}{\sqrt{2}},
\qquad
|-i\rangle = \frac{|0\rangle - i|1\rangle}{\sqrt{2}}
$$

Applying $S^\dagger = \begin{pmatrix} 1 & 0 \\ 0 & -i \end{pmatrix}$ followed by $H$ maps the $Y$-basis to the computational basis:

$$
H S^\dagger |+i\rangle = |0\rangle, \qquad H S^\dagger |-i\rangle = |1\rangle
$$

---

## 4. Observables, Expectation Values, and Uncertainty

In quantum mechanics, physical observables (such as energy, position, or spin) are represented by **Hermitian operators** $M = M^\dagger$.

### Spectral Theorem for Observables
Every Hermitian operator $M$ on $\mathbb{C}^d$ has real eigenvalues $\lambda_i \in \mathbb{R}$ and an orthonormal set of eigenvectors $\{|v_i\rangle\}$:

$$
M = \sum_i \lambda_i |v_i\rangle \langle v_i| = \sum_i \lambda_i P_i
$$

When measuring observable $M$:
- The only possible measurement outcomes are the eigenvalues $\lambda_i$.
- The probability of obtaining eigenvalue $\lambda_i$ is $P(\lambda_i) = \langle \psi | P_i | \psi \rangle$.
- The state collapses to the eigenstate $|v_i\rangle$.

### Expectation Value
The average value obtained from measuring $M$ over an ensemble of identically prepared states $|\psi\rangle$ is the **expectation value** $\langle M \rangle$:

$$
\langle M \rangle = \sum_i \lambda_i P(\lambda_i) = \sum_i \lambda_i \langle \psi | P_i | \psi \rangle = \langle \psi | \left( \sum_i \lambda_i P_i \right) | \psi \rangle = \langle \psi | M | \psi \rangle
$$

### Quantum Uncertainty (Variance)
The spread or uncertainty in the measurement of $M$ is defined as the standard deviation $\Delta M$:

$$
(\Delta M)^2 = \langle (M - \langle M \rangle I)^2 \rangle = \langle M^2 \rangle - \langle M \rangle^2
$$

**Key insight:** $\Delta M = 0$ if and only if $|\psi\rangle$ is an eigenstate of $M$. If $|\psi\rangle$ is not an eigenstate, quantum uncertainty is strictly positive ($\Delta M > 0$), representing an intrinsic quantum indeterminacy, not an experimental imperfection.

---

## 5. Multi-Qubit and Partial Measurements

When measuring an $n$-qubit system, two situations arise: measuring the entire system or measuring only a subset of qubits.

### Complete Measurement
For an $n$-qubit state $|\Psi\rangle = \sum_{x=0}^{2^n-1} c_x |x\rangle$, measuring all $n$ qubits in the computational basis yields bitstring $x \in \{0, 1\}^n$ with probability:

$$
P(x) = |c_x|^2
$$

The system collapses to the single basis state $|x\rangle$.

### Partial Measurement (Subsystem Measurement)
Suppose we have a two-qubit state:

$$
|\Psi\rangle = c_{00}|00\rangle + c_{01}|01\rangle + c_{10}|10\rangle + c_{11}|11\rangle
$$

and we measure **only the first qubit** (qubit 0).

The projector for measuring qubit 0 in state $|0\rangle$ while leaving qubit 1 untouched is:

$$
P_0^{(0)} = |0\rangle\langle 0| \otimes I_2
$$

The probability of measuring $0$ on the first qubit is:

$$
P(\text{qubit 0} = 0) = \langle \Psi | P_0^{(0)} | \Psi \rangle = |c_{00}|^2 + |c_{01}|^2
$$

The collapsed post-measurement state is:

$$
|\Psi'\rangle = \frac{P_0^{(0)} |\Psi\rangle}{\sqrt{P(\text{qubit 0} = 0)}} = \frac{c_{00}|00\rangle + c_{01}|01\rangle}{\sqrt{|c_{00}|^2 + |c_{01}|^2}} = |0\rangle \otimes \left( \frac{c_{00}|0\rangle + c_{01}|1\rangle}{\sqrt{|c_{00}|^2 + |c_{01}|^2}} \right)
$$

Notice that qubit 0 has collapsed to $|0\rangle$, while qubit 1 remains in a renormalized superposition determined by the original amplitudes.

#### Example: Measuring a Bell State
Consider the entangled Bell state:

$$
|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}
$$

1. Measure qubit 0:
   - Outcome $0$ occurs with probability $P(0) = |1/\sqrt{2}|^2 = 1/2$. The global state collapses to $|00\rangle$. Qubit 1 is now deterministically $|0\rangle$.
   - Outcome $1$ occurs with probability $P(1) = |1/\sqrt{2}|^2 = 1/2$. The global state collapses to $|11\rangle$. Qubit 1 is now deterministically $|1\rangle$.
2. Although qubit 1 was never physically touched, measuring qubit 0 instantaneously collapsed qubit 1 into the identical state. This is the hallmark of quantum entanglement.

---

## 6. The Principle of Deferred Measurement

A fundamental theorem in quantum circuit theory is the **Principle of Deferred Measurement**:

> Measurements performed in the middle of a quantum circuit can always be deferred to the end of the circuit without changing the final output probability distribution, provided any classically conditioned operations are replaced by equivalent coherent quantum controlled gates.

For example, measuring a control qubit and conditionally applying an $X$ gate based on the classical bit outcome is physically identical to applying a coherent `CNOT` gate directly, deferring the measurement to the end.

---

## 7. Python Implementation with `quantum_ed.measurement`

In `src/quantum_ed/measurement.py`, exact probability computation and sampling are implemented:

```python
import numpy as np
from quantum_ed import ket0, H, apply, probs_comp_basis, measure_comp_basis

# 1. Prepare superposition state |+>
psi = apply(H, ket0())

# 2. Compute exact theoretical probabilities
p0, p1 = probs_comp_basis(psi)
print(f"Theoretical probabilities: P(0) = {p0:.3f}, P(1) = {p1:.3f}")
# Output: P(0) = 0.500, P(1) = 0.500

# 3. Simulate projective measurements (sampling shots)
shots = 1000
samples = measure_comp_basis(psi, shots=shots, seed=42)
count_0 = np.sum(samples == 0)
count_1 = np.sum(samples == 1)

print(f"\nEmpirical counts over {shots} shots:")
print(f"Outcome 0: {count_0} ({count_0/shots * 100:.1f}%)")
print(f"Outcome 1: {count_1} ({count_1/shots * 100:.1f}%)")
```

---

## 8. Exercises and Worked Solutions

### Exercise 1: Single-Qubit Collapse
**Problem:** A qubit is prepared in $|\psi\rangle = \frac{1}{2}|0\rangle + \frac{\sqrt{3}}{2}|1\rangle$.
1. What is the probability of measuring outcome 0?
2. What is the state of the qubit immediately after obtaining outcome 1?

**Solution:**
1. $P(0) = |\alpha|^2 = |1/2|^2 = 1/4 = 0.25$ (or $25\%$).
2. The probability of outcome 1 is $P(1) = |\sqrt{3}/2|^2 = 3/4$.
   The collapsed state is:
   
$$
|\psi'\rangle = \frac{P_1 |\psi\rangle}{\sqrt{P(1)}} = \frac{\frac{\sqrt{3}}{2}|1\rangle}{\sqrt{3/4}} = |1\rangle
$$

### Exercise 2: Pauli-Z Expectation Value
**Problem:** Compute the expectation value $\langle Z \rangle$ for the state $|\psi\rangle = \cos(\theta/2)|0\rangle + \sin(\theta/2)|1\rangle$.
**Solution:**
The Pauli-Z matrix is $Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$.

$$
\langle Z \rangle = \langle \psi | Z | \psi \rangle = \begin{pmatrix} \cos(\theta/2) & \sin(\theta/2) \end{pmatrix} \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix} \begin{pmatrix} \cos(\theta/2) \\ \sin(\theta/2) \end{pmatrix}
$$

$$
\langle Z \rangle = \begin{pmatrix} \cos(\theta/2) & \sin(\theta/2) \end{pmatrix} \begin{pmatrix} \cos(\theta/2) \\ -\sin(\theta/2) \end{pmatrix} = \cos^2(\theta/2) - \sin^2(\theta/2) = \cos\theta
$$

This matches the $z$-component of the Bloch vector: $z = \cos\theta$.

---

## 9. Next Steps

Now explore how multi-qubit systems interact through entanglement:
- [Chapter 4: Entanglement](../04-entanglement/README.md)
- [Chapter 5: Circuits & Gates](../05-circuits-and-gates/README.md)
- Accompanying notebook: [`notebooks/01-qubit-bloch.ipynb`](https://github.com/cicixgliamici/quantum_ed/blob/main/notebooks/01-qubit-bloch.ipynb)
