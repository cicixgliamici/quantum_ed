# Noise & Quantum Channels

In textbook quantum mechanics, quantum systems are often treated as completely closed, evolving strictly under unitary operators ($|\psi'\rangle = U|\psi\rangle$). However, real-world quantum hardware is an **open quantum system**: physical qubits inevitably interact with their surrounding environment (thermal baths, stray electromagnetic fields, material defects, and control line fluctuations).

These environmental interactions introduce **noise, decoherence, and dissipation**, which degrade quantum information. To mathematically model, analyze, and mitigate these effects, quantum computing uses the framework of **quantum channels** and **completely positive trace-preserving (CPTP) maps**.

---

## 1. Closed vs Open Quantum Systems

The distinction between ideal and real quantum evolution is summarized below:

| Feature | Closed Quantum System | Open Quantum System |
| :--- | :--- | :--- |
| **Mathematical State** | State vector $|\psi\rangle \in \mathcal{H}$ | Density matrix $\rho \in \mathcal{L}(\mathcal{H})$ |
| **Dynamical Map** | Unitary transformation $\rho \mapsto U \rho U^\dagger$ | Quantum channel $\rho \mapsto \mathcal{E}(\rho)$ |
| **Energy Exchange** | Strictly conserved | Dissipation & relaxation into environment |
| **Coherence & Entropy** | Entropy is invariant ($S(\rho) = \text{const}$) | Purity decreases; entropy increases |
| **Reversibility** | Strictly reversible ($U^{-1} = U^\dagger$) | Irreversible in general |

### Stinespring Dilation: How Noise Arises

Every open quantum system can be understood as part of a larger closed system composed of the system of interest $S$ and an uncontrolled environment (or reservoir) $E$.

Suppose the system starts in state $\rho$ and the environment in a fiducial state $|e_0\rangle_E$. The joint system undergoes unitary evolution $U_{SE}$. Tracing out the inaccessible environment leaves the system in a noisy reduced state:

$$
\mathcal{E}(\rho) = \operatorname{Tr}_E \left( U_{SE} (\rho \otimes |e_0\rangle\langle e_0|_E) U_{SE}^\dagger \right)
$$

This result, known as the **Stinespring Dilation Theorem**, proves that every physically realizable noise process is mathematically equivalent to unitary interaction with an environment followed by partial trace.

---

## 2. The Kraus Operator-Sum Representation

Computing the full system-environment unitary is usually intractable. The **Kraus representation** allows us to describe the dynamics of system $S$ alone without explicitly tracking environmental states.

Let $\{|e_k\rangle_E\}$ be an orthonormal basis for the environment Hilbert space $\mathcal{H}_E$. Expanding the partial trace yields:

$$
\mathcal{E}(\rho) = \sum_k \langle e_k|_E U_{SE} |e_0\rangle_E \rho \langle e_0|_E U_{SE}^\dagger |e_k\rangle_E
$$

Defining the **Kraus operators** (or measurement operators) acting on $\mathcal{H}_S$:

$$
K_k \equiv \langle e_k|_E U_{SE} |e_0\rangle_E
$$

we arrive at the **operator-sum representation**:

$$
\mathcal{E}(\rho) = \sum_k K_k \rho K_k^\dagger
$$

### Completeness Relation (Trace Preservation)

For the channel $\mathcal{E}$ to preserve total probability ($\operatorname{Tr}(\mathcal{E}(\rho)) = 1$ for all $\rho$ with $\operatorname{Tr}(\rho) = 1$), the Kraus operators must satisfy the **completeness relation**:

$$
\sum_k K_k^\dagger K_k = I_S
$$

**Proof:**

$$
\operatorname{Tr}(\mathcal{E}(\rho)) = \operatorname{Tr}\left( \sum_k K_k \rho K_k^\dagger \right) = \sum_k \operatorname{Tr}(K_k \rho K_k^\dagger) = \sum_k \operatorname{Tr}(K_k^\dagger K_k \rho) = \operatorname{Tr}\left( \left(\sum_k K_k^\dagger K_k\right) \rho \right) = \operatorname{Tr}(\rho) = 1
$$

Any linear map $\mathcal{E}$ that admits an operator-sum representation satisfying $\sum_k K_k^\dagger K_k = I$ is **completely positive and trace-preserving (CPTP)**.

---

## 3. Canonical Single-Qubit Noise Channels

Physical noise on a single qubit is categorized into discrete Pauli errors, isotropic depolarization, pure dephasing, and energy relaxation.

### 1. The Bit-Flip Channel

The bit-flip channel models classical bit inversions: with probability $p$, a Pauli-$X$ gate is applied, flipping $|0\rangle \leftrightarrow |1\rangle$; with probability $(1-p)$, the qubit is untouched.

- **Kraus Operators:**

$$
K_0 = \sqrt{1-p} \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}, \quad K_1 = \sqrt{p} \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}
$$

