# Reproduce an environment and verify the installed package

The recorded dependency set is `uv.lock`. It fixes direct and transitive
versions, distribution hashes, and environment markers for the project and its
optional extras. The initial resolution preserves the scientific versions used
in the existing validated examples, including NumPy 2.3.5, SciPy 1.17.1,
Matplotlib 3.10.8, Qiskit 2.4.0, QDK 1.31.0, and PennyLane 0.45.1.

## Files with distinct responsibilities

| File | Responsibility |
| --- | --- |
| `pyproject.toml` | Package metadata, dependency declarations, extras, pinned build backend, and required uv version |
| `uv.lock` | Exact resolved packages, hashes and platform/Python branches |
| `.python-version` | Reference interpreter: CPython 3.14.3 |
| `tools/uv-requirement.txt` | Exact uv bootstrap version, checked against the project requirement |
| `tools/environment_report.py` | Actual interpreter/platform, installed distribution versions, lock fingerprint and installation mode |
| `.github/workflows/quality.yml` | Compatibility matrix and recorded verification artifacts |

The uv version is fixed at 0.13.1 and the build backend at setuptools 82.0.1.
Locking the resolver and backend makes updates explicit as well as fixing the
runtime dependencies. The library's minimum Python version remains 3.11.

## First locked installation

Run from the repository root, with Python and network access available for the
initial tool, interpreter and dependency downloads:

```bash
python -m pip install -r tools/uv-requirement.txt
uv sync --locked --extra test --no-editable
uv pip check --python .venv
uv run --no-sync python -I tools/environment_report.py --require-wheel
uv run --no-sync python -m pytest -q
```

The reference interpreter is selected by `.python-version`; uv can download it
when it is absent. The `test` extra installs pytest without the interactive
notebook stack. A normal, noneditable installation is used so tests import the
installed package rather than relying on an editable link to `src/`.

`--locked` fails when the project and lockfile disagree instead of silently
rewriting the recorded resolution. Once synchronization succeeds, `--no-sync`
runs commands in that environment without changing the chosen extras. These
semantics follow the official [locking and syncing documentation](https://docs.astral.sh/uv/concepts/projects/sync/).

The isolated `python -I` check rejects an editable package or an import outside
the selected environment. `uv pip check` explicitly targets `.venv`: a Python
selection override must not cause it to inspect the base interpreter instead.

## Select a profile from the same lock

| Task | Synchronization command |
| --- | --- |
| Core tests | `uv sync --locked --extra test --no-editable` |
| Interactive development | `uv sync --locked --extra dev` |
| Notebook execution | `uv sync --locked --extra notebooks --no-editable` |
| Documentation | `uv sync --locked --extra docs --no-editable` |
| Bell-noise comparison | `uv sync --locked --extra test --extra pennylane --no-editable` |
| All SDKs, notebook and documentation tools | `uv sync --locked --all-extras --no-editable` |

Exact synchronization removes packages outside the selected profile. Choose the
profile before running its commands. Core-only tests intentionally skip optional
SDK cases; that result is not a claim that SDK checks ran.

For the complete comparison:

```bash
uv sync --locked --all-extras --no-editable
uv run --no-sync python tools/validate_experiments.py --ecosystem numpy qiskit pennylane openqasm qsharp
uv run --no-sync python -m studies.bell_noise.run_study --output-dir build/bell-noise-review
uv run --no-sync python -m pytest -q
uv run --no-sync python -m mkdocs build --strict
```

For active editing, the `dev` profile uses uv's default editable install. If
checking changed source using the noneditable profile, explicitly reinstall the
project with `--reinstall-package quantum-ed` while retaining the desired extras.
This avoids testing an older installed copy after editing `src/`.

`requirements.txt` delegates convenience pip installs to the project metadata;
`environment.yml` provides a Conda convenience setup. Those routes alone do
not enforce the lockfile. Use the locked route for a reproducibility claim.

## Compatibility checks and evidence

| CI scope | Python targets | Operating systems |
| --- | --- | --- |
| Core, installed-package checks and NumPy experiments | 3.11, 3.12, 3.13, 3.14 | Linux and Windows |
| Qiskit, imported OpenQASM, Q#, and PennyLane jobs | 3.11 and reference 3.14.3 | Linux |
| Notebook execution and strict documentation build | Reference 3.14.3 | Linux |

Matrix jobs explicitly select their Python interpreter for every uv command,
overriding the reference file. Each installs the package noneditably from the
same lock and checks dependency consistency. The matrix describes configured
checks; consult the actual run artifacts for their results.

Every job uploads an `environment.json` recording the exact Python patch
version, platform, installed distributions, and SHA-256 of the lockfile with
LF-normalized line endings. Test jobs also retain JUnit XML. Scientific jobs
retain their generated data and figures. Failed jobs upload the evidence
already produced, so partial results are distinguishable from completed runs.

The minor-version matrix uses the patch release available to the runner;
the reference interpreter is pinned exactly. Python markers can select different
pinned transitive versions for different targets, as described in uv's
[resolution documentation](https://docs.astral.sh/uv/concepts/resolution/).

These checks do not freeze the host operating-system image, numerical libraries
outside the Python distributions, or hardware. They establish a versioned Python
dependency set and measured compatibility, not universally identical floating
point results or byte-identical figures across all machines. Scientific
tolerances remain defined by the [validation protocol](experiment-validation.md).

## Update deliberately

For a targeted dependency update, change the lock and review its diff:

```bash
uv lock --upgrade-package numpy
uv sync --locked --all-extras --no-editable
uv run --no-sync python -m pytest -q
uv run --no-sync python tools/validate_experiments.py --ecosystem numpy qiskit pennylane openqasm qsharp
uv run --no-sync python -m studies.bell_noise.run_study --output-dir build/bell-noise-updated
uv run --no-sync python -m mkdocs build --strict
```

Compare the regenerated scientific summary and data before replacing the
included artifacts. Update the resolver requirement and bootstrap file together
when changing uv. The build backend is pinned in `build-system.requires`, so
its updates are also visible in review. Commit the lockfile alongside the
dependency metadata, and retain the CI evidence for the tested change.
