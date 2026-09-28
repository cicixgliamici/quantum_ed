# Superdense Coding

**Superdense coding** is a foundational quantum communication protocol discovered by Charles Bennett and Stephen Wiesner in 1992. It allows a sender (**Alice**) to transmit **two classical bits** of information to a receiver (**Bob**) by physically sending only **one qubit**, provided they share a pre-distributed entangled Bell pair.

---

## 1. Holevo's Theorem and the Entanglement Advantage

To appreciate the significance of superdense coding, consider **Holevo's Theorem** (1973), which states:

> A single physical qubit without prior entanglement can transmit at most **1 bit** of accessible classical information ($C \le 1$ bit).

Superdense coding does not violate Holevo's theorem; instead, it reveals the power of **entanglement assistance**:

- **Classical Channel:** 1 bit transmitted $\to$ 1 bit of information.
- **Quantum Channel (No Entanglement):** 1 qubit transmitted $\to$ 1 bit of information.
- **Entanglement-Assisted Quantum Channel:** 1 qubit transmitted + 1 shared ebit $\to$ **2 bits of information**.

Pre-shared entanglement effectively doubles the classical communication capacity of a quantum channel!

### Resource Duality with Teleportation

Superdense coding and quantum teleportation are **exact operational duals**:

| Protocol | Resource Consumed | Physical Transmission | Output Achieved |
| :--- | :--- | :--- | :--- |
| **Quantum Teleportation** | 1 Bell pair (ebit) | 2 Classical bits | 1 Qubit transferred |
| **Superdense Coding** | 1 Bell pair (ebit) | 1 Physical qubit | 2 Classical bits transferred |

---

## 2. Step-by-Step Mathematical Protocol

The protocol is divided into four distinct stages:

```text
 ┌──────────────┐                               ┌──────────────┐
 │ Alice's Lab  │ ◄──── Qubit 0 ───┐            │  Bob's Lab   │
 │              │                  │            │              │
 │ Encode:      │          ┌───────┴───────┐    │              │
 │ U = Z^b₁ X^b₀│          │ Source: |Φ⁺⟩  │    │              │
 │              │          └───────┬───────┘    │              │
 │              │ ──── Qubit 0 ────┼──────────► │ Decode:      │
 └──────────────┘   (Transmitted)  └── Qubit 1 ─┤ CNOT + H     │
                                                │ Measure b₁b₀ │
                                                └──────────────┘
```

### Stage 0: Shared Entangled Resource

Alice and Bob initially share the maximally entangled Bell state $|\Phi^+\rangle$:

$$
|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}
$$

Alice holds qubit 0 (first index), and Bob holds qubit 1 (second index).

### Stage 1: Alice's Local Encoding

Alice wishes to transmit a 2-bit classical message $m = b_1 b_0 \in \{00, 01, 10, 11\}$.
She applies a single-qubit unitary operator $U_{b_1 b_0} = Z^{b_1} X^{b_0}$ exclusively to her local qubit 0:

$$
|\Psi_{\mathrm{encoded}}\rangle = (U_{b_1 b_0} \otimes I) |\Phi^+\rangle
$$

Depending on the 2-bit message, the state transforms into one of the four mutually orthogonal Bell states:

1. **Message `00` ($b_1=0, b_0=0$):**
   Alice applies $I$:

$$
(I \otimes I)|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}} = |\Phi^+\rangle
$$

2. **Message `01` ($b_1=0, b_0=1$):**
   Alice applies $X$ (bit-flip):

$$
(X \otimes I)|\Phi^+\rangle = \frac{X|0\rangle|0\rangle + X|1\rangle|1\rangle}{\sqrt{2}} = \frac{|10\rangle + |01\rangle}{\sqrt{2}} = |\Psi^+\rangle
$$

3. **Message `10` ($b_1=1, b_0=0$):**
   Alice applies $Z$ (phase-flip):

$$
(Z \otimes I)|\Phi^+\rangle = \frac{Z|0\rangle|0\rangle + Z|1\rangle|1\rangle}{\sqrt{2}} = \frac{|00\rangle - |11\rangle}{\sqrt{2}} = |\Phi^-\rangle
$$

