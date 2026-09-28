# Quantum Hardware & Physical Qubits

In theoretical quantum information, quantum algorithms are expressed in terms of ideal state vectors, arbitrary unitary operators, and all-to-all connectivity. In reality, a quantum processor is a delicate physical apparatus operating at the boundaries of experimental physics and nanotechnology.

A physical quantum computer is subject to:

- **Finite coherence times** ($T_1, T_2$)
- **Imperfect gate control** and control pulse distortions
- **Readout (SPAM) infidelities**
- **Topological connectivity constraints** on coupling graphs
- **Crosstalk and leakage** outside the two-level computational subspace

Understanding these hardware realities is essential for designing efficient quantum algorithms, optimizing circuit transpilation, and planning the transition from the NISQ era to Fault-Tolerant Quantum Computing (FTQC).

---

## 1. The DiVincenzo Criteria

In 1996 and 2000, theoretical physicist David DiVincenzo formulated the five necessary criteria that any physical system must satisfy to implement a viable quantum computer:

1. **A scalable physical system with well-characterized qubits:**
   The physical two-level quantum system must be precisely defined, with clear energy levels $\{|0\rangle, |1\rangle\}$ isolated from higher excited states, and capable of scaling to large numbers of qubits.
2. **The ability to initialize the state of the qubits to a simple fiducial state:**
   The register must be quickly and reliably initialized into a known fiducial state (typically $|00\dots 0\rangle$) with high fidelity ($>99.9\%$), either through active reset or thermal equilibration.
3. **Long relevant decoherence times, much longer than gate operation times:**
   The system must satisfy:

$$
\frac{T_1, T_2}{t_{\mathrm{gate}}} \gg 10^3\text{--}10^4
$$

   allowing thousands of coherent gate operations before environmental noise randomizes quantum phases.
4. **A universal set of quantum gates:**
   The hardware must support arbitrary single-qubit rotations and an entangling two-qubit gate (such as CNOT, CZ, or iSWAP) to synthesize any unitary transformation.
5. **A qubit-specific measurement capability:**
   The processor must measure individual qubits in the computational basis with high quantum efficiency and low cross-talk, without destroying or disturbing unmeasured qubits.

*(Two additional criteria apply to quantum communication: the ability to interconvert stationary and flying qubits, and the ability to faithfully transmit flying qubits between distant nodes).*

---

## 2. Leading Physical Qubit Modalities

Several physical implementations are actively pursued, each representing distinct engineering tradeoffs between gate speed, coherence duration, fidelity, and manufacturing maturity.

| Qubit Modality | Physical Carrier | 1-Qubit Gate Time | 2-Qubit Gate Time | Coherence $T_2$ | 2-Qubit Fidelity | Native Connectivity | Operating Temp |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Superconducting (Transmon)** | Josephson junction non-linear LC oscillator | $10\text{--}30\ \text{ns}$ | $50\text{--}200\ \text{ns}$ | $50\text{--}300\ \mu\text{s}$ | $99.0\text{--}99.8\%$ | Nearest-neighbor (planar grid) | $\sim 15\ \text{mK}$ |
| **Trapped Ions** | Hyperfine states of ions ($^{171}\text{Yb}^+, ^{40}\text{Ca}^+$) | $1\text{--}10\ \mu\text{s}$ | $50\text{--}200\ \mu\text{s}$ | $1\text{--}10\ \text{s}$ | $99.5\text{--}99.9\%$ | All-to-all (within trap) | Room / $4\ \text{K}$ |
| **Neutral Atoms** | Rydberg states in optical tweezer arrays | $10\text{--}50\ \text{ns}$ | $100\text{--}400\ \text{ns}$ | $1\text{--}5\ \text{s}$ | $99.0\text{--}99.5\%$ | Reconfigurable 2D/3D | Ultra-cold ($\sim \mu\text{K}$) |
| **Photonics** | Single photons in spatial/polarization modes | Instantaneous | Probabilistic / Fusion | $\infty$ (flying) | Variable | Reconfigurable waveguides | Room temp (detectors at $4\ \text{K}$) |
| **Silicon Spin** | Electron/hole spins in semiconductor quantum dots | $10\text{--}50\ \text{ns}$ | $50\text{--}200\ \text{ns}$ | $1\text{--}10\ \text{ms}$ | $98.0\text{--}99.5\%$ | Nearest-neighbor | $\sim 1\ \text{K}$ |

