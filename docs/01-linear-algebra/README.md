# Linear Algebra Essentials

Quantum computing is applied linear algebra over complex vector spaces. Every concept in quantum information—from single-qubit states and quantum gates to measurement collapse and multi-qubit entanglement—has a direct, exact mathematical counterpart in linear algebra.

This chapter provides a comprehensive, rigorous refresher of the linear algebra tools you will use throughout this repository.

---

## 1. Complex Vector Spaces and Dirac Notation

In quantum mechanics, physical states are represented by vectors in a complex Hilbert space $\mathcal{H}$. For a single qubit, this space is $\mathbb{C}^2$.

### Kets (State Vectors)
In Dirac notation, a column vector is denoted by a **ket** $|v\rangle$:

$$
|v\rangle = \begin{pmatrix} v_0 \\ v_1 \end{pmatrix} \in \mathbb{C}^2
$$

The standard computational basis vectors are defined as:

$$
|0\rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix},
\qquad
|1\rangle = \begin{pmatrix} 0 \\ 1 \end{pmatrix}
$$

Any general state vector $|\psi\rangle \in \mathbb{C}^2$ can be expressed as a linear combination (superposition) of these basis states:

$$
|\psi\rangle = \alpha |0\rangle + \beta |1\rangle = \begin{pmatrix} \alpha \\ \beta \end{pmatrix},
\quad \alpha, \beta \in \mathbb{C}
$$

### Bras (Dual Vectors)
To every ket $|v\rangle$, there corresponds a **bra** $\langle v|$, which is the conjugate transpose (Hermitian adjoint, denoted by $\dagger$) of $|v\rangle$:

$$
\langle v| = (|v\rangle)^\dagger = \begin{pmatrix} v_0^* & v_1^* \end{pmatrix}
$$

where $*$ denotes complex conjugation ($z = x + iy \implies z^* = x - iy$).

### Inner Product
The inner product between two vectors $|\phi\rangle = \begin{pmatrix} \phi_0 \\ \phi_1 \end{pmatrix}$ and $|\psi\rangle = \begin{pmatrix} \psi_0 \\ \psi_1 \end{pmatrix}$ is written as the bracket $\langle \phi | \psi \rangle$:

$$
\langle \phi | \psi \rangle = \begin{pmatrix} \phi_0^* & \phi_1^* \end{pmatrix} \begin{pmatrix} \psi_0 \\ \psi_1 \end{pmatrix} = \phi_0^* \psi_0 + \phi_1^* \psi_1 \in \mathbb{C}
$$

Key properties of the inner product in a complex Hilbert space:
1. **Conjugate symmetry:** $\langle \phi | \psi \rangle = (\langle \psi | \phi \rangle)^*$.
2. **Linearity in the second argument:** $\langle \phi | c_1 \psi_1 + c_2 \psi_2 \rangle = c_1 \langle \phi | \psi_1 \rangle + c_2 \langle \phi | \psi_2 \rangle$.
3. **Antilinearity in the first argument:** $\langle c_1 \phi_1 + c_2 \phi_2 | \psi \rangle = c_1^* \langle \phi_1 | \psi \rangle + c_2^* \langle \phi_2 | \psi \rangle$.
4. **Positive definiteness:** $\langle \psi | \psi \rangle \ge 0$, and $\langle \psi | \psi \rangle = 0 \iff |\psi\rangle = 0$.

#### Concrete Calculation: Overlap Between States
Consider the states $|\psi\rangle = \frac{1}{\sqrt{2}}|0\rangle + \frac{i}{\sqrt{2}}|1\rangle$ and $|+\rangle = \frac{1}{\sqrt{2}}|0\rangle + \frac{1}{\sqrt{2}}|1\rangle$:

$$
\langle + | \psi \rangle = \begin{pmatrix} \frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}} \end{pmatrix} \begin{pmatrix} \frac{1}{\sqrt{2}} \\ \frac{i}{\sqrt{2}} \end{pmatrix} = \left(\frac{1}{\sqrt{2}}\right)\left(\frac{1}{\sqrt{2}}\right) + \left(\frac{1}{\sqrt{2}}\right)\left(\frac{i}{\sqrt{2}}\right) = \frac{1 + i}{2}
$$

The transition probability between these states is the modulus squared:

$$
|\langle + | \psi \rangle|^2 = \left|\frac{1+i}{2}\right|^2 = \frac{1^2 + 1^2}{4} = \frac{2}{4} = \frac{1}{2}
$$

---

## 2. Norm, Normalization, and Orthogonality

### The Euclidean Norm
The length or norm of a state vector $|\psi\rangle$ is induced by the inner product:

