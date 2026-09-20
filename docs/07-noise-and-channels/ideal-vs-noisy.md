# Ideal and noisy execution

An ideal circuit model applies only unitary gates and projective measurements.
A noisy simulator additionally evolves density matrices through quantum
channels. The distinction matters because hardware error is not represented by
adding another ideal gate.

The repository's [capability study](https://github.com/cicixgliamici/quantum_ed/tree/main/studies/ideal-vs-noisy)
compares the same bit-flip channel in the transparent NumPy core and PennyLane's
mixed-state simulator. Both predict $P(1)=p$ after applying flip probability
$p$ to $|0\rangle$.

This comparison also documents a portability limit: circuit syntax can be
portable while noise semantics remain simulator- and provider-specific.
