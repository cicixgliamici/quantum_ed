# Noise & Quantum Channels

Real devices are noisy. We model noise with **quantum channels**.

In the simplest “from scratch” setting we implement:

- Depolarizing noise (mix with maximally mixed state)
- Dephasing noise (kills off-diagonal terms)

For full generality one uses Kraus operators, Lindblad master equations, etc.
Here we start small and test everything.
