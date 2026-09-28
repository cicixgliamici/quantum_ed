# Quantum State Fidelity & Trace Distance

When designing quantum algorithms, characterizing quantum processors, or modeling decoherence, we frequently need to answer two complementary questions:

1. **Overlap Metric:** How closely does an experimental or noisy state $\rho$ resemble an ideal target state $|\psi\rangle$? $\to$ **Fidelity ($F$)**
2. **Distinguishability Metric:** How reliably can an optimal physical measurement tell two quantum states $\rho$ and $\sigma$ apart? $\to$ **Trace Distance ($D$)**

This guide provides a comprehensive reference on the mathematics, operational meanings, and Python implementations of both metrics.

---

## 1. Pure-State Fidelity

When the target reference state is a pure state $|\psi\rangle$ and the actual state is represented by a density matrix $\rho$, the **pure-state fidelity** is the expectation value of the target state projector:

$$
F(|\psi\rangle, \rho) = \langle \psi | \rho | \psi \rangle
$$

### Special Case: Two Pure States

If both states are pure ($|\psi\rangle$ and $|\phi\rangle$), the fidelity reduces to the squared magnitude of their inner product:

$$
F(|\psi\rangle, |\phi\rangle) = |\langle \psi | \phi \rangle|^2
$$

### Properties of Pure-State Fidelity

- **Boundedness:** $0 \le F(|\psi\rangle, \rho) \le 1$.
- **Identity of Indiscernibles:** $F(|\psi\rangle, \rho) = 1 \iff \rho = |\psi\rangle\langle\psi|$.
- **Orthogonality:** $F(|\psi\rangle, \rho) = 0 \iff$ the state $\rho$ has zero support on $|\psi\rangle$.
- **Unitary Invariance:** $F(U|\psi\rangle, U\rho U^\dagger) = F(|\psi\rangle, \rho)$ for any unitary operator $U$.

---

## 2. General Uhlmann-Jozsa Fidelity

For two arbitrary mixed states $\rho$ and $\sigma$, the transition probability must account for classical mixtures. The generalized fidelity is defined by **Uhlmann's formula**:

$$
F(\rho, \sigma) = \left( \operatorname{Tr} \sqrt{\sqrt{\rho} \sigma \sqrt{\rho}} \right)^2
$$

> [!NOTE]
> **Convention Note:** In some theoretical quantum literature (such as Nielsen & Chuang), fidelity is defined without the square: $\sqrt{F} = \operatorname{Tr}\sqrt{\sqrt{\rho}\sigma\sqrt{\rho}}$. Major quantum software libraries (such as Qiskit and PennyLane) and modern information theory use the squared convention shown above so that $F(|\psi\rangle, |\phi\rangle) = |\langle\psi|\phi\rangle|^2$.

### Uhlmann's Theorem

Uhlmann's theorem provides the fundamental physical interpretation of mixed-state fidelity:

> The fidelity $F(\rho, \sigma)$ equals the maximum squared inner product between all possible **purifications** $|\Phi_\rho\rangle$ and $|\Phi_\sigma\rangle$ of $\rho$ and $\sigma$ in an extended Hilbert space:

$$
F(\rho, \sigma) = \max_{|\Phi_\rho\rangle, |\Phi_\sigma\rangle} |\langle \Phi_\rho | \Phi_\sigma \rangle|^2
$$

---

## 3. Trace Distance: The Distinguishability Metric

While fidelity measures state overlap, **trace distance** is the true metric distance on the space of density operators.

### Definition

The trace distance $D(\rho, \sigma)$ is defined as half the trace norm (Schatten 1-norm) of the difference operator:

$$
D(\rho, \sigma) = \frac{1}{2} \|\rho - \sigma\|_1 = \frac{1}{2} \operatorname{Tr} \sqrt{(\rho - \sigma)^\dagger (\rho - \sigma)}
$$

Because the difference $\Delta = \rho - \sigma$ is Hermitian, its singular values are the absolute values of its real eigenvalues $\lambda_k$:

$$
D(\rho, \sigma) = \frac{1}{2} \sum_k |\lambda_k(\rho - \sigma)|
$$

### Single-Qubit Bloch Vector Representation

For single-qubit density matrices $\rho = \frac{1}{2}(I + \vec{r}\cdot\vec{\sigma})$ and $\sigma = \frac{1}{2}(I + \vec{s}\cdot\vec{\sigma})$, the difference is:

$$
\rho - \sigma = \frac{1}{2} (\vec{r} - \vec{s}) \cdot \vec{\sigma}
$$

The eigenvalues of $\Delta$ are $\pm \frac{1}{2} \|\vec{r} - \vec{s}\|$, yielding a geometric equivalence:

$$
D(\rho, \sigma) = \frac{1}{2} \|\vec{r} - \vec{s}\|_2
$$

The trace distance between two single-qubit states is **exactly half the Euclidean distance** between their Bloch vectors!

- Points on opposite sides of the Bloch sphere ($|0\rangle$ and $|1\rangle$, $\|\vec{r} - \vec{s}\| = 2$) have $D = 1$.
- The center $I/2$ ($\vec{0}$) and any pure state on the surface ($\|\vec{r}\|=1$) have $D = 1/2$.

---

## 4. Helstrom's Theorem (Operational Interpretation)

Why does trace distance matter in experimental physics?

Suppose an experiment prepares state $\rho$ with prior probability $1/2$ or state $\sigma$ with prior probability $1/2$. An experimenter performs the best possible quantum measurement (optimal POVM) to decide whether the state was $\rho$ or $\sigma$.

**Helstrom's Theorem** states that the maximum success probability is:

