# Entanglement

When we combine two qubits, the joint system lives in

$$
\mathbb{C}^2 \otimes \mathbb{C}^2
$$

which is a 4-dimensional complex vector space.

This is where one of the most distinctive features of quantum theory appears: **entanglement**.

---

## 1. Product states

A two-qubit state is called a **product state** or **separable state** if it can be written as

$$
|\psi\rangle \otimes |\phi\rangle
$$

for some one-qubit states $|\psi\rangle$ and $|\phi\rangle$.

Example:

$$
|0\rangle \otimes |1\rangle = |01\rangle
$$

This is a separable state.

The two qubits are described independently.

---

## 2. Entangled states

A state is **entangled** if it cannot be written as a product state.

That means the global system is well defined, but the two subsystems cannot be treated as fully independent pure states.

This is not just a mathematical curiosity.

Entanglement is central to:

- Bell inequalities
- teleportation
- superdense coding
- quantum advantage more broadly

---

## 3. Bell state example

A classic example is the Bell state

$$
|\Phi^+\rangle = \frac{1}{\sqrt{2}}\left(|00\rangle + |11\rangle\right)
$$

This state cannot be written as

$$
|\psi\rangle \otimes |\phi\rangle
$$

so it is not separable.

It is one of the simplest and most important examples of entanglement.

---

## 4. Why entanglement matters

The key idea is that the global state may be pure even when the parts do not admit an independent pure-state description.

This becomes clearer when we move from state vectors to density matrices.

For an entangled two-qubit state:

- the full system can be pure
- a single qubit, viewed alone, can appear mixed

This is why entanglement naturally leads to:

- reduced density matrices
- partial trace
- subsystem-based reasoning

---

## 5. From Bell states to reduced states

If we form the density matrix

$$
\rho_{AB} = |\Phi^+\rangle \langle \Phi^+|
$$

and then trace out one qubit, the remaining qubit is described by a reduced density matrix.

For Bell states, that reduced state is maximally mixed.

This is one of the most important conceptual bridges in quantum information.

---

## In code

Relevant functions and objects in this repository:

- `kron_n`
- `CNOT`
- `rho_from_ket`
- `partial_trace_two_qubits`

Main files:

- `src/quantum_ed/gates.py`
- `src/quantum_ed/density.py`

---

## Exercises

### Exercise 1

Explain why

$$
|00\rangle
$$

is separable.

### Exercise 2

Write the Bell state

$$
|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)
$$

and explain why it is not a simple tensor product.

### Exercise 3

Why does entanglement force us to think about subsystems differently from classical product descriptions?

---

## Notebook

- `../../notebooks/02-bell-entanglement.ipynb`

## Next

- `docs/07-density-matrices/README.md`
- `docs/06-noise-and-channels/README.md`
