# Noise & Quantum Channels

Real quantum devices are noisy.

To model noise, we use **quantum channels**, which transform a state into another state while accounting for imperfect physical evolution.

In this repository, we start with simple one-qubit channels written in terms of density matrices.

## Main examples

### Depolarizing noise

Depolarizing noise pushes the state toward the maximally mixed state:

$$
\rho \mapsto (1-p)\rho + p\frac{I}{2}
$$

As $p$ increases, the state loses information and becomes more random.

### Dephasing noise

Dephasing noise suppresses coherence while keeping basis populations unchanged.

A simple one-qubit description is:

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

This makes dephasing the natural model for loss of phase information.

## Fidelity

To quantify how much noise damages a target state, we use **fidelity**.

For a pure target state $|\psi\rangle$ and a density matrix $\rho$, the fidelity is:

$$
F = \langle \psi | \rho | \psi \rangle
$$

A value close to $1$ means the noisy state is still close to the target state.

## In this repository

Current functions include:

- `depolarize_rho`
- `dephase_rho`
- `fidelity_pure`

## Extras

- Fidelity notes: `FIDELITY.md`
- Notebook: `../../notebooks/03-noise-fidelity.ipynb`
