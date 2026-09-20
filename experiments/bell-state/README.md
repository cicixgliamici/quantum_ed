# Bell-state experiment

## Goal

Prepare the Bell state

$$
|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}
$$

and verify its perfect computational-basis correlation.

## Quantum pattern

1. Start from $|00\rangle$.
2. Apply `H` to qubit 0.
3. Apply `CNOT` with qubit 0 as control.
4. Measure both qubits.

The ideal result contains only `00` and `11`, each with probability $1/2$.
Individual finite-shot counts will fluctuate.

## Implementations

| Ecosystem | Source | Main abstraction |
| --- | --- | --- |
| NumPy | [`numpy/bell_state.py`](numpy/bell_state.py) | Explicit state vectors and matrices |
| Qiskit | [`qiskit/bell_state.py`](qiskit/bell_state.py) | Circuit construction and local sampling |
| Q# | [`qsharp/BellState.qs`](qsharp/BellState.qs) | Qubit allocation, measurement, and reset |
| OpenQASM 3 | [`openqasm/bell_state.qasm`](openqasm/bell_state.qasm) | Portable circuit representation |
| PennyLane | [`pennylane/bell_state.py`](pennylane/bell_state.py) | Analytic QNode probabilities |

The mathematical implementation is provided by `quantum_ed.states` and
`quantum_ed.gates`; see the [entanglement chapter](../../docs/04-entanglement/README.md).

## Bit ordering

Qubit indexes describe the same physical roles in every implementation.
Displayed classical strings can be reversed by an SDK's formatting convention,
so compare correlations and consult the
[bit-ordering reference](../../docs/reference/bit-ordering.md).

## Run

```bash
python experiments/bell-state/qiskit/bell_state.py
```
