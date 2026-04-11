# Hardware Overview

Quantum computing is not only about abstract states and matrices.

Real devices are physical systems, and their behavior is constrained by noise, control precision, connectivity, and measurement limitations.

This chapter gives a compact conceptual overview of the hardware side.

---

## 1. Why hardware matters

In theory, we often describe quantum systems with ideal states and ideal gates.

In practice, every implementation is affected by:

- decoherence
- imperfect control
- imperfect readout
- architectural constraints

That is why hardware is not a secondary detail.

Hardware determines what kinds of circuits are feasible, how long they can run, and how reliable the output can be.

---

## 2. What a physical qubit is

A physical qubit is a real system whose dynamics can be controlled so that two quantum states behave like the logical basis states $|0\rangle$ and $|1\rangle$.

Examples include:

- superconducting circuits
- trapped ions
- photons

The abstract qubit from linear algebra is the mathematical model.

The physical qubit is the real-world system that tries to realize that model.

---

## 3. T1 and T2

Two of the most important timescales in quantum hardware are:

- **T1** — relaxation time
- **T2** — coherence or dephasing time

### T1
T1 measures how quickly an excited state tends to decay toward the ground state.

This is related to energy loss.

### T2
T2 measures how quickly phase information is lost.

This is related to decoherence.

In practice, both times limit how much computation can be performed before noise dominates.

---

## 4. Gate times and error rates

A quantum gate is never perfectly instantaneous or perfectly exact.

Two key questions are:

- how long does the gate take?
- how often does it fail or deviate from the ideal unitary?

Shorter gates can help reduce exposure to decoherence, but control complexity and noise still matter.

A realistic processor is judged not only by whether it supports certain gates, but by how accurately and reliably those gates can be applied.

---

## 5. Readout

At the end of a computation, the qubits must be measured.

Real measurement is not perfect.

Readout errors can arise because:

- the device misidentifies the state
- the signal is noisy
- the measurement process itself is imperfect

So even if the quantum evolution were ideal, the final classical output could still be wrong.

---

## 6. Connectivity

In the abstract circuit model, we often imagine that any qubit can interact with any other qubit.

Real hardware usually has limited connectivity.

This means:

- only certain pairs of qubits can directly interact
- extra swap operations may be needed
- circuit compilation becomes hardware-dependent

Connectivity is one of the main ways architecture influences algorithm performance.

---

## 7. Main hardware platforms

### Superconducting qubits

Superconducting qubits, especially transmon-style devices, are among the most widely used current platforms.

Typical features:

- fast gate times
- strong engineering momentum
- significant sensitivity to noise and calibration issues

These systems are often associated with chip-based architectures and nearest-neighbor connectivity patterns.

### Trapped ions

Trapped-ion platforms encode qubits in ions manipulated by electromagnetic fields and laser control.

Typical features:

- very high gate fidelity
- long coherence times
- slower gate operations compared with some superconducting systems

They are often attractive for precision and control.

### Photonics

Photonic approaches use photons as carriers of quantum information.

Typical features:

- low interaction with the environment
- natural compatibility with communication settings
- significant engineering challenges for scalable interactions and gates

Photonics is especially important in quantum communication and network-oriented settings.

---

## 8. Relation to the rest of the repo

This repository starts from the mathematical model:

- vectors
- gates
- measurement
- density matrices
- noise channels

The hardware perspective explains **why** those later topics matter.

For example:

- dephasing is linked to loss of coherence
- relaxation is linked to energy decay
- noisy channels reflect imperfect physical operations
- circuit depth matters because coherence time is limited

So the hardware chapter connects the abstract formalism to real implementation constraints.

---

## 9. Key intuition

A quantum algorithm is never run in an abstract vacuum.

It runs on a physical device with finite coherence, imperfect gates, imperfect readout, and architectural constraints.

That is why the study of quantum computing naturally connects:

- mathematics
- information theory
- software tooling
- hardware engineering

---

## Next

- `docs/06-noise-and-channels/README.md`
- `docs/07-density-matrices/README.md`
