# Circuits & Gates — Exercise Solutions

This file contains worked solutions for the exercises in:

```text
docs/05-circuits-and-gates/README.md
```

The goal is to connect the algebraic solution with the corresponding NumPy implementation in `quantum_ed`.

---

## Exercise 1 — Show that X² = I

We want to show that:

$$
X^2 = I
$$

The Pauli-X matrix is:

$$
X =
\begin{bmatrix}
0 & 1 \\
1 & 0
\end{bmatrix}
$$

Compute:

$$
X^2 =
\begin{bmatrix}
0 & 1 \\
1 & 0
\end{bmatrix}
\begin{bmatrix}
0 & 1 \\
1 & 0
\end{bmatrix}
$$

Matrix multiplication gives:

$$
X^2 =
\begin{bmatrix}
1 & 0 \\
0 & 1
\end{bmatrix}
=
I
$$

So:

$$
X^2 = I
$$

Python verification:

```python
import numpy as np

from quantum_ed.gates import X, I

assert np.allclose(X @ X, I)
```

---

## Exercise 2 — Compute H|0⟩ and H|1⟩

The Hadamard matrix is:

$$
H =
\frac{1}{\sqrt{2}}
\begin{bmatrix}
1 & 1 \\
1 & -1
\end{bmatrix}
$$

The computational basis states are:

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

First compute:

$$
H|0\rangle =
\frac{1}{\sqrt{2}}
\begin{bmatrix}
1 & 1 \\
1 & -1
\end{bmatrix}
\begin{bmatrix}
1 \\
0
\end{bmatrix}
$$

So:

$$
H|0\rangle =
\frac{1}{\sqrt{2}}
\begin{bmatrix}
1 \\
1
\end{bmatrix}
=
\frac{|0\rangle + |1\rangle}{\sqrt{2}}
$$

Now compute:

$$
H|1\rangle =
\frac{1}{\sqrt{2}}
\begin{bmatrix}
1 & 1 \\
1 & -1
\end{bmatrix}
\begin{bmatrix}
0 \\
1
\end{bmatrix}
$$

So:

$$
H|1\rangle =
\frac{1}{\sqrt{2}}
\begin{bmatrix}
1 \\
-1
\end{bmatrix}
=
\frac{|0\rangle - |1\rangle}{\sqrt{2}}
$$

Python verification:

```python
import numpy as np

from quantum_ed.gates import H, apply
from quantum_ed.states import ket0, ket1

plus = (1 / np.sqrt(2)) * np.array([[1], [1]], dtype=complex)
minus = (1 / np.sqrt(2)) * np.array([[1], [-1]], dtype=complex)

assert np.allclose(apply(H, ket0()), plus)
assert np.allclose(apply(H, ket1()), minus)
```

---

## Exercise 3 — Build a Bell State with H and CNOT

We start from:

$$
|00\rangle
$$

Using vector notation:

$$
|00\rangle =
\begin{bmatrix}
1 \\
0 \\
0 \\
0
\end{bmatrix}
$$

First, apply the Hadamard gate to the first qubit and the identity to the second qubit:

$$
H \otimes I
$$

So:

$$
(H \otimes I)|00\rangle
=
\frac{|00\rangle + |10\rangle}{\sqrt{2}}
$$

Now apply CNOT, where the first qubit is the control and the second qubit is the target.

CNOT acts as:

$$
\mathrm{CNOT}|00\rangle = |00\rangle
$$

and:

$$
\mathrm{CNOT}|10\rangle = |11\rangle
$$

Therefore:

$$
\mathrm{CNOT}(H \otimes I)|00\rangle
=
\frac{|00\rangle + |11\rangle}{\sqrt{2}}
$$

This is the Bell state:

$$
|\Phi^+\rangle =
\frac{|00\rangle + |11\rangle}{\sqrt{2}}
$$

Python verification:

```python
import numpy as np

from quantum_ed.gates import CNOT, H, I, apply, kron_n
from quantum_ed.states import basis_00, bell_phi_plus

state = basis_00()

state = apply(kron_n(H, I), state)
state = apply(CNOT, state)

assert np.allclose(state, bell_phi_plus())
```

---

## Exercise 4 — Verify the SWAP Truth Table

The SWAP gate exchanges two qubits.

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

In matrix form, using the basis order:

$$
|00\rangle,\ |01\rangle,\ |10\rangle,\ |11\rangle
$$

the SWAP matrix is:

$$
\mathrm{SWAP} =
\begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

Check the two non-trivial cases:

$$
\mathrm{SWAP}|01\rangle = |10\rangle
$$

and:

$$
\mathrm{SWAP}|10\rangle = |01\rangle
$$

Python verification:

```python
import numpy as np

from quantum_ed.gates import SWAP, apply
from quantum_ed.states import basis_00, basis_01, basis_10, basis_11

assert np.allclose(apply(SWAP, basis_00()), basis_00())
assert np.allclose(apply(SWAP, basis_01()), basis_10())
assert np.allclose(apply(SWAP, basis_10()), basis_01())
assert np.allclose(apply(SWAP, basis_11()), basis_11())
```

---

## Exercise 5 — Check that Rx(0), Ry(0), and Rz(0) Are the Identity

The rotation gates are:

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

At:

$$
\theta = 0
$$

we have:

$$
\cos(0/2) = \cos(0) = 1
$$

and:

$$
\sin(0/2) = \sin(0) = 0
$$

Therefore:

$$
R_x(0) =
\begin{bmatrix}
1 & 0 \\
0 & 1
\end{bmatrix}
=
I
$$

Also:

$$
R_y(0) =
\begin{bmatrix}
1 & 0 \\
0 & 1
\end{bmatrix}
=
I
$$

For $R_z$:

$$
e^{-i0/2} = e^0 = 1
$$

and:

$$
e^{i0/2} = e^0 = 1
$$

so:

$$
R_z(0) =
\begin{bmatrix}
1 & 0 \\
0 & 1
\end{bmatrix}
=
I
$$

Thus:

$$
R_x(0) = R_y(0) = R_z(0) = I
$$

Python verification:

```python
import numpy as np

from quantum_ed.gates import I, rx, ry, rz

assert np.allclose(rx(0.0), I)
assert np.allclose(ry(0.0), I)
assert np.allclose(rz(0.0), I)
```

---

## Combined Verification Script

The following script verifies all exercises together:

```python
import numpy as np

from quantum_ed.gates import (
    CNOT,
    H,
    I,
    SWAP,
    X,
    apply,
    kron_n,
    rx,
    ry,
    rz,
)
from quantum_ed.states import (
    basis_00,
    basis_01,
    basis_10,
    basis_11,
    bell_phi_plus,
    ket0,
    ket1,
)

# Exercise 1
assert np.allclose(X @ X, I)

# Exercise 2
plus = (1 / np.sqrt(2)) * np.array([[1], [1]], dtype=complex)
minus = (1 / np.sqrt(2)) * np.array([[1], [-1]], dtype=complex)

assert np.allclose(apply(H, ket0()), plus)
assert np.allclose(apply(H, ket1()), minus)

# Exercise 3
state = basis_00()
state = apply(kron_n(H, I), state)
state = apply(CNOT, state)

assert np.allclose(state, bell_phi_plus())

# Exercise 4
assert np.allclose(apply(SWAP, basis_00()), basis_00())
assert np.allclose(apply(SWAP, basis_01()), basis_10())
assert np.allclose(apply(SWAP, basis_10()), basis_01())
assert np.allclose(apply(SWAP, basis_11()), basis_11())

# Exercise 5
assert np.allclose(rx(0.0), I)
assert np.allclose(ry(0.0), I)
assert np.allclose(rz(0.0), I)

print("All circuit and gate exercise checks passed.")
```

---

