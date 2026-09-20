# Verifiable exercises

Exercises connect a mathematical objective to an executable reference solution.
Each directory contains a prompt, prerequisites, expected properties, and a
small solution module. Tests under `tests/exercises/` verify the same properties
a learner should check in their own implementation.

| Exercise | Topic | Difficulty |
| --- | --- | --- |
| [Normalize a state](01-normalize-state/README.md) | State vectors | Introductory |
| [Prepare a Bell state](02-prepare-bell-state/README.md) | Gates and entanglement | Introductory |
| [Validate a noise channel](03-validate-noise-channel/README.md) | Density matrices | Intermediate |

Run only the exercise checks with:

```bash
python -m pytest -q tests/exercises
```
