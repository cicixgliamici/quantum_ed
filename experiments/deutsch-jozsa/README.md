# Deutsch-Jozsa experiment

## Goal

Classify a promised Boolean function as constant or balanced with one oracle
query. The included oracle is the balanced function $f(x)=x_0$ over three
input bits.

## Expected result

The final input measurement is not all zero, so the oracle is classified as
`balanced`. The output qubit is intentionally not measured because it carries
no classification result.

## Implementations

| Ecosystem | Source |
| --- | --- |
| NumPy | [`numpy/deutsch_jozsa.py`](numpy/deutsch_jozsa.py) |
| Qiskit | [`qiskit/deutsch_jozsa.py`](qiskit/deutsch_jozsa.py) |
| Q# | [`qsharp/DeutschJozsa.qs`](qsharp/DeutschJozsa.qs) |
| OpenQASM 3 | [`openqasm/deutsch_jozsa.qasm`](openqasm/deutsch_jozsa.qasm) |
| PennyLane | [`pennylane/deutsch_jozsa.py`](pennylane/deutsch_jozsa.py) |

Read the [derivation](../../docs/10-quantum-algorithms/deutsch-jozsa.md) and the
[ecosystem comparison](../../docs/10-quantum-algorithms/language-comparison.md).

## Run

```bash
python experiments/deutsch-jozsa/qiskit/deutsch_jozsa.py
```