$$
\||\psi\rangle\| = \sqrt{\langle \psi | \psi \rangle} = \sqrt{\sum_i |\psi_i|^2}
$$

### The Normalization Condition
In quantum mechanics, the norm of a state vector must equal $1$:

$$
\langle \psi | \psi \rangle = 1
$$

For a single qubit $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$, this requires:

$$
|\alpha|^2 + |\beta|^2 = 1
$$

This constraint ensures that the total probability of all mutually exclusive measurement outcomes sums to 1 (Born rule).

If a vector $|v\rangle$ is not normalized, it can be normalized by dividing by its norm:

$$
|v_{\text{norm}}\rangle = \frac{|v\rangle}{\||v\rangle\|} = \frac{|v\rangle}{\sqrt{\langle v | v \rangle}}
$$

### Orthogonality
Two vectors $|\phi\rangle$ and $|\psi\rangle$ are **orthogonal** if their inner product is zero:

$$
\langle \phi | \psi \rangle = 0
$$

A set of vectors $\{|e_i\rangle\}$ is **orthonormal** if every vector has unit norm and distinct vectors are orthogonal:

$$
\langle e_i | e_j \rangle = \delta_{ij} = \begin{cases} 1 & \text{if } i = j \\ 0 & \text{if } i \ne j \end{cases}
$$

The standard basis $\{|0\rangle, |1\rangle\}$ is orthonormal:

$$
\langle 0 | 0 \rangle = 1, \quad \langle 1 | 1 \rangle = 1, \quad \langle 0 | 1 \rangle = 0, \quad \langle 1 | 0 \rangle = 0
$$

---

## 3. Outer Products and Spectral Decomposition

While the inner product $\langle \phi | \psi \rangle$ contracts two vectors into a scalar, the **outer product** $|\psi\rangle \langle \phi|$ expands them into a matrix (linear operator).

Given $|\psi\rangle = \begin{pmatrix} \alpha \\ \beta \end{pmatrix}$ and $|\phi\rangle = \begin{pmatrix} \gamma \\ \delta \end{pmatrix}$:

$$
|\psi\rangle \langle \phi| = \begin{pmatrix} \alpha \\ \beta \end{pmatrix} \begin{pmatrix} \gamma^* & \delta^* \end{pmatrix} = \begin{pmatrix} \alpha \gamma^* & \alpha \delta^* \\ \beta \gamma^* & \beta \delta^* \end{pmatrix}
$$

### Completeness Relation (Resolution of Identity)
For any orthonormal basis $\{|e_i\rangle\}_{i=0}^{d-1}$ of a $d$-dimensional Hilbert space:

$$
\sum_{i=0}^{d-1} |e_i\rangle \langle e_i| = I
$$

For a single qubit in the computational basis:

$$
|0\rangle\langle 0| + |1\rangle\langle 1| = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix} + \begin{pmatrix} 0 & 0 \\ 0 & 1 \end{pmatrix} = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} = I
$$

### Spectral Decomposition
Any normal operator $A$ (satisfying $A^\dagger A = A A^\dagger$, which includes all Hermitian and unitary operators) has a set of orthonormal eigenvectors $\{|v_i\rangle\}$ with eigenvalues $\lambda_i$. It can be decomposed as:

$$
A = \sum_i \lambda_i |v_i\rangle \langle v_i|
$$

---

## 4. Matrices, Adjoints, and Special Operator Classes

An operator $A$ acting on $\mathbb{C}^2$ is represented by a $2 \times 2$ complex matrix:

$$
A = \begin{pmatrix} A_{00} & A_{01} \\ A_{20} & A_{11} \end{pmatrix},
\qquad A_{ij} = \langle i | A | j \rangle
$$

### Hermitian Adjoint (Dagger)
The conjugate transpose $A^\dagger$ is obtained by transposing the matrix and complex-conjugating every entry:

$$
(A^\dagger)_{ij} = (A_{ji})^*
$$

Key algebraic properties:
- $(AB)^\dagger = B^\dagger A^\dagger$ (order reverses!)
- $(cA)^\dagger = c^* A^\dagger$
- $(A^\dagger)^\dagger = A$
- $(A \otimes B)^\dagger = A^\dagger \otimes B^\dagger$

### Hermitian Operators (Observables)
A matrix $H$ is **Hermitian** (or self-adjoint) if:

$$
H^\dagger = H
$$

Fundamental properties:
- All eigenvalues of a Hermitian matrix are real: $\lambda_i \in \mathbb{R}$.
- Eigenvectors corresponding to distinct eigenvalues are mutually orthogonal.
- **Physical significance:** All measurable physical quantities (observables) in quantum mechanics are represented by Hermitian operators.

