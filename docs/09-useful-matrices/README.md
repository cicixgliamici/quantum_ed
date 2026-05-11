# Useful Matrices in Quantum Computing

This page collects the most common matrices used in introductory quantum computing.

The goal is not to create a disconnected formula sheet, but to provide a practical reference that links:

- linear algebra
- quantum states
- gates
- measurement
- density matrices
- noise channels
- Python implementations in `src/quantum_ed/`

---

## 1. Computational Basis

The standard one-qubit computational basis is:

$$
|0\rangle =
\begin{bmatrix}
1 \\
0
\end{bmatrix},
\qquad
|1\rangle =
\begin{bmatrix}
0 \\
1
\end{bmatrix}
$$

A generic one-qubit state is written as:

$$
|\psi\rangle = \alpha |0\rangle + \beta |1\rangle
$$

with normalization condition:

$$
|\alpha|^2 + |\beta|^2 = 1
$$

For two qubits, this repository uses the standard basis ordering:

$$
|00\rangle,\ |01\rangle,\ |10\rangle,\ |11\rangle
$$

This ordering is important because it determines the matrix representation of two-qubit gates such as `CNOT`, `CZ`, and `SWAP`.

---

## 2. Identity Matrix

The identity matrix is:

$$
I =
\begin{bmatrix}
1 & 0 \\
0 & 1
\end{bmatrix}
$$

It leaves every state unchanged:

$$
I|0\rangle = |0\rangle
$$

$$
I|1\rangle = |1\rangle
$$

$$
I|\psi\rangle = |\psi\rangle
$$

Properties:

$$
I^\dagger I = I
$$

$$
I^\dagger = I
$$

$$
I^2 = I
$$

In code:

```python
from quantum_ed.gates import I
```

---

## 3. Pauli Matrices

The Pauli matrices are among the most important matrices in quantum computing.

They are used as:

- quantum gates
- observables
- generators of rotations
- components of Hamiltonians
- building blocks for noise models

---

### 3.1 Pauli-X Gate

$$
X =
\begin{bmatrix}
0 & 1 \\
1 & 0
\end{bmatrix}
$$

The Pauli-X gate acts like a quantum NOT gate on computational-basis states:

$$
X|0\rangle = |1\rangle
$$

$$
X|1\rangle = |0\rangle
$$

Properties:

$$
X^\dagger X = I
$$

$$
X^\dagger = X
$$

$$
X^2 = I
$$

Geometric intuition: `X` corresponds to a rotation by pi around the x-axis of the Bloch sphere.

In code:

```python
from quantum_ed.gates import X
```

---

### 3.2 Pauli-Y Gate

$$
Y =
\begin{bmatrix}
0 & -i \\
i & 0
\end{bmatrix}
$$

The Pauli-Y gate flips basis states while introducing complex phases:

$$
Y|0\rangle = i|1\rangle
$$

$$
Y|1\rangle = -i|0\rangle
$$

Properties:

$$
Y^\dagger Y = I
$$

$$
Y^\dagger = Y
$$

$$
Y^2 = I
$$

Geometric intuition: `Y` corresponds to a rotation by pi around the y-axis of the Bloch sphere.

In code:

```python
from quantum_ed.gates import Y
```

---

### 3.3 Pauli-Z Gate

$$
Z =
\begin{bmatrix}
1 & 0 \\
0 & -1
\end{bmatrix}
$$

The Pauli-Z gate leaves $|0\rangle$ unchanged and flips the phase of $|1\rangle$:

$$
Z|0\rangle = |0\rangle
$$

$$
Z|1\rangle = -|1\rangle
$$

Properties:

$$
Z^\dagger Z = I
$$

$$
Z^\dagger = Z
$$

$$
Z^2 = I
$$

Geometric intuition: `Z` corresponds to a rotation by pi around the z-axis of the Bloch sphere.

In code:

```python
from quantum_ed.gates import Z
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

It maps computational-basis states into equal superpositions:

$$
H|0\rangle =
\frac{|0\rangle + |1\rangle}{\sqrt{2}}
$$

$$
H|1\rangle =
\frac{|0\rangle - |1\rangle}{\sqrt{2}}
$$

The states produced are usually called:

$$
|+\rangle =
\frac{|0\rangle + |1\rangle}{\sqrt{2}}
$$

$$
|-\rangle =
\frac{|0\rangle - |1\rangle}{\sqrt{2}}
$$

Properties:

$$
H^\dagger H = I
$$

$$
H^\dagger = H
$$

$$
H^2 = I
$$

The Hadamard gate is often used before an entangling gate such as `CNOT` to create Bell states:

$$
\mathrm{CNOT}(H \otimes I)|00\rangle
=
\frac{|00\rangle + |11\rangle}{\sqrt{2}}
$$

In code:

```python
from quantum_ed.gates import H
```

---

## 5. Phase Gates

Phase gates do not directly change the probabilities of measuring $|0\rangle$ or $|1\rangle$.

Instead, they change the relative phase between basis components.

---

### 5.1 S Gate

$$
S =
\begin{bmatrix}
1 & 0 \\
0 & i
\end{bmatrix}
$$

Action on basis states:

$$
S|0\rangle = |0\rangle
$$

$$
S|1\rangle = i|1\rangle
$$

Properties:

$$
S^\dagger S = I
$$

$$
S^2 = Z
$$

The matrix $S$ is unitary but not Hermitian.

In code:

```python
from quantum_ed.gates import S
```

---

### 5.2 T Gate

$$
T =
\begin{bmatrix}
1 & 0 \\
0 & e^{i\pi/4}
\end{bmatrix}
$$

Action on basis states:

$$
T|0\rangle = |0\rangle
$$

$$
T|1\rangle = e^{i\pi/4}|1\rangle
$$

Properties:

$$
T^\dagger T = I
$$

$$
T^2 = S
$$

The matrix $T$ is unitary but not Hermitian.

In code:

```python
from quantum_ed.gates import T
```

---

## 6. Rotation Gates

Rotation gates are parameterized gates.

They are especially important in:

- variational quantum algorithms
- quantum machine learning
- hardware-level pulse intuition
- Bloch sphere dynamics

---

### 6.1 Rotation Around X

$$
R_x(\theta) =
\begin{bmatrix}
\cos(\theta/2) & -i\sin(\theta/2) \\
-i\sin(\theta/2) & \cos(\theta/2)
\end{bmatrix}
$$

---

### 6.2 Rotation Around Y

$$
R_y(\theta) =
\begin{bmatrix}
\cos(\theta/2) & -\sin(\theta/2) \\
\sin(\theta/2) & \cos(\theta/2)
\end{bmatrix}
$$

---

### 6.3 Rotation Around Z

$$
R_z(\theta) =
\begin{bmatrix}
e^{-i\theta/2} & 0 \\
0 & e^{i\theta/2}
\end{bmatrix}
$$

Basic check:

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

## 7. Two-Qubit Gates

Two-qubit gates act on four-dimensional state vectors.

The basis order used here is:

$$
|00\rangle,\ |01\rangle,\ |10\rangle,\ |11\rangle
$$

---

### 7.1 CNOT Gate

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

In this convention:

- the first qubit is the control
- the second qubit is the target

Truth table:

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

CNOT is a key entangling gate:

$$
\mathrm{CNOT}(H \otimes I)|00\rangle
=
\frac{|00\rangle + |11\rangle}{\sqrt{2}}
$$

In code:

```python
from quantum_ed.gates import CNOT
```

---

### 7.2 Controlled-Z Gate

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

Action:

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

Unlike CNOT, CZ does not flip a target bit. It applies a phase only when both qubits are $1$.

In code:

```python
from quantum_ed.gates import CZ
```

---

### 7.3 SWAP Gate

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

Action:

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

In code:

```python
from quantum_ed.gates import SWAP
```

---

## 8. Projectors and Measurement Matrices

Measurement in the computational basis can be described using projectors.

The projector onto $|0\rangle$ is:

$$
P_0 =
|0\rangle\langle 0|
=
\begin{bmatrix}
1 & 0 \\
0 & 0
\end{bmatrix}
$$

The projector onto $|1\rangle$ is:

$$
P_1 =
|1\rangle\langle 1|
=
\begin{bmatrix}
0 & 0 \\
0 & 1
\end{bmatrix}
$$

For a one-qubit state:

$$
|\psi\rangle = \alpha |0\rangle + \beta |1\rangle
$$

the measurement probabilities are:

$$
\Pr(0) =
\langle \psi | P_0 | \psi \rangle
=
|\alpha|^2
$$

$$
\Pr(1) =
\langle \psi | P_1 | \psi \rangle
=
|\beta|^2
$$

Projectors are Hermitian but generally not unitary. They satisfy:

$$
P_0 + P_1 = I
$$

$$
P_0P_1 = 0
$$

---

## 9. Density Matrices

A pure state density matrix is:

$$
\rho = |\psi\rangle\langle\psi|
$$

For example:

$$
|0\rangle\langle 0|
=
\begin{bmatrix}
1 & 0 \\
0 & 0
\end{bmatrix}
$$

$$
|1\rangle\langle 1|
=
\begin{bmatrix}
0 & 0 \\
0 & 1
\end{bmatrix}
$$

The maximally mixed one-qubit state is:

$$
\rho =
\frac{1}{2}I
=
\begin{bmatrix}
1/2 & 0 \\
0 & 1/2
\end{bmatrix}
$$

Density matrices are useful because they represent:

- pure states
- mixed states
- subsystems of entangled systems
- noisy quantum states

In code:

```python
from quantum_ed.density import rho_from_ket
```

---

## 10. Bell-State Density Matrix

The Bell state is:

$$
|\Phi^+\rangle =
\frac{|00\rangle + |11\rangle}{\sqrt{2}}
$$

Its density matrix is:

$$
\rho_{\Phi^+}
=
|\Phi^+\rangle\langle\Phi^+|
$$

Explicitly:

$$
\rho_{\Phi^+}
=
\frac{1}{2}
\begin{bmatrix}
1 & 0 & 0 & 1 \\
0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 \\
1 & 0 & 0 & 1
\end{bmatrix}
$$

This matrix is useful for studying:

- entanglement
- partial trace
- reduced density matrices
- mixed states arising from subsystems

In code:

```python
from quantum_ed.states import bell_phi_plus
from quantum_ed.density import rho_from_ket
```

---

## 11. Noise-Channel Matrices

Quantum noise can be represented using Kraus operators.

A noisy channel maps a density matrix as:

$$
\rho_{\mathrm{out}} = \sum_i K_i \rho K_i^\dagger
$$

where the Kraus operators satisfy:

$$
\sum_i K_i^\dagger K_i = I
$$

---

### 11.1 Bit-Flip Channel

The bit-flip channel applies $X$ with probability $p$:

$$
K_0 = \sqrt{1-p}\,I
$$

$$
K_1 = \sqrt{p}\,X
$$

---

### 11.2 Phase-Flip Channel

The phase-flip channel applies $Z$ with probability $p$:

$$
K_0 = \sqrt{1-p}\,I
$$

$$
K_1 = \sqrt{p}\,Z
$$

---

### 11.3 Depolarizing Channel

A one-qubit depolarizing channel can be described using Pauli matrices:

$$
\rho_{\mathrm{out}}
=
(1-p)\rho
+
\frac{p}{3}X\rho X
+
\frac{p}{3}Y\rho Y
+
\frac{p}{3}Z\rho Z
$$

This shows why the Pauli matrices are not only gates, but also a natural basis for describing noise.

---

## 12. Quick Reference Table

| Matrix | Dimension | Unitary | Hermitian | Main role |
|---|---:|---:|---:|---|
| $I$ | $2 \times 2$ | yes | yes | identity |
| $X$ | $2 \times 2$ | yes | yes | bit flip |
| $Y$ | $2 \times 2$ | yes | yes | phase + bit flip |
| $Z$ | $2 \times 2$ | yes | yes | phase flip |
| $H$ | $2 \times 2$ | yes | yes | superposition |
| $S$ | $2 \times 2$ | yes | no | phase gate |
| $T$ | $2 \times 2$ | yes | no | phase gate |
| $R_x(\theta)$ | $2 \times 2$ | yes | generally no | x-axis rotation |
| $R_y(\theta)$ | $2 \times 2$ | yes | generally no | y-axis rotation |
| $R_z(\theta)$ | $2 \times 2$ | yes | generally no | z-axis rotation |
| $\mathrm{CNOT}$ | $4 \times 4$ | yes | yes | controlled bit flip |
| $\mathrm{CZ}$ | $4 \times 4$ | yes | yes | controlled phase |
| $\mathrm{SWAP}$ | $4 \times 4$ | yes | yes | exchange two qubits |
| $P_0, P_1$ | $2 \times 2$ | no | yes | measurement |
| $\rho$ | $n \times n$ | no | yes | quantum state as density matrix |

---

## 13. Code Connection

The matrices and operations described here are connected to the repository code:

```text
src/quantum_ed/gates.py
src/quantum_ed/linalg.py
src/quantum_ed/states.py
src/quantum_ed/density.py
src/quantum_ed/channels.py
```

Recommended validation command:

```bash
python -m pytest -q
```

Useful tests to add or inspect:

```text
tests/test_gates.py
tests/test_linalg.py
tests/test_density.py
tests/test_channels.py
```

The intended idea is:

```text
formula -> implementation -> test -> notebook demonstration
```

This keeps the repository educational, inspectable, and technically credible.
