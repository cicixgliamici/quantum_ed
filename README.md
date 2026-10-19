# Quantum-Ed

Quantum computing from explicit mathematics to verifiable simulations.

Quantum-Ed combines a small NumPy toolkit, structured theory, seven notebooks,
and nine experiments expressed in NumPy, Qiskit, PennyLane, Q#, and OpenQASM 3.
Its central question is whether the code reproduces the mathematical claim:
including relative phases, bit order, mixed states, and numerical tolerances.

Start with the [ten-minute reviewer guide](docs/reviewer-guide.md), the
[Bell-pair noise study](studies/bell_noise/README.md), or the
[experiment index](experiments/README.md).

## A complete study: what survives when a Bell pair becomes noisy?

The [study report](docs/07-noise-and-channels/bell-noise-study.md) compares
independent NumPy and PennyLane implementations of three local noise channels.
It checks 606 density matrices against analytical predictions and explains two
observable effects: Z-basis probabilities can stay unchanged after entanglement
is lost, and purity can return to one for a separable state.

![Bell-pair fidelity, entanglement, and purity under three local noise models](docs/assets/bell-noise/metrics.png)

[CSV data](docs/assets/bell-noise/results.csv) and the
[validation summary](docs/assets/bell-noise/summary.json) record the results,
parameters, numerical discrepancies, and software versions. The figures are
available as PNG and SVG and can be regenerated from source.

## What is implemented

| Component | Concrete evidence |
| --- | --- |
| NumPy teaching toolkit | [States](src/quantum_ed/states.py), [gates](src/quantum_ed/gates.py), measurement, density matrices, and single-qubit noise channels |
| Nine concept-first experiments | Bell states, superdense coding, teleportation, Deutsch-Jozsa, Bernstein-Vazirani, Grover, QFT, QPE, and a one-qubit VQE |
| Scientific comparisons | [Shared analytical checks](tools/validate_experiments.py), full-state phase-sensitive checks for QFT/teleportation, and explicit sampling bounds |
| Bell-noise investigation | [Derivations and interpretation](docs/07-noise-and-channels/bell-noise-study.md), independent models, validated data, and reproducible plots |
| Learning material | [Theory chapters](docs/index.md), [seven notebooks](notebooks/README.md), and [three exercises](exercises/README.md) with executable solutions |
| Automated verification | [Tests](tests/), repository/source-link checks, notebook execution, and strict documentation builds in [CI](.github/workflows/quality.yml) |

## Run a first example

The package requires Python 3.11 or newer. The locked reference environment
uses CPython 3.14.3, and the core CI matrix covers Python 3.11-3.14 on Linux and
Windows. From the repository root:

```bash
python -m pip install -r tools/uv-requirement.txt
uv sync --locked --extra test --no-editable
uv run --no-sync python -m pytest -q
uv run --no-sync python demos/bell_cli.py
```

The demo prepares a Bell pair using H and CNOT. Its only nonzero amplitudes
are those of `00` and `11`, each giving ideal measurement probability 1/2.
The normal package installation also exercises packaging instead of depending
on an editable source link. Core-only tests skip optional SDK examples.

[Reproducible environments](docs/reference/reproducibility.md) explains the
lockfile, profiles, installation checks, and environment reports. Convenience
pip and [Conda](environment.yml) routes remain available, but do not enforce
the locked versions by themselves.

## Reproduce the comparisons

For all five ecosystems and the full Bell-noise study:

```bash
uv sync --locked --all-extras --no-editable
uv run --no-sync python tools/validate_experiments.py --ecosystem numpy qiskit pennylane openqasm qsharp
uv run --no-sync python -m studies.bell_noise.run_study --output-dir build/bell-noise-review
uv run --no-sync python -m pytest -q
```

The [experiment validation protocol](docs/reference/experiment-validation.md)
states which outputs are compared, where full states are inspected, and how
finite-shot results are accepted. The study's output directory contains CSV,
JSON provenance, and two figures in PNG and SVG formats.

A lightweight study run is also available:

```bash
uv run --no-sync python -m studies.bell_noise.run_study --numpy-only --output-dir build/bell-noise-numpy
```

That mode validates NumPy against theory and explicitly records that no SDK
comparison was performed.

## Read or build the documentation

Follow the [reviewer route](docs/reviewer-guide.md) for a short technical review,
or start with [linear algebra](docs/01-linear-algebra/README.md) and proceed
through states, measurement, entanglement, circuits, mixed states, and noise.

```bash
uv sync --locked --extra docs --no-editable
uv run --no-sync python tools/verify_repository.py
uv run --no-sync python -m mkdocs build --strict
uv run --no-sync python -m mkdocs serve
```

[Scientific scope](docs/reference/scientific-scope.md) distinguishes identities,
model assumptions, dated hardware estimates, and numerical evidence.
[Input contracts](docs/reference/input-contracts.md) and
[bit ordering](docs/reference/bit-ordering.md) define the code's conventions.

## Repository map

| Location | Purpose |
| --- | --- |
| `src/quantum_ed/` | Installable NumPy-first toolkit |
| `docs/` | Theory, study report, reviewer route, and references |
| `notebooks/` | Ordered interactive lessons |
| `experiments/` | Equivalent concepts across five ecosystems |
| `studies/` | Capability comparisons and the complete Bell-noise study |
| `exercises/` | Prompts and reference solutions |
| `demos/` | Small runnable demonstrations |
| `tests/` and `tools/` | Mathematical, behavioral, and repository checks |

## Scope and future directions

This is an educational scientific-computing project using small simulated
instances. The one-qubit VQE illustrates an optimization loop; its Q# and
OpenQASM versions prepare the optimal ansatz without running an optimizer.
The Bell study covers one initial state and identical independent local noise
on two qubits. These examples demonstrate known effects and reproducible
reasoning, without claiming quantum advantage or hardware performance.

Possible extensions include unequal or correlated noise, finite-shot
entanglement certification, and hardware-calibrated timing models. They are
future directions rather than completed features.

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution and verification
conventions. Licensed under [MIT](LICENSE).