### 1. Superconducting Transmon Qubits
- **Operating Principle:** An LC circuit where the classical inductor is replaced by a **Josephson junction** (a thin insulating barrier between two superconducting aluminum layers). The non-linear Josephson inductance creates an anharmonic potential, separating the transition frequency $\omega_{01}$ from $\omega_{12}$ by an anharmonicity $\Delta = \omega_{12} - \omega_{01} \approx -200\text{ to } -350\ \text{MHz}$. This isolates the $\{|0\rangle, |1\rangle\}$ subspace.
- **Strengths:** Fast gate speeds ($10\text{--}100\ \text{ns}$), fabricated using established solid-state lithography, mature microwave engineering.
- **Challenges:** Requires dilution refrigerators ($\sim 15\ \text{mK}$), cryogenic microwave coaxial wiring bottlenecks, planar connectivity limitations, and material two-level system (TLS) defects.

### 2. Trapped Ion Qubits
- **Operating Principle:** Individual atomic ions are levitated in ultra-high vacuum using radio-frequency Paul traps. Qubits are encoded in stable electronic hyperfine ground states and addressed with focused laser beams. Two-qubit entangling gates are mediated by Coulomb repulsion (shared motional phonon modes, e.g. Mølmer-Sørensen gate).
- **Strengths:** Natural, identical quantum emitters (zero manufacturing variance), exceptional coherence times ($T_2 > 1\ \text{s}$), highest recorded 2-qubit gate fidelities ($>99.9\%$), and full all-to-all connectivity within a single trap.
- **Challenges:** Slower gate speeds ($10\text{--}100\ \mu\text{s}$), optical control scaling, laser phase noise, and limits on ion chain length before motional modes become crowded.

### 3. Neutral Atom Qubits (Rydberg Arrays)
- **Operating Principle:** Hundreds of individual neutral atoms are held in arbitrary 2D/3D configurations using optical tweezers (tightly focused laser beams). Laser excitation to high-lying **Rydberg states** (principal quantum number $n \approx 50\text{--}100$) induces a massive electric dipole moment, creating a **Rydberg blockade** that prevents simultaneous excitation of neighboring atoms within a blockade radius $R_b \approx 5\text{--}10\ \mu\text{m}$, directly implementing entangling gates.
- **Strengths:** Rapidly scalable to thousands of qubits in clean optical lattices, dynamically reconfigurable connectivity via physical atom shuttling during circuit execution.
- **Challenges:** Finite trap vacuum lifetime (atoms occasionally lost), optical intensity noise, finite Rydberg lifetime.

---

## 3. Hardware Error Budgeting

In any quantum algorithm, total circuit error is a composite sum of distinct physical error channels:

$$
\epsilon_{\mathrm{circuit}} \approx 1 - \prod_{g \in \text{gates}} (1 - \epsilon_g) \prod_{q \in \text{qubits}} (1 - \epsilon_{\mathrm{SPAM}})
$$

### Single-Qubit vs Two-Qubit Gate Bottlenecks

- **Single-Qubit Gate Error ($\epsilon_{1Q} \sim 10^{-4}\text{--}10^{-3}$):** Fast pulses (e.g. $20\ \text{ns}$ microwave drive) with low error.
- **Two-Qubit Gate Error ($\epsilon_{2Q} \sim 10^{-2}\text{--}10^{-3}$):** The dominant error source in modern processors. Because entangling gates require physical interaction between qubits, they take $5\times$ to $20\times$ longer than single-qubit gates, exposing both qubits to environmental decoherence ($T_1, T_2$) during the operation.

