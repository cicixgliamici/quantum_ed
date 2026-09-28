# Quantum Entanglement

When two quantum systems interact, their state space is formed by the tensor product:

$$
\mathcal{H}_{AB} = \mathcal{H}_A \otimes \mathcal{H}_B
$$

For two qubits, $\mathcal{H}_{AB} = \mathbb{C}^2 \otimes \mathbb{C}^2 \cong \mathbb{C}^4$.

In this four-dimensional space lies the most distinctively quantum phenomenon in nature: **entanglement**. Erwin Schrödinger identified entanglement as *"not one, but rather the characteristic trait of quantum mechanics, the one that enforces its entire departure from classical lines of thought."*

---

## 1. Separable States vs. Entangled States

### Product (Separable) States
A two-qubit pure state $|\Psi\rangle \in \mathbb{C}^4$ is called a **product state** (or **separable state**) if and only if it can be factored into the tensor product of two independent single-qubit pure states:

$$
|\Psi\rangle = |\psi_A\rangle \otimes |\phi_B\rangle
$$

for some $|\psi_A\rangle \in \mathcal{H}_A$ and $|\phi_B\rangle \in \mathcal{H}_B$.

#### Example:
The state $|01\rangle = |0\rangle \otimes |1\rangle$ is separable by definition.
Similarly, the state:

$$
\frac{|00\rangle + |01\rangle}{\sqrt{2}} = |0\rangle \otimes \left( \frac{|0\rangle + |1\rangle}{\sqrt{2}} \right) = |0\rangle \otimes |+\rangle
$$

is separable because qubit $A$ is deterministically $|0\rangle$, while qubit $B$ is independently in $|+\rangle$.

### Entangled States
A state is **entangled** if it **cannot** be written as a product state:

$$
|\Psi\rangle \ne |\psi_A\rangle \otimes |\phi_B\rangle \quad \text{for any } |\psi_A\rangle, |\phi_B\rangle
$$

In an entangled state, the system as a whole possesses a definite pure state, but its individual constituent qubits do not.

### The Algebraic Test for Two-Qubit Entanglement
Any normalized two-qubit state can be expanded in the computational basis as:

$$
|\Psi\rangle = a|00\rangle + b|01\rangle + c|10\rangle + d|11\rangle, \quad |a|^2 + |b|^2 + |c|^2 + |d|^2 = 1
$$

**Theorem:** The state $|\Psi\rangle$ is separable if and only if:

$$
ad - bc = 0
$$

*Proof:*
If $|\Psi\rangle$ is separable, there exist $(\alpha_0|0\rangle + \alpha_1|1\rangle)$ and $(\beta_0|0\rangle + \beta_1|1\rangle)$ such that:

$$
|\Psi\rangle = \alpha_0\beta_0|00\rangle + \alpha_0\beta_1|01\rangle + \alpha_1\beta_0|10\rangle + \alpha_1\beta_1|11\rangle
$$

Matching coefficients: $a = \alpha_0\beta_0$, $b = \alpha_0\beta_1$, $c = \alpha_1\beta_0$, $d = \alpha_1\beta_1$.
Computing the determinant:

$$
ad - bc = (\alpha_0\beta_0)(\alpha_1\beta_1) - (\alpha_0\beta_1)(\alpha_1\beta_0) = \alpha_0\alpha_1\beta_0\beta_1 - \alpha_0\alpha_1\beta_0\beta_1 = 0
$$

Conversely, if $ad - bc \ne 0$, the state is guaranteed to be entangled!

---

## 2. The Four Canonical Bell States (EPR Pairs)

The four maximally entangled two-qubit states form the **Bell basis**, named after John Stewart Bell:

$$
|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}
$$

$$
|\Phi^-\rangle = \frac{|00\rangle - |11\rangle}{\sqrt{2}}
$$

$$
|\Psi^+\rangle = \frac{|01\rangle + |10\rangle}{\sqrt{2}}
$$

$$
|\Psi^-\rangle = \frac{|01\rangle - |10\rangle}{\sqrt{2}}
$$

