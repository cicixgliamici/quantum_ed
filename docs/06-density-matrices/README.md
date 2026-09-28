# Density Matrices & Quantum Subsystems

The state-vector formalism ($|\psi\rangle \in \mathcal{H}$) is sufficient for closed, isolated quantum systems undergoing ideal unitary dynamics. However, real-world quantum computing requires a more general mathematical framework: the **density operator** (or **density matrix**) formalism.

Density matrices are indispensable whenever:

1. **Statistical ensembles occur:** We face classical uncertainty regarding which quantum state was prepared (e.g., preparation noise).
2. **Subsystems of entangled pairs are inspected:** Individual qubits in an entangled state cannot be described by single kets.
3. **Decoherence and environmental interactions take place:** Non-unitary noise processes transform pure states into mixed states.

---

## 1. Classical Mixtures vs Quantum Superpositions

In classical probability theory, uncertainty is purely epistemological: a system is in a definite state, but our knowledge is incomplete. In pure quantum mechanics, superposition is ontological: a particle simultaneously possesses probability amplitudes for multiple outcomes.

The density operator formalism seamlessly unifies both kinds of uncertainty.

### An Ensemble of Pure States

Suppose a quantum source prepares a system in state $|\psi_i\rangle$ with classical probability $p_i$, forming an ensemble:

$$
\mathcal{E} = \{ (p_i, |\psi_i\rangle) \}, \quad p_i \ge 0, \quad \sum_i p_i = 1
$$

The **density operator** $\rho$ describing this ensemble is:

$$
\rho = \sum_i p_i |\psi_i\rangle \langle \psi_i|
$$

### Pure State vs Classical Mixture

To grasp why density matrices are necessary, compare the quantum superposition $|+\rangle$ with an equal classical mixture of $|0\rangle$ and $|1\rangle$:

1. **Quantum Superposition ($|+\rangle$):**
   A single system prepared in:

$$
|+\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}
$$

   Its density matrix is the rank-1 projector:

$$
\rho_+ = |+\rangle \langle +| = \frac{1}{2} \begin{bmatrix} 1 \\ 1 \end{bmatrix} \begin{bmatrix} 1 & 1 \end{bmatrix} = \begin{bmatrix} 1/2 & 1/2 \\ 1/2 & 1/2 \end{bmatrix}
$$

2. **Classical Mixture ($50\%$ $|0\rangle$, $50\%$ $|1\rangle$):**
   A machine flipping a fair coin and emitting $|0\rangle$ with probability $0.5$ or $|1\rangle$ with probability $0.5$:

$$
\rho_{\mathrm{mix}} = \frac{1}{2}|0\rangle\langle 0| + \frac{1}{2}|1\rangle\langle 1| = \frac{1}{2}\begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix} + \frac{1}{2}\begin{bmatrix} 0 & 0 \\ 0 & 1 \end{bmatrix} = \begin{bmatrix} 1/2 & 0 \\ 0 & 1/2 \end{bmatrix} = \frac{I}{2}
$$

### Physical Distinguishability

Although measuring both states in the computational ($Z$) basis yields $|0\rangle$ with probability $1/2$ and $|1\rangle$ with probability $1/2$, they are **physically distinct quantum states**:

- If measured in the $X$-basis $\{|+\rangle, |-\rangle\}$:
  - For $\rho_+$: The probability of obtaining $|+\rangle$ is $\operatorname{Tr}(|+\rangle\langle +| \rho_+) = 1.0$ (certainty).
  - For $\rho_{\mathrm{mix}}$: The probability of obtaining $|+\rangle$ is $\operatorname{Tr}(|+\rangle\langle +| \rho_{\mathrm{mix}}) = 0.5$ (complete randomness).

The non-zero off-diagonal terms ($\rho_{01} = \rho_{10} = 1/2$) in $\rho_+$ encode **quantum coherence** (relative phase interference). When noise destroys these off-diagonal terms, the superposition decays into a classical mixture.

---

## 2. Fundamental Properties of Density Operators

An operator $\rho$ acting on Hilbert space $\mathcal{H}$ is a physically valid density operator if and only if it satisfies three axioms:

