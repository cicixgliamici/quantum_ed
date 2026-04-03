# CHSH inequality (simulation-friendly)

A common way to demonstrate quantum non-locality is the **CHSH** inequality.

Define two measurement settings for Alice: \(A_0, A_1\)
and two for Bob: \(B_0, B_1\), each producing outcomes \(\pm 1\).

The CHSH expression is:
\[
S = E(A_0 B_0) + E(A_0 B_1) + E(A_1 B_0) - E(A_1 B_1)
\]

Classical (local hidden variable) models satisfy:
\[
|S| \le 2
\]

Quantum mechanics can reach up to:
\[
|S| \le 2\sqrt{2}
\]
(Tsirelson's bound)

In the notebooks we will compute correlations on the Bell state \(|\Phi^+\rangle\)
using Pauli observables and show a violation.
