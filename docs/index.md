# Quantum-Ed

Quantum-Ed connects mathematical quantum computing to executable simulations
in NumPy, Qiskit, PennyLane, Q#, and OpenQASM 3. The code and notes make the
assumptions and expected results inspectable.

[Review the project](reviewer-guide.md){ .md-button .md-button--primary }
[Start learning](00-intro/README.md){ .md-button }

## Choose your route

<div class="grid cards" markdown>

- **Evaluate the evidence**

    Follow a ten-minute route through the mathematical claims, implementation,
    validation protocol, and limits of the project.

    [Open the reviewer guide](reviewer-guide.md)

- **Learn the foundations**

    Build from linear algebra to qubits, measurement, entanglement, and noise.
    Each chapter connects mathematical notation to a computational model.

    [Begin with the introduction](00-intro/README.md)

- **Compare implementations**

    Inspect nine experiments across NumPy, Qiskit, PennyLane, Q#, and OpenQASM 3,
    with explicit expected results and conventions.

    [Explore the experiments](experiments.md)

- **Work through the code**

    Use seven ordered notebooks for exploration and three exercises for
    practice. Run the programs locally using the documented environment.

    [Read the executed notebooks](notebooks.md)
    · [Try the exercises](exercises.md)

</div>

## A question with reproducible evidence

Can measurement probabilities stay unchanged after entanglement is lost?
The Bell-noise study derives the answer and checks three local channels using
independent NumPy and PennyLane models. Its figures, CSV data, and validation
summary connect each conclusion to a computation.

![Bell-pair fidelity, entanglement, and purity under local noise](assets/bell-noise/metrics.png)

[Read the study](07-noise-and-channels/bell-noise-study.md){ .md-button }

Inspect the [CSV measurements](assets/bell-noise/results.csv) and
[validation summary](assets/bell-noise/summary.json) alongside the derivations.

## Start here

1. Review the [mathematical foundations](01-linear-algebra/README.md).
2. Learn how [qubits and states](02-qubits-and-states/README.md) are represented.
3. Continue through [measurement](03-measurement/README.md) and
   [entanglement](04-entanglement/README.md).
4. Inspect the [concept-first experiments](experiments.md).
5. Solve the [verifiable exercises](exercises.md).
6. Use the [reference section](reference/README.md) when comparing ecosystems.

## Evidence and conventions

- [Experiment validation](reference/experiment-validation.md) defines analytical
  references, phase-sensitive checks, and sampling tolerances.
- [Input contracts](reference/input-contracts.md) explains dimensions,
  normalization, and physical-state validation.
- [Scientific scope](reference/scientific-scope.md) distinguishes mathematical
  identities, simplified models, empirical claims, and conditional estimates.

## Repository layers

- **Theory** derives concepts and protocols.
- **NumPy core** keeps the linear algebra transparent and testable.
- **Experiments** compare the same outcome across programming ecosystems.
- **Studies** expose framework-specific capabilities and portability limits.
- **Notebooks** support interactive exploration.
- **Exercises** turn mathematical properties into executable checks.