4. **Message `11` ($b_1=1, b_0=1$):**
   Alice applies $Z \cdot X = -i Y$:

$$
(ZX \otimes I)|\Phi^+\rangle = \frac{ZX|0\rangle|0\rangle + ZX|1\rangle|1\rangle}{\sqrt{2}} = \frac{|01\rangle - |10\rangle}{\sqrt{2}} = -|\Psi^-\rangle
$$

By acting locally on only half of the entangled pair, Alice transforms the global state into four **distinguishable, mutually orthogonal states**:

$$
\langle \Phi^+ | \Psi^+ \rangle = \langle \Phi^+ | \Phi^- \rangle = \langle \Phi^+ | \Psi^- \rangle = 0
$$

### Stage 2: Transmission

Alice sends her single physical qubit (qubit 0) to Bob through a quantum channel.

### Stage 3: Bob's Bell-Basis Decoding

Bob now holds both qubits 0 and 1. To distinguish the four Bell states, he applies the **inverse of the Bell-state preparation circuit**:

1. Apply $\mathrm{CNOT}_{0 \to 1}$ (control = qubit 0, target = qubit 1).
2. Apply $H_0$ to qubit 0.

Let us trace the evolution for each of the four Bell states:

- **If $|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$:**

$$
\frac{|00\rangle + |11\rangle}{\sqrt{2}} \xrightarrow{\mathrm{CNOT}} \frac{|00\rangle + |10\rangle}{\sqrt{2}} = \left( \frac{|0\rangle + |1\rangle}{\sqrt{2}} \right) |0\rangle = |+\rangle |0\rangle \xrightarrow{H_0} |00\rangle
$$

- **If $|\Psi^+\rangle = \frac{|01\rangle + |10\rangle}{\sqrt{2}}$:**

$$
\frac{|01\rangle + |10\rangle}{\sqrt{2}} \xrightarrow{\mathrm{CNOT}} \frac{|01\rangle + |11\rangle}{\sqrt{2}} = \left( \frac{|0\rangle + |1\rangle}{\sqrt{2}} \right) |1\rangle = |+\rangle |1\rangle \xrightarrow{H_0} |01\rangle
$$

- **If $|\Phi^-\rangle = \frac{|00\rangle - |11\rangle}{\sqrt{2}}$:**

$$
\frac{|00\rangle - |11\rangle}{\sqrt{2}} \xrightarrow{\mathrm{CNOT}} \frac{|00\rangle - |10\rangle}{\sqrt{2}} = \left( \frac{|0\rangle - |1\rangle}{\sqrt{2}} \right) |0\rangle = |-\rangle |0\rangle \xrightarrow{H_0} |10\rangle
$$

- **If $-|\Psi^-\rangle = \frac{|01\rangle - |10\rangle}{\sqrt{2}}$:**

$$
\frac{|01\rangle - |10\rangle}{\sqrt{2}} \xrightarrow{\mathrm{CNOT}} \frac{|01\rangle - |11\rangle}{\sqrt{2}} = \left( \frac{|0\rangle - |1\rangle}{\sqrt{2}} \right) |1\rangle = |-\rangle |1\rangle \xrightarrow{H_0} |11\rangle
$$

### Stage 4: Readout

Bob measures both qubits in the computational basis:
- Qubit 0 yields $b_1$ (the phase bit).
- Qubit 1 yields $b_0$ (the bit-flip bit).

The measurement returns the exact classical bitstring $b_1 b_0$ with **$100\%$ probability**!

---

## 3. Python Verification with `quantum_ed`

