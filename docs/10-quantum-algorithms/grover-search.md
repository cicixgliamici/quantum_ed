# Grover's Search Algorithm & Amplitude Amplification

Searching an unsorted database of size $N$ on a classical computer requires $O(N)$ queries in the worst case and $N/2$ queries on average. In 1996, Lov Grover introduced a quantum algorithm capable of solving the unstructured search problem in:

$$
O(\sqrt{N}) \quad \text{oracle queries}
$$

This represents a provable **quadratic speedup**. Bennett, Bernstein, Brassard, and Vazirani (the BBBV theorem, 1997) proved that Grover's algorithm is asymptotically optimal: no quantum algorithm can search an unstructured database in fewer than $\Omega(\sqrt{N})$ queries.

---

## 1. Problem Formulation

Consider an unstructured search space of $N = 2^n$ items, indexed by $n$-bit strings $x \in \{0, 1\}^n$. A Boolean function $f: \{0, 1\}^n \to \{0, 1\}$ evaluates whether an item is a solution:

$$
f(x) = \begin{cases} 1 & \text{if } x = \omega \quad (\text{marked target state}) \\ 0 & \text{if } x \neq \omega \end{cases}
$$

The goal is to identify $\omega$ using the minimum number of oracle queries.

---

## 2. Geometric Interpretation in a 2D Subspace

The core intuition behind Grover's algorithm is that the evolution of the quantum state remains confined within a **two-dimensional subspace** of the full $2^n$-dimensional Hilbert space, regardless of $n$.

### The Two Orthonormal Basis Vectors

Define two orthonormal vectors spanning this subspace:

1. **The Target State $|\omega\rangle$:** The marked solution state.
2. **The Orthogonal Superposition of Non-Target States $|s'\rangle$:**

$$
|s'\rangle = \frac{1}{\sqrt{N - 1}} \sum_{x \neq \omega} |x\rangle
$$

### The Initial Uniform Superposition

The algorithm begins by applying Hadamard gates to all $n$ qubits initialized in $|0\rangle^{\otimes n}$, preparing the uniform superposition $|s\rangle$:

$$
|s\rangle = H^{\otimes n} |0\rangle^{\otimes n} = \frac{1}{\sqrt{N}} \sum_{x=0}^{N-1} |x\rangle
$$

