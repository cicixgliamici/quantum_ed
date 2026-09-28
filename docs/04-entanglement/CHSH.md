# The CHSH Inequality & Bell Non-Locality

The **CHSH inequality**, formulated in 1969 by John Clauser, Michael Horne, Abner Shimony, and Richard Holt, is the definitive experimental protocol used to test **Bell's theorem**. It provides a rigorous, testable criterion to distinguish between:

1. **Local Realism (Classical Physics):** The worldview that physical systems possess definite, pre-existing properties independent of measurement, and that no signal or physical effect can travel faster than the speed of light.
2. **Quantum Mechanics:** The reality that entangled particles exhibit non-local correlations that cannot be explained by any local hidden-variable (LHV) theory.

The experimental violation of Bell inequalities earned Alain Aspect, John Clauser, and Anton Zeilinger the **2022 Nobel Prize in Physics**.

---

## 1. The Experimental Setup: The CHSH Game

Imagine two space-like separated observers, **Alice** and **Bob**, who share an entangled pair of particles (such as two polarization-entangled photons).

```text
               ┌──────────────┐
               │ Alice's Lab  │ ◄──── Qubit A ────┐
               └──────────────┘                   │
                                          ┌───────┴───────┐
                                          │ Source: |Φ⁺⟩  │
                                          └───────┬───────┘
               ┌──────────────┐                   │
               │  Bob's Lab   │ ◄──── Qubit B ────┘
               └──────────────┘
```

1. Alice randomly chooses between two measurement settings, labeled by input $x \in \{0, 1\}$, measuring observable $A_x \in \{A_0, A_1\}$.
2. Bob independently and randomly chooses between two measurement settings, labeled by input $y \in \{0, 1\}$, measuring observable $B_y \in \{B_0, B_1\}$.
3. Each measurement produces a binary outcome $a, b \in \{-1, +1\}$.

The correlation (expectation value) between Alice's and Bob's measurements for a given setting pair $(x, y)$ is:

$$
E(A_x, B_y) = \langle A_x \otimes B_y \rangle = P(a = b | x, y) - P(a \neq b | x, y)
$$

The **CHSH correlator** $S$ is defined as the linear combination:

$$
S = E(A_0, B_0) + E(A_0, B_1) + E(A_1, B_0) - E(A_1, B_1)
$$

Notice the negative sign on the final term: it acts as a test of whether the correlations can satisfy all four conditions simultaneously.

---

## 2. The Classical Bound: $|S| \le 2$

Under the hypothesis of **local realism**, the measurement outcomes are determined by some underlying hidden variable $\lambda$, distributed according to a probability density $\rho(\lambda) \ge 0$ with $\int \rho(\lambda) d\lambda = 1$:

- Alice's outcome $A(x, \lambda) \in \{-1, +1\}$ depends only on her setting $x$ and $\lambda$.
- Bob's outcome $B(y, \lambda) \in \{-1, +1\}$ depends only on his setting $y$ and $\lambda$.

### Proof of the Classical Bound

Consider the algebraic quantity for a single deterministic instance with fixed $\lambda$:

$$
C(\lambda) = A_0 B_0 + A_0 B_1 + A_1 B_0 - A_1 B_1
$$

Factor out Alice's values:

$$
C(\lambda) = A_0 (B_0 + B_1) + A_1 (B_0 - B_1)
$$

Because $B_0, B_1 \in \{-1, +1\}$, there are only two possibilities:

1. **If $B_0 = B_1$:** Then $(B_0 + B_1) = \pm 2$, while $(B_0 - B_1) = 0$:

$$
C(\lambda) = A_0 (\pm 2) + A_1 (0) = \pm 2
$$

2. **If $B_0 \neq B_1$:** Then $(B_0 + B_1) = 0$, while $(B_0 - B_1) = \pm 2$:

$$
C(\lambda) = A_0 (0) + A_1 (\pm 2) = \pm 2
$$

In all cases, for every individual particle pair:

$$
C(\lambda) \in \{-2, +2\} \implies |C(\lambda)| \le 2
$$

Integrating over the hidden-variable probability distribution:

$$
S_{\mathrm{classical}} = \int C(\lambda) \rho(\lambda) d\lambda \implies |S_{\mathrm{classical}}| \le \int |C(\lambda)| \rho(\lambda) d\lambda \le 2 \int \rho(\lambda) d\lambda = 2
$$

This is the **CHSH inequality**: any theory based on local realism strictly obeys:

$$
|S| \le 2
$$

---

## 3. Quantum Violation: Reaching $2\sqrt{2}$

Quantum mechanics violates the CHSH inequality by utilizing quantum entanglement and non-commuting observables.

### The Quantum State

Alice and Bob share the maximally entangled Bell pair:

$$
|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}
$$

### Optimal Measurement Bases

To maximize the CHSH correlator, Alice and Bob measure along mutually unbiased directions on the Bloch sphere equator/meridian:

**Alice's Observables:**

