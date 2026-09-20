# Quantum teleportation

Quantum teleportation transfers an unknown qubit state from Alice to Bob using
one shared Bell pair and two classical bits. It does not copy the state: Alice's
original state is consumed by the protocol.

## Initial state

Let the message be

$$
|\psi\rangle = \alpha|0\rangle + \beta|1\rangle.
$$

Alice and Bob also share $|\Phi^+\rangle$. The complete state is
$|\psi\rangle\otimes|\Phi^+\rangle$.

## Bell-basis interaction

Alice applies `CNOT` from the message qubit to her Bell qubit, followed by `H`
on the message. The resulting state can be written as

$$
\frac{1}{2}\left(
|00\rangle|\psi\rangle +
|01\rangle X|\psi\rangle +
|10\rangle Z|\psi\rangle +
|11\rangle XZ|\psi\rangle
\right).
$$

Alice measures her two qubits and sends the outcomes to Bob. Bob applies `X`
when the second bit is one and `Z` when the first bit is one. His qubit then
equals $|\psi\rangle$ for every measurement branch.

## Deferred measurement

A measurement that controls a later gate can be deferred by replacing the
classical condition with a coherent quantum control. The repository experiment
therefore applies controlled `X` and controlled `Z` before measuring Alice's
qubits. This static circuit has the same reduced state on Bob's qubit and is
easier to express consistently across NumPy, Qiskit, Q#, and OpenQASM 3.

## What teleportation does not do

- It does not move a physical particle.
- It does not clone the input state.
- It cannot communicate faster than light because Bob still needs classical
  information in the textbook form.
- It consumes the shared entangled pair.

## Repository experiment

The [cross-ecosystem experiment](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/quantum-teleportation)
teleports $|1\rangle$, which makes the final verification deterministic and
easy to inspect. The derivation remains valid for every normalized qubit state.