```python
import numpy as np
from quantum_ed.gates import I, X, Z, H, CNOT, kron_n
from quantum_ed.states import bell_phi_plus

def superdense_encode_decode(b1: int, b0: int) -> tuple[int, int]:
    # 1. Prepare shared resource |Phi+>
    state = bell_phi_plus()

    # 2. Alice encodes: U = Z^b1 @ X^b0 on qubit 0
    alice_op = I
    if b0 == 1:
        alice_op = X @ alice_op
    if b1 == 1:
        alice_op = Z @ alice_op
    
    encoded_op = kron_n(alice_op, I)
    state = encoded_op @ state

    # 3. Bob decodes: CNOT(0 -> 1) then H(0)
    state = CNOT @ state
    decoding_h = kron_n(H, I)
    state = decoding_h @ state

    # 4. Measure computational basis probabilities
    probs = np.abs(state)**2
    measured_idx = int(np.argmax(probs))
    
    # Map index 0->(0,0), 1->(0,1), 2->(1,0), 3->(1,1)
    meas_b1 = (measured_idx >> 1) & 1
    meas_b0 = measured_idx & 1
    return meas_b1, meas_b0

# Test all 4 messages
for b1 in (0, 1):
    for b0 in (0, 1):
        out_b1, out_b0 = superdense_encode_decode(b1, b0)
        print(f"Sent: ({b1}, {b0}) -> Received: ({out_b1}, {out_b0})")
        assert (b1, b0) == (out_b1, out_b0)
```

---

## 4. Multi-Ecosystem Showcase

The superdense coding protocol is verified across all five repository environments:

- [NumPy Implementation](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/superdense-coding/numpy/superdense_coding.py)
- [Qiskit Circuit](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/superdense-coding/qiskit/superdense_coding.py)
- [Q# Program](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/superdense-coding/qsharp/SuperdenseCoding.qs)
- [OpenQASM 3](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/superdense-coding/openqasm/superdense_coding.qasm)
- [PennyLane](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/superdense-coding/pennylane/superdense_coding.py)

---

## 5. Worked Exercises

### Exercise 1 — Why Can't Alice Transmit 3 Bits?
**Problem:**
Explain why Alice cannot transmit 3 classical bits ($8$ messages) using 1 shared Bell pair and 1 transmitted qubit.

**Solution:**
1. The global Hilbert space of two qubits has dimension $d = 2^2 = 4$.
2. In any Hilbert space of dimension $d$, there can be at most $d$ mutually orthogonal (and thus perfectly distinguishable) quantum states.
3. Because $d = 4$, the maximum number of distinguishable messages that can be reliably encoded and decoded is $\log_2(4) = 2$ classical bits.
4. Transmitting 3 classical bits would require $2^3 = 8$ mutually orthogonal states, which is mathematically impossible in a 4-dimensional Hilbert space.

---

### Exercise 2 — What Does an Eavesdropper Intercept?
**Problem:**
Suppose an eavesdropper (**Eve**) intercepts the qubit Alice sends to Bob in transit. Can Eve learn which 2-bit message Alice sent?

**Solution:**
When Eve intercepts qubit 0, she has access only to subsystem $A$.
Her state is described by the reduced density matrix $\rho_A = \operatorname{Tr}_B(\rho_{AB})$.

For each of the four possible encoded Bell states:
- If message is `00` ($|\Phi^+\rangle$): $\rho_A = \operatorname{Tr}_B(|\Phi^+\rangle\langle\Phi^+|) = \frac{I}{2}$.
- If message is `01` ($|\Psi^+\rangle$): $\rho_A = \operatorname{Tr}_B(|\Psi^+\rangle\langle\Psi^+|) = \frac{I}{2}$.
- If message is `10` ($|\Phi^-\rangle$): $\rho_A = \operatorname{Tr}_B(|\Phi^-\rangle\langle\Phi^-|) = \frac{I}{2}$.
- If message is `11` ($|\Psi^-\rangle$): $\rho_A = \operatorname{Tr}_B(|\Psi^-\rangle\langle\Psi^-|) = \frac{I}{2}$.

In all four cases, Eve's intercepted qubit is strictly in the **maximally mixed state $\frac{I}{2}$**!
Eve's measurement statistics are completely identical ($50\%$ 0, $50\%$ 1) regardless of Alice's message.
Without access to Bob's entangled qubit 1, Eve can extract **zero bits of information**. The message is completely encrypted by the shared entanglement.

---

## 6. Next Steps

- [Quantum Teleportation](quantum-teleportation.md) — the resource dual protocol
- [CHSH Inequality](CHSH.md) — testing non-locality and Bell inequalities
- [Density Matrices](../06-density-matrices/README.md) — explore partial trace calculations and reduced density matrices
