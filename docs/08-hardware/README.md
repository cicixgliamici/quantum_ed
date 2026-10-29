# Quantum Hardware & Physical Qubits

## Learning guide

- **Prerequisites:** [circuits](../05-circuits-and-gates/README.md), [density matrices](../06-density-matrices/README.md), and [noise](../07-noise-and-channels/README.md).
- **Goals:** relate physical encodings to noise, routing, readout, and conditional resource estimates.
- **Runnable companion:** run the readout-model Python example below; its assumptions are stated beside the code.
- **Practice:** change the readout confusion probabilities and explain which observed distribution changes; identify which parameters would require hardware calibration.
- **References:** [scientific scope](../reference/scientific-scope.md) and the dated primary sources cited next to each hardware claim below.

## Overview

Hardware constrains how an ideal circuit is implemented: qubits lose coherence,
gates and readout are imperfect, interactions have limited connectivity, and
states can leak outside the computational subspace. This chapter separates
physical mechanisms, conditional estimates, and mathematical identities.

Numerical examples below are **illustrative assumptions**, not a comparison of
current commercial processors. Experimental values require a named device,
measurement protocol, operating conditions, and a dated source.

## 1. Requirements for physical quantum computing

[DiVincenzo (2000)](https://arxiv.org/abs/quant-ph/0002077) describes five
requirements for quantum computation:

1. Scalable, well-characterized qubits.
2. Initialization into a known fiducial state.
3. Relevant coherence times long compared with operation times.
4. A universal set of quantum gates.
5. Qubit-specific measurement.

Quantum communication adds interfaces between stationary and flying qubits,
and transmission of flying qubits. The criteria do not impose one universal
reset fidelity or one fixed ratio of coherence time to gate duration.

## 2. Physical encodings and engineering tradeoffs

| Modality | Encoding and control | Constraints to investigate |
| --- | --- | --- |
| Superconducting transmons | Anharmonic Josephson circuits, microwave control, coupled resonators | Cryogenic control, relaxation, dephasing, leakage, coupling layout |
| Trapped ions | Hyperfine, Zeeman, or optical states; laser or microwave control | Motional modes, addressing, transport, optical control, gate scheduling |
| Neutral atoms | Long-lived atomic states with Rydberg-mediated interactions | Atom loss, excitation errors, interaction range, motion and addressing |
| Photonics | Photons encoded in modes such as path or polarization | Loss, indistinguishability, source and detector efficiency, probabilistic operations |
| Semiconductor spins | Electron or hole spins in quantum dots or donor systems | Charge noise, control uniformity, exchange tuning, readout and interconnects |

Background sources are [Krantz et al. (2019)](https://arxiv.org/abs/1904.06560),
[Bruzewicz et al. (2019)](https://arxiv.org/abs/1904.04178),
[Saffman et al. (2009 preprint; 2010 review)](https://arxiv.org/abs/0909.4777),
[Rudolph (2016)](https://arxiv.org/abs/1607.08535), and
[Burkard et al. (2021 preprint)](https://arxiv.org/abs/2112.08863), respectively.
These are background descriptions, not a live performance ranking.

Several distinctions matter when reading a specification. Atomic ground-state
coherence is not the lifetime of a Rydberg excitation. An ion trap's environment
temperature is not an ion's motional temperature. Photon propagation does not
imply infinite coherence or instantaneous gates: loss, mode mismatch, delays,
and detection remain physical limitations. Connectivity within one ion chain
also does not imply unconstrained simultaneous entangling operations.

## 3. Coherence times describe a model, not a hard gate count

For a qubit with stationary exponential relaxation and independent exponential
pure dephasing, in a frame removing ideal phase rotation:

$$
\rho_{11}(t)=\rho_{11}(0)e^{-t/T_1},\qquad
\rho_{01}(t)=\rho_{01}(0)e^{-t/T_2},\qquad
\frac1{T_2}=\frac1{2T_1}+\frac1{T_\phi}.
$$

This zero-temperature relaxation model gives $T_2\le2T_1$. A nonexponential
Ramsey envelope, echo experiment, driven gate, or changing environment requires
its own model; fitted times should not be substituted indiscriminately.
See the coherence discussion in [Krantz et al.](https://arxiv.org/abs/1904.06560)
and the [channel definitions](../07-noise-and-channels/README.md).

Assume each sequential layer lasts $t_{\rm layer}$ and coherence follows the
same undriven exponential throughout. The remaining coherence contrast is:

$$
C(D)=\frac{|\rho_{01}(D t_{\rm layer})|}{|\rho_{01}(0)|}
=e^{-D t_{\rm layer}/T_2}.
$$

For an explicitly chosen contrast target $0<C_{\min}<1$:

$$
D\le-\frac{T_2}{t_{\rm layer}}\ln C_{\min}.
$$

**Example:** assume $T_2=100\,\mu\mathrm{s}$ and
$t_{\rm layer}=200\,\mathrm{ns}$. Their ratio is 500, an e-folding scale:
at 500 layers contrast is $e^{-1}\approx0.368$, rather than abruptly zero.
Requiring at least half the initial contrast allows at most
$\lfloor500\ln2\rfloor=346$ complete layers under these assumptions.
This is a coherence estimate, not circuit fidelity or a device-wide depth limit.

For example, the integer layer count can be reproduced with
`int(np.floor(-(100e-6 / 200e-9) * np.log(0.5)))` after importing NumPy.

## 4. Gate infidelity, state fidelity, and fault probabilities

| Quantity | Meaning |
| --- | --- |
| State fidelity with a pure target | $F_\psi=\langle\psi|\rho|\psi\rangle$ for one output state |
| Average gate fidelity | Average state overlap of an implemented channel with its target unitary over pure inputs |
| No-fault probability | Probability that no specified stochastic fault occurs in a chosen noise model |
| Task success probability | Probability of satisfying the algorithm's output criterion |

These quantities cannot generally be interchanged. For example, a stochastic
Z error on the input `0` leaves that state unchanged: state fidelity remains
one even though the no-fault probability is less than one.

For the particular d-dimensional depolarizing model
$\mathcal E_p(\rho)=(1-p)\rho+pI/d$, overlap with any pure input is
$1-p+p/d$, so average gate infidelity is $r=p(d-1)/d$. Thus even here r is
not p. General gate-fidelity definitions and their relation to entanglement
fidelity are given by [Nielsen (2002)](https://arxiv.org/abs/quant-ph/0205035).

### A conditional stochastic error budget

Assume independent faults, with specified probabilities $p_g$ per operation
and $p_q^{\rm readout}$ per measured bit. In this selected model:

$$
P_{\rm no\ fault}=\prod_g(1-p_g)\prod_q(1-p_q^{\rm readout}).
$$

It is not obtained by multiplying arbitrary reported average gate fidelities.
Faults may cancel, commute with the prepared state, or affect the task in
different ways; coherent and correlated errors need different treatment.

**Worked example:** assign fault probabilities 0.001 to each of 50 single-qubit
operations, 0.015 to each of 20 two-qubit operations, and 0.02 to each of four
readout bits. Preparation is assumed ideal. The exact product is:

$$
P_{\rm no\ fault}=0.999^{50}\,0.985^{20}\,0.98^4
\approx0.64849006.
$$

The three factors are approximately 0.95120563, 0.73913643, and 0.92236816.
The approximation $(1-p)^n\approx e^{-np}$ is useful only when its error is
acceptable; using it for the first two factors gives approximately 0.64998186,
not the exact product. This calculation estimates no-fault probability only.

Likewise, $0.99^{70}\approx0.49483866$ describes 70 independent 1% fault
opportunities in that model. It is not a general formula for algorithm fidelity.

## 5. Preparation, readout, crosstalk, and leakage

Preparation errors and measurement errors are often grouped as SPAM, but
calibration must specify which effects are included. Readout can be modeled
by a classical assignment matrix with columns summing to one:

$$
M_{ij}=P(\text{recorded }i\mid\text{prepared }j),\qquad
\mathbf p_{\rm observed}=M\mathbf p_{\rm true}.
$$

An invertible, stationary, accurately calibrated M permits the linear estimate
$\widehat{\mathbf p}_{\rm true}=M^{-1}\widehat{\mathbf p}_{\rm observed}$.
Finite samples can produce negative estimates and an ill-conditioned inverse
can amplify uncertainty. A constrained fit can impose physical probabilities;
readout correction does not repair state-preparation or gate errors.
For a practical treatment see [Bravyi et al. (2020)](https://arxiv.org/abs/2006.14044).

**Worked example:** with

$$
M=\begin{bmatrix}0.95&0.10\\0.05&0.90\end{bmatrix},\qquad
\mathbf p_{\rm observed}=\begin{bmatrix}0.60\\0.40\end{bmatrix},
$$

$\det M=0.85$ and the linear estimate is
$(0.50/0.85,0.35/0.85)^T\approx(0.58823529,0.41176471)^T$.
This uses a known assignment matrix and does not itself account for calibration
uncertainty or drift.

The arithmetic of these examples is executable:

```python
import numpy as np

# A selected independent stochastic model, not average gate fidelity.
no_fault_probability = 0.999**50 * 0.985**20 * 0.98**4
assert np.isclose(no_fault_probability, 0.64849006, atol=5e-9, rtol=0)

# A chosen half-contrast target for a stationary exponential envelope.
complete_layers = int(np.floor(-(100e-6 / 200e-9) * np.log(0.5)))
assert complete_layers == 346

# Solve rather than explicitly forming an inverse for numerical evaluation.
assignment_matrix = np.array([[0.95, 0.10], [0.05, 0.90]])
observed = np.array([0.60, 0.40])
estimated = np.linalg.solve(assignment_matrix, observed)
assert np.allclose(estimated, [10 / 17, 7 / 17], atol=1e-12, rtol=0)
assert np.allclose(assignment_matrix @ estimated, observed, atol=1e-12, rtol=0)
```

Crosstalk makes an operation depend on neighboring activity. Leakage populates
levels outside the designated qubit subspace; a two-level Pauli channel does
not represent it. Leakage handling can be incorporated into an error-correction
architecture, but requires mechanisms beyond simply assuming every fault is X,
Y, or Z within the qubit space.

## 6. Connectivity and a specific SWAP-routing construction

Consider a bidirectional linear chain, a CNOT between endpoints at graph
distance k edges, and the requirement to restore the initial mapping.
One valid construction moves the control along k-1 edges, applies the adjacent
CNOT, and reverses those moves. If each SWAP is decomposed into three CNOTs:

$$
N_{\rm SWAP}=2(k-1),\qquad
N_{\rm CNOT}=6(k-1)+1.
$$

Distance 1 requires one CNOT; distance 2 requires seven; distance 3 requires
13. For `q0-q1-q2-q3`, swap `q0,q1`, then `q1,q2`, apply `CX(q2,q3)`,
and undo the swaps in reverse order. The logical operation is `CX(q0,q3)`
and all original wire assignments are restored.

This is the cost of this construction, not a minimum over all compilers.
Bridge circuits, native entangling gates, direction constraints, changed final
layouts, or cancellations with neighboring operations can change it.
[SABRE](https://arxiv.org/abs/1809.02573) is one approach to optimizing mappings.

Under the independent 1% CNOT-fault model, the seven-CNOT example has no-fault
probability $0.99^7\approx0.93206535$. Calling this its effective gate fidelity
would add an assumption that the calculation does not justify.

## 7. NISQ, error correction, and conditional resource estimates

[Preskill (2018)](https://arxiv.org/abs/1801.00862) introduced NISQ to discuss
processors limited by noise before large-scale fault tolerance. It is a
historical framing, not a fixed modern qubit-count interval. A small phase
estimation circuit can also run without error correction; the challenge is
reliably scaling deep computations.

The threshold principle requires a specified noise model and fault-tolerant
construction. Surface-code thresholds depend on syndrome circuits, decoder,
noise bias, correlations, and leakage assumptions. A common subthreshold
scaling model for odd code distance d is:

$$
p_L\approx A\left(\frac p{p_{\rm th}}\right)^{(d+1)/2}.
$$

This is a model-dependent approximation, not a universal theorem with fixed A
or a universal numerical threshold. Code distance and target logical error rate
must accompany an overhead estimate. Data and syndrome ancillas grow roughly
as $O(d^2)$ per surface-code patch; routing space and state factories add costs.
See [Fowler et al. (2012)](https://arxiv.org/abs/1208.0928).

For RSA-2048 factoring, two dated proposals illustrate why a single physical
qubit count is misleading:

| Proposal | Conditional estimate | Source assumptions |
| --- | --- | --- |
| Gidney and Eker?, 2019 preprint | About 20 million physical qubits and eight hours | Nearest-neighbor grid, physical gate error 0.1%, 1 microsecond code cycles, 10 microsecond reaction time |
| Gidney, 2025 preprint | Fewer than one million noisy qubits and less than one week | The same stated timing/error assumptions, with different arithmetic, storage, and state-factory choices |

These are algorithm-and-architecture resource estimates, not demonstrations
or claims about available processors. The primary sources are
[Gidney and Eker?](https://arxiv.org/abs/1905.09749) and
[Gidney](https://arxiv.org/abs/2505.15917); their differing runtimes also matter.

## Next steps

- [Noise channels](../07-noise-and-channels/README.md): channel definitions and T1/T2 assumptions.
- [Fidelity and trace distance](../07-noise-and-channels/FIDELITY.md): state metrics and their conventions.
- [Bell-pair noise study](../07-noise-and-channels/bell-noise-study.md): a validated local-noise model.
- [Scientific scope](../reference/scientific-scope.md): source and approximation conventions.
