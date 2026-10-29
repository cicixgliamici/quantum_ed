# Scientific validation across ecosystems

The experiment validators compare every declared implementation with shared
analytical references. A successful import or compilation alone is insufficient:
a circuit can run while using the wrong wire order or relative phases.

## Run the checks

Install the optional SDKs needed for a complete local comparison:

```bash
python -m pip install -r tools/uv-requirement.txt
uv sync --locked --all-extras --no-editable
uv run --no-sync python tools/validate_experiments.py --ecosystem numpy qiskit pennylane openqasm qsharp
uv run --no-sync python -m pytest -q
```

See [environment reproduction](reproducibility.md) for the pinned interpreter,
resolver, lockfile and compatibility matrix. Each ecosystem can be checked separately using the same `--ecosystem` option.
CI runs these checks in the corresponding SDK jobs. The existing
`validate_openqasm.py` and `validate_qsharp.py` commands now execute this
scientific validation, including actual program results.

## What is compared

| Experiment | Shared analytical reference |
| --- | --- |
| Bell pair | `P(00) = P(11) = 1/2`; all other outcomes impossible |
| Entanglement swapping | Four Bob outcomes with probability `1/4` each; every corrected endpoint branch is Phi-plus |
| Superdense coding | Default decoded message `10` |
| Teleportation | Bob recovers the full input density matrix |
| Deutsch-Jozsa | `100` in input-wire order for the oracle `f(x)=x_0` |
| Bernstein-Vazirani | Secret `101` in input-wire order |
| Grover | Marked state `11` with probability one |
| QFT | Fourier amplitudes `exp(2 pi i j k / 8) / sqrt(8)` |
| QPE | Wire-order result `100`, interpreted numerically as phase bits `001` |
| VQE | Objective `cos(theta)` and minimum energy `-1` |

NumPy, Qiskit, and PennyLane QFT preparations are checked on all eight basis
inputs. Q# exposes a shared `PrepareQft` operation and is also checked on all
eight. OpenQASM's fixed input `001` is checked after import, including phases.
Uniform probabilities alone would also accept a Fourier transform of the
wrong input, or one with the wrong sign in its exponent.

Teleportation is checked for `|0>`, `|1>`, `|+>`, `|->`, `|+i>`, `|-i>`, and
one generic state away from the axes. The validators trace out Alice's qubits
and compare Bob's reduced density matrix with the input projector. The Python
implementations accept input column vectors and normalize them explicitly.
Q# exposes the same protocol through `PrepareTeleportation`, and OpenQASM
through the imported `teleport` gate. These diagnostic preparations share the
code used by their default entrypoints.

The Python VQE implementations are checked at several angles and at the
optimizer output. Q# and OpenQASM only implement the optimal ansatz; validation
checks their resulting measurement, without claiming they run an optimizer.

## Wire order and classical destinations

Swapping uses four wires in order Alice, Bob-left, Bob-right, Charlie. Validators
inspect each conditional endpoint state, including its relative phase, and
check that every Bob outcome has probability `1/4`. This includes NumPy,
Qiskit, PennyLane, the imported OpenQASM circuit, and Q#'s shared
`PrepareSwapping` operation. Only endpoint wires 0 and 3 contribute to terminal
sampling. The separate core tests also verify the uncorrected `I4/4` ensemble
and the `I2/2` local marginals; see the [derivation](../11-quantum-networks/entanglement-swapping.md).

Comparisons use increasing logical output wire index. Qiskit's tensor axes
are reversed before state-vector comparisons. Marginal probabilities omit
ancillas and Alice's wires where appropriate.

Sampled Qiskit and imported OpenQASM results are decoded through the actual
wire-to-classical-bit measurement mapping. This handles superdense coding's
reversed classical destinations without assuming that every displayed string
should be reversed. Imported scalar OpenQASM bits are grouped into a classical
register for the sampler, preserving their original measurement destinations.

Q# returns results in the explicit tuple or array order used by each program.
The state-dump diagnostics use allocated qubits in array order, checked against
the same analytical states. NumPy's analytical QPE result labels integer phase
bits, so its labels are reversed when comparing with counting-wire order.

## Numerical and statistical tolerances

Analytical probabilities, density matrices, and state amplitudes use absolute
tolerance `1e-10` and relative tolerance zero. State-vector comparisons permit
a global phase while requiring unit norm and every relative phase.
PennyLane's iterative VQE optimizer is accepted within `1e-3` of ground energy;
its objective values still use the analytical tolerance.

Qiskit, imported OpenQASM, and Q# entrypoints use 4,096 shots with seed 42.
For a distribution with `K` expected outcomes and `N` shots, the simultaneous
absolute frequency bound is:

$$
\epsilon = \sqrt{\frac{\log(2K/\alpha)}{2N}},\qquad \alpha = 10^{-6}.
$$

Hoeffding's inequality and a union bound give failure probability at most
`alpha` per checked distribution under independent ideal sampling. Impossible
outcomes are rejected even if observed only once. This bound describes sampling
fluctuation, not numerical error or hardware noise.

The suite also includes deliberately incorrect relative phases, reversed bits,
and biased counts to verify that these checks reject scientifically different
results. These are finite educational cases; passing does not prove arbitrary
program equivalence or establish correctness on quantum hardware.
