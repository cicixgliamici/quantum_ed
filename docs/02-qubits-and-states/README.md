# Qubits & States

A single qubit lives in a 2D complex Hilbert space.

## State vector
A pure state is a unit vector:

\[
|\psi\rangle = \alpha |0\rangle + \beta |1\rangle, \quad \alpha,\beta \in \mathbb{C}, \quad |\alpha|^2 + |\beta|^2 = 1
\]

Global phase does not matter: \( e^{i\phi}|\psi\rangle \) is physically indistinguishable from \(|\psi\rangle\).

## Bloch sphere
Any pure qubit can be written (up to global phase) as:

\[
|\psi\rangle = \cos(\tfrac{\theta}{2})|0\rangle + e^{i\varphi}\sin(\tfrac{\theta}{2})|1\rangle
\]

and mapped to a point on the Bloch sphere:
\[
\vec{r} = (\sin\theta\cos\varphi,\ \sin\theta\sin\varphi,\ \cos\theta)
\]

## Notebook
- `../../notebooks/01-qubit-bloch.ipynb`
