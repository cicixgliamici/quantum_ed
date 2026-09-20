# Superdense coding

Superdense coding uses a shared entangled pair to communicate two classical
bits while physically sending one qubit. The Bell pair must be distributed
before the message is chosen, so the protocol does not violate causality or
send information through entanglement alone.

## Shared resource

Alice owns qubit 0 and Bob owns qubit 1. They initially share

$$
|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}.
$$

Alice encodes a phase bit $b_0$ and a flip bit $b_1$ on her qubit with

$$
Z^{b_0}X^{b_1}.
$$

The four possible messages therefore select the four orthogonal Bell states:

| Message $b_0b_1$ | Alice applies | Shared state |
| --- | --- | --- |
| `00` | $I$ | $|\Phi^+\rangle$ |
| `01` | $X$ | $|\Psi^+\rangle$ |
| `10` | $Z$ | $|\Phi^-\rangle$ |
| `11` | $ZX$ | $|\Psi^-\rangle$ up to global phase |

## Decoding

Alice sends qubit 0 to Bob. Bob now holds both qubits and applies `CNOT(0, 1)`
followed by `H(0)`. This is the inverse of Bell-state preparation and maps the
Bell basis to the computational basis:

$$
|\Phi^+\rangle \mapsto |00\rangle, \quad
|\Psi^+\rangle \mapsto |01\rangle,
$$

$$
|\Phi^-\rangle \mapsto |10\rangle, \quad
|\Psi^-\rangle \mapsto |11\rangle.
$$

Measuring both qubits recovers $b_0b_1$ deterministically in an ideal circuit.

## What the resource accounting means

The protocol transmits one qubit after the message is selected, but it also
consumes one previously shared Bell pair. Its advantage is therefore about the
classical capacity of quantum communication assisted by entanglement, not free
communication without a physical channel.

## Repository experiment

The [cross-ecosystem experiment](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/superdense-coding)
encodes `10` in Qiskit, Q#, and OpenQASM 3. Its README documents how each tool
represents the two measured bits.