### Properties of the Bell Basis
1. **Maximal Entanglement:** Applying the algebraic condition $ad - bc$:
   - For $|\Phi^\pm\rangle$: $a = 1/\sqrt{2}, b = 0, c = 0, d = \pm 1/\sqrt{2} \implies ad - bc = \pm 1/2 \ne 0$.
   - For $|\Psi^\pm\rangle$: $a = 0, b = 1/\sqrt{2}, c = \pm 1/\sqrt{2}, d = 0 \implies ad - bc = \mp 1/2 \ne 0$.
2. **Orthonormality:** The four Bell states are mutually orthogonal and normalized:

$$
\langle \Phi^\pm | \Phi^\mp \rangle = 0, \quad \langle \Psi^\pm | \Psi^\mp \rangle = 0, \quad \langle \Phi^\pm | \Psi^\pm \rangle = 0
$$

3. **Complete Basis:** Any arbitrary two-qubit state can be uniquely decomposed in the Bell basis:

$$
\sum_{\mu \in \{\Phi^\pm, \Psi^\pm\}} |\mu\rangle \langle \mu| = I_4
$$

### Generating Bell States from Circuits
All four Bell states can be prepared from computational basis inputs using a simple circuit: a Hadamard gate $H$ followed by a `CNOT` gate.

```
q0: ──| H |──■──
             │  
q1: ─────────■──
```

1. **Input $|00\rangle$ produces $|\Phi^+\rangle$:**

$$
|00\rangle \xrightarrow{H \otimes I} \frac{|00\rangle + |10\rangle}{\sqrt{2}} \xrightarrow{\mathrm{CNOT}} \frac{|00\rangle + |11\rangle}{\sqrt{2}} = |\Phi^+\rangle
$$

2. **Input $|10\rangle$ produces $|\Phi^-\rangle$:**

$$
|10\rangle \xrightarrow{H \otimes I} \frac{|00\rangle - |10\rangle}{\sqrt{2}} \xrightarrow{\mathrm{CNOT}} \frac{|00\rangle - |11\rangle}{\sqrt{2}} = |\Phi^-\rangle
$$

3. **Input $|01\rangle$ produces $|\Psi^+\rangle$:**

$$
|01\rangle \xrightarrow{H \otimes I} \frac{|01\rangle + |11\rangle}{\sqrt{2}} \xrightarrow{\mathrm{CNOT}} \frac{|01\rangle + |10\rangle}{\sqrt{2}} = |\Psi^+\rangle
$$

4. **Input $|11\rangle$ produces $|\Psi^-\rangle$:**

$$
|11\rangle \xrightarrow{H \otimes I} \frac{|01\rangle - |11\rangle}{\sqrt{2}} \xrightarrow{\mathrm{CNOT}} \frac{|01\rangle - |10\rangle}{\sqrt{2}} = |\Psi^-\rangle
$$

---

## 3. Subsystem Paradox and Reduced Density Matrices

In classical mechanics, if you have complete knowledge of a composite system (such as the positions and velocities of two billiard balls), you automatically have complete knowledge of each individual part.

**In quantum mechanics, this is false.**

When two qubits are maximally entangled, the composite system is in a pure state with zero entropy (we know everything that can physically be known about the joint system). Yet if you look at qubit $A$ alone, it is in a **maximally mixed state**—you have zero information about its individual outcome!

### The Partial Trace
To find the state of subsystem $A$ alone, we take the **partial trace** over subsystem $B$:

$$
\rho_A = \operatorname{Tr}_B(\rho_{AB}) = \sum_{k=0}^1 (I_A \otimes \langle k|_B) \rho_{AB} (I_A \otimes |k\rangle_B)
$$

Let's compute the reduced state $\rho_A$ for the Bell state $|\Phi^+\rangle$:
The full density matrix is:

$$
\rho_{AB} = |\Phi^+\rangle \langle \Phi^+| = \frac{1}{2} \begin{pmatrix} 1 & 0 & 0 & 1 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 1 & 0 & 0 & 1 \end{pmatrix}
$$