- **Completeness:**

$$
K_0^\dagger K_0 + K_1^\dagger K_1 = (1-p)I + p X^2 = (1-p)I + pI = I
$$

- **Action on Density Matrix:**

$$
\mathcal{E}_{\mathrm{BF}}(\rho) = (1-p)\rho + p X \rho X = \begin{bmatrix}
(1-p)\rho_{00} + p\rho_{11} & (1-p)\rho_{01} + p\rho_{10} \\
(1-p)\rho_{10} + p\rho_{01} & (1-p)\rho_{11} + p\rho_{00}
\end{bmatrix}
$$

### 2. The Phase-Flip Channel

The phase-flip channel models phase randomization: with probability $p$, a Pauli-$Z$ gate is applied, flipping the relative phase $|1\rangle \mapsto -|1\rangle$; with probability $(1-p)$, the qubit is unaffected.

- **Kraus Operators:**

$$
K_0 = \sqrt{1-p} I, \quad K_1 = \sqrt{p} Z
$$

- **Action on Density Matrix:**

$$
\mathcal{E}_{\mathrm{PF}}(\rho) = (1-p)\rho + p Z \rho Z = \begin{bmatrix}
\rho_{00} & (1-2p)\rho_{01} \\
(1-2p)\rho_{10} & \rho_{11}
\end{bmatrix}
$$

Notice that the diagonal populations remain strictly unchanged, while the off-diagonal coherences are attenuated by a factor of $(1-2p)$. When $p=1/2$, the coherences vanish completely.

### 3. The Pure Dephasing Channel

In physical implementations (e.g. superconducting transmons), environmental fluctuations cause low-frequency shifts in qubit transition frequencies, causing the relative phase $\phi$ to diffuse continuously.

A general dephasing channel with dephasing parameter $\lambda \in [0, 1]$ acts as:

$$
\mathcal{E}_{\mathrm{dephase}}(\rho) = \begin{bmatrix}
\rho_{00} & (1-\lambda)\rho_{01} \\
(1-\lambda)\rho_{10} & \rho_{11}
\end{bmatrix}
$$

- For $\lambda = 0$: Identity map (no dephasing).
- For $\lambda = 1$: Complete dephasing ($\rho \to \operatorname{diag}(\rho_{00}, \rho_{11})$), completely converting a quantum superposition into a classical statistical mixture.
- **Bloch Sphere Geometry:** Dephasing contracts the Bloch sphere into an ellipsoid along the $x$ and $y$ axes with radius $(1-\lambda)$, leaving the $z$-axis untouched: $\vec{r} = (r_x, r_y, r_z) \mapsto ((1-\lambda)r_x, (1-\lambda)r_y, r_z)$.

### 4. The Depolarizing Channel

The depolarizing channel represents isotropic, worst-case decoherence. With probability $(1-p)$, the qubit survives intact; with probability $p$, it is degraded into the maximally mixed state $I/2$:

$$
\mathcal{E}_{\mathrm{dep}}(\rho) = (1-p)\rho + p \frac{I}{2}
$$

Equivalently, it can be expressed in terms of symmetric Pauli errors:

