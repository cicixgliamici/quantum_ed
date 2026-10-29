# NumPy demonstrations

Start here for short, local examples of the installed `quantum_ed` toolkit.
These demos use NumPy and do not require a quantum SDK.

From the repository root:

```bash
uv sync --locked --no-editable
uv run --no-sync python demos/bell_cli.py
```

| Demo | What to inspect | Run after installation |
| --- | --- | --- |
| [Bell amplitudes](bell_cli.py) | H and CNOT prepare equal `00` and `11` amplitudes | `uv run --no-sync python demos/bell_cli.py` |
| [Bell reduced states](bell_state_demo.py) | An entangled pure state has maximally mixed one-qubit reductions | `uv run --no-sync python demos/bell_state_demo.py` |
| [Noise comparison](noise_comparison_demo.py) | Five channels change fidelity and trace distance differently | `uv run --no-sync python demos/noise_comparison_demo.py` |

Continue with [SDK tutorials](../examples/README.md) for API-specific lessons,
[experiments](../experiments/README.md) for equivalent implementations, or
[studies](../studies/README.md) for reproducible investigations with data.
