# Repeaters and link budgets

The [swapping example](entanglement-swapping.md) assumes two perfect links
already exist. A network model must explain how they become available, what
counts as success, and how waiting affects stored states. This page defines
simple analytical models for that next step; they are not implemented network
benchmarks.

## 1. Loss and conditional state quality

For a toy fibre model with length `L` in kilometres and attenuation coefficient
`alpha` in dB/km, define transmissivity by

$$
\eta(L)=10^{-\alpha L/10}.
$$

This is the decibel conversion for the chosen loss-only model. Coupling,
conversion, detection, dark counts, source statistics, and the geometry of
the entanglement-generation protocol require additional parameters. No
particular `alpha` is assumed to describe all deployed fibres.

Attenuation and decoherence answer different questions. In an ideal erasure-only
model, a successful arrival can preserve the encoded state while becoming
less frequent with distance. Averaging a conditional fidelity without reporting
how often its condition occurs hides that cost.

## 2. A deliberately limited success-probability model

Suppose two elementary links are attempted independently in the same round,
without storing earlier successes. Let `p_AB` and `p_BC` be their success
probabilities and let `p_BSM` be the conditional success probability of the
middle-node Bell measurement. Then

$$
p_{\mathrm{round}}=p_{AB}p_{BC}p_{\mathrm{BSM}}.
$$

With independent rounds launched at a stated rate `r_attempt`, and no extra
dead time, the mean delivery rate in this toy model is
`r_attempt * p_round`. Once successful links can be stored while waiting for
another, this same-round product no longer describes the full protocol.
Scheduling, reset time, classical latency, and memory lifetime must then be
specified. Splitting a link alone does not establish a repeater advantage.

## 3. Why repeaters require more than swapping

[Briegel et al. (1998)](https://arxiv.org/abs/quant-ph/9803056)
proposed a repeater architecture using shorter entangled links and nested
purification. A network analysis must account for the resources and errors
of the chosen repeater protocol. Our circuit implements one ideal swapping
step; it does not implement purification, fault-tolerant repeaters, or
asynchronous link generation.

For a separate pure-dephasing memory model, one could assume an off-diagonal
decay factor `exp(-t/T2)` during a storage interval `t`. This is a stipulated
single-process model, not a universal memory characterization. Relaxation,
control errors, and parameter conventions must be added explicitly; consult
[noise and channels](../07-noise-and-channels/README.md).

## 4. What to report in a future study

| Quantity | Definition to state |
| --- | --- |
| Conditional fidelity | Target state, accepted events, and density matrix conditioned on them |
| Success probability | Trial definition and all discarded events |
| Delivery rate | Time per trial, latency, reset overhead, and memory policy |
| Storage cost | Number of memories, waiting-time distribution, and noise model |
| Numerical evidence | Independent references, tolerances, seeds, and environment versions |

An extension can reuse the project's
[Bell-noise conventions](../07-noise-and-channels/bell-noise-study.md), but it
needs a new model of link attempts and memory waiting. The existing noise
study does not establish a network transmission rate.

## Practice

If `p_AB=p_BC=0.2` and an ideal measurement always succeeds once both links
exist, the same-round success probability is `0.04`. Explain why this number
alone does not determine deliveries per second. Then identify which new
variables are needed if Bob can store one successful link.
