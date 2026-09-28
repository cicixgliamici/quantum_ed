# Quantum Teleportation

**Quantum teleportation** is a fundamental quantum communication protocol that transfers an unknown quantum state $|\psi\rangle$ from a sender (**Alice**) to a geographically separated receiver (**Bob**), without physically transmitting the particle that carries the state.

First proposed in 1993 by Charles Bennett, Gilles Brassard, Claude Crépeau, Richard Jozsa, Asher Peres, and William Wootters, the protocol consumes:

- **1 shared Bell pair** (pre-distributed entanglement)
- **2 classical bits** (transmitted over a classical channel)

to achieve:

- **1 qubit transferred** from Alice to Bob with $100\%$ fidelity.

---

## 1. Physical Principle & Resource Accounting

Quantum teleportation does not transmit matter or energy; it teleports the **quantum state information**.

### What Teleportation Does NOT Do

1. **Does not violate the No-Cloning Theorem:**
   The No-Cloning Theorem states that an unknown quantum state cannot be duplicated ($|\psi\rangle|0\rangle \not\to |\psi\rangle|\psi\rangle$). In teleportation, Alice's measurement collapses and destroys her original state. The quantum state is *transferred*, not copied.
2. **Does not enable faster-than-light communication (No-Signaling):**
   Until Bob receives Alice's 2 classical measurement bits, his local reduced density matrix is the maximally mixed state $\rho_B = I/2$, containing zero information about $|\psi\rangle$. Teleportation is strictly bounded by the speed of light.
3. **Does not transport physical particles:**
   Bob's local physical qubit is transformed into the exact mathematical state $|\psi\rangle$ that Alice held previously.

---

## 2. Complete Step-by-Step Mathematical Derivation

The protocol operates on a composite system of **three qubits**:

- **Qubit C (Alice):** Carries the arbitrary unknown message state:

$$
|\psi\rangle_C = \alpha |0\rangle_C + \beta |1\rangle_C, \qquad |\alpha|^2 + |\beta|^2 = 1
$$

- **Qubits A and B:** Form a pre-shared maximally entangled Bell state $|\Phi^+\rangle_{AB}$, with qubit $A$ held by Alice and qubit $B$ held by Bob:

$$
|\Phi^+\rangle_{AB} = \frac{|00\rangle_{AB} + |11\rangle_{AB}}{\sqrt{2}}
$$

### Step 0: Initial Three-Qubit State

The global state $|\Psi_0\rangle$ of the 3-qubit register (ordered $C, A, B$) is:

$$
|\Psi_0\rangle = |\psi\rangle_C \otimes |\Phi^+\rangle_{AB} = (\alpha |0\rangle_C + \beta |1\rangle_C) \otimes \frac{|00\rangle_{AB} + |11\rangle_{AB}}{\sqrt{2}}
$$

Expanding into the computational basis:

$$
|\Psi_0\rangle = \frac{1}{\sqrt{2}} \left( \alpha |000\rangle + \alpha |011\rangle + \beta |100\rangle + \beta |111\rangle \right)
$$

### Step 1: Alice Applies $\mathrm{CNOT}_{C \to A}$

Alice performs a $\mathrm{CNOT}$ gate using her message qubit $C$ as control and her half of the Bell pair $A$ as target:

- $|000\rangle \mapsto |000\rangle$
- $|011\rangle \mapsto |011\rangle$
- $|100\rangle \mapsto |110\rangle$
- $|111\rangle \mapsto |101\rangle$

The state becomes:

$$
|\Psi_1\rangle = \frac{1}{\sqrt{2}} \left( \alpha |000\rangle + \alpha |011\rangle + \beta |110\rangle + \beta |101\rangle \right)
$$

### Step 2: Alice Applies Hadamard to Qubit C

Alice applies a Hadamard gate $H$ to her message qubit $C$:

$$
H|0\rangle_C = \frac{|0\rangle + |1\rangle}{\sqrt{2}}, \qquad H|1\rangle_C = \frac{|0\rangle - |1\rangle}{\sqrt{2}}
$$

Substitute into $|\Psi_1\rangle$:

$$
|\Psi_2\rangle = \frac{1}{2} \left[ \alpha (|0\rangle + |1\rangle)|00\rangle + \alpha (|0\rangle + |1\rangle)|11\rangle + \beta (|0\rangle - |1\rangle)|10\rangle + \beta (|0\rangle - |1\rangle)|01\rangle \right]
$$

### Step 3: Regrouping by Alice's Measurement Outcomes

Factor out Alice's qubits (the first two qubits $C$ and $A$):

