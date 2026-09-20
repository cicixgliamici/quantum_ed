# Quantum-teleportation experiment

## Goal

Transfer the state $|1\rangle$ from Alice's message qubit to Bob's qubit using
a shared Bell pair. The protocol transfers a quantum state, not matter, and
still requires a communication channel.

## Static cross-ecosystem form

The textbook protocol measures Alice's qubits and applies `X` and `Z`
corrections controlled by two classical bits. This experiment uses the deferred
measurement principle: the corrections remain coherently controlled until the
end. Both circuits produce the same state on Bob's qubit, while the coherent
form is portable across static circuit representations.

## Implementations

| Ecosystem | Source | Expected result |
| --- | --- | --- |
| NumPy | [`numpy/quantum_teleportation.py`](numpy/quantum_teleportation.py) | Target probabilities `0: 0`, `1: 1` |
| Qiskit | [`qiskit/quantum_teleportation.py`](qiskit/quantum_teleportation.py) | Count key `1` only |
| Q# | [`qsharp/QuantumTeleportation.qs`](qsharp/QuantumTeleportation.qs) | `One` |
| OpenQASM 3 | [`openqasm/quantum_teleportation.qasm`](openqasm/quantum_teleportation.qasm) | Classical result `1` |
| PennyLane | [`pennylane/quantum_teleportation.py`](pennylane/quantum_teleportation.py) | Target probabilities `[0, 1]` |

## Theory

Read the [protocol derivation](../../docs/04-entanglement/quantum-teleportation.md).

## Run

```bash
python experiments/quantum-teleportation/numpy/quantum_teleportation.py
python experiments/quantum-teleportation/qiskit/quantum_teleportation.py
```