$$
\mathcal{E}_{\mathrm{dep}}(\rho) = \left(1 - \frac{3p}{4}\right)\rho + \frac{p}{4} (X\rho X + Y\rho Y + Z\rho Z)
$$

- **Kraus Operators:**

$$
K_0 = \sqrt{1 - \frac{3p}{4}} I, \quad K_1 = \frac{\sqrt{p}}{2} X, \quad K_2 = \frac{\sqrt{p}}{2} Y, \quad K_3 = \frac{\sqrt{p}}{2} Z
$$

- **Bloch Sphere Geometry:** The entire Bloch ball is scaled uniformly toward the origin:

$$
\vec{r} \mapsto (1-p)\vec{r}
$$

  Every point inside or on the surface of the sphere shrinks isotropically.

### 5. The Amplitude Damping Channel (Energy Relaxation)

Unlike the previous channels, amplitude damping is **non-unital** ($\mathcal{E}(I) \neq I$). It models physical dissipation: the spontaneous decay of an excited state $|1\rangle$ to the ground state $|0\rangle$ via emission of an energy quantum (photon or phonon) into a cold environment at $T = 0$ K.

- **Kraus Operators:**
  With decay probability $\gamma \in [0, 1]$:

$$
K_0 = \begin{bmatrix} 1 & 0 \\ 0 & \sqrt{1-\gamma} \end{bmatrix}, \quad K_1 = \begin{bmatrix} 0 & \sqrt{\gamma} \\ 0 & 0 \end{bmatrix}
$$

  Notice the physical interpretation:
  - $K_1 = \sqrt{\gamma} |0\rangle\langle 1|$ represents the physical jump from $|1\rangle \to |0\rangle$.
  - $K_0$ represents the no-jump evolution (monitoring that decay has not yet occurred).

- **Completeness:**

$$
K_0^\dagger K_0 + K_1^\dagger K_1 = \begin{bmatrix} 1 & 0 \\ 0 & 1-\gamma \end{bmatrix} + \begin{bmatrix} 0 & 0 \\ 0 & \gamma \end{bmatrix} = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} = I
$$

- **Action on Density Matrix:**

$$
\mathcal{E}_{\mathrm{AD}}(\rho) = K_0 \rho K_0^\dagger + K_1 \rho K_1^\dagger = \begin{bmatrix}
\rho_{00} + \gamma \rho_{11} & \sqrt{1-\gamma}\rho_{01} \\
\sqrt{1-\gamma}\rho_{10} & (1-\gamma)\rho_{11}
\end{bmatrix}
$$

Notice that as $\gamma \to 1$ (long time limit), any initial state $\rho$ converges unconditionally to the pure ground state $|0\rangle\langle 0|$:

$$
\lim_{\gamma \to 1} \mathcal{E}_{\mathrm{AD}}(\rho) = \begin{bmatrix} \rho_{00} + \rho_{11} & 0 \\ 0 & 0 \end{bmatrix} = \begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix} = |0\rangle\langle 0|
$$

---

## 4. Physical Relaxation Times: $T_1$, $T_2$, and the Coherence Limit

In physical hardware characterization, noise channels are parameterized by characteristic relaxation timescales:

### $T_1$ — Longitudinal Relaxation Time

$T_1$ measures how long an excited qubit stays in $|1\rangle$ before decaying into $|0\rangle$ through energy dissipation:

$$
\rho_{11}(t) = \rho_{11}(0) e^{-t / T_1}
$$

The decay parameter in amplitude damping is related to time by:

$$
\gamma(t) = 1 - e^{-t / T_1}
$$

### $T_2$ — Transverse Coherence Time

$T_2$ measures how long quantum superpositions and relative phases persist before decohering:

$$
\rho_{01}(t) = \rho_{01}(0) e^{-t / T_2}
$$

### The Fundamental Coherence Relation

Coherence decay arises from two distinct physical sources:
1. **Energy relaxation ($T_1$):** When an excited state decays, its phase relationship is also destroyed.
2. **Pure dephasing ($T_\phi$):** Fluctuations in environmental fields randomize phase without exchanging energy.

