# Density Matrices

State vectors are enough for **closed, pure-state** quantum systems.

But in realistic quantum computing we also need a more general formalism, because:

- we may have **statistical mixtures**
- we may only observe a **subsystem**
- noise and decoherence are more naturally expressed on density matrices

---

## 1. From pure states to density matrices

If a system is in a pure state `|psi>`, its density matrix is

\[
\rho = |\psi\rangle \langle \psi|
\]

This object contains the same physical information as the ket, but in matrix form.

Example:

\[
|0\rangle =
\begin{pmatrix}
1 \\
0
\end{pmatrix}
\quad \Rightarrow \quad
\rho_0 =
|0\rangle\langle 0|
=
\begin{pmatrix}
1 & 0 \\
0 & 0
\end{pmatrix}
\]

Likewise, for

\[
|+\rangle = \frac{1}{\sqrt{2}} \left(|0\rangle + |1\rangle\right)
\]

we get

\[
\rho_+ =
\frac{1}{2}
\begin{pmatrix}
1 & 1 \\
1 & 1
\end{pmatrix}
\]

---

## 2. Mixed states

A mixed state is not a single ket, but a probabilistic ensemble:

\[
\rho = \sum_i p_i |\psi_i\rangle \langle \psi_i|
\]

with:

- \( p_i \ge 0 \)
- \( \sum_i p_i = 1 \)

Example: a classical 50/50 mixture of `|0>` and `|1>` gives

\[
\rho =
\frac{1}{2}|0\rangle\langle 0| +
\frac{1}{2}|1\rangle\langle 1|
=
\frac{1}{2}
\begin{pmatrix}
1 & 0 \\
0 & 1
\end{pmatrix}
\]

This is **not** the same as the pure superposition `|+>`.

That distinction is one of the main reasons density matrices matter.

---

## 3. Properties of a density matrix

A valid density matrix must satisfy:

1. **Hermitian**
   \[
   \rho^\dagger = \rho
   \]

2. **Positive semidefinite**
   all eigenvalues are non-negative

3. **Trace one**
   \[
   \mathrm{Tr}(\rho) = 1
   \]

These are the core mathematical checks for physical validity.

---

## 4. Why off-diagonal terms matter

For a qubit density matrix

\[
\rho =
\begin{pmatrix}
\rho_{00} & \rho_{01} \\
\rho_{10} & \rho_{11}
\end{pmatrix}
\]

- the diagonal terms describe basis populations
- the off-diagonal terms encode **coherence**

Noise processes such as **dephasing** reduce off-diagonal terms while preserving populations.

This is why dephasing is often described as “loss of phase information”.

---

## 5. Reduced states and partial trace

Suppose two qubits are entangled in a Bell state:

\[
|\Phi^+\rangle =
\frac{1}{\sqrt{2}} (|00\rangle + |11\rangle)
\]

The full system is pure:

\[
\rho_{AB} = |\Phi^+\rangle \langle \Phi^+|
\]

But if we look only at qubit A, we compute the **partial trace** over B:

\[
\rho_A = \mathrm{Tr}_B(\rho_{AB})
\]

and obtain

\[
\rho_A = \frac{I}{2}
\]

So the subsystem is maximally mixed, even though the global state is pure.

This is one of the most important conceptual points in quantum information.

---

## 6. Density matrices and noise

Noise channels are often written as maps

\[
\rho \mapsto \mathcal{E}(\rho)
\]

In this repository, we currently implement simple one-qubit channels such as:

- depolarizing noise
- dephasing noise

These are easier to define and reason about using density matrices than using only state vectors.

---

## 7. In this repository

Relevant functions:

- `rho_from_ket`
- `fidelity_pure`
- `partial_trace_two_qubits`
- `depolarize_rho`
- `dephase_rho`

Suggested reading order:

1. `docs/02-qubits-and-states/README.md`
2. `docs/04-entanglement/README.md`
3. this chapter
4. `docs/06-noise-and-channels/README.md`

---

## 8. Exercises

### Exercise 1
Compute the density matrix of:

\[
|+\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}
\]

and identify diagonal and off-diagonal terms.

### Exercise 2
Show explicitly that the 50/50 classical mixture of `|0>` and `|1>` is different from the pure state `|+>`.

### Exercise 3
Take a Bell state, form `rho_AB`, then compute the reduced state of one qubit. What do you observe?

### Exercise 4
Apply dephasing to `|+><+|` and describe what changes as the parameter `p` grows from `0` to `1`.

---

## 9. Key intuition

A ket describes a pure state of a whole system.

A density matrix lets us describe:

- pure states
- mixed states
- subsystems
- noisy evolution

That is why density matrices are not an optional technicality: they are the natural language of realistic quantum information.