$$
|\Psi_2\rangle = \frac{1}{2} \Big[ |00\rangle_{CA} (\alpha|0\rangle + \beta|1\rangle)_B + |01\rangle_{CA} (\alpha|1\rangle + \beta|0\rangle)_B + |10\rangle_{CA} (\alpha|0\rangle - \beta|1\rangle)_B + |11\rangle_{CA} (\alpha|1\rangle - \beta|0\rangle)_B \Big]
$$

Express Bob's state in terms of Pauli operators acting on the target state $|\psi\rangle$:

$$
|\Psi_2\rangle = \frac{1}{2} \Big[ |00\rangle_{CA} \left( |\psi\rangle \right)_B + |01\rangle_{CA} \left( X|\psi\rangle \right)_B + |10\rangle_{CA} \left( Z|\psi\rangle \right)_B + |11\rangle_{CA} \left( XZ|\psi\rangle \right)_B \Big]
$$

---

## 3. Alice's Measurement and Bob's Correction

Alice measures her two qubits $C$ and $A$ in the computational basis, obtaining one of four equiprobable pairs of classical bits $(m_C, m_A) \in \{00, 01, 10, 11\}$, each with probability:

$$
P(m_C, m_A) = \left| \frac{1}{2} \right|^2 = \frac{1}{4} = 25\%
$$

Alice sends the classical bits $(m_C, m_A)$ to Bob over a classical communication channel.

Bob applies the decoding Pauli correction $X^{m_A} Z^{m_C}$ to his qubit:

| Alice Measures $(m_C, m_A)$ | Bob's Immediate State | Bob's Correction Operator | Bob's Final State |
| :---: | :---: | :---: | :---: |
| `00` | $|\psi\rangle = \alpha\|0\rangle + \beta\|1\rangle$ | $I$ (do nothing) | $|\psi\rangle$ |
| `01` | $X\|\psi\rangle = \alpha\|1\rangle + \beta\|0\rangle$ | $X$ | $X(X\|\psi\rangle) = |\psi\rangle$ |
| `10` | $Z\|\psi\rangle = \alpha\|0\rangle - \beta\|1\rangle$ | $Z$ | $Z(Z\|\psi\rangle) = |\psi\rangle$ |
| `11` | $XZ\|\psi\rangle = \alpha\|1\rangle - \beta\|0\rangle$ | $Z \cdot X$ | $(Z X)(X Z\|\psi\rangle) = |\psi\rangle$ |

In all four branches, Bob's qubit is restored **exactly** to the original message state $|\psi\rangle$.

---

## 4. The Principle of Deferred Measurement

In physical circuit simulators and some hardware backends, conditioned feedforward operations (applying quantum gates conditioned on mid-circuit classical measurement outcomes) can be difficult to serialize.

The **Principle of Deferred Measurement** states that:
> Any measurement followed by classically conditioned quantum operations is mathematically equivalent to replacing the classical controls with coherent quantum controls, deferring all measurements to the end of the circuit.

### Coherent Teleportation Circuit

In deferred form:
- The classical condition on $m_A$ (controlled by qubit $A$) becomes a quantum $\mathrm{CX}_{A \to B}$ gate.
- The classical condition on $m_C$ (controlled by qubit $C$) becomes a quantum $\mathrm{CZ}_{C \to B}$ gate.

```text
Message |ψ⟩ ───●───[ H ]───────────────●─── [ Measure ]
               │                       │
Alice Bell  ───X───────────────●───────┼─── [ Measure ]
                               │       │
Bob Bell    ───────────────────X───────Z─── |ψ⟩ (Teleported)
```

The reduced density matrix of Bob's qubit $\rho_B = \operatorname{Tr}_{CA}(\rho_{\mathrm{final}})$ is identically $|\psi\rangle\langle\psi|$.

---

## 5. Python Verification in `quantum_ed`

