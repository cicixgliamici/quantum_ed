# Fidelity (intro)

To compare quantum states, one common metric is **fidelity**.

For a pure reference state \(|\psi\rangle\) and a (possibly mixed) state \(\rho\):
\[
F(|\psi\rangle, \rho) = \langle \psi|\rho|\psi\rangle
\]

If \(\rho = |\phi\rangle\langle\phi|\) is also pure, then:
\[
F = |\langle \psi | \phi \rangle|^2
\]

In practice:
- Fidelity close to 1 means “very similar”
- Noise typically decreases fidelity