The total dephasing rate is the sum of the pure dephasing rate and half the energy decay rate:

$$
\frac{1}{T_2} = \frac{1}{2T_1} + \frac{1}{T_\phi}
$$

Since the pure dephasing rate is always non-negative ($1/T_\phi \ge 0$), this establishes the **fundamental physical bound on quantum coherence**:

$$
T_2 \le 2 T_1
$$

In an ideal device with zero pure dephasing ($T_\phi \to \infty$), the coherence time reaches its theoretical upper limit: $T_2 = 2T_1$. In current NISQ hardware, typical transmon processors exhibit $T_1 \approx 50\text{--}150\ \mu\text{s}$ and $T_2 \approx 40\text{--}120\ \mu\text{s}$.

---

## 5. Noise and Channel Implementation in `quantum_ed`

The repository implements standard single-qubit noise channels in [`src/quantum_ed/channels.py`](file:///c:/Progetti/quantum_ed/src/quantum_ed/channels.py) and metrics in [`src/quantum_ed/density.py`](file:///c:/Progetti/quantum_ed/src/quantum_ed/density.py):

```python
import numpy as np
from quantum_ed.states import basis_0, basis_1
from quantum_ed.density import rho_from_ket, fidelity_pure
from quantum_ed.channels import (
    depolarize_rho,
    dephase_rho,
    bit_flip_rho,
    phase_flip_rho,
    amplitude_damp_rho,
)

# Prepare pure superposition |+>
ket_plus = (basis_0() + basis_1()) / np.sqrt(2)
rho_plus = rho_from_ket(ket_plus)

# 1. Apply Dephasing with strength p = 0.3
rho_dephased = dephase_rho(rho_plus, p=0.3)
print("Dephased rho:\n", rho_dephased)
# Off-diagonal elements drop from 0.5 to 0.5 * (1 - 0.3) = 0.35

# 2. Check fidelity degradation
f_dephased = fidelity_pure(ket_plus, rho_dephased)
print(f"Fidelity after dephasing: {f_dephased:.4f}")  # 0.8500

# 3. Apply Amplitude Damping to |1> with decay probability p = 0.5
rho_1 = rho_from_ket(basis_1())
rho_relaxed = amplitude_damp_rho(rho_1, p=0.5)
print("Amplitude damped |1><1|:\n", rho_relaxed)
# Diagonal is [[0.5, 0], [0, 0.5]]

# Check ground state population
f_ground = fidelity_pure(basis_0(), rho_relaxed)
print(f"Ground state population: {f_ground:.4f}")  # 0.5000
```

---

## 6. Worked Exercises

### Exercise 1 — Full Depolarization
**Problem:**
Calculate the output state $\mathcal{E}_{\mathrm{dep}}(|0\rangle\langle 0|)$ under full depolarizing noise with $p=1$.

**Solution:**
Using the depolarizing channel definition:

$$
\mathcal{E}_{\mathrm{dep}}(\rho) = (1-p)\rho + p \frac{I}{2}
$$

Substitute $p = 1$:

$$
\mathcal{E}_{\mathrm{dep}}(|0\rangle\langle 0|) = 0 \cdot |0\rangle\langle 0| + 1 \cdot \frac{I}{2} = \frac{I}{2} = \begin{bmatrix} 1/2 & 0 \\ 0 & 1/2 \end{bmatrix}
$$

The qubit has completely lost its initial state and decayed into the maximally mixed state.

---

### Exercise 2 — Dephasing Coherence Loss
**Problem:**
Let $\rho = |+\rangle\langle +|$. Compute the output under pure dephasing $\mathcal{E}_{\mathrm{dephase}}$ with parameter $p$. Compute the fidelity $F(|+\rangle, \mathcal{E}(\rho))$ as a function of $p$.

**Solution:**

$$
\rho = \frac{1}{2} \begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}
$$

Under dephasing with strength $p$:

$$
\mathcal{E}(\rho) = \frac{1}{2} \begin{bmatrix} 1 & 1-p \\ 1-p & 1 \end{bmatrix}
$$

The fidelity with the pure target $|+\rangle$ is:

$$
F(|+\rangle, \mathcal{E}(\rho)) = \langle +| \mathcal{E}(\rho) |+\rangle = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \end{bmatrix} \frac{1}{2} \begin{bmatrix} 1 & 1-p \\ 1-p & 1 \end{bmatrix} \frac{1}{\sqrt{2}} \begin{bmatrix} 1 \\ 1 \end{bmatrix}
$$

$$
= \frac{1}{4} \begin{bmatrix} 1 & 1 \end{bmatrix} \begin{bmatrix} 2-p \\ 2-p \end{bmatrix} = \frac{1}{4} (4 - 2p) = 1 - \frac{p}{2}
$$

- For $p=0$: Fidelity is 1.0 (no noise).
- For $p=1$: Fidelity drops to $1 - 1/2 = 0.5$.

---

### Exercise 3 — Amplitude Damping on Ground vs Excited State
**Problem:**
Compute $\mathcal{E}_{\mathrm{AD}}(|0\rangle\langle 0|)$ and $\mathcal{E}_{\mathrm{AD}}(|1\rangle\langle 1|)$ for arbitrary decay probability $\gamma \in [0, 1]$.

**Solution:**
Using the amplitude damping map:

$$
\mathcal{E}_{\mathrm{AD}}(\rho) = \begin{bmatrix} \rho_{00} + \gamma \rho_{11} & \sqrt{1-\gamma}\rho_{01} \\ \sqrt{1-\gamma}\rho_{10} & (1-\gamma)\rho_{11} \end{bmatrix}
$$

1. For ground state $|0\rangle\langle 0|$ ($\rho_{00}=1, \rho_{11}=0$):

$$
\mathcal{E}_{\mathrm{AD}}(|0\rangle\langle 0|) = \begin{bmatrix} 1 + 0 & 0 \\ 0 & 0 \end{bmatrix} = |0\rangle\langle 0|
$$

   The ground state is a stationary state (fixed point) of amplitude damping because it has zero excess energy to dissipate.

2. For excited state $|1\rangle\langle 1|$ ($\rho_{00}=0, \rho_{11}=1$):

$$
\mathcal{E}_{\mathrm{AD}}(|1\rangle\langle 1|) = \begin{bmatrix} \gamma & 0 \\ 0 & 1-\gamma \end{bmatrix} = \gamma |0\rangle\langle 0| + (1-\gamma) |1\rangle\langle 1|
$$

   When $\gamma = 1$, the excited state decays completely to the ground state $|0\rangle\langle 0|$.

---

### Exercise 4 — Phase-Flip Channel Kraus Representation
**Problem:**
Verify that the Kraus operators for the phase-flip channel satisfy the completeness relation $\sum_k K_k^\dagger K_k = I$.

**Solution:**
The Kraus operators are $K_0 = \sqrt{1-p} I$ and $K_1 = \sqrt{p} Z$.
Compute:

$$
K_0^\dagger K_0 = (\sqrt{1-p} I)^\dagger (\sqrt{1-p} I) = (1-p) I
$$

$$
K_1^\dagger K_1 = (\sqrt{p} Z)^\dagger (\sqrt{p} Z) = p Z^\dagger Z = p Z^2
$$

Since $Z^2 = I$:

$$
K_0^\dagger K_0 + K_1^\dagger K_1 = (1-p) I + p I = I
$$

Completeness is satisfied for all $p \in [0, 1]$.

---

## 7. Next Steps

- [Fidelity & Trace Distance](FIDELITY.md) — explore mathematical geometry and state overlap metrics
- [Ideal vs Noisy Execution](ideal-vs-noisy.md) — study the practical degradation of quantum algorithm circuits under noise
- [Hardware Overview](../08-hardware/README.md) — understand physical qubit implementations and actual experimental $T_1$ and $T_2$ times