```python
import numpy as np
from quantum_ed.gates import H, CNOT, CZ, I, apply, kron_n
from quantum_ed.states import basis_0, basis_1, bell_phi_plus
from quantum_ed.density import rho_from_ket, fidelity_pure

# 1. Prepare an arbitrary normalized state |psi> = alpha|0> + beta|1>
theta = 0.73
phi_angle = 1.25
alpha = np.cos(theta)
beta = np.sin(theta) * np.exp(1j * phi_angle)
psi_target = np.array([alpha, beta], dtype=complex)

# 2. Prepare 3-qubit state: |psi> (wire 0) (x) |Phi+> (wires 1, 2)
bell = bell_phi_plus()
state = np.kron(psi_target, bell)

# 3. Alice's Bell-basis interaction: CNOT(0 -> 1) then H(0)
# CNOT(0 -> 1) on 3 qubits: CNOT (x) I
cnot_01 = np.kron(CNOT, I)
state = cnot_01 @ state

# H(0) on 3 qubits: H (x) I (x) I
h_0 = kron_n(H, I, I)
state = h_0 @ state

# 4. Deferred measurement corrections to Bob's qubit (wire 2):
# CX(1 -> 2): I (x) CNOT
cx_12 = np.kron(I, CNOT)
state = cx_12 @ state

# CZ(0 -> 2): Controlled-Z from wire 0 to wire 2
cz_02 = np.array(np.diag([1, 1, 1, 1, 1, -1, 1, -1]), dtype=complex)
# (adds -1 phase when wire 0 and wire 2 are both 1)
state = cz_02 @ state

# 5. Verify Bob's state by partial trace over Alice's qubits (0 and 1)
rho_full = rho_from_ket(state)

# Tracing out qubits 0 and 1:
rho_bob = np.zeros((2, 2), dtype=complex)
for a in range(2):
    for b in range(2):
        for c in range(2):
            for cp in range(2):
                idx1 = 4 * a + 2 * b + c
                idx2 = 4 * a + 2 * b + cp
                rho_bob[c, cp] += rho_full[idx1, idx2]

# Compute fidelity with target state
fid = fidelity_pure(psi_target, rho_bob)
print(f"Teleportation Fidelity: {fid:.6f}")
assert np.isclose(fid, 1.0)
```

---

## 6. Multi-Ecosystem Showcase

The teleportation protocol is verified across all five repository environments:

- [NumPy Implementation](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/quantum-teleportation/numpy/quantum_teleportation.py)
- [Qiskit Circuit](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/quantum-teleportation/qiskit/quantum_teleportation.py)
- [Q# Program](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/quantum-teleportation/qsharp/QuantumTeleportation.qs)
- [OpenQASM 3](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/quantum-teleportation/openqasm/quantum_teleportation.qasm)
- [PennyLane](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/quantum-teleportation/pennylane/quantum_teleportation.py)

---

## 7. Worked Exercises

### Exercise 1 — Teleporting an Entangled Qubit
**Problem:**
Suppose Alice holds qubit $C$, which is entangled with a fourth qubit $D$ held by Charlie in state $|\Psi\rangle_{CD} = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$. If Alice teleports qubit $C$ to Bob, what is the resulting joint state of Charlie and Bob?

**Solution:**
Because quantum mechanics is completely linear, teleportation acts as the identity channel on any subspace:

$$
\mathcal{T}_{C \to B} \left( |\Psi\rangle_{CD} \right) = (I_D \otimes \mathcal{T}_{C \to B}) \left( |\Psi\rangle_{CD} \right) = \frac{|0\rangle_D |0\rangle_B + |1\rangle_D |1\rangle_B}{\sqrt{2}}
$$

Charlie and Bob now share the entangled state $|\Phi^+\rangle_{DB}$, even though they never physically interacted! This protocol is known as **Entanglement Swapping**, and forms the basis of quantum repeaters and quantum networks.

---

### Exercise 2 — What if Classical Bits are Lost?
**Problem:**
Suppose Alice measures her qubits but fails to send the classical bits to Bob. What is Bob's state? Can he learn anything about $|\psi\rangle$?

**Solution:**
If Bob does not know Alice's outcomes $(m_C, m_A)$, his state is the classical mixture over all 4 possible branches with equal probability $1/4$:

$$
\rho_B = \frac{1}{4} |\psi\rangle\langle\psi| + \frac{1}{4} X|\psi\rangle\langle\psi|X + \frac{1}{4} Z|\psi\rangle\langle\psi|Z + \frac{1}{4} XZ|\psi\rangle\langle\psi|ZX
$$

For any pure state $|\psi\rangle = \frac{1}{2}(I + \vec{r}\cdot\vec{\sigma})$:

$$
\frac{1}{4} \sum_{P \in \{I, X, Z, XZ\}} P |\psi\rangle\langle\psi| P^\dagger = \frac{I}{2}
$$

Bob's state is strictly the **maximally mixed state $\frac{I}{2}$** with zero Bloch vector ($\vec{r} = \vec{0}$). Without the 2 classical bits, Bob possesses zero information about $|\psi\rangle$, proving that teleportation strictly respects relativistic causality.

---

## 8. Next Steps

- [Superdense Coding](superdense-coding.md) — the operational dual: transmitting 2 classical bits using 1 qubit
- [CHSH Inequality](CHSH.md) — verifying non-locality and entanglement quality
- [Density Matrices](../06-density-matrices/README.md) — understanding open subsystems and mixed states