### Coherence-Limited Circuit Depth

The maximum number of coherent gate layers $D_{\max}$ a device can sustain before quantum information is destroyed by dephasing is bounded by:

$$
D_{\max} \le \frac{T_2}{t_{\mathrm{gate}}}
$$

For a typical superconducting transmon with $T_2 = 100\ \mu\text{s}$ and two-qubit gate duration $t_{2Q} = 200\ \text{ns}$:

$$
D_{\max} \le \frac{100\ \mu\text{s}}{0.2\ \mu\text{s}} = 500\ \text{layers}
$$

In practice, because gate infidelities ($\epsilon_{2Q} \approx 1\%$) accumulate exponentially, circuit fidelity drops below $50\%$ after only $\sim 70$ two-qubit gates without error correction:

$$
F_{\mathrm{alg}} \approx (1 - 0.01)^{70} \approx 0.494
$$

### SPAM Errors (State Preparation and Measurement)

Even if a circuit executes flawlessly, measurement results can be corrupted:

- **State Preparation Infidelity:** Residual thermal excitations leave a small fraction of qubits in state $|1\rangle$ instead of $|0\rangle$ during reset.
- **Readout Infidelity:** Dispersive readout (measuring microwave transmission shift through a coupled resonator) has finite signal-to-noise ratio (SNR), leading to misclassification:
  - $P(1|0)$: probability of measuring $|1\rangle$ when the state was $|0\rangle$.
  - $P(0|1)$: probability of measuring $|0\rangle$ when the state was $|1\rangle$.

#### Readout Error Mitigation (REM)

Readout error can be partially corrected via calibration. Experimentally measure the **confusion matrix** $M$:

$$
M = \begin{bmatrix} P(0|0) & P(0|1) \\ P(1|0) & P(1|1) \end{bmatrix}
$$

Given the observed noisy probability distribution $\vec{P}_{\mathrm{meas}}$, the mitigated ideal distribution $\vec{P}_{\mathrm{ideal}}$ is obtained by matrix inversion:

$$
\vec{P}_{\mathrm{ideal}} = M^{-1} \vec{P}_{\mathrm{meas}}
$$

### Crosstalk and Leakage

1. **Crosstalk:** Applying microwave control tones to drive qubit $A$ induces stray electromagnetic fields that weakly drive neighboring qubit $B$, shifting its transition frequency or rotating its state.
2. **Subspace Leakage:** The transmon is not a perfect two-level system; it is an anharmonic oscillator with higher excited states $|2\rangle, |3\rangle, \dots$. Strong, fast microwave pulses have finite frequency bandwidth that can drive transitions $|1\rangle \to |2\rangle$. Once leaked, the state falls outside the computational basis and standard quantum error correction codes cannot directly correct it.

---

## 4. Connectivity Constraints and SWAP Routing

In quantum algorithms (e.g. Quantum Fourier Transform, Quantum Phase Estimation), gates are often required between arbitrary pairs of qubits $(q_i, q_j)$. However, solid-state quantum processors have fixed, localized coupling graphs.

```text
Linear Chain:       q₀ --- q₁ --- q₂ --- q₃

Heavy-Hex (IBM):    q₀ --- q₁ --- q₂
                           |
                          q₃
                           |
                    q₄ --- q₅ --- q₆
```

### The Cost of Non-Adjacent Gates

If an algorithm requires a $\mathrm{CNOT}(q_0 \to q_2)$ on a linear chain where $q_0$ and $q_2$ are not directly connected:

1. A $\mathrm{SWAP}$ gate must be inserted between $q_1$ and $q_2$ to bring the states adjacent.
2. The $\mathrm{CNOT}$ is executed between $q_0$ and the new position.
3. Another $\mathrm{SWAP}$ is executed to restore the original qubit layout.

$$
\mathrm{CNOT}(q_0 \to q_2) \implies \mathrm{SWAP}(q_1, q_2)\ \mathrm{CNOT}(q_0 \to q_1)\ \mathrm{SWAP}(q_1, q_2)
$$

