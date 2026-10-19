# Framework capability studies

Studies compare capabilities that do not map honestly to every programming
ecosystem. Unlike experiments, they are not required to provide equivalent
entrypoints for static circuit languages.

- [Bell-pair noise study](bell_noise/README.md) is the complete study: independent
  NumPy and PennyLane models, analytical predictions, entanglement metrics,
  reproducible figures, raw CSV data, and validation provenance.

- [Ideal versus noisy simulation](ideal-vs-noisy/README.md) compares the
  repository's density-matrix implementation with PennyLane `default.mixed`
  through a minimal single-qubit bit-flip baseline.
