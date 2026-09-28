# Ideal vs Noisy Execution: A Capability Study

In quantum computing education and software development, developers frequently transition between **ideal unitary simulators** and **noisy open-system models**. Understanding the fundamental mathematical and computational differences between these two simulation paradigms is essential for realistic hardware emulation.

This document examines:

1. The architectural trade-offs between **state-vector**, **density-matrix**, and **stochastic trajectory** simulators.
2. The **portability limit** of quantum noise semantics across software frameworks.
3. The repository's comparative study between pure NumPy and PennyLane's mixed-state engine.
4. The quantitative degradation of algorithm fidelity as circuit depth increases.

---

## 1. The Three Quantum Simulation Paradigms

Simulating quantum circuits on classical hardware is governed by distinct computational complexities:

| Simulation Paradigm | Mathematical Object | Memory Scaling ($n$ Qubits) | Simulates Noise? | Key Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **State-Vector Simulator** | Complex vector $|\psi\rangle \in \mathbb{C}^{2^n}$ | $2^n$ amplitudes ($16 \times 2^n$ bytes) | No (ideal unitaries only) | Fast algorithmic validation ($n \le 30$) |
| **Density-Matrix Simulator** | Hermitian matrix $\rho \in \mathbb{C}^{2^n \times 2^n}$ | $4^n$ entries ($16 \times 4^n$ bytes) | Yes (exact CPTP channels) | Small open systems ($n \le 15$) |
| **Stochastic Trajectory (Monte Carlo)** | Ensemble of state vectors $\{|\psi^{(s)}\rangle\}$ | $2^n$ amplitudes | Yes (stochastic quantum jumps) | Moderate-sized noisy circuits ($n \le 26$) |

### 1. State-Vector Simulation
State-vector simulators (such as Qiskit's `Statevector` or PennyLane's `default.qubit`) represent the quantum state as a column vector of length $2^n$. Applying a gate $U$ corresponds to matrix-vector multiplication $|\psi'\rangle = U|\psi\rangle$.
- **Limitation:** Cannot represent classical mixtures, subsystem decoherence, or non-unitary channels without artificially enlarging the Hilbert space.

### 2. Density-Matrix Simulation
Density-matrix simulators (such as PennyLane's `default.mixed` or Qiskit Aer's `density_matrix` method) track the full $2^n \times 2^n$ matrix $\rho$. A quantum channel $\mathcal{E}$ is simulated using the Kraus operator-sum representation:

$$
\rho' = \sum_k K_k \rho K_k^\dagger
$$

- **Limitation:** The memory requirement scales as $O(4^n) = O(2^{2n})$. Simulating 16 qubits requires $4^{16} \times 16\ \text{bytes} \approx 68.7\ \text{GB}$ of RAM, compared to only $1\ \text{MB}$ for state-vector simulation.

---

## 2. The Portability Limit of Quantum Noise Models

A critical observation documented in this repository's studies is the **portability limit**:

> **Circuit syntax (gates, wires, angles) can be fully standardized and portable (e.g. OpenQASM 3), but noise semantics remain vendor- and simulator-specific.**

- **Ideal Circuit Execution:** The statement `cx q[0], q[1];` has identical mathematical meaning ($|x, y\rangle \mapsto |x, x \oplus y\rangle$) across Qiskit, Q#, OpenQASM, and PennyLane.
- **Noisy Circuit Execution:** How noise is attached to that gate differs fundamentally:
  - In **Qiskit Aer**, noise is declared via a `NoiseModel` object associating a discrete CPTP channel with specific gate names and qubit pairings.
  - In **PennyLane**, noise is expressed directly inside the circuit as quantum operations (e.g. `qml.DepolarizingChannel(p, wires=0)`).
  - In **physical hardware**, noise is not a discrete map at all, but a time-continuous open-system Lindbladian generator $\dot{\rho} = -i[H(t), \rho] + \sum_k \mathcal{D}[L_k]\rho$ reflecting physical control pulses, crosstalk, and thermal bath coupling.

---

## 3. The Repository Showcase Study: Bit-Flip Noise

To demonstrate cross-ecosystem consistency on transparent primitives, the repository evaluates a parameterized **bit-flip noise channel** acting on the ground state $|0\rangle$:

### Theoretical Derivation

1. Start with the ground state:

$$
\rho_0 = |0\rangle\langle 0| = \begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}
$$

2. Apply a bit-flip channel with error probability $p \in [0, 1]$:

$$
\mathcal{E}_{\mathrm{BF}}(\rho) = (1-p)\rho + p X \rho X
$$

3. Compute the resulting density matrix:

$$
\mathcal{E}_{\mathrm{BF}}(\rho_0) = (1-p)\begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix} + p \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}\begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}\begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}
$$

$$
= (1-p)\begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix} + p \begin{bmatrix} 0 & 0 \\ 0 & 1 \end{bmatrix} = \begin{bmatrix} 1-p & 0 \\ 0 & p \end{bmatrix}
$$

4. Expected measurement probability of outcome $|1\rangle$:

