# Circuits & Gates

Quantum circuits are built by applying gates to quantum states.

In the state-vector model used in this repository:

- states are column vectors
- gates are matrices
- one-qubit gates are usually `2 x 2` matrices
- two-qubit gates are usually `4 x 4` matrices
- applying a gate means multiplying the gate matrix by the state vector

If the current state is:

$$
|\psi\rangle
$$

and the gate is:

$$
U
$$

then the new state is:

$$
|\psi'\rangle = U|\psi\rangle
$$

This repository keeps these operations explicit and NumPy-based so that the mathematical structure remains inspectable.

---

## 1. Why Gates Are Unitary

Quantum gates must preserve the norm of the state vector.

If a state is normalized, then:

$$
\langle \psi | \psi \rangle = 1
$$

After applying a gate $U$, we want:

$$
\langle \psi' | \psi' \rangle = 1
$$

Since:

$$
|\psi'\rangle = U|\psi\rangle
$$

we get:

$$
\langle \psi' | \psi' \rangle = \langle \psi | U^\dagger U | \psi \rangle
$$

So the condition for norm preservation is:

$$
U^\dagger U = I
$$

A matrix satisfying this condition is called **unitary**.

This is why gates such as `X`, `Y`, `Z`, `H`, `S`, `T`, `CNOT`, `CZ`, and `SWAP` are implemented as unitary matrices.

In code, unitarity is checked with:

```python
from quantum_ed.linalg import is_unitary
```

---

## 2. One-Qubit Gates

A one-qubit gate acts on a one-qubit state:

$$
|\psi\rangle =
\alpha |0\rangle + \beta |1\rangle
$$

where:

$$
|\alpha|^2 + |\beta|^2 = 1
$$

The corresponding state-vector representation is:

$$
|\psi\rangle =
\begin{bmatrix}
\alpha \\
\beta
\end{bmatrix}
$$

A one-qubit gate is represented by a `2 x 2` matrix.

---

## 3. Pauli Gates

The Pauli gates are:

$$
X =
\begin{bmatrix}
0 & 1 \\
1 & 0
\end{bmatrix}
$$

$$
Y =
\begin{bmatrix}
0 & -i \\
i & 0
\end{bmatrix}
$$

$$
Z =
\begin{bmatrix}
1 & 0 \\
0 & -1
\end{bmatrix}
$$

They satisfy:

$$
X^2 = I
$$

$$
Y^2 = I
$$

$$
Z^2 = I
$$

They are also Hermitian:

$$
X^\dagger = X
$$

$$
Y^\dagger = Y
$$

$$
Z^\dagger = Z
$$

and unitary:

$$
X^\dagger X = I
$$

$$
Y^\dagger Y = I
$$

$$
Z^\dagger Z = I
$$

Operationally:

- `X` flips $|0\rangle$ and $|1\rangle$
- `Y` flips the basis states and introduces complex phases
- `Z` flips the phase of $|1\rangle$

In code:

```python
from quantum_ed.gates import X, Y, Z
```

---

## 4. Hadamard Gate

The Hadamard gate is:

$$
H =
\frac{1}{\sqrt{2}}
\begin{bmatrix}
1 & 1 \\
1 & -1
\end{bmatrix}
$$

It creates equal superpositions from computational-basis states:

$$
H|0\rangle =
\frac{|0\rangle + |1\rangle}{\sqrt{2}}
$$

$$
H|1\rangle =
\frac{|0\rangle - |1\rangle}{\sqrt{2}}
$$

The Hadamard gate satisfies:

$$
H^2 = I
$$

and:

$$
H^\dagger = H
$$

So it is both unitary and Hermitian.

In code:

```python
from quantum_ed.gates import H
```

---

## 5. Phase Gates

The phase gates modify the relative phase of a qubit.

The `S` gate is:

$$
S =
\begin{bmatrix}
1 & 0 \\
0 & i
\end{bmatrix}
$$

