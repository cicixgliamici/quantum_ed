# Learning path

Choose a route by the question you want to answer. The main chapters begin
with a learning guide linking prerequisites, runnable companions, practice,
and references. Read the derivations before comparing SDK syntax.

## Follow the foundations

| Stage | Read | Practice or inspect |
| --- | --- | --- |
| 1. Conventions | [Introduction](00-intro/README.md) | [Environment setup](notebooks.md) |
| 2. Mathematical tools | [Linear algebra](01-linear-algebra/README.md) | Normalize a complex state and check its norm |
| 3. States | [Qubits and states](02-qubits-and-states/README.md) | Compare global and relative phase in the Bloch lesson |
| 4. Observations | [Measurement](03-measurement/README.md) | Calculate probabilities in two measurement bases |
| 5. Correlations | [Entanglement](04-entanglement/README.md) | Prepare a Bell pair and inspect a reduced state |
| 6. Programs | [Circuits and gates](05-circuits-and-gates/README.md) | Reconstruct H followed by CNOT |
| 7. Mixtures | [Density matrices](06-density-matrices/README.md) | Contrast a pure superposition with a classical mixture |
| 8. Open systems | [Noise and channels](07-noise-and-channels/README.md) | Follow the [Bell-noise investigation](07-noise-and-channels/bell-noise-study.md) |
| 9. Algorithms | [Quantum algorithms](10-quantum-algorithms/README.md) | Compare implementations in the [experiment catalog](experiments.md) |
| 10. Networks | [Quantum communication and networks](11-quantum-networks/README.md) | Connect two Bell pairs through [entanglement swapping](11-quantum-networks/entanglement-swapping.md) |

Consult [useful matrices](09-useful-matrices/README.md) as a reference.
Read [hardware](08-hardware/README.md) after noise to distinguish simulator
models from dated physical estimates.

## Choose the right kind of code

| Material | Purpose | Where to start |
| --- | --- | --- |
| Demos | One short result using the NumPy toolkit | [Demo index](https://github.com/cicixgliamici/quantum_ed/blob/main/demos/README.md) |
| SDK examples | Learn a framework's APIs step by step | [Qiskit tutorials](https://github.com/cicixgliamici/quantum_ed/blob/main/examples/qiskit/README.md) |
| Notebooks | Change parameters and inspect calculations | [Executed lessons](notebooks.md) |
| Exercises | Turn a mathematical property into a check | [Exercise path](exercises.md) |
| Experiments | Compare one concept across ecosystems | [Experiment catalog](experiments.md) |
| Studies | Investigate a question with models, data, and interpretation | [Bell-pair noise study](07-noise-and-channels/bell-noise-study.md) |

## Review the project

Use the [ten-minute reviewer route](reviewer-guide.md) to inspect evidence,
then read the [design rationale](project-design.md) for implementation choices
and the [scientific scope](reference/scientific-scope.md) for boundaries.
