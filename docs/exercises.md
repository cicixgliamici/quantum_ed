# Verifiable exercises

The exercise path converts theoretical statements into properties that can be
checked by tests. Attempt each prompt before opening its reference solution.

| Exercise | Main property |
| --- | --- |
| [Normalize a state](https://github.com/cicixgliamici/quantum_ed/tree/main/exercises/01-normalize-state) | Output norm equals one |
| [Prepare a Bell state](https://github.com/cicixgliamici/quantum_ed/tree/main/exercises/02-prepare-bell-state) | Correlations and reduced states match theory |
| [Validate a noise channel](https://github.com/cicixgliamici/quantum_ed/tree/main/exercises/03-validate-noise-channel) | Density-matrix invariants are preserved |

Run the public checks with:

```bash
python -m pytest -q tests/exercises
```
