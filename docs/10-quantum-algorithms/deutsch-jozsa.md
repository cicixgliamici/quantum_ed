# Deutsch-Jozsa algorithm

## Problem

Given a black-box function

$$
f:\{0,1\}^n\rightarrow\{0,1\},
$$

we are promised that exactly one of these cases holds:

- **constant:** $f(x)$ has the same value for every input;
- **balanced:** $f(x)=0$ for half of the inputs and $f(x)=1$ for the other half.

The task is to determine which case applies.

The promise matters. A general Boolean function may be neither constant nor
balanced, and the algorithm makes no guarantee for such an oracle.

## Classical and quantum query cost

A deterministic classical algorithm may need $2^{n-1}+1$ oracle queries in the
worst case. After seeing the same result $2^{n-1}$ times, one more input must be
checked to rule out a balanced function.

Deutsch-Jozsa needs one quantum oracle query in the ideal query model. This is
an exponential separation from deterministic exact classical computation, not
a claim that the algorithm solves a broadly useful real-world task.

## Circuit

Start with $n$ input qubits and one output qubit:

$$
|0\rangle^{\otimes n}|1\rangle.
$$

Apply a Hadamard gate to every qubit:

$$
\frac{1}{\sqrt{2^n}}\sum_{x\in\{0,1\}^n}|x\rangle|-\rangle.
$$

After one oracle query, phase kickback gives

$$
\frac{1}{\sqrt{2^n}}
\sum_x(-1)^{f(x)}|x\rangle|-\rangle.
$$

Apply $H^{\otimes n}$ to the input register. The amplitude of
$|0\rangle^{\otimes n}$ becomes

$$
\frac{1}{2^n}\sum_x(-1)^{f(x)}.
$$

- For a constant function, all terms have the same sign, so measuring the
  input register returns `000...0`.
- For a balanced function, the positive and negative terms cancel, so the
  all-zero outcome has zero probability.

Therefore, all zeros means constant; any `1` means balanced.

## Repository example

The showcase uses $n=3$ and the balanced function

$$
f(x_0,x_1,x_2)=x_0.
$$

Its oracle is a single controlled-X from input $x_0$ to the output qubit.
The ideal per-qubit results are $x_0=1$, $x_1=0$, and $x_2=0$. Q# therefore
returns `[One, Zero, Zero]`, while Qiskit's conventional highest-index-first
display prints `001`. Each implementation documents its convention:

- [Qiskit](../../src/showcase/qiskit/deutsch_jozsa.py)
- [Q#](../../src/showcase/qsharp/DeutschJozsa.qs)
- [OpenQASM 3](../../src/showcase/openqasm/deutsch_jozsa.qasm)

## What the example teaches

The algorithm does not read every value of $f(x)$. It extracts one global
property of the function by arranging destructive and constructive
interference. This distinction is essential: superposition alone does not
provide access to every function value after measurement.