The `T` gate is:

$$
T =
\begin{bmatrix}
1 & 0 \\
0 & e^{i\pi/4}
\end{bmatrix}
$$

They satisfy:

$$
S^2 = Z
$$

and:

$$
T^2 = S
$$

In code:

```python
from quantum_ed.gates import S, T
```

---

## 6. Rotation Gates

Rotation gates are parameterized gates.

They are useful for:

- Bloch-sphere intuition
- variational circuits
- hardware-aware reasoning
- algorithms with tunable parameters

The basic rotations are:

$$
R_x(\theta) =
\begin{bmatrix}
\cos(\theta/2) & -i\sin(\theta/2) \\
-i\sin(\theta/2) & \cos(\theta/2)
\end{bmatrix}
$$

$$
R_y(\theta) =
\begin{bmatrix}
\cos(\theta/2) & -\sin(\theta/2) \\
\sin(\theta/2) & \cos(\theta/2)
\end{bmatrix}
$$

$$
R_z(\theta) =
\begin{bmatrix}
e^{-i\theta/2} & 0 \\
0 & e^{i\theta/2}
\end{bmatrix}
$$

At zero angle, each rotation becomes the identity:

$$
R_x(0) = I
$$

$$
R_y(0) = I
$$

$$
R_z(0) = I
$$

In code:

```python
from quantum_ed.gates import rx, ry, rz
```

---

## 7. Tensor Products and Multi-Qubit States

To combine qubits, we use the tensor product.

For example, the two-qubit state $|00\rangle$ is:

$$
|00\rangle =
|0\rangle \otimes |0\rangle
$$

Using the computational basis ordering:

$$
|00\rangle,\ |01\rangle,\ |10\rangle,\ |11\rangle
$$

a two-qubit state is represented by a four-dimensional vector.

For example:

$$
|00\rangle =
\begin{bmatrix}
1 \\
0 \\
0 \\
0
\end{bmatrix}
$$

To apply a one-qubit gate to part of a two-qubit state, we use tensor products of gates.

For example, applying `H` to the first qubit and doing nothing to the second qubit is:

$$
H \otimes I
$$

In code:

```python
from quantum_ed.gates import H, I, kron_n

op = kron_n(H, I)
```

### Multi-Qubit Gate Embedding

In an $n$-qubit quantum register, applying a single-qubit gate $U$ to qubit $k$ (with 0-indexed positions from left to right) while leaving all other qubits unchanged is represented mathematically by the tensor product:

$$
U^{(k)} = I^{\otimes k} \otimes U \otimes I^{\otimes (n - 1 - k)}
$$

For example, in a 3-qubit register ($n=3$):

- Applying $X$ to qubit 0: $X \otimes I \otimes I$
- Applying $H$ to qubit 1: $I \otimes H \otimes I$
- Applying $Z$ to qubit 2: $I \otimes I \otimes Z$

In this repository's NumPy architecture, you construct these operators using `kron_n`:

```python
from quantum_ed.gates import H, I, kron_n

# Apply H to qubit 1 in a 3-qubit system:
op_q1 = kron_n(I, H, I)  # 8x8 matrix operator
```

---

## 8. Two-Qubit Gates

Two-qubit gates act on two-qubit states and are represented by `4 x 4` matrices.

The two-qubit gates currently implemented include:

- `CNOT`
- `CZ`
- `SWAP`

In code:

```python
from quantum_ed.gates import CNOT, CZ, SWAP
```

---

## 9. CNOT Gate

The CNOT gate is:

$$
\mathrm{CNOT} =
\begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 0 & 1 \\
0 & 0 & 1 & 0
\end{bmatrix}
$$

With the basis ordering:

$$
|00\rangle,\ |01\rangle,\ |10\rangle,\ |11\rangle
$$

this convention means:

- the first qubit is the control
- the second qubit is the target

The truth table is:

$$
\mathrm{CNOT}|00\rangle = |00\rangle
$$

$$
\mathrm{CNOT}|01\rangle = |01\rangle
$$

$$
\mathrm{CNOT}|10\rangle = |11\rangle
$$

$$
\mathrm{CNOT}|11\rangle = |10\rangle
$$

CNOT is important because it can create entanglement when combined with superposition.

---

## 10. Controlled-Z Gate

The controlled-Z gate is:

$$
\mathrm{CZ} =
\begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & -1
\end{bmatrix}
$$

Its action is:

$$
\mathrm{CZ}|00\rangle = |00\rangle
$$

$$
\mathrm{CZ}|01\rangle = |01\rangle
$$

$$
\mathrm{CZ}|10\rangle = |10\rangle
$$

$$
\mathrm{CZ}|11\rangle = -|11\rangle
$$

Unlike CNOT, `CZ` does not flip a qubit. It only adds a phase when both qubits are in state $|1\rangle$.

---

## 11. SWAP Gate

The SWAP gate exchanges two qubits:

$$
\mathrm{SWAP} =
\begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

Its action is:

$$
\mathrm{SWAP}|00\rangle = |00\rangle
$$

$$
\mathrm{SWAP}|01\rangle = |10\rangle
$$

$$
\mathrm{SWAP}|10\rangle = |01\rangle
$$

$$
\mathrm{SWAP}|11\rangle = |11\rangle
$$

SWAP is useful when reasoning about qubit ordering and hardware connectivity.

---

## 12. General Controlled Gates and Circuit Identities

A two-qubit controlled gate applies an arbitrary single-qubit unitary $U$ to the target qubit if and only if the control qubit is in state $|1\rangle$. Mathematically, in block-diagonal matrix form:

$$
C(U) = |0\rangle\langle 0| \otimes I + |1\rangle\langle 1| \otimes U = \begin{bmatrix} I & 0 \\ 0 & U \end{bmatrix}
$$

When $U = X$, we recover the standard $\mathrm{CNOT}$ gate:

$$
\mathrm{CNOT} = |0\rangle\langle 0| \otimes I + |1\rangle\langle 1| \otimes X
$$

When $U = Z$, we obtain the controlled-Z gate $\mathrm{CZ}$:

$$
\mathrm{CZ} = |0\rangle\langle 0| \otimes I + |1\rangle\langle 1| \otimes Z = |00\rangle\langle 00| + |01\rangle\langle 01| + |10\rangle\langle 10| - |11\rangle\langle 11|
$$

Notice that $\mathrm{CZ}$ is completely symmetric under exchange of control and target: it introduces a $(-1)$ phase factor only when both qubits are in state $|1\rangle$. Therefore, either qubit can be viewed as control or target.

### Useful Circuit Equivalence Identities

Several algebraic identities are fundamental for circuit optimization and hardware compilation:

1. **Conjugation between $\mathrm{CNOT}$ and $\mathrm{CZ}$:**
   Since $H X H = Z$ and $H Z H = X$, placing Hadamard gates on the target qubit converts $\mathrm{CZ}$ into $\mathrm{CNOT}$ and vice versa:

$$
\mathrm{CNOT}_{0\to 1} = (I \otimes H) \mathrm{CZ} (I \otimes H)
$$

2. **Reversing the Direction of CNOT:**
   Surrounding both qubits of a $\mathrm{CNOT}$ with Hadamard gates reverses the control and target roles:

$$
\mathrm{CNOT}_{1\to 0} = (H \otimes H) \mathrm{CNOT}_{0\to 1} (H \otimes H)
$$

   This identity is widely used in quantum compilers when hardware coupling maps only support directional CNOTs.

3. **SWAP Decomposition into 3 CNOTs:**
   A two-qubit $\mathrm{SWAP}$ gate can be synthesized entirely from three alternating $\mathrm{CNOT}$ gates:

$$
\mathrm{SWAP} = \mathrm{CNOT}_{0\to 1}\ \mathrm{CNOT}_{1\to 0}\ \mathrm{CNOT}_{0\to 1}
$$

   In NumPy verification:

```python
import numpy as np
from quantum_ed.gates import CNOT, H, I, SWAP, kron_n

H2 = kron_n(H, H)
cnot_rev = H2 @ CNOT @ H2  # CNOT with control=1, target=0
swap_synth = CNOT @ cnot_rev @ CNOT

assert np.allclose(swap_synth, SWAP)
```

---

## 13. The Phase Kickback Phenomenon

Phase kickback is the core engine behind quantum speedups in algorithms such as Deutsch-Jozsa, Bernstein-Vazirani, Grover search, and Quantum Phase Estimation (QPE).

Suppose a controlled gate $C(U)$ is applied where the target qubit is prepared in an eigenstate $|u\rangle$ of $U$ with eigenvalue $e^{i\theta}$:

$$
U|u\rangle = e^{i\theta}|u\rangle
$$

Let the control qubit be in an arbitrary superposition $\alpha|0\rangle + \beta|1\rangle$. The action of $C(U)$ on the joint state is:

$$
C(U) [(\alpha|0\rangle + \beta|1\rangle) \otimes |u\rangle] = \alpha |0\rangle \otimes |u\rangle + \beta |1\rangle \otimes U|u\rangle
$$

$$
= \alpha |0\rangle \otimes |u\rangle + \beta e^{i\theta} |1\rangle \otimes |u\rangle = (\alpha |0\rangle + \beta e^{i\theta}|1\rangle) \otimes |u\rangle
$$

**The key insight:** Even though the gate nominally targets the second qubit, the eigenvalue phase $e^{i\theta}$ is "kicked back" into the relative phase of the control qubit, leaving the target state $|u\rangle$ completely unchanged and unentangled.

For a standard $\mathrm{CNOT}$, the target state $|-\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}}$ is an eigenstate of $X$ with eigenvalue $(-1)$:

$$
X|-\rangle = -|-\rangle
$$

Applying $\mathrm{CNOT}$ with target $|-\rangle$ yields:

$$
\mathrm{CNOT}[(\alpha|0\rangle + \beta|1\rangle) \otimes |-\rangle] = (\alpha|0\rangle - \beta|1\rangle) \otimes |-\rangle
$$

The target qubit flipped the relative sign of the control qubit without changing its own state.

---

## 14. Circuit Composition & Temporal Ordering

A quantum circuit represents a sequence of gate applications over time. When translating a circuit diagram into matrix algebra:

1. **Left-to-right in circuit diagrams = Right-to-left in matrix multiplication:**
   If a circuit applies gate $U_1$, then $U_2$, then $U_3$ to initial state $|\psi_0\rangle$:

   ```text
   |ψ₀⟩ ---[ U₁ ]---[ U₂ ]---[ U₃ ]---> |ψ_final⟩
   ```

   The final state vector is:

$$
|\psi_{\mathrm{final}}\rangle = U_3 U_2 U_1 |\psi_0\rangle
$$

   The operator acting first appears adjacent to the ket $|\psi_0\rangle$.

2. **Sequential application in code:**

   ```python
   from quantum_ed.gates import apply

   state = apply(U1, state)
   state = apply(U2, state)
   state = apply(U3, state)
   ```

3. **Circuit Depth and Parallelism:**
   Gates that act on disjoint sets of qubits commute and can be executed simultaneously in the same time step (layer). The **depth** of a circuit is the number of discrete time steps required to execute all layers, which dictates how long qubits must retain their coherence.

---

## 15. Single-Qubit Euler ($ZYZ$) Decomposition & Universality

### Euler Angle ($ZYZ$) Decomposition

