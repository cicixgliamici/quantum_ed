# Qiskit tutorials

Use these scripts to learn Qiskit's circuit and result APIs. For comparisons
against other ecosystems and shared analytical checks, use the
[experiment collection](../../experiments/README.md).

## Run a tutorial

From the repository root:

```bash
uv sync --locked --extra showcase --no-editable
uv run --no-sync python examples/qiskit/00_first_circuit.py
```

The `showcase` dependency extra retains its existing name for compatibility.
All scripts simulate locally. The numbered filenames preserve the original
lesson order; gaps do not indicate missing installation steps.

## Lesson sequence

| Lesson | Focus |
| --- | --- |
| [00: First circuit](00_first_circuit.py) | Circuit construction and measurement |
| [01: Single-qubit gates](01_single_qubit_gates.py) | X, Y, Z, H, and phase gates |
| [02: Rotation gates](02_rotation_gates.py) | Parameterized rotations and phases |
| [03: Multi-qubit gates](03_multi_qubit_gates.py) | Control, target, SWAP, and Toffoli |
| [04: Measurement](04_measurement.py) | Classical registers and displayed bit strings |
| [05: Statevectors](05_statevector.py) | Amplitudes, probabilities, and phase |
| [06: Operators and observables](06_operators_and_observables.py) | Unitaries and expectation values |
| [07: Tensor products](07_tensor_products.py) | Combining states and matching circuit order |
| [08: Parameterized circuits](08_parameterized_circuits.py) | Binding circuit parameters |
| [09: Sampler](09_sampler.py) | Shots, result containers, and seeded sampling |
| [13: Bell state](13_bell_state.py) | Preparation, statevector, and correlated counts |
| [20: Deutsch-Jozsa](20_deutsch_jozsa.py) | Oracle classification |
| [21: Bernstein-Vazirani](21_bernstein_vazirani.py) | Hidden-string recovery |

## Bit ordering

These scripts use Qiskit's displayed ket order `|q[n-1] ... q[0]>`.
For two qubits, `X` on qubit 0 prepares `|01>`; `H` on qubit 0 prepares
`(|00> + |01>) / sqrt(2)`. This differs from the NumPy core's leftmost-wire
convention. See the [repository conventions](../../docs/reference/bit-ordering.md)
and [IBM's bit-ordering guide](https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering).
