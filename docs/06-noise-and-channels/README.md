# Noise & Quantum Channels

Real quantum devices are noisy.

The ideal picture of perfectly unitary evolution is extremely useful, but real hardware is affected by decoherence, imperfect control, and imperfect measurement.

To model this, we use **quantum channels**.

---

## 1. Why noise matters

In a perfectly isolated system, evolution is described by unitary matrices.

In real devices, however, the system interacts with its environment.

This can cause:

- loss of coherence
- energy relaxation
- drift away from the intended target state

That is why noise is not a side topic.

It is part of the core language of realistic quantum computing.

---

## 2. Density-matrix viewpoint

Noise is most naturally described using density matrices.

Instead of only working with pure states $|\psi\rangle$, we work with

$$
\rho
$$

A quantum channel acts as a map

$$
\rho \mapsto \mathcal{E}(\rho)
$$

This lets us describe:

- pure states
- mixed states
- subsystem states
- noisy evolution

---

## 3. Depolarizing noise

A simple model of depolarizing noise is

$$
\rho \mapsto (1-p)\rho + p \frac{I}{2}
$$

Here:

- $p = 0$ means no noise
- $p = 1$ means the state becomes maximally mixed

So depolarizing noise pushes the system toward

$$
\frac{I}{2}
$$

which represents complete one-qubit uncertainty.

---

## 4. Dephasing noise

Dephasing noise reduces phase coherence while preserving basis populations.

A simple one-qubit form is:

$$
\rho =
\begin{pmatrix}
\rho_{00} & \rho_{01} \\
\rho_{10} & \rho_{11}
\end{pmatrix}
\mapsto
\begin{pmatrix}
\rho_{00} & (1-p)\rho_{01} \\
(1-p)\rho_{10} & \rho_{11}
\end{pmatrix}
$$

So the diagonal terms remain unchanged, while the off-diagonal terms shrink.

This is why dephasing is often described as coherence loss.

---

## 5. Fidelity

To measure how much noise degrades a target state, we use **fidelity**.

For a pure target state $|\psi\rangle$ and a density matrix $\rho$, the fidelity is

$$
F = \langle \psi | \rho | \psi \rangle
$$

A value near $1$ means the noisy state is still close to the target state.

A value farther from $1$ means the state has drifted away more substantially.

---

## 6. Why this chapter matters

Noise and channels connect the abstract mathematical formalism to real implementation limits.

They also connect naturally to:

- density matrices
- hardware constraints
- realistic simulation

This is one of the key places where “ideal quantum computing” becomes “physical quantum computing”.

---

## In code

Relevant functions in this repository:

- `depolarize_rho`
- `dephase_rho`
- `fidelity_pure`

Main files:

- `src/quantum_ed/channels.py`
- `src/quantum_ed/density.py`

---

## Exercises

### Exercise 1

What happens to

$$
|0\rangle\langle 0|
$$

under full depolarizing noise with $p=1$?

### Exercise 2

What happens to the off-diagonal terms of

$$
|+\rangle\langle +|
$$

under full dephasing with $p=1$?

### Exercise 3

Why is the density-matrix formalism more natural than pure state vectors when describing noise?

---

## Extras

- Fidelity notes: `FIDELITY.md`
- Notebook: `../../notebooks/03-noise-fidelity.ipynb`

## Next

- `docs/07-density-matrices/README.md`
- `docs/08-hardware/README.md`