Any arbitrary single-qubit unitary $U \in U(2)$ can be parameterized by four real angles $(\alpha, \beta, \gamma, \delta)$ as a sequence of rotations about the $Z$ and $Y$ axes:

$$
U = e^{i\alpha} R_z(\beta) R_y(\gamma) R_z(\delta)
$$

Because $R_z$ and $R_y$ rotate around orthogonal axes on the Bloch sphere, any orientation can be reached by:
1. Rotating around the $Z$-axis by $\delta$
2. Rotating around the $Y$-axis by $\gamma$
3. Rotating around the $Z$-axis by $\beta$
4. Adding an overall global phase $e^{i\alpha}$

This is the standard decomposition used by hardware transpilers (e.g. Qiskit's `U3` or `RZ-SX-RZ` decomposition) to implement arbitrary single-qubit gates on physical hardware.

### Quantum Universality

A set of quantum gates is called **universal** if any unitary operation on any number of qubits can be approximated to arbitrary accuracy by a circuit composed entirely of gates from that set.

- **Exact Universality (Barenco et al., 1995):**
  The set of all single-qubit gates together with the two-qubit $\mathrm{CNOT}$ gate is universal for quantum computation. Any $n$-qubit unitary can be decomposed into single-qubit rotations and CNOTs.

- **The Clifford Group and Gottesman-Knill Theorem:**
  The Clifford group $\mathcal{C}_n$ is the group of unitaries that map the Pauli group back into itself under conjugation:

$$
U \mathcal{P}_n U^\dagger = \mathcal{P}_n
$$

  The Clifford group is generated by $\{H, S, \mathrm{CNOT}\}$. While Clifford gates generate superposition, entanglement, and teleportation, the **Gottesman-Knill Theorem** proves that any circuit composed solely of:
  1. Preparation of computational basis states $|0\dots 0\rangle$
  2. Clifford gates ($H, S, \mathrm{CNOT}$)
  3. Measurement of Pauli observables ($Z$)
  can be **simulated efficiently on a classical computer in polynomial time $O(n^2)$** using stabilizer tableaus.

- **Fault-Tolerant Universality (Clifford + $T$):**
  To achieve quantum computational advantage, we must include a non-Clifford gate. The standard choice is the $T$ gate ($\pi/8$ gate):

$$
T = \begin{bmatrix} 1 & 0 \\ 0 & e^{i\pi/4} \end{bmatrix}
$$

  The set $\{H, S, \mathrm{CNOT}, T\}$ forms a universal gate set for quantum computing.

- **The Solovay-Kitaev Theorem:**
  The Solovay-Kitaev theorem guarantees that any arbitrary single-qubit gate can be approximated to within precision $\epsilon > 0$ using a sequence of only $O(\log^c(1/\epsilon))$ gates from a discrete universal set (such as Clifford + $T$), where $c \approx 1$ to $2$. This logarithmic scaling makes fault-tolerant compilation practical.

---

## 16. Bell-State Circuit

A canonical two-qubit example is creating the maximally entangled Bell state:

$$
|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}
$$

1. Prepare $|00\rangle$:

$$
|\psi_0\rangle = |00\rangle
$$

2. Apply Hadamard to qubit 0 to create an equal superposition:

$$
|\psi_1\rangle = (H \otimes I)|00\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}} \otimes |0\rangle = \frac{|00\rangle + |10\rangle}{\sqrt{2}}
$$

3. Apply $\mathrm{CNOT}$ (control=0, target=1). When qubit 0 is $|0\rangle$, qubit 1 remains $|0\rangle$. When qubit 0 is $|1\rangle$, qubit 1 flips to $|1\rangle$:

$$
|\psi_2\rangle = \mathrm{CNOT}|\psi_1\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}
$$

In Python:

```python
from quantum_ed.gates import CNOT, H, I, apply, kron_n
from quantum_ed.states import basis_00

state = basis_00()
state = apply(kron_n(H, I), state)
state = apply(CNOT, state)
```

