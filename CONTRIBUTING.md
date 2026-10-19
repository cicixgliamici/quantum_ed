# Contributing

Quantum-Ed connects a quantum concept to transparent mathematics, executable
examples, and equivalent ecosystem implementations. Contributions should keep
that path easy to inspect.

## Choose the right location

- Put reusable NumPy-first teaching code in `src/quantum_ed/`.
- Put theory and derivations in `docs/`.
- Put interactive lessons in `notebooks/`.
- Put comparable, concept-specific programs in `experiments/<concept>/`.
- Put property-driven learning tasks in `exercises/`.
- Put capability-specific comparisons that cannot map to every circuit language
  in `studies/`, and explain the portability boundary.
- Put unit tests in `tests/` and cross-module checks in `tests/integration/`.

Do not place runnable portfolio examples under `src/`; that directory is
reserved for installable package code.

## Add an experiment

Start with a concept directory containing a `README.md` and `experiment.json`.
Document the goal, quantum pattern, expected result, bit-ordering convention,
implementation links, and run commands. The manifest must conform to
`experiments/schema.json` and declare one source for every supported ecosystem.
Add ecosystems only when they implement the same logical experiment.

## Code expectations

- Write code and comments in English.
- Prefer short functions with descriptive names.
- Use comments to explain decisions and quantum intent.
- Keep the NumPy-first core lightweight; framework dependencies stay optional.
- Use PennyLane for differentiable or mixed-state workflows, not as a replacement
  for the explicit NumPy derivation.
- Add tests for mathematical invariants and failure cases.

## Verification

For scientific notes, follow the [scope and evidence conventions](docs/reference/scientific-scope.md).
State approximation assumptions and distinguish state/gate fidelity from fault
probability. Cite dated primary sources for experimental or resource claims.
Add runnable examples to the reviewed-example checks when they support a
numerical result; comparisons must state tensor order and numerical tolerances.

```bash
python -m pip install -r tools/uv-requirement.txt
uv sync --locked --extra test --no-editable
uv run --no-sync python tools/verify_repository.py
uv run --no-sync python -m pytest -q
```

For Qiskit experiments, install `.[showcase]` and run the command documented in
the relevant experiment README.

The GitHub Actions workflow executes declared experiments against analytical
references in separate SDK jobs, including Q# and imported OpenQASM. It also
reproduces the Bell-noise study, executes clean notebook copies, and builds
the MkDocs site in strict mode. Core-only installation skips optional SDK tests;
the corresponding jobs install and test those dependencies explicitly.

For active source editing, use `uv sync --locked --extra dev` for an editable
installation. For a noneditable recheck after changing source, add
`--reinstall-package quantum-ed` to synchronization. Dependency updates must
include the lockfile and should follow the
[environment reproduction guide](docs/reference/reproducibility.md).