$$
A_0 = Z = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}, \qquad A_1 = X = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}
$$

**Bob's Observables (Rotated by $45^\circ$ relative to Alice):**

$$
B_0 = \frac{Z + X}{\sqrt{2}}, \qquad B_1 = \frac{Z - X}{\sqrt{2}}
$$

### Computing the Correlation Terms

Recall the expectation values of Pauli pairs on $|\Phi^+\rangle$:
- $\langle \Phi^+ | Z \otimes Z | \Phi^+ \rangle = 1$
- $\langle \Phi^+ | X \otimes X | \Phi^+ \rangle = 1$
- $\langle \Phi^+ | Z \otimes X | \Phi^+ \rangle = 0$
- $\langle \Phi^+ | X \otimes Z | \Phi^+ \rangle = 0$

Now evaluate each of the four terms in the CHSH operator:

1. **Term 1:**

$$
E(A_0, B_0) = \left\langle \Phi^+ \left| Z \otimes \frac{Z + X}{\sqrt{2}} \right| \Phi^+ \right\rangle = \frac{1}{\sqrt{2}} \left( \langle Z \otimes Z \rangle + \langle Z \otimes X \rangle \right) = \frac{1 + 0}{\sqrt{2}} = \frac{1}{\sqrt{2}}
$$

2. **Term 2:**

$$
E(A_0, B_1) = \left\langle \Phi^+ \left| Z \otimes \frac{Z - X}{\sqrt{2}} \right| \Phi^+ \right\rangle = \frac{1}{\sqrt{2}} \left( \langle Z \otimes Z \rangle - \langle Z \otimes X \rangle \right) = \frac{1 - 0}{\sqrt{2}} = \frac{1}{\sqrt{2}}
$$

3. **Term 3:**

$$
E(A_1, B_0) = \left\langle \Phi^+ \left| X \otimes \frac{Z + X}{\sqrt{2}} \right| \Phi^+ \right\rangle = \frac{1}{\sqrt{2}} \left( \langle X \otimes Z \rangle + \langle X \otimes X \rangle \right) = \frac{0 + 1}{\sqrt{2}} = \frac{1}{\sqrt{2}}
$$

4. **Term 4:**

$$
E(A_1, B_1) = \left\langle \Phi^+ \left| X \otimes \frac{Z - X}{\sqrt{2}} \right| \Phi^+ \right\rangle = \frac{1}{\sqrt{2}} \left( \langle X \otimes Z \rangle - \langle X \otimes X \rangle \right) = \frac{0 - 1}{\sqrt{2}} = -\frac{1}{\sqrt{2}}
$$

### The Quantum Value of $S$

Summing all four terms:

$$
S_{\mathrm{quantum}} = E(A_0, B_0) + E(A_0, B_1) + E(A_1, B_0) - E(A_1, B_1)
$$

$$
S_{\mathrm{quantum}} = \frac{1}{\sqrt{2}} + \frac{1}{\sqrt{2}} + \frac{1}{\sqrt{2}} - \left( -\frac{1}{\sqrt{2}} \right) = \frac{4}{\sqrt{2}} = 2\sqrt{2} \approx 2.8284
$$

Because $2\sqrt{2} > 2$, **quantum mechanics strictly violates the CHSH inequality**.

---

## 4. Tsirelson's Bound

Can a physical theory produce an even larger violation, up to the algebraic maximum of $S = 4$?

In 1980, Soviet-Israeli mathematician Boris Tsirelson proved that within the framework of quantum mechanics (Hilbert spaces and operator algebras), the maximum possible value of the CHSH operator is:

$$
|S| \le 2\sqrt{2} \approx 2.8284
$$

### Proof Sketch

Define the CHSH operator:

$$
\mathcal{B} = A_0 \otimes B_0 + A_0 \otimes B_1 + A_1 \otimes B_0 - A_1 \otimes B_1
$$

Square the operator $\mathcal{B}$:

$$
\mathcal{B}^2 = 4 I - [A_0, A_1] \otimes [B_0, B_1]
$$

Since $A_x^2 = I$ and $B_y^2 = I$, the commutator norm is bounded by $\|[A_0, A_1]\| \le 2 \|A_0\| \|A_1\| = 2$.
Applying the triangle inequality:

$$
\|\mathcal{B}^2\| \le 4 + \|[A_0, A_1]\| \cdot \|[B_0, B_1]\| \le 4 + 2 \cdot 2 = 8
$$

Taking the square root:

$$
\|\mathcal{B}\| \le \sqrt{8} = 2\sqrt{2}
$$

### Summary of Bounds

| Framework | Maximum $|S|$ | Underlying Physical Principle |
| :--- | :--- | :--- |
| **Local Realism (Classical)** | $2.000$ | Local hidden variables, determinism |
| **Quantum Mechanics** | $2\sqrt{2} \approx 2.828$ | Hilbert spaces, operator commutators |
| **Non-Signaling (PR-Boxes)** | $4.000$ | Relativistic causality (no superluminal signaling) |