1. **Hermiticity:**

$$
\rho^\dagger = \rho
$$

   Ensures all eigenvalues are real and observables have real expectation values.

2. **Positive Semidefiniteness ($\rho \ge 0$):**
   For all vectors $|\phi\rangle$:

$$
\langle \phi | \rho | \phi \rangle \ge 0
$$

   Equivalently, all eigenvalues $\lambda_k$ of $\rho$ are non-negative ($\lambda_k \ge 0$). This guarantees all measurement probabilities are non-negative.

3. **Unit Trace (Normalization):**

$$
\operatorname{Tr}(\rho) = \sum_k \lambda_k = 1
$$

   Guarantees that total probability across all measurement outcomes sums to 1.

### Expectation Values & Born Rule for Density Matrices

For any observable $A$:

$$
\langle A \rangle = \operatorname{Tr}(A \rho)
$$

**Proof:**
If $\rho = \sum_i p_i |\psi_i\rangle \langle \psi_i|$:

$$
\operatorname{Tr}(A \rho) = \operatorname{Tr}\left( A \sum_i p_i |\psi_i\rangle \langle \psi_i| \right) = \sum_i p_i \operatorname{Tr}(A |\psi_i\rangle \langle \psi_i|) = \sum_i p_i \langle \psi_i | A | \psi_i \rangle
$$

which matches the weighted average of the quantum expectation values.

For a projective measurement described by projectors $\{\Pi_m\}$:
- The probability of obtaining outcome $m$ is:

$$
P(m) = \operatorname{Tr}(\Pi_m \rho)
$$

- The post-measurement state (Lüders rule) is:

$$
\rho' = \frac{\Pi_m \rho \Pi_m}{\operatorname{Tr}(\Pi_m \rho)}
$$

---

## 3. Purity and the Bloch Ball

How can we quantitatively determine whether a density matrix is pure or mixed?

### The Purity Metric

The **purity** $\gamma(\rho)$ of a state $\rho$ is defined as:

$$
\gamma(\rho) = \operatorname{Tr}(\rho^2)
$$

In terms of the eigenvalues $\lambda_k$ of $\rho$:

$$
\gamma(\rho) = \sum_k \lambda_k^2
$$

Since $\lambda_k \ge 0$ and $\sum_k \lambda_k = 1$:

1. **Pure States:** Exactly one eigenvalue equals 1, and all others are 0:

$$
\gamma(\rho) = 1 \iff \rho^2 = \rho \quad (\text{idempotent projector})
$$

2. **Mixed States:** More than one eigenvalue is non-zero:

$$
\frac{1}{d} \le \gamma(\rho) < 1
$$

   where $d = \dim(\mathcal{H})$.

3. **Maximally Mixed State:** All $d$ eigenvalues are equal ($\lambda_k = 1/d$):

$$
\rho = \frac{I}{d} \implies \gamma\left(\frac{I}{d}\right) = \frac{1}{d}
$$

   For a single qubit ($d=2$), the minimum purity is $\gamma = 1/2$.

### The Bloch Ball for Single-Qubit Density Matrices

Any $2 \times 2$ Hermitian matrix with unit trace can be expanded in the orthogonal basis $\{I, X, Y, Z\}$:

$$
\rho = \frac{1}{2} (I + \vec{r} \cdot \vec{\sigma}) = \frac{1}{2} (I + r_x X + r_y Y + r_z Z)
$$

Written explicitly as a matrix:

$$
\rho = \frac{1}{2} \begin{bmatrix} 1 + r_z & r_x - i r_y \\ r_x + i r_y & 1 - r_z \end{bmatrix}
$$

where $\vec{r} = (r_x, r_y, r_z) \in \mathbb{R}^3$ is the **Bloch vector**, with components:

$$
r_x = \operatorname{Tr}(\rho X), \quad r_y = \operatorname{Tr}(\rho Y), \quad r_z = \operatorname{Tr}(\rho Z)
$$

The eigenvalues of $\rho$ are:

$$
\lambda_{1,2} = \frac{1 \pm \|\vec{r}\|}{2}
$$

For $\rho$ to be positive semidefinite ($\lambda_k \ge 0$), we must have:

$$
\|\vec{r}\| = \sqrt{r_x^2 + r_y^2 + r_z^2} \le 1
$$

This defines the **Bloch ball**:

- **$\|\vec{r}\| = 1$:** Lies on the spherical surface $\to$ **pure state** ($\gamma = 1$).
- **$0 < \|\vec{r}\| < 1$:** Lies strictly inside the sphere $\to$ **mixed state** ($\frac{1}{2} < \gamma < 1$).
- **$\|\vec{r}\| = 0$:** Lies at the origin $\vec{r} = (0,0,0) \to$ **maximally mixed state** $\rho = I/2$ ($\gamma = 1/2$).

The purity is directly related to the length of the Bloch vector:

$$
\operatorname{Tr}(\rho^2) = \frac{1 + \|\vec{r}\|^2}{2}
$$

---

## 4. Composite Systems and the Partial Trace

When two quantum systems $A$ and $B$ interact or become entangled, their joint state $\rho_{AB}$ lives in $\mathcal{H}_A \otimes \mathcal{H}_B$. If an experimenter has access only to system $A$, how is the local state of $A$ described?

The answer is the **partial trace**, denoted $\operatorname{Tr}_B(\rho_{AB})$.

### Definition of Partial Trace

The partial trace over subsystem $B$ is the unique linear map $\operatorname{Tr}_B: \mathcal{L}(\mathcal{H}_A \otimes \mathcal{H}_B) \to \mathcal{L}(\mathcal{H}_A)$ that preserves all local measurement statistics:

$$
\operatorname{Tr}( (M_A \otimes I_B) \rho_{AB} ) = \operatorname{Tr}( M_A \rho_A ) \quad \forall M_A
$$

On product operators, it acts as:

$$
\operatorname{Tr}_B(M_A \otimes M_B) = M_A \operatorname{Tr}(M_B)
$$

In an orthonormal basis $\{|k\rangle_B\}$ for subsystem $B$:

$$
\rho_A = \operatorname{Tr}_B(\rho_{AB}) = \sum_{k} (I_A \otimes \langle k|_B) \rho_{AB} (I_A \otimes |k\rangle_B)
$$

### Worked Example: Tracing Out an Entangled Bell State

Consider the maximally entangled Bell pair:

$$
|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}
$$

The global density matrix $\rho_{AB} = |\Phi^+\rangle\langle\Phi^+|$ is pure:

$$
\rho_{AB} = \frac{1}{2} \left( |00\rangle\langle 00| + |00\rangle\langle 11| + |11\rangle\langle 00| + |11\rangle\langle 11| \right)
$$

In matrix representation with basis ordering $|00\rangle, |01\rangle, |10\rangle, |11\rangle$:

$$
\rho_{AB} = \frac{1}{2} \begin{bmatrix}
1 & 0 & 0 & 1 \\
0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 \\
1 & 0 & 0 & 1
\end{bmatrix}
$$

Let us compute the reduced density matrix $\rho_A = \operatorname{Tr}_B(\rho_{AB})$:

$$
\rho_A = \langle 0|_B \rho_{AB} |0\rangle_B + \langle 1|_B \rho_{AB} |1\rangle_B
$$

Evaluating term by term:
- $\langle 0|_B (|00\rangle\langle 00|) |0\rangle_B = |0\rangle\langle 0| (\langle 0|0\rangle)^2 = |0\rangle\langle 0|$
- $\langle 0|_B (|11\rangle\langle 11|) |0\rangle_B = |1\rangle\langle 1| (\langle 0|1\rangle)^2 = 0$
- $\langle 0|_B (|00\rangle\langle 11|) |0\rangle_B = |0\rangle\langle 1| \langle 0|0\rangle \langle 1|0\rangle = 0$
- $\langle 1|_B (|11\rangle\langle 11|) |1\rangle_B = |1\rangle\langle 1|$

Summing the non-zero terms:

$$
\rho_A = \frac{1}{2} |0\rangle\langle 0| + \frac{1}{2} |1\rangle\langle 1| = \begin{bmatrix} 1/2 & 0 \\ 0 & 1/2 \end{bmatrix} = \frac{I}{2}
$$

