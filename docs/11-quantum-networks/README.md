# Quantum communication and networks

## Learning guide

- **Prerequisites:** [entanglement](../04-entanglement/README.md), [teleportation](../04-entanglement/quantum-teleportation.md), [density matrices](../06-density-matrices/README.md), and controlled gates.
- **Goals:** distinguish quantum links from classical control, explain entanglement swapping, and separate state quality from delivery probability.
- **Runnable companion:** the [swapping experiment](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/entanglement-swapping/README.md) and the network lesson in [executed notebooks](../notebooks.md).
- **Practice:** derive all four of Bob's outcomes and predict the endpoint state when his classical record is discarded.
- **References:** the dated primary sources below and the [validation protocol](../reference/experiment-validation.md).

## Overview

A quantum network connects devices that can prepare, transmit, store, or
process quantum states. Its resources include quantum links and shared
entanglement, alongside classical communication. The long-term quantum-internet
vision includes connecting quantum processors; the development stages in
[Wehner, Elkouss, and Hanson (2018)](https://doi.org/10.1126/science.aam9288)
provide a useful framework, rather than a claim that every capability is
already deployed.

## 1. Network components

| Component | Role in a network | Question to ask |
| --- | --- | --- |
| Stationary qubit or memory | Holds a state while other operations complete | How long does useful coherence survive? |
| Flying qubit, often a photon | Connects separated devices | What are the transmission and detection probabilities? |
| Entanglement-generation interface | Creates a shared resource between nodes | How is success announced and what state is produced? |
| Local processor | Performs gates, measurements, and corrections | Which operations are available and how accurately? |
| Classical channel | Carries announcements, outcomes, and control messages | What latency and authentication assumptions apply? |

Keep physical transmission, successful detection, and the conditional state
after detection distinct. A protocol description must specify which events
are retained and how they are announced.

## 2. Protocols and resource accounting

| Protocol | Required resource | Classical communication | Result in the ideal model |
| --- | --- | --- | --- |
| [Teleportation](../04-entanglement/quantum-teleportation.md) | One shared Bell pair and one input qubit | Two measurement bits | Transfer of the input state |
| [Superdense coding](../04-entanglement/superdense-coding.md) | One shared Bell pair and physical transmission of one qubit | No additional correction message in the elementary protocol | Two classical message bits decoded |
| [Entanglement swapping](entanglement-swapping.md) | Two Bell pairs meeting at a node holding two qubits | Two Bell-measurement outcome bits for a chosen endpoint correction | A Bell pair between the outer nodes |

The Bell pairs in this table are resources to create and consume. Their
availability is an assumption in the circuit examples, not a free network
service or a measurement of transmission performance.

## 3. Why classical communication remains necessary

Teleportation transfers a quantum state using shared entanglement and classical
outcomes. It does not copy the input. Swapping similarly produces different
conditional endpoint states for different measurement outcomes. Those states
cannot all be interpreted as the same corrected resource before the outcome
is available. See the [complete branch calculation](entanglement-swapping.md).

An unknown state also cannot generally be copied for classical-style
amplification. If a unitary cloned arbitrary states, preservation of inner
products would require

$$
\langle\psi|\phi\rangle = \langle\psi|\phi\rangle^2,
$$

which fails for nonorthogonal distinct states. This motivates quantum-network
strategies built around state transfer, entanglement distribution, and error
handling, rather than copying an arbitrary incoming qubit.

## 4. Repeaters and the role of memory

The repeater proposal of
[Briegel et al. (1998)](https://arxiv.org/abs/quant-ph/9803056) combines shorter
entangled links and nested purification. Swapping is one building block;
a complete system must also handle unsuccessful attempts and imperfect
operations. Read [repeaters and link budgets](repeaters-and-link-budgets.md)
for the assumptions behind simple loss and waiting-time models.

The current implementation covers ideal swapping. It does not implement
repeater scheduling, purification, lossy photonic measurements, or noisy
quantum memories.

## 5. QKD and other applications

Quantum key distribution establishes classical secret keys under a specified
security model, using quantum communication and an authenticated classical
channel. It is one application of quantum communication; a successful key
exchange alone does not demonstrate general transfer of quantum states between
networked processors. Practical security depends on protocol and device
assumptions; see [Scarani et al. (2009)](https://arxiv.org/abs/0802.4155).

QKD is introduced here as context. This repository does not implement a QKD
protocol, finite-key analysis, or a security proof. Other motivations include
distributed quantum computation and sensing, whose resource requirements go
beyond the ideal swapping circuit.

## 6. Experimental context and project scope

[Hermans et al. (2022)](https://doi.org/10.1038/s41586-022-04697-y)
demonstrated teleportation between non-neighbouring nodes in a three-node
network, using swapping and a memory qubit to prepare the remote resource.
An [open author preprint](https://arxiv.org/abs/2110.11373) describes the experiment.
This is experimental context, not a hardware result reproduced by our simulator.

Our [experiment](entanglement-swapping.md) starts with two perfect Bell pairs,
performs ideal local operations, and validates every measurement branch.
The notebook exposes the states and resulting density matrices. The main
lesson is the distinction between a conditional entangled state, the ensemble
without its classical record, and a corrected resource shared by the endpoints.

## Continue

- [Entanglement swapping](entanglement-swapping.md): derivation, corrections, and executable evidence.
- [Repeaters and link budgets](repeaters-and-link-budgets.md): loss, memory, and performance boundaries.
- [Bell-pair noise study](../07-noise-and-channels/bell-noise-study.md): validated channel models for a possible future extension.
