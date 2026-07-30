# Quantum ecosystem showcase

This directory presents the same experiments in several quantum programming
ecosystems. Keeping the implementations side by side makes the syntax and
abstraction level easy to compare.

The installable, NumPy-first teaching library remains in `src/quantum_ed`.
These examples are intentionally independent: they are portfolio samples, not
runtime dependencies of the core package.

## Bell state

| Ecosystem | File | What it demonstrates |
| --- | --- | --- |
| Qiskit | [`qiskit/bell_state.py`](qiskit/bell_state.py) | Circuit construction and local sampling |
| Q# | [`qsharp/BellState.qs`](qsharp/BellState.qs) | Qubit allocation, entanglement, measurement, and reset |
| OpenQASM 3 | [`openqasm/bell_state.qasm`](openqasm/bell_state.qasm) | Portable, low-level circuit representation |

All three programs perform the same experiment:

1. Start from $|00\rangle$.
2. Apply a Hadamard gate to the first qubit.
3. Apply a controlled-X gate.
4. Measure both qubits.

The expected outcomes are `00` and `11`, each with probability close to
$1/2$.

## First algorithms

| Algorithm | Qiskit | Q# | OpenQASM 3 |
| --- | --- | --- | --- |
| Deutsch-Jozsa | [`deutsch_jozsa.py`](qiskit/deutsch_jozsa.py) | [`DeutschJozsa.qs`](qsharp/DeutschJozsa.qs) | [`deutsch_jozsa.qasm`](openqasm/deutsch_jozsa.qasm) |
| Bernstein-Vazirani | [`bernstein_vazirani.py`](qiskit/bernstein_vazirani.py) | [`BernsteinVazirani.qs`](qsharp/BernsteinVazirani.qs) | [`bernstein_vazirani.qasm`](openqasm/bernstein_vazirani.qasm) |

The accompanying [theory chapter](../../docs/10-quantum-algorithms/README.md)
derives both algorithms and explains their query complexity.
The [language comparison](../../docs/10-quantum-algorithms/language-comparison.md)
maps allocation, gates, measurement, execution, and bit ordering across all
three ecosystems.

## Run the examples

### Qiskit

Install the optional showcase dependency from the repository root:

```bash
python -m pip install -e ".[showcase]"
python src/showcase/qiskit/bell_state.py
python src/showcase/qiskit/deutsch_jozsa.py
python src/showcase/qiskit/bernstein_vazirani.py
```

### Q#

Open `qsharp/BellState.qs` with the Microsoft Quantum Development Kit extension
for Visual Studio Code and run the `Main` operation.

### OpenQASM 3

Load `openqasm/bell_state.qasm` in an OpenQASM 3-compatible simulator or
hardware toolchain. Execution commands vary by provider, so the source stays
vendor-neutral.