We can express $|s\rangle$ directly in the $\{|s'\rangle, |\omega\rangle\}$ basis:

$$
|s\rangle = \sqrt{\frac{N-1}{N}} |s'\rangle + \frac{1}{\sqrt{N}} |\omega\rangle = \cos(\theta/2) |s'\rangle + \sin(\theta/2) |\omega\rangle
$$

where the initial angle $\theta/2$ is defined by:

$$
\sin(\theta/2) = \frac{1}{\sqrt{N}}
$$

For large $N$, $\sin(\theta/2) \approx \theta/2 \approx 1/\sqrt{N}$, meaning the state $|s\rangle$ is almost completely aligned with the non-target subspace $|s'\rangle$.

---

## 3. The Two Reflection Operators

Grover's algorithm amplifies the amplitude of $|\omega\rangle$ by applying a composite rotation consisting of **two geometric reflections**:

### 1. The Oracle Reflection ($R_\omega$)

The phase oracle marks the target state by flipping its sign:

$$
R_\omega = I - 2|\omega\rangle\langle\omega|
$$

Its action on the basis states:

$$
R_\omega |\omega\rangle = -|\omega\rangle, \qquad R_\omega |s'\rangle = |s'\rangle
$$

Geometrically, $R_\omega$ is a **reflection across the $|s'\rangle$ axis** (it inverts the component parallel to $|\omega\rangle$).

### 2. The Grover Diffusion Operator ($D$)

The diffusion operator (or inversion-about-the-mean operator) reflects any quantum state across the initial uniform superposition vector $|s\rangle$:

$$
D = 2|s\rangle\langle s| - I
$$

#### Circuit Implementation of $D$

Since $|s\rangle = H^{\otimes n} |0\dots 0\rangle$, the diffusion operator can be decomposed into elementary quantum gates:

$$
D = 2 (H^{\otimes n} |0\dots 0\rangle\langle 0\dots 0| H^{\otimes n}) - I = H^{\otimes n} (2|0\dots 0\rangle\langle 0\dots 0| - I) H^{\otimes n}
$$

The central reflection $(2|0\dots 0\rangle\langle 0\dots 0| - I)$ flips the phase of every state *except* $|0\dots 0\rangle$, which can be implemented using $X$ gates and a multi-controlled $Z$ gate.

---

## 4. The Grover Iteration (Grover Step)

One full Grover iteration $G$ is the product of the two reflections:

$$
G = D \cdot R_\omega = (2|s\rangle\langle s| - I) (I - 2|\omega\rangle\langle\omega|)
$$

### Angular Rotation

In the 2D plane spanned by $\{|s'\rangle, |\omega\rangle\}$:
1. $R_\omega$ reflects the state vector across the horizontal axis $|s'\rangle$.
2. $D$ reflects the resulting state across the line $|s\rangle$, which makes an angle $\theta/2$ with $|s'\rangle$.

By elementary plane geometry, the composition of two reflections across lines separated by an angle $\theta/2$ is a **counterclockwise rotation by angle $\theta$**:

$$
\theta \approx \frac{2}{\sqrt{N}} \quad (\text{for } N \gg 1)
$$

After $k$ iterations, the state vector is:

$$
G^k |s\rangle = \cos\left( \frac{2k+1}{2} \theta \right) |s'\rangle + \sin\left( \frac{2k+1}{2} \theta \right) |\omega\rangle
$$

Each iteration rotates the state vector toward the target state $|\omega\rangle$ by an angle $\theta$.

---

## 5. Optimal Number of Iterations & Overcooking

We wish to stop when the state is as close as possible to $|\omega\rangle$, which occurs when the angle reaches $\pi/2$:

$$
\frac{2R + 1}{2} \theta \approx \frac{\pi}{2} \implies 2R \cdot \frac{2}{\sqrt{N}} \approx \pi \implies R \approx \frac{\pi}{4} \sqrt{N}
$$

The optimal number of Grover iterations is:

$$
R = \left\lfloor \frac{\pi}{4} \sqrt{N} \right\rfloor
$$

### The "Overcooking" Phenomenon

Unlike classical search, which monotonically increases the probability of finding the target with additional queries, **Grover's algorithm is periodic**.

If the algorithm continues beyond $R$ iterations, the state vector rotates *past* $|\omega\rangle$ back toward $|s'\rangle$, causing the success probability to decrease. Accurate knowledge of the number of solutions is required to determine the optimal stopping point (or quantum counting via QPE must be used).

### Multiple Target Solutions ($M \ge 1$)

If there are $M$ marked items out of $N$, the initial overlap is $\sin(\theta/2) = \sqrt{M/N}$, and the optimal number of iterations becomes:

$$
R \approx \frac{\pi}{4} \sqrt{\frac{N}{M}}
$$

---

## 6. Worked Example: 2 Qubits ($N = 4$) with Target $|11\rangle$

For a 2-qubit register ($N = 2^2 = 4$):

$$
|s\rangle = \frac{1}{2} (|00\rangle + |01\rangle + |10\rangle + |11\rangle)
$$

The initial angle satisfies $\sin(\theta/2) = 1/\sqrt{4} = 1/2 \implies \theta/2 = 30^\circ \implies \theta = 60^\circ$.

The optimal number of iterations is:

$$
R \approx \frac{\pi}{4}\sqrt{4} = \frac{\pi}{2} \approx 1.57 \implies R = 1 \text{ iteration}
$$

After exactly **$R = 1$ iteration**, the total rotation angle is:

$$
\frac{2(1) + 1}{2} \theta = \frac{3}{2} (60^\circ) = 90^\circ = \frac{\pi}{2}
$$

The final state aligns **exactly** with $|11\rangle$, giving a theoretical success probability of:

$$
P(|11\rangle) = \sin^2(90^\circ) = 1.0 \quad (100\%)
$$

### Step-by-Step State Evolution

1. **Initial uniform superposition:**

$$
|\psi_0\rangle = |s\rangle = \begin{bmatrix} 1/2 \\ 1/2 \\ 1/2 \\ 1/2 \end{bmatrix}
$$

2. **Apply Phase Oracle $R_\omega$ (marks $|11\rangle$ by flipping sign):**

$$
|\psi_1\rangle = R_\omega |\psi_0\rangle = \begin{bmatrix} 1/2 \\ 1/2 \\ 1/2 \\ -1/2 \end{bmatrix}
$$

3. **Compute the mean amplitude:**

$$
\mu = \frac{1}{4} \left( \frac{1}{2} + \frac{1}{2} + \frac{1}{2} - \frac{1}{2} \right) = \frac{1}{4} (1) = \frac{1}{4}
$$

4. **Inversion about the mean ($a_i' = 2\mu - a_i$):**
   - For non-target states ($a_i = 1/2$):

$$
a_i' = 2\left(\frac{1}{4}\right) - \frac{1}{2} = \frac{1}{2} - \frac{1}{2} = 0
$$

   - For target state ($a_i = -1/2$):

$$
a_i' = 2\left(\frac{1}{4}\right) - \left(-\frac{1}{2}\right) = \frac{1}{2} + \frac{1}{2} = 1
$$

The resulting state is:

$$
|\psi_2\rangle = \begin{bmatrix} 0 \\ 0 \\ 0 \\ 1 \end{bmatrix} = |11\rangle
$$

Measuring the circuit yields $|11\rangle$ with $100\%$ certainty in a single query!

---

## 7. Python Implementation in NumPy

```python
import numpy as np
from quantum_ed.gates import H, kron_n

# 1. Prepare 2-qubit Hadamard transform
H2 = kron_n(H, H)
s = H2 @ np.array([1, 0, 0, 0], dtype=complex)  # uniform |s>

# 2. Oracle marking |11>
R_omega = np.diag([1, 1, 1, -1])

# 3. Diffusion operator: D = 2|s><s| - I
D = 2 * np.outer(s, np.conj(s)) - np.eye(4)

# 4. Execute 1 Grover iteration
psi = D @ (R_omega @ s)

# 5. Probabilities
probs = np.abs(psi)**2
print(f"Outcome probabilities: {np.round(probs, 4)}")
# Expected: [0., 0., 0., 1.] -> 100% target |11>
```

---

## 8. Multi-Ecosystem Showcase

The 2-qubit Grover instance targeting $|11\rangle$ is implemented across all five supported environments:

- [NumPy Implementation](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/grover-search/numpy/grover_search.py) — explicit matrix algebra
- [Qiskit Circuit](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/grover-search/qiskit/grover_search.py) — CZ oracle and H-X-CZ-X-H diffusion
- [Q# Program](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/grover-search/qsharp/GroverSearch.qs) — idiomatic Microsoft Q# with adjoint blocks
- [OpenQASM 3](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/grover-search/openqasm/grover_search.qasm) — standard circuit representation
- [PennyLane](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/grover-search/pennylane/grover_search.py) — QNode pipeline

---

## 9. Worked Exercises

### Exercise 1 — Inversion About the Mean Formula
**Problem:**
Prove that the operator $D = 2|s\rangle\langle s| - I$ maps any amplitude $a_x$ of state $|\psi\rangle = \sum_x a_x |x\rangle$ to $a_x' = 2\mu - a_x$, where $\mu = \frac{1}{N}\sum_x a_x$ is the average amplitude.

**Solution:**
1. Compute the inner product $\langle s|\psi\rangle$:

$$
\langle s|\psi\rangle = \left(\frac{1}{\sqrt{N}}\sum_y \langle y|\right)\left(\sum_x a_x |x\rangle\right) = \frac{1}{\sqrt{N}}\sum_x a_x = \sqrt{N}\mu
$$

2. Apply $2|s\rangle\langle s|$ to $|\psi\rangle$:

$$
2|s\rangle (\langle s|\psi\rangle) = 2 \left(\frac{1}{\sqrt{N}}\sum_x |x\rangle\right) (\sqrt{N}\mu) = 2\mu \sum_x |x\rangle
$$

3. Subtract $I|\psi\rangle = \sum_x a_x |x\rangle$:

$$
D|\psi\rangle = \sum_x (2\mu - a_x) |x\rangle
$$

Thus, each amplitude is reflected about the mean: $a_x' = 2\mu - a_x$.

---

### Exercise 2 — Scaling for 10 Qubits ($N = 1024$)
**Problem:**
For an unstructured database with $n = 10$ qubits ($N = 1024$) and a single marked target ($M = 1$):
1. Compute the optimal number of Grover iterations $R$.
2. Compare the number of oracle queries with classical average search.

**Solution:**
1. Number of iterations:

$$
R = \left\lfloor \frac{\pi}{4}\sqrt{N} \right\rfloor = \left\lfloor \frac{\pi}{4}\sqrt{1024} \right\rfloor = \left\lfloor \frac{\pi}{4} \cdot 32 \right\rfloor = \lfloor 8\pi \rfloor = \lfloor 25.1327 \rfloor = 25 \text{ iterations}
$$

2. Classical comparison:
   - Classical average search: $N/2 = 1024 / 2 = 512$ queries.
   - Quantum search: $25$ queries.
   - The quantum algorithm achieves a $\approx 20\times$ speedup at $n=10$, scaling quadratically as $N$ grows ($N=10^6 \implies \approx 785$ quantum queries vs $500,000$ classical queries).

---

## 10. Next Steps

- [Quantum Fourier Transform](quantum-fourier-transform.md) — the spectral engine behind exponential quantum speedups
- [Quantum Phase Estimation](quantum-phase-estimation.md) — estimating eigenvalues and phases with exponential accuracy
- [Deutsch-Jozsa Algorithm](deutsch-jozsa.md) — exact query speedups with Hadamard interference