### The Core Conceptual Insight of Entanglement

This calculation reveals a foundational truth of quantum mechanics:

> **A composite quantum system can be in a state of complete certainty (pure state $\rho_{AB}$, zero entropy), while each of its constituent subsystems is in a state of maximal uncertainty (mixed state $\rho_A = I/2$, maximum entropy).**

In classical mechanics, if you know the exact state of the whole engine, you know the exact state of every gear. In quantum mechanics, bipartite entanglement distributes information into correlations between systems rather than within local systems.

---

## 5. Von Neumann Entropy

To quantify the degree of mixture or quantum entanglement, we use the **von Neumann entropy**.

### Definition

For a density matrix $\rho$ with spectral decomposition $\rho = \sum_k \lambda_k |k\rangle\langle k|$:

$$
S(\rho) = -\operatorname{Tr}(\rho \log_2 \rho) = -\sum_k \lambda_k \log_2 \lambda_k
$$

(By convention, $0 \log_2 0 \equiv 0$).

### Key Properties

1. **Non-negativity:** $S(\rho) \ge 0$, with $S(\rho) = 0$ if and only if $\rho$ is a pure state.
2. **Maximum Entropy:** $S(\rho) \le \log_2 d$, with equality if and only if $\rho = I/d$ (maximally mixed). For a qubit, $S(I/2) = 1$ bit.
3. **Unitary Invariance:** $S(U \rho U^\dagger) = S(\rho)$ for any unitary $U$. Closed system unitary evolution preserves entropy.
4. **Subadditivity:** For any bipartite system:

$$
S(\rho_{AB}) \le S(\rho_A) + S(\rho_B)
$$

   with equality if and only if $\rho_{AB} = \rho_A \otimes \rho_B$ (uncorrelated).
5. **Entanglement Entropy:** For any pure bipartite state $|\psi_{AB}\rangle$, the subsystem entropies are identical:

$$
S(\rho_A) = S(\rho_B)
$$

   This quantity directly measures the degree of bipartite entanglement between $A$ and $B$. For a Bell state, $S(\rho_A) = S(I/2) = 1$ ebit of entanglement.

---

## 6. Distinguishability: Fidelity and Trace Distance

When analyzing quantum noise or validating quantum state preparation, we must measure how close an experimental density matrix $\rho$ is to a target state $\sigma$.

### 1. Pure-State Fidelity

When the target state is pure ($|\psi\rangle$), the fidelity is the expectation value of the target projector:

$$
F(|\psi\rangle, \rho) = \langle \psi | \rho | \psi \rangle
$$

- $F = 1$ if and only if $\rho = |\psi\rangle\langle\psi|$.
- $0 \le F \le 1$.

### 2. General Uhlmann Fidelity

For two arbitrary mixed states $\rho$ and $\sigma$:

$$
F(\rho, \sigma) = \left( \operatorname{Tr} \sqrt{\sqrt{\rho} \sigma \sqrt{\rho}} \right)^2
$$

### 3. Trace Distance

The **trace distance** $D(\rho, \sigma)$ is defined as:

$$
D(\rho, \sigma) = \frac{1}{2} \|\rho - \sigma\|_1 = \frac{1}{2} \operatorname{Tr}\sqrt{(\rho - \sigma)^\dagger (\rho - \sigma)}
$$

Because $\rho - \sigma$ is Hermitian, its singular values are the absolute values of its eigenvalues $\lambda_k(\rho - \sigma)$:

$$
D(\rho, \sigma) = \frac{1}{2} \sum_k |\lambda_k(\rho - \sigma)|
$$

### Operational Interpretation

Trace distance represents the **maximum probability of distinguishing** between two quantum states in a single single-shot measurement:

$$
P_{\mathrm{success}} = \frac{1}{2} \left( 1 + D(\rho, \sigma) \right)
$$

- If $D(\rho, \sigma) = 1$ (orthogonal states), $P_{\mathrm{success}} = 1.0$ (perfect distinguishability).
- If $D(\rho, \sigma) = 0$ (identical states), $P_{\mathrm{success}} = 0.5$ (pure guesswork).

---

## 7. Python Implementation in `quantum_ed`