### Unitary Operators (Quantum Gates)
A square matrix $U$ is **unitary** if its adjoint equals its inverse:

$$
U^\dagger U = U U^\dagger = I
$$

Fundamental properties:
- **Norm preservation:** For any vector $|\psi\rangle$, $\||U\psi\rangle\| = \||\psi\rangle\|$.
- **Inner product preservation:** $\langle U\phi | U\psi \rangle = \langle \phi | U^\dagger U | \psi \rangle = \langle \phi | \psi \rangle$.
- **Modulus of eigenvalues:** All eigenvalues of a unitary matrix lie on the complex unit circle: $\lambda = e^{i\theta}$ with $\theta \in \mathbb{R}$.
- **Physical significance:** Closed-system quantum evolution (including quantum logic gates) is strictly unitary, ensuring that total probability is conserved at all times.

### Trace of an Operator
The **trace** of a square matrix $A$ is the sum of its diagonal entries:

$$
\operatorname{Tr}(A) = \sum_i A_{ii}
$$

Important properties:
- **Linearity:** $\operatorname{Tr}(cA + B) = c\operatorname{Tr}(A) + \operatorname{Tr}(B)$.
- **Cyclic property:** $\operatorname{Tr}(ABC) = \operatorname{Tr}(BCA) = \operatorname{Tr}(CAB)$.
- **Basis independence:** The trace equals the sum of the eigenvalues $\sum_i \lambda_i$.
- **Inner product relation:** $\operatorname{Tr}(|\psi\rangle\langle\phi|) = \langle \phi | \psi \rangle$.

---

## 5. Tensor Products ($\otimes$)

To describe composite quantum systems (e.g., registers of multiple qubits), we use the **tensor product** (Kronecker product) of Hilbert spaces:

$$
\mathcal{H}_{AB} = \mathcal{H}_A \otimes \mathcal{H}_B
$$

If $\dim(\mathcal{H}_A) = m$ and $\dim(\mathcal{H}_B) = n$, then $\dim(\mathcal{H}_{AB}) = m \times n$.
For an $n$-qubit quantum computer:

$$
\dim\left((\mathbb{C}^2)^{\otimes n}\right) = 2^n
$$

This exponential growth ($2, 4, 8, 16, \dots, 2^n$) is the source of the immense state space available to quantum algorithms.

### Kronecker Product of Vectors
For two vectors $|\psi\rangle = \begin{pmatrix} \alpha_0 \\ \alpha_1 \end{pmatrix}$ and $|\phi\rangle = \begin{pmatrix} \beta_0 \\ \beta_1 \end{pmatrix}$:

$$
|\psi\rangle \otimes |\phi\rangle = \begin{pmatrix} \alpha_0 \begin{pmatrix} \beta_0 \\ \beta_1 \end{pmatrix} \\ \alpha_1 \begin{pmatrix} \beta_0 \\ \beta_1 \end{pmatrix} \end{pmatrix} = \begin{pmatrix} \alpha_0 \beta_0 \\ \alpha_0 \beta_1 \\ \alpha_1 \beta_0 \\ \alpha_1 \beta_1 \end{pmatrix}
$$

Often written in compact shorthand: $|\psi\rangle \otimes |\phi\rangle \equiv |\psi\rangle|\phi\rangle \equiv |\psi\phi\rangle$.

### Kronecker Product of Matrices
For $A = \begin{pmatrix} a_{00} & a_{01} \\ a_{10} & a_{11} \end{pmatrix}$ and $B$:

$$
A \otimes B = \begin{pmatrix} a_{00} B & a_{01} B \\ a_{10} B & a_{11} B \end{pmatrix}
$$

#### Example: $X \otimes Z$
Let $X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ and $Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$:

$$
X \otimes Z = \begin{pmatrix} 0 \cdot Z & 1 \cdot Z \\ 1 \cdot Z & 0 \cdot Z \end{pmatrix} = \begin{pmatrix} 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & -1 \\ 1 & 0 & 0 & 0 \\ 0 & -1 & 0 & 0 \end{pmatrix}
$$

### The Mixed-Product Property
A critical identity used constantly in quantum circuit analysis:

$$
(A \otimes B)(C \otimes D) = (AC) \otimes (BD)
$$

This means applying gate $A$ to qubit 0 and gate $B$ to qubit 1 on an initial state $|v\rangle \otimes |w\rangle$ is equivalent to:

$$
(A \otimes B)(|v\rangle \otimes |w\rangle) = (A|v\rangle) \otimes (B|w\rangle)
$$

---

## 6. Projectors