Since each $\mathrm{SWAP}$ decomposes into three CNOTs:

$$
\mathrm{SWAP} = \mathrm{CNOT}_{0\to 1}\ \mathrm{CNOT}_{1\to 0}\ \mathrm{CNOT}_{0\to 1}
$$

A single non-adjacent $\mathrm{CNOT}$ across distance 2 requires:

$$
3 + 1 + 3 = 7\ \text{physical CNOT gates!}
$$

### Impact on Algorithm Fidelity

If each physical CNOT has fidelity $F_{\mathrm{CNOT}} = 99\%$, the effective fidelity of that single non-adjacent two-qubit gate drops to:

$$
F_{\mathrm{effective}} = (0.99)^7 \approx 93.2\%
$$

This drastic overhead underscores why **hardware-aware circuit transpilation and routing** (e.g. SABRE heuristic routing in Qiskit) is a primary focus of quantum compiler research.

---

## 5. From NISQ to Fault-Tolerant Quantum Computing (FTQC)

John Preskill coined the term **NISQ (Noisy Intermediate-Scale Quantum)** in 2018 to describe current quantum computers:

- **50 to 1,000 physical qubits**
- **No quantum error correction (QEC)**
- Limited circuit depth ($\sim 20\text{--}100$ entangling layers)
- Algorithms designed for this regime: **VQE** (Variational Quantum Eigensolver) and **QAOA** (Quantum Approximate Optimization Algorithm), which use shallow parameterised circuits and classical optimization loops.

### The Threshold Theorem & Logical Qubits

To execute deep algorithms like Shor's factoring or full-scale quantum chemistry simulations, we must transition to **Fault-Tolerant Quantum Computing (FTQC)**.

- **The Quantum Threshold Theorem:**
  If the physical error rate per gate $\epsilon$ falls below a rigorous threshold ($\epsilon < \epsilon_{\mathrm{th}} \approx 10^{-2}$ to $10^{-3}$ for surface codes), quantum error correction can suppress logical error rates exponentially with code distance $d$:

$$
P_{\mathrm{logical}} \propto \left( \frac{\epsilon}{\epsilon_{\mathrm{th}}} \right)^{\frac{d+1}{2}}
$$

- **Physical to Logical Qubit Overhead:**
  Encoding a single fault-tolerant **logical qubit** in a surface code typically requires $100$ to $1,000$ physical data and ancilla qubits.
- A full-scale Shor algorithm capable of factoring RSA-2048 keys requires $\approx 4,000$ logical qubits, translating to roughly **$1\text{--}4$ million physical qubits** with current error rates.

---

## 6. Worked Study Problems

### Problem 1 — Estimating Circuit Fidelity
**Problem:**
A quantum circuit contains 50 single-qubit gates and 20 two-qubit CNOT gates, followed by measurement on 4 qubits.
Assume average gate error rates:
- $\epsilon_{1Q} = 0.001$ ($99.9\%$ fidelity)
- $\epsilon_{2Q} = 0.015$ ($98.5\%$ fidelity)
- Measurement readout error $\epsilon_{\mathrm{SPAM}} = 0.02$ ($98\%$ fidelity per qubit)

Estimate the overall circuit success probability $F_{\mathrm{circuit}}$.

**Solution:**
Assuming independent, uncorrelated errors:

$$
F_{\mathrm{circuit}} \approx (1 - \epsilon_{1Q})^{50} \times (1 - \epsilon_{2Q})^{20} \times (1 - \epsilon_{\mathrm{SPAM}})^4
$$

$$
(1 - 0.001)^{50} \approx e^{-0.05} \approx 0.9512
$$

$$
(1 - 0.015)^{20} \approx e^{-0.30} \approx 0.7386
$$

$$
(1 - 0.02)^4 \approx 0.9224
$$

Multiplying the components:

$$
F_{\mathrm{circuit}} \approx 0.9512 \times 0.7386 \times 0.9224 \approx 0.6480 \quad (64.8\%)
$$