The repository provides introductory density-matrix and subsystem tools in [`src/quantum_ed/density.py`](file:///c:/Progetti/quantum_ed/src/quantum_ed/density.py):

```python
import numpy as np
from quantum_ed.states import basis_0, basis_1, bell_phi_plus
from quantum_ed.density import (
    rho_from_ket,
    fidelity_pure,
    trace_distance,
    partial_trace_two_qubits,
)

# 1. Construct pure state density matrices
ket_plus = (basis_0() + basis_1()) / np.sqrt(2)
rho_plus = rho_from_ket(ket_plus)

# 2. Construct mixed state (50/50 mixture)
rho_mix = 0.5 * rho_from_ket(basis_0()) + 0.5 * rho_from_ket(basis_1())

# 3. Check distinguishability via Trace Distance
d = trace_distance(rho_plus, rho_mix)
print(f"Trace distance: {d:.4f}")  # 0.5000

# 4. Partial trace on Bell state |Phi+>
phi_plus = bell_phi_plus()
rho_bell = rho_from_ket(phi_plus)

# Keep qubit 0 (trace out qubit 1)
rho_A = partial_trace_two_qubits(rho_bell, keep=0)
print("Reduced state rho_A:\n", rho_A)
# Output is [[0.5, 0.0], [0.0, 0.5]] (I/2)

# Check fidelity with |0>
f0 = fidelity_pure(basis_0(), rho_A)
print(f"Fidelity <0|rho_A|0>: {f0:.4f}")  # 0.5000
```

---

## 8. Worked Exercises

### Exercise 1 — Density Matrix of $|-\rangle$ vs Diagonal Mixture

**Problem:**
1. Compute the density matrix $\rho_-$ of $|-\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}}$.
2. Compare its diagonal and off-diagonal elements with $\rho_{\mathrm{mix}} = \frac{1}{2}I$.

**Solution:**

$$
\rho_- = |-\rangle\langle -| = \frac{1}{2} \begin{bmatrix} 1 \\ -1 \end{bmatrix} \begin{bmatrix} 1 & -1 \end{bmatrix} = \begin{bmatrix} 1/2 & -1/2 \\ -1/2 & 1/2 \end{bmatrix}
$$

- The diagonal elements are $\rho_{00} = 1/2$ and $\rho_{11} = 1/2$, identical to $\rho_{\mathrm{mix}}$.
- The off-diagonal coherence terms are $\rho_{01} = \rho_{10} = -1/2$. In $\rho_{\mathrm{mix}}$, these terms are $0$.
- The relative minus sign ($e^{i\pi}$) is completely stored in the off-diagonal coherence!

---

### Exercise 2 — Purity of a Parameterized State

**Problem:**
Let $\rho(p) = (1-p)|0\rangle\langle 0| + p \frac{I}{2}$ for $p \in [0, 1]$.
Compute the purity $\gamma(p) = \operatorname{Tr}(\rho^2)$ and find its minimum.

**Solution:**
Write $\rho(p)$ in matrix form:

$$
\rho(p) = (1-p) \begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix} + \frac{p}{2} \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} = \begin{bmatrix} 1 - \frac{p}{2} & 0 \\ 0 & \frac{p}{2} \end{bmatrix}
$$

Compute $\rho^2$:

$$
\rho^2 = \begin{bmatrix} \left(1 - \frac{p}{2}\right)^2 & 0 \\ 0 & \left(\frac{p}{2}\right)^2 \end{bmatrix}
$$

Taking the trace:

$$
\gamma(p) = \operatorname{Tr}(\rho^2) = \left(1 - \frac{p}{2}\right)^2 + \frac{p^2}{4} = 1 - p + \frac{p^2}{4} + \frac{p^2}{4} = 1 - p + \frac{p^2}{2}
$$

- At $p = 0$: $\gamma(0) = 1$ (pure state $|0\rangle$).
- At $p = 1$: $\gamma(1) = 1/2$ (maximally mixed state $I/2$).
- The derivative $\frac{d\gamma}{dp} = -1 + p = 0 \implies p = 1$, so the minimum purity is indeed $1/2$ at $p=1$.

---