$$
P(1) = \operatorname{Tr}(|1\rangle\langle 1| \rho') = \rho'_{11} = p
$$

The probability of observing an error is strictly linear in $p$.

### Cross-Framework Verification

Both the NumPy core and PennyLane's mixed-state simulator produce identical predictions:

```python
import numpy as np
import pennylane as qml
from quantum_ed.states import basis_0
from quantum_ed.density import rho_from_ket
from quantum_ed.channels import bit_flip_rho

p_val = 0.25

# 1. NumPy core implementation
rho_init = rho_from_ket(basis_0())
rho_noisy = bit_flip_rho(rho_init, p=p_val)
prob_numpy = float(np.real(rho_noisy[1, 1]))

# 2. PennyLane mixed-state simulator
dev = qml.device("default.mixed", wires=1)

@qml.qnode(dev)
def noisy_circuit(p):
    qml.BitFlip(p, wires=0)
    return qml.probs(wires=0)

probs_pennylane = noisy_circuit(p_val)
prob_pl = float(probs_pennylane[1])

print(f"NumPy P(1):     {prob_numpy:.4f}")
print(f"PennyLane P(1): {prob_pl:.4f}")
assert np.isclose(prob_numpy, prob_pl)
```

---

## 4. Impact of Noise on Circuit Depth

In realistic quantum algorithms, each gate layer introduces an incremental probability of error.

### Fidelity Decay Under Depolarizing Noise

Suppose an $n$-qubit circuit consists of $L$ sequential layers, where each layer introduces an average depolarizing error $p_{\mathrm{layer}}$. The fidelity with respect to the ideal target pure state decays exponentially:

$$
F(L) = \frac{1}{2^n} + \left( 1 - \frac{1}{2^n} \right) (1 - p_{\mathrm{layer}})^L
$$

- When $L = 0$: $F(0) = \frac{1}{2^n} + 1 - \frac{1}{2^n} = 1.0$ (perfect fidelity).
- As $L \to \infty$: $F(L) \to \frac{1}{2^n}$ (the state converges to the maximally mixed state $I/2^n$, pure white noise containing zero computational signal).

### The Quantum Volume & Coherent Depth Threshold

This exponential decay establishes a hard upper limit on the **coherent circuit depth**:

$$
L_{\mathrm{threshold}} \approx \frac{1}{p_{\mathrm{layer}}}
$$

For a current NISQ processor with average two-qubit gate error $p = 1\% = 0.01$, circuits deeper than $\sim 100$ entangling layers produce outputs indistinguishable from uniform random noise unless error mitigation or quantum error correction is applied.

---

## 5. Worked Exercises

### Exercise 1 — Memory Requirements for Density-Matrix Simulation
**Problem:**
Calculate the RAM required to store the state of a 20-qubit quantum register on:
1. An ideal state-vector simulator.
2. A density-matrix simulator.
Assume double-precision complex numbers (16 bytes per entry: 8 bytes real, 8 bytes imaginary).

**Solution:**
1. State-vector simulator ($2^n$ entries):
   - $N = 2^{20} = 1,048,576$ entries.
   - Memory = $1,048,576 \times 16\ \text{bytes} = 16,777,216\ \text{bytes} = 16\ \text{MB}$.
2. Density-matrix simulator ($4^n$ entries):
   - $N = 4^{20} = (2^{20})^2 = 1,099,511,627,776$ entries.
   - Memory = $4^{20} \times 16\ \text{bytes} \approx 1.76 \times 10^{13}\ \text{bytes} \approx 17.6\ \text{Terabytes}$ (TB) of RAM!
This dramatic difference demonstrates why density-matrix simulation is computationally restricted to small quantum registers ($n \le 14\text{--}15$).

---

### Exercise 2 — Readout Error vs Gate Error
**Problem:**
An experiment applies a single $X$ gate with error rate $p_{\mathrm{gate}} = 0.01$, followed by a measurement with symmetric readout error $\epsilon_{\mathrm{SPAM}} = 0.03$. Starting from $|0\rangle$, what is the total probability of observing outcome `0`?

**Solution:**
1. Ideal state after $X$: $|1\rangle$.
2. State after noisy gate:
   - True state is $|1\rangle$ with probability $1 - p_{\mathrm{gate}} = 0.99$.
   - True state is $|0\rangle$ with probability $p_{\mathrm{gate}} = 0.01$.
3. Outcome of noisy measurement:
   - If true state is $|1\rangle$, outcome is `0` with probability $\epsilon_{\mathrm{SPAM}} = 0.03$.
   - If true state is $|0\rangle$, outcome is `0` with probability $1 - \epsilon_{\mathrm{SPAM}} = 0.97$.
4. Total probability of measuring `0`:

$$
P(\text{measured } 0) = (0.99)(0.03) + (0.01)(0.97) = 0.0297 + 0.0097 = 0.0394 \quad (3.94\%)
$$

Notice that readout error ($\sim 3\%$) dominates over gate error ($\sim 1\%$), showing why readout error mitigation (REM) is a crucial post-processing step in NISQ experiments.

---

## 6. Next Steps

- [Noise & Quantum Channels](README.md) — explore mathematical formulations of Kraus operators
- [Fidelity & Trace Distance](FIDELITY.md) — deep dive into distance metrics for quantum states
- [Hardware Overview](../08-hardware/README.md) — physical origins of hardware decoherence
