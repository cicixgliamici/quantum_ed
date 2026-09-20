# Fidelity and Trace Distance

To compare quantum states, one common metric is fidelity.

For a pure reference state $|\psi\rangle$ and a possibly mixed state $\rho$:

$$
F(|\psi\rangle, \rho) = \langle \psi | \rho | \psi \rangle
$$

If $\rho = |\phi\rangle\langle\phi|$ is also pure, then:

$$
F = |\langle \psi | \phi \rangle|^2
$$

In practice:

- fidelity close to 1 means the states are very close
- noise typically decreases fidelity with respect to a target state

Another useful metric is trace distance:

$$
D(\rho, \sigma) = \frac{1}{2}\|\rho - \sigma\|_1
$$

For Hermitian matrices, this can be computed from the eigenvalues of $\rho - \sigma$.

In practice:

- trace distance 0 means the states are identical
- larger trace distance means the states are more distinguishable

In this repository:

- `fidelity_pure` answers "how close is this noisy state to my target pure state?"
- `trace_distance` answers "how far apart are these two density matrices?"
