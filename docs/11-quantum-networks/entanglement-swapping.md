# Entanglement swapping

Can Alice and Charlie share entanglement when their qubits have never directly
interacted? In the ideal model, Bob can connect two already shared Bell pairs
by a joint measurement on the two qubits he holds. Classical outcomes identify
which endpoint state was prepared and which correction to apply.

## 1. Four qubits across three nodes

Use tensor order **Alice, Bob-left, Bob-right, Charlie**, abbreviated
`A, B1, B2, C`. The two independent links are

$$
|\Psi_0\rangle = |\Phi^+\rangle_{AB_1}\otimes|\Phi^+\rangle_{B_2C},
\qquad |\Phi^+\rangle=\frac{|00\rangle+|11\rangle}{\sqrt 2}.
$$

```text
Alice          Bob                     Charlie
  A ---- Bell ---- B1     B2 ---- Bell ---- C
                  |       |
                  Bell measurement
                          |
                   two classical bits ----> correction on C
```

Bob applies CNOT from `B1` to `B2`, then H on `B1`, then measures both in the
computational basis. Label the result `zx`, with `z` from `B1` and `x` from
`B2`. This maps a Bell-basis measurement to ordinary readout.

## 2. Derive every outcome

Projecting onto Bob's outcome gives probability `1/4` in every branch. Up to
an irrelevant branch-global phase, the normalized endpoint state is

$$
|\chi_{zx}\rangle_{AC}=(I\otimes X^x Z^z)|\Phi^+\rangle_{AC}.
$$

Charlie applies X if `x=1`, followed by Z if `z=1`. Thus the total correction
matrix is `Z^z X^x`, since the rightmost operator acts first.

| Bob's result `zx` | Conditional endpoint state | Correction on Charlie |
| --- | --- | --- |
| `00` | Phi-plus: `(00 + 11)/sqrt(2)` | Identity |
| `01` | Psi-plus: `(01 + 10)/sqrt(2)` | X |
| `10` | Phi-minus: `(00 - 11)/sqrt(2)` | Z |
| `11` | Psi-minus: `(01 - 10)/sqrt(2)` | X followed by Z |

All four corrected endpoint density matrices equal the Phi-plus projector.
No branch is discarded. Conditional on the assumed two perfect links and a
complete ideal Bell measurement, the protocol succeeds for every outcome.
This does not assign unit success probability to a real photonic network.

## 3. What happens without the classical record?

Before correction, averaging over Bob's four outcomes gives

$$
\rho_{AC}^{\mathrm{unrecorded}}
=\frac14\sum_{z,x}|\chi_{zx}\rangle\langle\chi_{zx}|=\frac{I_4}{4}
=\frac{I_2}{2}\otimes\frac{I_2}{2}.
$$

That ensemble is separable, even though each conditional branch is a Bell
state. It also equals the endpoint density matrix before Bob's measurement.
His unannounced local measurement does not change it.

After outcome-dependent correction and averaging, the endpoint density matrix
is instead `|Phi+><Phi+|`. This requires the classical outcome to control the
correction. Alice's and Charlie's individual reduced states remain `I2/2` in
both cases. These distinctions prevent interpreting swapping as instantaneous
usable communication.

Computational-basis probabilities alone are insufficient: Phi-plus and
Phi-minus both give `P(00)=P(11)=1/2`. The validator checks the relative phase
inside every conditional branch, as well as its probability.

## 4. Execute and inspect

Install the package from the repository root with
`uv sync --locked --extra test --no-editable`, then run:

```python
import numpy as np
from quantum_ed.density import rho_from_ket
from quantum_ed.networks import OUTCOMES, conditional_endpoint_state, endpoint_density
from quantum_ed.states import bell_phi_plus

target = rho_from_ket(bell_phi_plus())
for outcome in OUTCOMES:
    probability, state = conditional_endpoint_state(outcome)
    assert np.isclose(probability, 0.25)
    assert np.allclose(rho_from_ket(state), target)

assert np.allclose(endpoint_density(), np.eye(4) / 4)
assert np.allclose(endpoint_density(corrected=True), target)
```

The [experiment README](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/entanglement-swapping/README.md)
links all five implementations. The network lesson in
[executed notebooks](../notebooks.md) displays a branch table and density-matrix
figures. [Core tests](https://github.com/cicixgliamici/quantum_ed/blob/main/tests/test_networks.py)
check raw states, corrected states, and reduced states;
[cross-ecosystem tests](https://github.com/cicixgliamici/quantum_ed/blob/main/tests/experiments/test_entanglement_swapping.py)
also reject omitted phase corrections and single-branch postselection.

## 5. Static circuits and physical interpretation

The SDK circuits use coherent controls from `B2` to C and `B1` to C in place
of mid-circuit readout and classical corrections. Deferring the measurement
reproduces the endpoint statistics and conditional states in an ideal
simulator. It does not provide a remote physical gate between nodes.

A physical realization requires readout, messaging, local corrections or a
tracked Pauli frame, and a timing model. These operations consume the
pre-established links. See [Hermans et al. (2022)](https://arxiv.org/abs/2110.11373)
for an experimental network using swapping, and
[repeaters and link budgets](repeaters-and-link-budgets.md) for assumptions that
the ideal circuit deliberately leaves out.

## Practice

1. Omit only the Z correction. Which branches keep the same computational-basis probabilities while having the wrong relative phase?
2. Retain only result `00`. What is the probability of that event, and why must fidelity be reported together with the selection probability?
3. Compare the local reduced states before and after feed-forward. Which joint observable distinguishes the two endpoint ensembles?
