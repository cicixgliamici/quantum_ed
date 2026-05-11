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
\langle \psi' | \psi' \rangle
=
\langle \psi | U^\dagger U | \psi \rangle
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

## 12. Circuit Composition

A circuit is a sequence of gate applications.

If a circuit applies gates:

$$
U_1,\ U_2,\ U_3
$$

to an initial state:

$$
|\psi_0\rangle
$$

then the final state is:

$$
|\psi_{\mathrm{final}}\rangle
=
U_3 U_2 U_1 |\psi_0\rangle
$$

The order matters: the first gate applied to the state appears closest to the state vector.

In code:

```python
from quantum_ed.gates import apply

state = apply(U1, state)
state = apply(U2, state)
state = apply(U3, state)
```

This explicit style is useful for education because it makes the matrix multiplication order visible.

---

## 13. Bell-State Circuit

A simple example is the creation of the Bell state:

$$
|\Phi^+\rangle =
\frac{|00\rangle + |11\rangle}{\sqrt{2}}
$$

Start with:

$$
|00\rangle
$$

Apply `H` to the first qubit:

$$
(H \otimes I)|00\rangle
=
\frac{|00\rangle + |10\rangle}{\sqrt{2}}
$$

Then apply `CNOT`:

$$
\mathrm{CNOT}(H \otimes I)|00\rangle
=
\frac{|00\rangle + |11\rangle}{\sqrt{2}}
$$

In code:

```python
from quantum_ed.gates import CNOT, H, I, apply, kron_n
from quantum_ed.states import basis_00

state = basis_00()
state = apply(kron_n(H, I), state)
state = apply(CNOT, state)
```

This exact behavior is validated in the tests.

---

## 14. Code Connection

The main code for this chapter is located in:

```text
src/quantum_ed/gates.py
src/quantum_ed/linalg.py
src/quantum_ed/states.py
```

Useful functions and constants include:

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

The relevant tests are in:

```text
tests/test_gates.py
tests/test_bell_states.py
tests/test_linalg.py
```

Run them with:

```bash
python -m pytest -q
```

---

## 15. Exercises

### Exercise 1

Show that:

$$
X^2 = I
$$

Then verify it with NumPy.

---

### Exercise 2

Compute:

$$
H|0\rangle
$$

and:

$$
H|1\rangle
$$

Then verify the result using `quantum_ed.gates.H`.

---

### Exercise 3

Starting from $|00\rangle$, apply:

$$
H \otimes I
$$

then apply:

$$
\mathrm{CNOT}
$$

Verify that the result is:

$$
\frac{|00\rangle + |11\rangle}{\sqrt{2}}
$$

---

### Exercise 4

Verify the truth table of `SWAP`:

$$
\mathrm{SWAP}|01\rangle = |10\rangle
$$

and:

$$
\mathrm{SWAP}|10\rangle = |01\rangle
$$

---

### Exercise 5

Check numerically that:

$$
R_x(0) = R_y(0) = R_z(0) = I
$$

---

## 16. Next Steps

After this chapter, the natural next topics are:

- measurement in the computational basis
- density matrices
- partial trace
- noise channels
- simple circuit pipelines
- comparison with frameworks such as Qiskit
