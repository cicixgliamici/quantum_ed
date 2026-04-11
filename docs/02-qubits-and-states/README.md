# Qubits & States

A single qubit lives in a 2D complex Hilbert space.

This is the basic mathematical object of quantum computing: a normalized vector in

$$
\mathbb{C}^2
$$

---

## 1. State vector

A pure qubit state is a unit vector of the form

$$
|\psi\rangle = \alpha |0\rangle + \beta |1\rangle
$$

where

$$
\alpha,\beta \in \mathbb{C}
$$

and normalization requires

$$
|\alpha|^2 + |\beta|^2 = 1
$$

The basis states are

$$
|0\rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix},
\qquad
|1\rangle = \begin{pmatrix} 0 \\ 1 \end{pmatrix}
$$

A qubit is therefore not just “0 or 1”, but a complex superposition of the two basis states.

---

## 2. Global phase

Not every difference in the state vector corresponds to a physically observable difference.

If two states differ only by a global phase factor,

$$
|\psi'\rangle = e^{i\phi} |\psi\rangle
$$

then they describe the same physical state.

So

$$
|\psi\rangle
\quad \text{and} \quad
e^{i\phi} |\psi\rangle
$$

are physically indistinguishable.

This is why quantum states are really rays in Hilbert space, not just raw vectors.

---

## 3. Bloch sphere

Any pure qubit state can be written, up to global phase, as

$$
|\psi\rangle = \cos\left(\frac{\theta}{2}\right)|0\rangle + e^{i\varphi}\sin\left(\frac{\theta}{2}\right)|1\rangle
$$

This gives a geometric representation on the Bloch sphere.

The corresponding Bloch vector is

$$
\vec{r} = (\sin\theta\cos\varphi,\ \sin\theta\sin\varphi,\ \cos\theta)
$$

This representation is useful because it turns an abstract qubit state into a point on a sphere:

- north pole: $|0\rangle$
- south pole: $|1\rangle$
- equator: equal-weight superpositions with different phases

---

## 4. Why this matters

The qubit is the basic information unit of quantum computing.

Understanding pure states means understanding:

- amplitudes
- normalization
- phase
- geometric intuition

These ideas are the basis for gates, measurement, entanglement, and noise.

---

## In code

Relevant functions in this repository:

- `ket0`
- `ket1`
- `normalize`
- `bloch_vector`
- `state_from_bloch`

These live in:

- `src/quantum_ed/states.py`

---

## Exercises

### Exercise 1

Show that $|0\rangle$ and $|1\rangle$ are normalized.

### Exercise 2

Construct the state

$$
|+\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)
$$

and verify that it is normalized.

### Exercise 3

What is the Bloch vector of $|0\rangle$?

### Exercise 4

What is the Bloch vector of $|1\rangle$?

---

## Notebook

- `../../notebooks/01-qubit-bloch.ipynb`

## Next

- `docs/03-measurement/README.md`
- `docs/04-entanglement/README.md`