### Exercise 3 — Partial Trace of the Singlet State

**Problem:**
Given the singlet state $|\Psi^-\rangle = \frac{|01\rangle - |10\rangle}{\sqrt{2}}$, show that $\operatorname{Tr}_B(|\Psi^-\rangle\langle \Psi^-|) = \frac{I}{2}$.

**Solution:**
The full density operator is:

$$
\rho_{AB} = \frac{1}{2} \left( |01\rangle\langle 01| - |01\rangle\langle 10| - |10\rangle\langle 01| + |10\rangle\langle 10| \right)
$$

Tracing out subsystem $B$:

$$
\rho_A = \langle 0|_B \rho_{AB} |0\rangle_B + \langle 1|_B \rho_{AB} |1\rangle_B
$$

- Projecting with $\langle 0|_B$:
  The only terms with $|0\rangle_B$ on the right and left are $|10\rangle\langle 10|$:

$$
\langle 0|_B \rho_{AB} |0\rangle_B = \frac{1}{2} |1\rangle\langle 1|
$$

- Projecting with $\langle 1|_B$:
  The only terms with $|1\rangle_B$ on the right and left are $|01\rangle\langle 01|$:

$$
\langle 1|_B \rho_{AB} |1\rangle_B = \frac{1}{2} |0\rangle\langle 0|
$$

Combining both terms gives:

$$
\rho_A = \frac{1}{2} |0\rangle\langle 0| + \frac{1}{2} |1\rangle\langle 1| = \frac{I}{2}
$$

---

### Exercise 4 — Bloch Vector Calculation

**Problem:**
Given the density matrix:

$$
\rho = \begin{bmatrix} 3/4 & 1/4 \\ 1/4 & 1/4 \end{bmatrix}
$$

1. Verify that $\rho$ is a valid density matrix.
2. Find its Bloch vector $\vec{r}$.
3. Calculate its purity and verify that $\|\vec{r}\| \le 1$.

**Solution:**
1. Validity:
   - $\rho^\dagger = \rho$ (symmetric and real $\implies$ Hermitian).
   - $\operatorname{Tr}(\rho) = 3/4 + 1/4 = 1$.
   - Eigenvalues: characteristic equation $\det(\rho - \lambda I) = (3/4 - \lambda)(1/4 - \lambda) - 1/16 = \lambda^2 - \lambda + 2/16 = 0$.
     Roots are $\lambda = \frac{1 \pm \sqrt{1 - 1/2}}{2} = \frac{1 \pm 1/\sqrt{2}}{2} \approx 0.8536$ and $0.1464$. Both $\lambda_i \ge 0$, so $\rho \ge 0$.
2. Bloch vector components:
   - $r_z = \rho_{00} - \rho_{11} = 3/4 - 1/4 = 1/2$.
   - $r_x = \rho_{01} + \rho_{10} = 1/4 + 1/4 = 1/2$.
   - $r_y = i(\rho_{01} - \rho_{10}) = i(1/4 - 1/4) = 0$.
   Therefore, $\vec{r} = (1/2, 0, 1/2)$.
3. Length and purity:
   - $\|\vec{r}\|^2 = (1/2)^2 + 0^2 + (1/2)^2 = 1/4 + 1/4 = 1/2 \implies \|\vec{r}\| = 1/\sqrt{2} \approx 0.7071 \le 1$.
   - Purity $\gamma = \frac{1 + \|\vec{r}\|^2}{2} = \frac{1 + 1/2}{2} = 3/4 = 0.75$.
   - Directly from matrix: $\operatorname{Tr}(\rho^2) = (3/4)^2 + 2(1/4)^2 + (1/4)^2 = 9/16 + 2/16 + 1/16 = 12/16 = 3/4$. Exact match!

---

## 9. Next Steps

- [Noise & Quantum Channels](../07-noise-and-channels/README.md) — see how physical noise transforms density matrices via Kraus operators
- [Fidelity & Trace Distance](../07-noise-and-channels/FIDELITY.md) — deep dive into state distance geometry
- [Quantum Hardware](../08-hardware/README.md) — understand physical relaxation ($T_1$) and dephasing ($T_2$) mechanisms