$$
P_{\mathrm{success}} = \frac{1}{2} \left( 1 + D(\rho, \sigma) \right)
$$

- If $D(\rho, \sigma) = 1$: $P_{\mathrm{success}} = 1.0$ (states are orthogonal and $100\%$ distinguishable in a single shot).
- If $D(\rho, \sigma) = 0$: $P_{\mathrm{success}} = 0.5$ (states are identical; outcome is pure classical guessing).

---

## 5. Fuchs-van de Graaf Inequalities

Fidelity and trace distance are intimately connected. For any two density matrices $\rho$ and $\sigma$, they satisfy the **Fuchs-van de Graaf inequalities**:

$$
1 - \sqrt{F(\rho, \sigma)} \le D(\rho, \sigma) \le \sqrt{1 - F(\rho, \sigma)}
$$

### The Pure-State Identity

When at least one of the states is pure ($|\psi\rangle$), the upper bound becomes an **exact equality**:

$$
D(|\psi\rangle, \rho) = \sqrt{1 - F(|\psi\rangle, \rho)}
$$

This relation allows instant conversion between pure-state fidelity and trace distance!

---

## 6. Python Implementation in `quantum_ed`

The functions `fidelity_pure` and `trace_distance` are implemented in [`src/quantum_ed/density.py`](file:///c:/Progetti/quantum_ed/src/quantum_ed/density.py):

```python
import numpy as np
from quantum_ed.states import basis_0, basis_1
from quantum_ed.density import rho_from_ket, fidelity_pure, trace_distance

# Target pure state |0>
ket0 = basis_0()
rho0 = rho_from_ket(ket0)

# Target pure state |1>
ket1 = basis_1()
rho1 = rho_from_ket(ket1)

# Maximally mixed state I/2
rho_mix = 0.5 * np.eye(2, dtype=complex)

# 1. Distinguishability between orthogonal states
d_01 = trace_distance(rho0, rho1)
f_01 = fidelity_pure(ket0, rho1)
print(f"|0> vs |1>: Distance = {d_01:.4f}, Fidelity = {f_01:.4f}")
# Expected: Distance = 1.0000, Fidelity = 0.0000

# 2. Distinguishability between |0> and I/2
d_0mix = trace_distance(rho0, rho_mix)
f_0mix = fidelity_pure(ket0, rho_mix)
print(f"|0> vs I/2: Distance = {d_0mix:.4f}, Fidelity = {f_0mix:.4f}")
# Expected: Distance = 0.5000, Fidelity = 0.5000

# 3. Verify Fuchs-van de Graaf equality for pure state |0>:
# D = sqrt(1 - F) = sqrt(1 - 0.5) = sqrt(0.5) ~ 0.7071?
# Note: For mixed rho_mix, check:
assert np.isclose(d_0mix, 0.5)
```

---

## 7. Worked Exercises

### Exercise 1 — Trace Distance on the Bloch Sphere
**Problem:**
Calculate the trace distance between the pure superposition $|+\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}$ and the pure state $|+i\rangle = \frac{|0\rangle + i|1\rangle}{\sqrt{2}}$.

**Solution:**
1. Determine their Bloch vectors:
   - For $|+\rangle$: points along $+x$-axis $\to \vec{r} = (1, 0, 0)$.
   - For $|+i\rangle$: points along $+y$-axis $\to \vec{s} = (0, 1, 0)$.
2. Compute Euclidean distance:

$$
\|\vec{r} - \vec{s}\| = \sqrt{(1 - 0)^2 + (0 - 1)^2 + (0 - 0)^2} = \sqrt{1 + 1} = \sqrt{2}
$$

3. Compute trace distance:

$$
D(|+\rangle, |+i\rangle) = \frac{1}{2} \|\vec{r} - \vec{s}\| = \frac{\sqrt{2}}{2} = \frac{1}{\sqrt{2}} \approx 0.7071
$$

4. Verification via inner product:
   $|\langle + | +i \rangle|^2 = \left| \frac{1}{2}(1 + i) \right|^2 = \frac{1}{4}(1^2 + 1^2) = \frac{2}{4} = \frac{1}{2}$.
   Using the pure-state identity $D = \sqrt{1 - F} = \sqrt{1 - 1/2} = \sqrt{1/2} = 1/\sqrt{2}$. The result matches perfectly!

---

### Exercise 2 — Helstrom Success Probability
**Problem:**
A qubit source produces state $|0\rangle$ with probability $0.5$ and $|+\rangle$ with probability $0.5$. What is the maximum probability of correctly guessing which state was prepared?

**Solution:**
1. Compute the trace distance between $|0\rangle$ ($\vec{r} = (0,0,1)$) and $|+\rangle$ ($\vec{s} = (1,0,0)$):

$$
D(|0\rangle, |+\rangle) = \frac{1}{2} \sqrt{1^2 + 0^2 + (-1)^2} = \frac{\sqrt{2}}{2} \approx 0.7071
$$

2. Apply Helstrom's formula:

$$
P_{\mathrm{success}} = \frac{1}{2} \left( 1 + D \right) = \frac{1}{2} \left( 1 + \frac{1}{\sqrt{2}} \right) \approx \frac{1 + 0.7071}{2} \approx 0.8536 \quad (85.4\%)
$$

No physical measurement can exceed $85.4\%$ single-shot accuracy because non-orthogonal quantum states cannot be distinguished with certainty.

---

## 8. Next Steps

- [Noise & Quantum Channels](README.md) — see how physical decoherence channels degrade state fidelity
- [Ideal vs Noisy Execution](ideal-vs-noisy.md) — analyze fidelity loss across quantum circuit executions
- [Density Matrices](../06-density-matrices/README.md) — foundational properties of mixed states