Tracing out qubit $B$:

$$
\rho_A = \frac{1}{2} |0\rangle\langle 0| + \frac{1}{2} |1\rangle\langle 1| = \frac{1}{2} \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} = \frac{1}{2} I_2
$$

The reduced density matrix is proportional to the identity. This means:
- The probability of measuring $0$ on qubit $A$ is exactly $1/2$.
- The probability of measuring $1$ on qubit $A$ is exactly $1/2$.
- The Bloch vector of qubit $A$ is $(0, 0, 0)$—at the exact dead center of the Bloch sphere!
- The purity $\operatorname{Tr}(\rho_A^2) = \operatorname{Tr}(I/4) = 1/2 < 1$, confirming it is completely mixed.

---

## 4. Quantum Nonlocality and the No-Signaling Theorem

### Nonlocal Correlations (EPR & Bell)
In 1935, Einstein, Podolsky, and Rosen (EPR) argued that because measuring qubit $A$ appears to instantaneously collapse qubit $B$ across space, either:
1. Quantum mechanics is incomplete, and "hidden variables" already determined the outcomes at creation (Local Realism).
2. Quantum mechanics involves "spooky action at a distance."

In 1964, John S. Bell proved that **no local hidden variable theory can reproduce all predictions of quantum mechanics**.
This is experimentally tested via Bell inequalities, such as the **CHSH inequality**:
- Any local realistic theory satisfies: $|\langle S \rangle| \le 2$.
- Quantum mechanics on a Bell state achieves: $|\langle S \rangle| = 2\sqrt{2} \approx 2.828$ (Tsirelson's bound).

*(See [CHSH Inequality Tutorial](CHSH.md) for full derivation and simulation).*

### The No-Signaling Theorem
Does the instantaneous collapse of an entangled state allow faster-than-light communication? **No.**

**Proof:**
Suppose Alice and Bob share $|\Phi^+\rangle$. Alice chooses to measure her qubit in basis $\{|v_0\rangle, |v_1\rangle\}$.
Before Alice communicates her classical measurement outcome to Bob, Bob's description of his qubit is obtained by averaging over Alice's possible outcomes:

$$
\rho_B = \operatorname{Tr}_A(\rho_{AB}) = \frac{1}{2}I_2
$$

Bob's local density matrix $\rho_B$ is completely independent of:
1. Whether Alice measured her qubit or not.
2. What measurement basis Alice chose.
3. What outcome Alice obtained.

No measurement Bob performs can reveal Alice's actions without receiving classical information from her (which travels at or below the speed of light $c$).

---

## 5. Entanglement as an Information Resource

Entanglement is not just a philosophical puzzle; it is a physical and computational **resource** (measured in units called **ebits**):

### Superdense Coding (2 Classical Bits via 1 Qubit)
Two parties (Alice and Bob) share one entangled Bell pair $|\Phi^+\rangle$.
- Alice wants to transmit 2 classical bits ($00, 01, 10, \text{or } 11$) to Bob.
- She applies one of the four local Pauli gates $\{I, X, Z, XZ\}$ to **only her single qubit** and sends that qubit to Bob.
- Bob performs a Bell-basis measurement on the pair and deterministically decodes both classical bits!
- *(See [Superdense Coding Guide](superdense-coding.md)).*

### Quantum Teleportation (1 Qubit via 2 Classical Bits + 1 ebit)
- Alice possesses an unknown quantum state $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$ that she wishes to send to Bob.
- Alice and Bob share an entangled Bell pair $|\Phi^+\rangle$.
- Alice performs a Bell measurement on her unknown qubit and her half of the Bell pair, obtaining 2 classical bits.
- Alice sends the 2 classical bits to Bob over a classical channel.
- Bob applies a conditional Pauli correction $\{I, X, Z, XZ\}$ to his qubit.
- Bob's qubit is now in the exact state $|\psi\rangle$! The original state was destroyed at Alice's end (in accordance with the No-Cloning Theorem).
- *(See [Quantum Teleportation Guide](quantum-teleportation.md)).*

---

## 6. Python Implementation with `quantum_ed`

The repository provides explicit functions to build and analyze entangled states:

```python
import numpy as np
from quantum_ed.states import bell_phi_plus
from quantum_ed.density import rho_from_ket, partial_trace_two_qubits

# 1. Prepare Bell state |Phi+> = (|00> + |11>) / sqrt(2)
phi_plus = bell_phi_plus()
print("Bell state |Phi+>:\n", phi_plus)

# 2. Form the pure 4x4 density matrix rho = |Phi+><Phi+|
rho_joint = rho_from_ket(phi_plus)
print("\nJoint density matrix rho_AB (shape 4x4):\n", rho_joint)

# 3. Compute partial trace over qubit B to inspect qubit A
rho_A = partial_trace_two_qubits(rho_joint, keep='A')
print("\nReduced density matrix rho_A (shape 2x2):\n", rho_A)

# 4. Verify that rho_A is maximally mixed: 0.5 * I_2
is_maximally_mixed = np.allclose(rho_A, 0.5 * np.eye(2))
print("\nIs qubit A maximally mixed (entropy = 1 bit)?", is_maximally_mixed)  # True
```

---

## 7. Exercises and Worked Solutions

### Exercise 1: Algebraic Separability Check
**Problem:** Determine whether the state $|\psi\rangle = \frac{1}{2}|00\rangle + \frac{1}{2}|01\rangle + \frac{1}{2}|10\rangle + \frac{1}{2}|11\rangle$ is separable or entangled.
**Solution:**
Identify the coefficients: $a = 1/2, b = 1/2, c = 1/2, d = 1/2$.
Compute the determinant $ad - bc$:

$$
ad - bc = \left(\frac{1}{2}\right)\left(\frac{1}{2}\right) - \left(\frac{1}{2}\right)\left(\frac{1}{2}\right) = \frac{1}{4} - \frac{1}{4} = 0
$$

Since $ad - bc = 0$, the state is **separable**.
Indeed, it factors into:

$$
|\psi\rangle = \left(\frac{|0\rangle + |1\rangle}{\sqrt{2}}\right) \otimes \left(\frac{|0\rangle + |1\rangle}{\sqrt{2}}\right) = |+\rangle \otimes |+\rangle
$$

### Exercise 2: Normalization and Entanglement of an Arbitrary State
**Problem:** Consider the state $|\psi\rangle = \frac{1}{\sqrt{3}}|00\rangle + \sqrt{\frac{2}{3}}|11\rangle$.
1. Is it normalized?
2. Is it entangled?

**Solution:**
1. Check norm: $|1/\sqrt{3}|^2 + |\sqrt{2/3}|^2 = 1/3 + 2/3 = 1$. It is normalized.
2. Check separability: $a = 1/\sqrt{3}, b = 0, c = 0, d = \sqrt{2/3}$.
   
$$
ad - bc = \left(\frac{1}{\sqrt{3}}\right)\left(\sqrt{\frac{2}{3}}\right) - 0 = \frac{\sqrt{2}}{3} \ne 0
$$

Since $ad - bc \ne 0$, the state is **entangled** (though not maximally entangled, since $|a| \ne |d|$).

---

## 8. Next Steps and Interactive Explorations

Explore quantum protocols and the computing layer:
- [CHSH Inequality Simulation](CHSH.md)
- [Superdense Coding Protocol](superdense-coding.md)
- [Quantum Teleportation Protocol](quantum-teleportation.md)
- [Chapter 5: Circuits & Gates](../05-circuits-and-gates/README.md)
- Accompanying notebook: [`notebooks/02-bell-entanglement.ipynb`](https://github.com/cicixgliamici/quantum_ed/blob/main/notebooks/02-bell-entanglement.ipynb)
- Cross-ecosystem experiment: [Bell State Experiment](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/bell-state)
