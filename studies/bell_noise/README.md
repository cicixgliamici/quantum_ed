# Bell-pair noise: fidelity, entanglement, and purity

**Question:** How does independent local noise change a Bell pair, and can
unchanged measurement probabilities hide lost entanglement?

This study compares NumPy Kraus sums with PennyLane `default.mixed` for
dephasing, depolarizing noise, and amplitude damping. It validates full density
matrices and five observables against independently derived analytical formulas
on 101 parameter values per channel: 606 states across two implementations.

Read the [complete study](../../docs/07-noise-and-channels/bell-noise-study.md)
for derivations, results, interpretation, primary references, and limitations.

![Fidelity, negativity, and purity](../../docs/assets/bell-noise/metrics.png)

## Reproduce from the repository root

```bash
python -m pip install -r tools/uv-requirement.txt
uv sync --locked --extra test --extra pennylane --no-editable
uv run --no-sync python -m studies.bell_noise.run_study
uv run --no-sync python -m pytest -q tests/studies
```

The default command validates both models and regenerates the committed
figures and data. It fails if a physicality or agreement check fails.

For a lightweight core-only run, explicitly select NumPy and a separate directory:

```bash
uv run --no-sync python -m studies.bell_noise.run_study --numpy-only --output-dir build/bell-noise-numpy
```

This alternative makes no cross-framework validation claim. Use `--points`
to change the endpoint-inclusive grid and `--output-dir` to export elsewhere.

## Review the evidence

- [Metrics figure](../../docs/assets/bell-noise/metrics.svg)
- [Coherence figure](../../docs/assets/bell-noise/coherence.svg)
- [CSV data](../../docs/assets/bell-noise/results.csv)
- [Validation summary and environment](../../docs/assets/bell-noise/summary.json)

## Source map

| File | Responsibility |
| --- | --- |
| [numpy_model.py](numpy_model.py) | Explicit Bell preparation and local Kraus channels |
| [pennylane_model.py](pennylane_model.py) | Built-in SDK channels with matched physical parameters |
| [theory.py](theory.py) | Analytical density matrices and observable formulas |
| [metrics.py](metrics.py) | Fidelity, partial transpose, negativity, purity, and correlations |
| [run_study.py](run_study.py) | Parameter sweep, validation, CSV, and provenance |
| [plots.py](plots.py) | Standalone PNG and SVG figures |

The contribution is a transparent, tested reproduction of known quantum-noise
behavior, including explicit parameter conversions and counterexamples to
judging entanglement from computational-basis probabilities or purity alone.
