# Scientific scope, conventions, and evidence

This repository combines exact mathematics, deliberately simplified models,
and implementations of small examples. They support different claims.
The notes below explain how to read those claims and maintain their evidence.

## Definitions and conventions

State vectors are normalized qubit column vectors unless an operation explicitly
normalizes its input. Tensor order, measurement destinations, and phase-bit
interpretation are documented in [input contracts](input-contracts.md) and
[bit ordering](bit-ordering.md).

Fidelity F uses the squared convention. If a source defines root fidelity f,
then F=f squared. The identity between trace distance and the square root of
one minus fidelity is guaranteed when **both** states are pure; one pure
reference alone does not suffice. See the counterexample and primary sources
in [fidelity and trace distance](../07-noise-and-channels/FIDELITY.md).

State fidelity, average gate fidelity, no-fault probability, and task success
probability are distinct quantities. A product of independent fault-survival
probabilities is a result for that stochastic model, not a general circuit
fidelity formula. The [hardware chapter](../08-hardware/README.md) defines
the quantities and works through numerical examples.

## How quantitative claims are supported

| Kind of statement | Evidence and scope to include |
| --- | --- |
| Mathematical identity or inequality | Definitions, hypotheses, convention, derivation or primary reference |
| Analytical noise prediction | Initial state, exact channel, subsystem mapping, parameter range |
| Numerical experiment | Runnable source, parameters, data, metric definitions, numerical or statistical tolerance |
| Illustrative hardware calculation | Explicit assumed inputs and model; no implication that these characterize every device |
| Experimental performance | Named experiment/device, date, measurement protocol and source; no unsourced modality-wide ranking |
| Resource estimate | Algorithm, architecture, error/timing assumptions, overheads and target runtime, with dated source |
| Algorithmic speedup | Task, access model, precision, preparation/readout cost, and classical comparison |

The hardware overview uses qualitative platform descriptions and sourced,
dated resource examples instead of an unsourced table of supposedly current
record fidelities. Its coherence-depth estimate specifies a target remaining
contrast. Surface-code scaling is labeled model-dependent; a physical-qubit
count is not converted to logical capacity using one universal multiplier.

## Areas examined in the scientific review

| Area | Clarification or correction |
| --- | --- |
| Hardware error budget | Independent no-fault probability distinguished from state/gate fidelity; arithmetic recomputed |
| Coherence depth | Exponential contrast with a chosen target, rather than a universal hard cutoff |
| Readout correction | Stationarity, calibration, invertibility and uncertainty assumptions |
| SWAP routing | A specified layout-restoring construction costs `6*(k-1)+1` CNOTs; this is not a compiler optimum |
| Fidelity | Pure/pure identity distinguished from pure/mixed inequalities, with an executable counterexample |
| Open-system noise | Purity and entropy may move in either direction; channel/dilation assumptions stated |
| T1/T2 | Exponential Markovian model separated from arbitrary fitted decay envelopes |
| Simulation memory | Complex128 storage, working-memory caveat, and explicit decimal/binary units |
| VQE | Ansatz and optimizer limits, correct Y-basis gate order, parameter-shift hypotheses and finite-shot uncertainty |
| QPE | Integer versus fractional Fourier labels, numerical versus wire order, and controlled-power cost |
| Other affected examples | Runnable density-matrix/teleportation snippets; qualified algorithmic-complexity and CHSH statements |

This is a targeted review of these areas, not a formal proof of every statement
in the repository. The [Bell-noise study](../07-noise-and-channels/bell-noise-study.md)
also states the finite family of states and channels it validates.

## Automated checks and their limits

```bash
python -m pytest -q tests/test_documentation_examples.py tests/test_repository_links.py
python tools/verify_repository.py
python -m mkdocs build --strict
```

The example tests execute the Python blocks in the reviewed numerical pages,
with optional SDK examples skipped only when their SDK is absent. Independent
checks cover the fidelity counterexample, Y-basis measurement, routed CNOT
unitaries, phase-estimation output distributions, and the parameter-shift
restriction for a shared parameter.

Repository validation checks local Markdown links and links to this repository's
`blob/main` and `tree/main` paths against the current checkout. It does not
validate the contents of external papers or prove a scientific statement merely
because a citation URL exists. Primary papers and author-written references
are linked next to the claims they support.

Contributors should preserve these distinctions when adding examples or
updating performance numbers. A new empirical figure should come with its
measurement conditions; a new approximation should explain its assumptions
and compare against an exact expression when one is available.
