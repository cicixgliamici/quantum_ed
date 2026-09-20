# Quantum Fourier transform

For $N=2^n$, the quantum Fourier transform maps a basis state $|x\rangle$ to

$$
\operatorname{QFT}|x\rangle = \frac{1}{\sqrt{N}}
\sum_{k=0}^{N-1} e^{2\pi i xk/N}|k\rangle.
$$

Every output amplitude has the same magnitude. The input is encoded in relative
phases, which explains why direct computational-basis measurement is uniform.
QFT becomes useful when a later interference step converts those phases into
measurable structure, as in phase estimation and Shor's algorithm.

The gate decomposition uses Hadamards, controlled phase rotations, and final
swaps that correct reversed wire order.

See the [five-ecosystem experiment](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/quantum-fourier-transform).
