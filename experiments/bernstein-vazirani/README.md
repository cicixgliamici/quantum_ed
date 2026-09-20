# Bernstein-Vazirani experiment

## Goal

Recover the hidden string `101` with one oracle query. The oracle writes the
Boolean inner product between the input and the secret into a target qubit.

## Expected result

The input register is measured as `101`. The implementations document whether
that value is expressed in qubit-index order or display order.

## Implementations

| Ecosystem | Source |
| --- | --- |
| NumPy | [`numpy/bernstein_vazirani.py`](numpy/bernstein_vazirani.py) |
| Qiskit | [`qiskit/bernstein_vazirani.py`](qiskit/bernstein_vazirani.py) |
| Q# | [`qsharp/BernsteinVazirani.qs`](qsharp/BernsteinVazirani.qs) |
| OpenQASM 3 | [`openqasm/bernstein_vazirani.qasm`](openqasm/bernstein_vazirani.qasm) |
| PennyLane | [`pennylane/bernstein_vazirani.py`](pennylane/bernstein_vazirani.py) |

Read the [derivation](../../docs/10-quantum-algorithms/bernstein-vazirani.md)
and the [bit-ordering reference](../../docs/reference/bit-ordering.md).

## Run

```bash
python experiments/bernstein-vazirani/qiskit/bernstein_vazirani.py
```
