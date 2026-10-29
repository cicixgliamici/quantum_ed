# Entanglement-swapping experiment

Connect two perfect Bell pairs through a middle node and verify the resulting
endpoint state. Read the [network chapter](../../docs/11-quantum-networks/README.md)
and [derivation](../../docs/11-quantum-networks/entanglement-swapping.md).

## Protocol and conventions

Use four logical wires in order `A=0, B1=1, B2=2, C=3`. Bob owns wires 1 and 2.
Prepare Phi-plus on `(A, B1)` and `(B2, C)`, then apply CNOT `(B1, B2)` and H on
`B1` for Bob's Bell measurement. Outcome `zx` means `z=B1`, `x=B2`.
Charlie applies X for `x=1`, then Z for `z=1`.

NumPy explicitly projects the four branches. The SDK circuits defer readout
and use coherent controls for the same corrections. Those controls describe
ideal simulation; a physical network needs classical messaging and local
feed-forward. Qiskit's printed ket axes are reversed relative to logical wire
order; validation converts them before comparing states.

## Expected results and checks

- Each of Bob's four outcomes occurs with probability `1/4`.
- Every corrected Alice-Charlie branch is Phi-plus, including its relative phase.
- Corrected endpoint probabilities are `P(00)=P(11)=1/2`.
- Discarding Bob's record before correction gives `rho_AC=I4/4`.
- Every individual endpoint marginal remains `I2/2`.

No branch is postselected in the corrected protocol. The source assumes
pre-existing ideal links and a complete Bell measurement; it does not model
photon loss, memory decoherence, or physical delivery rates.

## Implementations

| Ecosystem | Entry point | State inspection |
| --- | --- | --- |
| NumPy | [entanglement_swapping.py](numpy/entanglement_swapping.py) | Explicit branch projection through `quantum_ed.networks` |
| Qiskit | [entanglement_swapping.py](qiskit/entanglement_swapping.py) | Four-wire statevector before terminal measurement |
| PennyLane | [entanglement_swapping.py](pennylane/entanglement_swapping.py) | Independent QNode state preparation |
| Q# | [EntanglementSwapping.qs](qsharp/EntanglementSwapping.qs) | Shared `PrepareSwapping` operation |
| OpenQASM 3 | [entanglement_swapping.qasm](openqasm/entanglement_swapping.qasm) | Imported circuit before endpoint measurement |

## Run and reproduce

From the repository root:

```bash
uv sync --locked --extra test --no-editable
uv run --no-sync python experiments/entanglement-swapping/numpy/entanglement_swapping.py
uv run --no-sync python -m pytest -q tests/test_networks.py tests/experiments/test_entanglement_swapping.py
```

For all five ecosystems:

```bash
uv sync --locked --extra test --extra showcase --extra pennylane --extra openqasm --extra qsharp --no-editable
uv run --no-sync python tools/validate_experiments.py --ecosystem numpy qiskit pennylane openqasm qsharp
```

The [network notebook](../../notebooks/07-entanglement-swapping.ipynb) displays
the branch table and density matrices. The shared validator inspects all
four corrected branches in every ecosystem, rather than accepting endpoint
Z-basis counts alone. See the [validation protocol](../../docs/reference/experiment-validation.md).
