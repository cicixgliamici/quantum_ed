# Measurement

## Born rule (projective measurement in computational basis)
Given \(|\psi\rangle = \alpha|0\rangle + \beta|1\rangle\), measuring in the \(|0\rangle,|1\rangle\) basis yields:

- outcome 0 with probability \(|\alpha|^2\)
- outcome 1 with probability \(|\beta|^2\)

After measuring, the state collapses to the corresponding basis vector.

## Measurement operators
Projectors:
\[
P_0 = |0\rangle\langle 0|,\quad P_1 = |1\rangle\langle 1|
\]
Probability:
\[
p(i)=\langle \psi|P_i|\psi\rangle
\]
Post-measurement state:
\[
|\psi'\rangle = \frac{P_i|\psi\rangle}{\sqrt{p(i)}}
\]
