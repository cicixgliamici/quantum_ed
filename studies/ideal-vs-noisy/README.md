# Ideal versus noisy simulation

This study prepares $|0\rangle$ and applies bit-flip noise:

$$
\mathcal{E}(\rho)=(1-p)\rho+pX\rho X.
$$

The ideal case $p=0$ always measures zero. Under noise, the probability of
measuring one is exactly $p$.

- [`numpy_model.py`](numpy_model.py) uses `quantum_ed` density matrices.
- [`pennylane_model.py`](pennylane_model.py) uses PennyLane `default.mixed` and
  `BitFlip`.

The study is framework-specific rather than a five-ecosystem experiment because
Q# and OpenQASM describe programs and circuits but do not standardize a shared
simulator noise model. Making that capability boundary explicit is part of the
comparison.
