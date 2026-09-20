# Superdense-coding experiment

## Goal

Transmit the two-bit classical message `10` by sending one qubit after Alice
and Bob have shared a Bell pair. Entanglement is a pre-shared resource; it does
not transmit information on its own.

## Quantum pattern

1. Alice and Bob prepare $|\Phi^+\rangle$.
2. Alice encodes the first bit with `Z` and the second bit with `X`.
3. Alice sends her qubit to Bob.
4. Bob applies `CNOT` and `H` to decode the Bell state.
5. Bob measures the two-qubit computational-basis state.

For message `10`, Alice applies `Z` but not `X`. Ideal decoding is deterministic.

## Implementations

| Ecosystem | Source | Expected representation |
| --- | --- | --- |
| NumPy | [`numpy/superdense_coding.py`](numpy/superdense_coding.py) | Computational-basis label `10` |
| Qiskit | [`qiskit/superdense_coding.py`](qiskit/superdense_coding.py) | Displayed count key `10` |
| Q# | [`qsharp/SuperdenseCoding.qs`](qsharp/SuperdenseCoding.qs) | `[One, Zero]` in array order |
| OpenQASM 3 | [`openqasm/superdense_coding.qasm`](openqasm/superdense_coding.qasm) | `results[0]=1`, `results[1]=0` |
| PennyLane | [`pennylane/superdense_coding.py`](pennylane/superdense_coding.py) | Analytic basis probabilities |

Qiskit normally displays the highest classical index first, so its measurements
intentionally use reversed classical destinations. This makes the displayed key
match the logical phase-bit/flip-bit order used by the other implementations.
See the [bit-ordering reference](../../docs/reference/bit-ordering.md).

## Theory

Read the [superdense-coding derivation](../../docs/04-entanglement/superdense-coding.md)
for the four encodings and their Bell-state correspondence.

## Run

```bash
python experiments/superdense-coding/qiskit/superdense_coding.py
```