---

## 17. Code Connection

The main code for this chapter is located in:

- [`src/quantum_ed/gates.py`](file:///c:/Progetti/quantum_ed/src/quantum_ed/gates.py)
- [`src/quantum_ed/linalg.py`](file:///c:/Progetti/quantum_ed/src/quantum_ed/linalg.py)
- [`src/quantum_ed/states.py`](file:///c:/Progetti/quantum_ed/src/quantum_ed/states.py)

Key gate definitions and functions:

```python
from quantum_ed.gates import (
    I,
    X,
    Y,
    Z,
    H,
    S,
    T,
    CNOT,
    CZ,
    SWAP,
    rx,
    ry,
    rz,
    kron_n,
    apply,
)
```

Run test suite:

```bash
python -m pytest tests/test_gates.py tests/test_bell_states.py -q
```

---

## 18. Exercises

Detailed solutions for Exercises 1–5 are available in [solutions.md](solutions.md).

### Exercise 1 — Pauli Involutions
Show analytically and verify with NumPy that:

$$
X^2 = I, \quad Y^2 = I, \quad Z^2 = I
$$

### Exercise 2 — Hadamard Action
Compute the explicit matrix-vector products $H|0\rangle$ and $H|1\rangle$ and express the results in terms of $|+\rangle$ and $|-\rangle$.

### Exercise 3 — Entanglement Generation
Starting from $|00\rangle$, apply $(H \otimes I)$ followed by $\mathrm{CNOT}$. Compute the resulting state vector and verify that it equals $|\Phi^+\rangle$.

### Exercise 4 — SWAP Truth Table
Verify analytically and numerically that $\mathrm{SWAP}|01\rangle = |10\rangle$ and $\mathrm{SWAP}|10\rangle = |01\rangle$.

### Exercise 5 — Identity Limit of Rotations
Demonstrate that $R_x(0) = R_y(0) = R_z(0) = I$.

### Exercise 6 — CNOT Control/Target Inversion
Prove that surrounding a $\mathrm{CNOT}$ with Hadamard gates on both qubits reverses its direction:

$$
(H \otimes H) \mathrm{CNOT}_{0\to 1} (H \otimes H) = \mathrm{CNOT}_{1\to 0}
$$

**Solution hint:** Write out the matrix product using $H \otimes H = \frac{1}{2} \begin{bmatrix} 1 & 1 & 1 & 1 \\ 1 & -1 & 1 & -1 \\ 1 & 1 & -1 & -1 \\ 1 & -1 & -1 & 1 \end{bmatrix}$ and compute $(H \otimes H)\mathrm{CNOT}(H \otimes H)$.

### Exercise 7 — SWAP Synthesis
Show that three alternating CNOT gates synthesize a SWAP gate:

$$
\mathrm{CNOT}_{0\to 1}\ \mathrm{CNOT}_{1\to 0}\ \mathrm{CNOT}_{0\to 1} = \mathrm{SWAP}
$$

**Solution hint:** Trace the evolution of computational basis kets $|a, b\rangle$:
1. After first CNOT: $|a, a \oplus b\rangle$
2. After second CNOT: $|a \oplus (a \oplus b), a \oplus b\rangle = |b, a \oplus b\rangle$
3. After third CNOT: $|b, (a \oplus b) \oplus b\rangle = |b, a\rangle$
Since $|a, b\rangle \mapsto |b, a\rangle$ for all $a, b \in \{0, 1\}$, the composite circuit equals $\mathrm{SWAP}$.

---

## 19. Next Steps

After mastering unitary gates and circuit composition, continue with:

- [Density Matrices](../06-density-matrices/README.md) — generalizing to mixed states and open systems
- [Noise & Channels](../07-noise-and-channels/README.md) — modeling decoherence and gate errors
- [Quantum Algorithms](../10-quantum-algorithms/README.md) — synthesizing gates into oracles and quantum speedups
