# Introduction

Welcome to **Quantum-Ed**, an educational platform designed to build a deep, rigorous, and practical understanding of quantum computing and quantum information.

---

## 1. Philosophy: Math First, Code Driven

Many quantum computing tutorials fall into one of two extremes:
1. **Purely abstract mathematics**, detached from executable algorithms and circuits.
2. **Framework-specific API tutorials**, which treat quantum gates as black boxes and obscure the underlying linear algebra and physical principles.

**Quantum-Ed** bridges this gap:
- **Math-first:** We derive every concept from basic linear algebra in complex Hilbert spaces ($\mathbb{C}^2$, $\mathbb{C}^4$, $\mathbb{C}^{2^n}$).
- **Transparent NumPy core:** In `src/quantum_ed/`, all states, gates, density matrices, and noise channels are implemented with explicit NumPy array operations. Nothing is hidden behind complex abstractions.
- **Multi-ecosystem cross-validation:** Algorithms and protocols are implemented and compared across five leading industry ecosystems: **NumPy**, **Qiskit**, **Q#**, **OpenQASM 3**, and **PennyLane**.

---

## 2. Curriculum Architecture

The repository is structured into progressive conceptual layers:

```
00-intro/            --> Course roadmap and fundamental conventions
01-linear-algebra/   --> Complex vector spaces, inner products, unitaries, tensor products
02-qubits-and-states/--> Pure states, global vs relative phase, Bloch sphere geometry
03-measurement/      --> Born rule, projectors, collapse, expectation values, observables
04-entanglement/     --> Separability, Bell states, partial trace, quantum correlations
05-circuits-and-gates/-> Unitary operations, gate decomposition, universality, circuit compilation
06-density-matrices/ --> Mixed states, ensembles, purity, Bloch ball
07-noise-and-channels/-> Open quantum systems, Kraus operators, decoherence models
08-hardware/         --> Physical modalities (superconducting, trapped ions, photonics), noise budgets
09-useful-matrices/  --> Reference catalog of standard matrices, gates, and projectors
10-quantum-algorithms/-> Deutsch-Jozsa, Bernstein-Vazirani, Grover, QFT, QPE, VQE
```

---

## 3. Core Mathematical Conventions

To avoid ambiguity across literature and software frameworks, this repository establishes the following conventions:

### Vectors and Operators
- A pure state vector is written in Dirac bra-ket notation as a column vector ket:

$$
|\psi\rangle = \begin{pmatrix} \alpha \\ \beta \end{pmatrix} \in \mathbb{C}^2
$$

- The bra $\langle \psi|$ is the conjugate transpose (Hermitian adjoint):

$$
\langle \psi| = |\psi\rangle^\dagger = \begin{pmatrix} \alpha^* & \beta^* \end{pmatrix}
$$

- The inner product is $\langle \phi | \psi \rangle = \sum_i \phi_i^* \psi_i \in \mathbb{C}$.
- The outer product is $|\psi\rangle\langle \phi|$, producing a rank-1 linear operator (matrix).

### Basis and Index Ordering
- The standard computational basis for a single qubit is:

$$
|0\rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix},
\qquad
|1\rangle = \begin{pmatrix} 0 \\ 1 \end{pmatrix}
$$

- For multi-qubit systems, the tensor product follows **big-endian (lexicographic) qubit ordering**:
  
$$
|01\rangle = |0\rangle \otimes |1\rangle = \begin{pmatrix} 0 \\ 1 \\ 0 \\ 0 \end{pmatrix}
$$
  
  where qubit 0 is the most significant (leftmost) and qubit 1 is the least significant (rightmost).

---

## 4. Quickstart with `quantum_ed`

The accompanying Python package `quantum_ed` provides lightweight, inspectable primitives:

```python
import numpy as np
from quantum_ed import ket0, H, apply, probs_comp_basis, bloch_vector

# 1. Start with ground state |0>
psi_0 = ket0()
print("Initial state |0>:\n", psi_0)

# 2. Apply Hadamard gate H to create superposition |+>
psi_plus = apply(H, psi_0)
print("\nSuperposition state |+>:\n", psi_plus)

# 3. Compute measurement probabilities in computational basis
p0, p1 = probs_comp_basis(psi_plus)
print(f"\nProbabilities: P(0) = {p0:.2f}, P(1) = {p1:.2f}")

# 4. Compute Bloch sphere vector (x, y, z)
rx, ry, rz = bloch_vector(psi_plus)
print(f"Bloch vector: ({rx:.1f}, {ry:.1f}, {rz:.1f})")  # (1.0, 0.0, 0.0)
```

---

## 5. Next Steps

Begin your journey with the fundamental linear algebra toolkit:

- [Chapter 1: Linear Algebra Essentials](../01-linear-algebra/README.md)
- Accompanying notebook: [`notebooks/01-qubit-bloch.ipynb`](https://github.com/cicixgliamici/quantum_ed/blob/main/notebooks/01-qubit-bloch.ipynb)