---

## 5. Python Verification with NumPy

```python
import numpy as np
from quantum_ed.gates import X, Z, kron_n
from quantum_ed.states import bell_phi_plus

# 1. State vector |Phi+>
phi = bell_phi_plus()

# 2. Alice's observables
A0 = Z
A1 = X

# 3. Bob's observables
B0 = (Z + X) / np.sqrt(2)
B1 = (Z - X) / np.sqrt(2)

# 4. Compute expectation values <phi| A x B |phi>
def expval(A, B, state):
    op = kron_n(A, B)
    return float(np.real(np.conj(state) @ op @ state))

e00 = expval(A0, B0, phi)
e01 = expval(A0, B1, phi)
e10 = expval(A1, B0, phi)
e11 = expval(A1, B1, phi)

S = e00 + e01 + e10 - e11

print(f"E(A0, B0) = {e00:.4f}")
print(f"E(A0, B1) = {e01:.4f}")
print(f"E(A1, B0) = {e10:.4f}")
print(f"E(A1, B1) = {e11:.4f}")
print(f"CHSH Value S = {S:.4f}")  # Expected: 2.8284

assert np.isclose(S, 2.0 * np.sqrt(2))
```

---

## 6. Worked Exercises

### Exercise 1 — CHSH with a Separable State
**Problem:**
Calculate the CHSH value $S$ using the same measurement settings ($A_0 = Z, A_1 = X, B_0 = \frac{Z+X}{\sqrt{2}}, B_1 = \frac{Z-X}{\sqrt{2}}$) on the separable product state $|\psi\rangle = |00\rangle$. Show that $|S| \le 2$.

**Solution:**
1. Compute the local expectations on $|0\rangle$:
   - For Alice: $\langle 0|Z|0\rangle = 1$, $\langle 0|X|0\rangle = 0$.
   - For Bob: $\langle 0|B_0|0\rangle = \frac{\langle 0|Z|0\rangle + \langle 0|X|0\rangle}{\sqrt{2}} = \frac{1+0}{\sqrt{2}} = \frac{1}{\sqrt{2}}$.
   - For Bob: $\langle 0|B_1|0\rangle = \frac{\langle 0|Z|0\rangle - \langle 0|X|0\rangle}{\sqrt{2}} = \frac{1-0}{\sqrt{2}} = \frac{1}{\sqrt{2}}$.
2. For product states, joint expectation values factor: $\langle A \otimes B \rangle = \langle A \rangle \langle B \rangle$:
   - $E(A_0, B_0) = (1)(1/\sqrt{2}) = 1/\sqrt{2}$
   - $E(A_0, B_1) = (1)(1/\sqrt{2}) = 1/\sqrt{2}$
   - $E(A_1, B_0) = (0)(1/\sqrt{2}) = 0$
   - $E(A_1, B_1) = (0)(1/\sqrt{2}) = 0$
3. Compute $S$:

$$
S = \frac{1}{\sqrt{2}} + \frac{1}{\sqrt{2}} + 0 - 0 = \frac{2}{\sqrt{2}} = \sqrt{2} \approx 1.414 \le 2
$$

Separable states cannot violate the classical bound. Entanglement is an absolute prerequisite for non-local correlations.

---

### Exercise 2 — No-Signaling in the CHSH Game
**Problem:**
Prove that Bob cannot determine Alice's measurement choice ($x = 0$ or $x = 1$) from his local measurement statistics, showing that CHSH non-locality does not enable faster-than-light communication.

**Solution:**
Bob's local measurement outcome distribution for observable $B_y$ is:

$$
P(b|y, x) = \operatorname{Tr}\left( (I_A \otimes \Pi_b^B) \rho_{AB} \right) = \operatorname{Tr}_B\left( \Pi_b^B \operatorname{Tr}_A(\rho_{AB}) \right) = \operatorname{Tr}_B(\Pi_b^B \rho_B)
$$

For the Bell state $|\Phi^+\rangle$, Bob's reduced density matrix is $\rho_B = \operatorname{Tr}_A(|\Phi^+\rangle\langle\Phi^+|) = \frac{I}{2}$.
Therefore, for any observable $B_y$:

$$
P(b = +1) = \operatorname{Tr}\left( \frac{I+B_y}{2} \cdot \frac{I}{2} \right) = \frac{1}{2}
$$

Bob's local outcomes are uniformly random ($50\%$ $+1$, $50\%$ $-1$) regardless of whether Alice measured $A_0$, $A_1$, or nothing at all. The non-local correlations only appear when Alice and Bob compare their results classically after the experiment.

---

## 7. Next Steps

- [Quantum Teleportation](quantum-teleportation.md) — transmitting quantum states using shared entanglement and classical bits
- [Superdense Coding](superdense-coding.md) — transmitting two classical bits using a single transmitted qubit
- [Density Matrices](../06-density-matrices/README.md) — see how partial trace enforces the no-signaling theorem
