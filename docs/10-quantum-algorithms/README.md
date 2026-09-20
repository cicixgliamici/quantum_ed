# Quantum algorithms

This chapter starts with two early quantum query algorithms:

1. [Deutsch-Jozsa](deutsch-jozsa.md) decides whether a promised Boolean
   function is constant or balanced.
2. [Bernstein-Vazirani](bernstein-vazirani.md) recovers a hidden bit string.

It then extends the path toward:

3. [Grover search](grover-search.md) and amplitude amplification.
4. The [quantum Fourier transform](quantum-fourier-transform.md).
5. [Quantum phase estimation](quantum-phase-estimation.md).
6. The hybrid [variational quantum eigensolver](variational-quantum-eigensolver.md).

They are useful teaching examples because both expose the same core ideas:

- an oracle represents information as a unitary operation;
- superposition evaluates phase information across all inputs;
- phase kickback moves the oracle output into relative phases;
- interference turns those phases into a measurable answer.

The implementations use the same small instances in
[`experiments`](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments),
making NumPy, Qiskit, Q#, OpenQASM 3, and PennyLane directly comparable.

See the dedicated
[language and implementation comparison](language-comparison.md) for a
concept-by-concept mapping of the three ecosystems.

## Shared oracle model

For a Boolean function $f:\{0,1\}^n\rightarrow\{0,1\}$, the standard oracle is

$$
U_f|x\rangle|y\rangle = |x\rangle|y\oplus f(x)\rangle.
$$

Preparing the output qubit in

$$
|-\rangle = \frac{|0\rangle-|1\rangle}{\sqrt{2}}
$$

turns the target-bit flip into a phase:

$$
U_f|x\rangle|-\rangle = (-1)^{f(x)}|x\rangle|-\rangle.
$$

This phase-kickback identity is the bridge between the oracle and the final
interference step in both algorithms.
