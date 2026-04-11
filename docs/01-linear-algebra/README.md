# Linear Algebra Essentials

Quantum computing is built on linear algebra.

States are vectors, gates are matrices, measurement probabilities come from amplitudes, and multi-qubit systems are described through tensor products.

This chapter is a compact refresher of the main linear-algebra ideas used throughout the repository.

---

## 1. Complex vectors and inner products

A pure quantum state is represented by a complex column vector.

For example, a qubit lives in:

$$
\mathbb{C}^2
$$

with standard basis states

$$
|0\rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix},
\qquad
|1\rangle = \begin{pmatrix} 0 \\ 1 \end{pmatrix}
$$

Given two complex vectors $|\psi\rangle$ and $|\phi\rangle$, their inner product is

$$
\langle \psi | \phi \rangle
$$

where $\langle \psi|$ is the conjugate transpose of $|\psi\rangle$.

The inner product tells us about overlap between states and is central to normalization, orthogonality, and measurement probabilities.

---

## 2. Norm and normalization

A valid pure state must have norm $1$.

If $|\psi\rangle$ is a state vector, its norm is determined by

$$
\langle \psi | \psi \rangle
$$

and normalization means:

$$
\langle \psi | \psi \rangle = 1
$$

For a qubit written as

$$
|\psi\rangle = \alpha |0\rangle + \beta |1\rangle
$$

the normalization condition becomes

$$
|\alpha|^2 + |\beta|^2 = 1
$$

Normalization matters because measurement probabilities must sum to $1$.

---

## 3. Unitary matrices

Quantum gates are represented by **unitary** matrices.

A matrix $U$ is unitary if

$$
U^\dagger U = I
$$

This means the transformation preserves norms and therefore preserves total probability.

Examples of unitary quantum gates include:

- the identity gate
- Pauli gates
- the Hadamard gate

Unitary evolution is the mathematical form of ideal closed-system quantum dynamics.

---

## 4. Tensor products

When we combine quantum systems, we do not add vector spaces in the ordinary sense.

We use the **tensor product**.

Two qubits live in

$$
\mathbb{C}^2 \otimes \mathbb{C}^2
$$

which is isomorphic to

$$
\mathbb{C}^4
$$

For example,

$$
|0\rangle \otimes |1\rangle = |01\rangle
$$

Tensor products are what make multi-qubit systems possible.

They are also where entanglement enters the picture.

---

## 5. Projectors

Given a normalized state $|\psi\rangle$, the matrix

$$
|\psi\rangle \langle \psi|
$$

is called a **projector** onto that state.

Projectors are useful because they connect state vectors to density matrices and also appear naturally in measurement theory.

For example,

$$
|0\rangle\langle 0| =
\begin{pmatrix}
1 & 0 \\
0 & 0
\end{pmatrix}
$$

---

## In code

Relevant functions in this repository:

- `dagger`
- `is_unitary`
- `projector`
- `trace`
- `kron`

These live in:

- `src/quantum_ed/linalg.py`

---

## Exercises

### Exercise 1
Verify that $|0\rangle$ and $|1\rangle$ are normalized.

### Exercise 2
Check that the Hadamard matrix is unitary.

### Exercise 3
Compute the tensor product $|0\rangle \otimes |1\rangle$ explicitly as a column vector.

### Exercise 4
Write the projector $|1\rangle\langle 1|$ as a matrix.

---

## Next

- `docs/02-qubits-and-states/README.md`
- Notebook: `../../notebooks/01-qubit-bloch.ipynb`