A linear operator $P$ is an **orthogonal projector** if and only if it is:
1. **Idempotent:** $P^2 = P$ (applying the projection a second time does not change the result).
2. **Hermitian:** $P^\dagger = P$.

### Rank-1 Projectors
For any normalized pure state $|\psi\rangle$, the outer product:

$$
P_\psi = |\psi\rangle \langle \psi|
$$

is a projector onto the 1D subspace spanned by $|\psi\rangle$.
Check idempotency:

$$
P_\psi^2 = (|\psi\rangle\langle\psi|)(|\psi\rangle\langle\psi|) = |\psi\rangle \underbrace{\langle\psi|\psi\rangle}_{=1} \langle\psi| = |\psi\rangle\langle\psi| = P_\psi
$$

Check Hermiticity:

$$
P_\psi^\dagger = (|\psi\rangle\langle\psi|)^\dagger = (\langle\psi|)^\dagger (|\psi\rangle)^\dagger = |\psi\rangle\langle\psi| = P_\psi
$$

The computational basis projectors are:

$$
P_0 = |0\rangle\langle 0| = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix},
\qquad
P_1 = |1\rangle\langle 1| = \begin{pmatrix} 0 & 0 \\ 0 & 1 \end{pmatrix}
$$

---

## 7. Python Implementation with `quantum_ed.linalg`

The repository implements these operations explicitly in `src/quantum_ed/linalg.py`.

```python
import numpy as np
from quantum_ed.linalg import dagger, is_unitary, projector, trace, kron

# 1. Complex vectors and adjoints
psi = np.array([[1/np.sqrt(2)], [1j/np.sqrt(2)]], dtype=complex)
psi_dagger = dagger(psi)
norm_sq = (psi_dagger @ psi)[0, 0]
print("Norm squared <psi|psi>:", np.real(norm_sq))  # 1.0

# 2. Check Unitarity of Hadamard gate
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
print("Is H unitary?", is_unitary(H))  # True

# 3. Outer product / Projector onto |0>
P0 = projector(np.array([[1], [0]], dtype=complex))
print("P0 = |0><0|:\n", P0)

# 4. Kronecker product of Pauli X and Z
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
XZ = kron(X, Z)
print("X (x) Z shape:", XZ.shape)  # (4, 4)
```

---

## 8. Exercises and Worked Solutions

### Exercise 1: Normalization Check
**Problem:** Determine if the state $|\psi\rangle = \frac{\sqrt{3}}{2}|0\rangle - \frac{i}{2}|1\rangle$ is normalized.
**Solution:**
Calculate the sum of modulus squared:

$$
\langle \psi | \psi \rangle = \left|\frac{\sqrt{3}}{2}\right|^2 + \left|-\frac{i}{2}\right|^2 = \frac{3}{4} + \frac{1}{4} = 1
$$

Yes, the state is normalized.

### Exercise 2: Overlap and Transition Probability
**Problem:** For $|\psi\rangle = \frac{\sqrt{3}}{2}|0\rangle - \frac{i}{2}|1\rangle$, find the overlap $\langle 1 | \psi \rangle$ and the probability of measuring outcome 1.
**Solution:**
The inner product is:

$$
\langle 1 | \psi \rangle = \begin{pmatrix} 0 & 1 \end{pmatrix} \begin{pmatrix} \frac{\sqrt{3}}{2} \\ -\frac{i}{2} \end{pmatrix} = -\frac{i}{2}
$$

The probability is:

$$
P(1) = |\langle 1 | \psi \rangle|^2 = \left|-\frac{i}{2}\right|^2 = \frac{1}{4} = 0.25
$$

### Exercise 3: Unitarity Verification
**Problem:** Show analytically that the Pauli-Y matrix $Y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}$ is unitary.
**Solution:**
First, compute the Hermitian adjoint $Y^\dagger$:

$$
Y^\dagger = \begin{pmatrix} 0^* & i^* \\ (-i)^* & 0^* \end{pmatrix} = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix} = Y
$$

(Notice that $Y$ is Hermitian). Now compute the product $Y^\dagger Y$:

$$
Y^\dagger Y = Y^2 = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix} \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix} = \begin{pmatrix} (-i)(i) & 0 \\ 0 & (i)(-i) \end{pmatrix} = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} = I
$$

Since $Y^\dagger Y = I$, $Y$ is unitary.

---

## 9. Next Steps

Now that you have mastered the linear-algebra foundation:
- [Chapter 2: Qubits & States](../02-qubits-and-states/README.md)
- Accompanying notebook: [`notebooks/01-qubit-bloch.ipynb`](https://github.com/cicixgliamici/quantum_ed/blob/main/notebooks/01-qubit-bloch.ipynb)
