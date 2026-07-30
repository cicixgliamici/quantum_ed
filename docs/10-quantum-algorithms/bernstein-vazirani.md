# Bernstein-Vazirani algorithm

## Problem

An unknown string $s\in\{0,1\}^n$ is encoded in the function

$$
f_s(x)=s\cdot x \pmod 2,
$$

where

$$
s\cdot x = s_0x_0\oplus s_1x_1\oplus\cdots\oplus s_{n-1}x_{n-1}.
$$

The task is to recover the complete string $s$ by querying an oracle for
$f_s$.

## Classical and quantum query cost

A classical algorithm can query the $n$ unit vectors to learn one secret bit
per query, requiring $n$ queries in the standard deterministic strategy.

Bernstein-Vazirani recovers all $n$ bits with one quantum oracle query in the
ideal query model.

## Circuit and derivation

The circuit starts exactly like Deutsch-Jozsa:

$$
|0\rangle^{\otimes n}|1\rangle
\xrightarrow{H^{\otimes(n+1)}}
\frac{1}{\sqrt{2^n}}\sum_x|x\rangle|-\rangle.
$$

The oracle writes the hidden linear function into the phase:

$$
\frac{1}{\sqrt{2^n}}\sum_x(-1)^{s\cdot x}|x\rangle|-\rangle.
$$

The Hadamard transform satisfies

$$
H^{\otimes n}|x\rangle =
\frac{1}{\sqrt{2^n}}\sum_y(-1)^{x\cdot y}|y\rangle.
$$

After the final Hadamards, the input register is therefore exactly

$$
|s\rangle.
$$

One measurement reveals the hidden string.

## Repository example

All three implementations use three input qubits and the secret `101`, in
qubit-index order:

$$
s_0=1,\qquad s_1=0,\qquad s_2=1.
$$

The oracle applies controlled-X gates from input qubits 0 and 2 to the output
qubit. A measurement returns `101` with ideal probability 1.

- [Qiskit](../../src/showcase/qiskit/bernstein_vazirani.py)
- [Q#](../../src/showcase/qsharp/BernsteinVazirani.qs)
- [OpenQASM 3](../../src/showcase/openqasm/bernstein_vazirani.qasm)

## Relationship to Deutsch-Jozsa

The quantum circuit pattern is the same, but the promise and interpretation
are different. Every nonzero Bernstein-Vazirani function is balanced, while
the final bit string contains more information than the single
constant-versus-balanced decision.

On noisy hardware, repeated shots and transpilation are needed to estimate the
most likely output. The one-query statement refers to the logical oracle in
the ideal query-complexity model.
