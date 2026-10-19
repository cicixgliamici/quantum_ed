# Quantum phase estimation

## Problem

Given a unitary operator $U$ and an eigenstate $|\psi\rangle$ such that

$$
U|\psi\rangle = e^{2\pi i \theta}|\psi\rangle,
$$

with unknown phase $\theta \in [0, 1)$, the goal of **quantum phase estimation (QPE)** is to estimate $\theta$ to $m$ bits of precision.

The eigenstate is assumed to be available and controlled powers of U must be
implementable. An early primary source for phase estimation is
[Kitaev (1995)](https://arxiv.org/abs/quant-ph/9511026). This page describes the
Fourier-register construction and makes its precision and bit order explicit.

## Why it matters

Phase estimation is one of the most fundamental subroutines in quantum algorithms:

- **Shor's factoring algorithm:** order finding reduces to phase estimation of a modular multiplication unitary $U|y\rangle = |ay \pmod N\rangle$.
- **Quantum chemistry & simulation:** estimating the eigenvalues (energy levels) of molecular and physical Hamiltonians via time evolution unitaries $U = e^{-iHt}$.
- **HHL algorithm:** solving linear systems of equations $A|x\rangle = |b\rangle$ by decomposing $|b\rangle$ into the eigenbasis of $A$ via phase estimation.

## Circuit and mathematical derivation

The circuit uses two registers:
1. An **$m$-qubit counting register** initialized to $|0\rangle^{\otimes m}$, which will store the binary estimate of $\theta$.
2. A **target register** initialized in the eigenstate $|\psi\rangle$.

### Step 1: Superposition
Apply Hadamard gates $H^{\otimes m}$ to the counting register:

$$
|\psi_1\rangle = \frac{1}{\sqrt{2^m}} \sum_{k=0}^{2^m-1} |k\rangle |\psi\rangle.
$$

### Step 2: Controlled-$U^{2^j}$ operations (Phase kickback)

Here wire j controls power $2^j$, so its numerical weight is $2^j$.
The integer label k in the equations means the bits `q[m-1]...q[0]`, not
the repository's usual tensor label `q[0]...q[m-1]`. The two descriptions
refer to the same physical wires and are related by bit reversal.
For each counting qubit $j \in \{0, 1, \dots, m-1\}$, apply a controlled unitary $C\text{-}U^{2^j}$ targeted at $|\psi\rangle$.
Since $U^{2^j}|\psi\rangle = e^{2\pi i 2^j \theta}|\psi\rangle$, phase kickback imparts the phase into the counting register:

$$
|\psi_2\rangle = \frac{1}{\sqrt{2^m}} \sum_{k=0}^{2^m-1} e^{2\pi i \theta k} |k\rangle |\psi\rangle.
$$

Let $M=2^m$. If $b=M\theta$ is an integer, the counting state equals the
Fourier transform of the valid basis label b:

$$
|\psi_{\text{counting}}\rangle = \operatorname{QFT}_M|b\rangle,
\qquad b=M\theta\in\{0,\ldots,M-1\}.
$$

For noninteger $M\theta$, there is no computational-basis ket with that
fractional label. The phase-weighted sum above remains the correct state.

### Step 3: Inverse Quantum Fourier Transform ($\text{QFT}^\dagger$)
For an exact integer label $b=M\theta$, the inverse transform recovers that
basis state:

$$
\operatorname{QFT}_M^\dagger |\psi_{\text{counting}}\rangle = |b\rangle,
\qquad b=M\theta\in\mathbb Z.
$$

Otherwise the output is a superposition with the amplitudes given below,
not a basis state labeled by a fractional number.

### Step 4: Measurement
Measuring gives an integer y and the numerical estimate $\widehat\theta=y/M$.
For a general eigenphase its probability is:

$$
P(y)=\left|\frac1M\sum_{k=0}^{M-1}
e^{2\pi i k(\theta-y/M)}\right|^2.
$$

- **Exact case:** If $\theta$ can be expressed exactly as an $m$-bit binary fraction:

$$
\theta = 0.\theta_1 \theta_2 \dots \theta_m = \sum_{j=1}^m \theta_j 2^{-j},
$$

    the measurement returns the exact integer $2^m \theta$ with probability $1$.
- **Approximate case:** A nearest grid point, with phase distance understood
  modulo one, has probability at least $4/\pi^2\approx0.405$. A single outcome
  is not guaranteed to be nearest. Extra precision qubits can reduce the
  probability of errors larger than a chosen phase tolerance; the precision
  and failure-probability targets must be specified separately.

The precision is not free. If controlled powers are implemented by repeatedly
calling controlled U, the total number of such calls is
$1+2+\cdots+2^{m-1}=2^m-1$. Special unitaries can admit cheaper power
implementations, but merely counting m wires does not establish computational
cost or quantum advantage. If the target is a superposition of eigenstates,
the outcomes are a mixture of the corresponding phase distributions.

## Repository example

The repository implements a 4-qubit instance:

- **Target register (1 qubit):** prepared in $|\psi\rangle = |1\rangle$ using an $X$ gate.
- **Unitary operator:** the single-qubit $T$ gate:

$$
T = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\pi/4} \end{pmatrix}.
$$

    Its action on $|1\rangle$ is $T|1\rangle = e^{i\pi/4}|1\rangle = e^{2\pi i (1/8)}|1\rangle$, so the phase is $\theta = 1/8 = 0.125$.
- **Counting register (3 qubits):** $m = 3$ qubits provide $2^3 = 8$ discrete bins.
  The exact binary representation is $\theta = 0.001_2$, so $2^3 \theta = 1$.
- **Controlled powers:**
  - $j=0$: Controlled-$T^{2^0} = C\text{-}T = C\text{-}P(\pi/4)$
  - $j=1$: Controlled-$T^{2^1} = C\text{-}S = C\text{-}P(\pi/2)$
  - $j=2$: Controlled-$T^{2^2} = C\text{-}Z = C\text{-}P(\pi)$

After the inverse transform, the **numerical phase label** is `001` (value 1)
deterministically. The increasing wire-order label is `100`: wire 0 is one.
NumPy's analytical result and Qiskit's default count display use `001`,
whereas PennyLane's wire-order probability array has its peak at index 4
and Q# returns `[One, Zero, Zero]`. See the
[bit-ordering reference](../reference/bit-ordering.md).

$$
\theta = \frac{1}{2^3} = \frac{1}{8} = 0.125.
$$

See the implementations across five ecosystems:
- [Experiment guide](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/quantum-phase-estimation)
- [NumPy](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/quantum-phase-estimation/numpy/quantum_phase_estimation.py)
- [Qiskit](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/quantum-phase-estimation/qiskit/quantum_phase_estimation.py)
- [Q#](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/quantum-phase-estimation/qsharp/QuantumPhaseEstimation.qs)
- [OpenQASM 3](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/quantum-phase-estimation/openqasm/quantum_phase_estimation.qasm)
- [PennyLane](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/quantum-phase-estimation/pennylane/quantum_phase_estimation.py)

## What the example teaches

Phase estimation shows how quantum interference translates an invisible physical parameter (the eigenphase acquired during time evolution or unitary action) into macroscopic, readable measurement statistics. This connects quantum dynamics directly to information extraction.