Notice that the two-qubit gate errors account for the overwhelming majority of the fidelity loss ($26.1\%$ drop).

---

### Problem 2 — Readout Confusion Inversion
**Problem:**
A single qubit is measured 10,000 times. The raw counts are 6,000 zeros and 4,000 ones ($\vec{P}_{\mathrm{meas}} = [0.60, 0.40]^T$).
A calibration experiment reveals the confusion matrix:

$$
M = \begin{bmatrix} P(0|0) & P(0|1) \\ P(1|0) & P(1|1) \end{bmatrix} = \begin{bmatrix} 0.95 & 0.10 \\ 0.05 & 0.90 \end{bmatrix}
$$

Calculate the error-mitigated probabilities $\vec{P}_{\mathrm{ideal}}$.

**Solution:**
Compute the determinant of $M$:

$$
\det(M) = (0.95)(0.90) - (0.10)(0.05) = 0.855 - 0.005 = 0.850
$$

The inverse matrix $M^{-1}$ is:

$$
M^{-1} = \frac{1}{0.850} \begin{bmatrix} 0.90 & -0.10 \\ -0.05 & 0.95 \end{bmatrix}
$$

Multiply $M^{-1}$ by $\vec{P}_{\mathrm{meas}}$:

$$
\vec{P}_{\mathrm{ideal}} = \frac{1}{0.850} \begin{bmatrix} (0.90)(0.60) - (0.10)(0.40) \\ (-0.05)(0.60) + (0.95)(0.40) \end{bmatrix} = \frac{1}{0.850} \begin{bmatrix} 0.54 - 0.04 \\ -0.03 + 0.38 \end{bmatrix} = \frac{1}{0.850} \begin{bmatrix} 0.50 \\ 0.35 \end{bmatrix}
$$

$$
P_{\mathrm{ideal}}(0) = \frac{0.50}{0.85} \approx 0.5882, \quad P_{\mathrm{ideal}}(1) = \frac{0.35}{0.85} \approx 0.4118
$$

Readout mitigation adjusted the ground state probability from $60.0\%$ to $58.8\%$, correcting for asymmetric readout bias.

---

### Problem 3 — Routing Overhead on a Line Architecture
**Problem:**
Four qubits $q_0, q_1, q_2, q_3$ are arranged in a linear topology: $q_0 - q_1 - q_2 - q_3$.
An algorithm requires a two-qubit gate between $q_0$ and $q_3$.
How many additional SWAP gates and equivalent CNOT gates are required to execute this operation and restore the initial layout?

**Solution:**
To make $q_0$ and $q_3$ adjacent:
1. SWAP $q_0$ with $q_1$: register is $[q_1, q_0, q_2, q_3]$ (1 SWAP)
2. SWAP $q_0$ with $q_2$: register is $[q_1, q_2, q_0, q_3]$ (1 SWAP)
$q_0$ and $q_3$ are now adjacent! Execute the target two-qubit gate (1 CNOT).
3. Reverse routing: SWAP $q_0$ with $q_2$, then SWAP $q_0$ with $q_1$ (2 SWAPs).

Total overhead:
- Total SWAP gates required: $2 + 2 = 4\ \text{SWAP}$ gates.
- Since each SWAP contains 3 CNOTs: $4 \times 3 = 12\ \text{additional CNOT gates}$.
- Total two-qubit gates executed: $12 + 1 = 13\ \text{CNOTs}$.
- Distance $k = 3$ on a line imposes a $13\times$ two-qubit cost multiplier ($4(k-1) + 1$).

---

## 7. Next Steps

- [Noise & Quantum Channels](../07-noise-and-channels/README.md) — explore mathematical descriptions of $T_1$ and $T_2$ noise
- [Ideal vs Noisy Execution](../07-noise-and-channels/ideal-vs-noisy.md) — see how circuit depth degrades simulated algorithm outputs
- [Quantum Algorithms](../10-quantum-algorithms/README.md) — discover how algorithm design adapts to hardware reality
