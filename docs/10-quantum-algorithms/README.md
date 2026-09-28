# Quantum Algorithms

Quantum algorithms exploit the uniquely quantum mechanical phenomena of **superposition, entanglement, and quantum interference** to solve specific computational problems asymptotically faster than any known classical algorithm.

A common misconception is that a quantum computer achieves speedups through "brute-force parallel processing" by evaluating all inputs simultaneously. If one simply prepares an equal superposition of all $2^n$ inputs and measures, the wave function collapses to a single, completely random input with zero computational advantage.

The true algorithmic power lies in **constructive and destructive interference**: designing unitary operations such that computational paths leading to incorrect answers cancel each other out ($e^{i\pi} = -1$), while amplitudes corresponding to the correct answer reinforce constructively.

---

## 1. Complexity Classes: BPP vs BQP

To rigorously analyze quantum speedups, theoretical computer science defines complexity classes:

- **$\mathbf{P}$ (Polynomial Time):** Decision problems solvable by a deterministic classical Turing machine in polynomial time $O(n^c)$.
- **$\mathbf{BPP}$ (Bounded-Error Probabilistic Polynomial Time):** Problems solvable by a randomized classical algorithm in polynomial time with error probability $\le 1/3$.
- **$\mathbf{BQP}$ (Bounded-Error Quantum Polynomial Time):** The class of decision problems solvable by a quantum computer in polynomial time with error probability $\le 1/3$.

$$
\mathbf{P} \subseteq \mathbf{BPP} \subseteq \mathbf{BQP} \subseteq \mathbf{PSPACE}
$$

Problems such as **Integer Factorization** and **Discrete Logarithms** (solved exponentially fast by Shor's algorithm) and **Quantum Hamiltonian Simulation** belong to $\mathbf{BQP}$, but are widely believed to lie outside $\mathbf{BPP}$.

---

## 2. The Black-Box (Oracle) Model

Many foundational quantum algorithms operate in the **query model** (or black-box model). Rather than inspecting the internal logic of a Boolean function $f: \{0,1\}^n \to \{0,1\}^m$, the algorithm is given access to a unitary subroutine (an **oracle**) and is judged by the number of queries required to determine a global property of $f$.

### Bit Oracle vs Phase Oracle

To remain unitary and reversible, a classical Boolean function $f: \{0,1\}^n \to \{0,1\}$ is encoded as a $(n+1)$-qubit **bit oracle** $U_f$:

$$
U_f |x\rangle |y\rangle = |x\rangle |y \oplus f(x)\rangle
$$

where $x \in \{0,1\}^n$ is the $n$-qubit query register, $y \in \{0,1\}$ is the 1-qubit target ancilla, and $\oplus$ denotes addition modulo 2 (XOR).

### The Phase Kickback Identity

The bridge between a bit-flipping oracle and quantum interference is **phase kickback**. Preparing the target ancilla in the state $|-\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}}$ transforms the bit oracle into a **phase oracle**:

$$
U_f |x\rangle |-\rangle = (-1)^{f(x)} |x\rangle |-\rangle
$$

#### Mathematical Proof

Expand the action of $U_f$ on $|x\rangle |-\rangle$:

$$
U_f |x\rangle |-\rangle = U_f \left( \frac{|x\rangle|0\rangle - |x\rangle|1\rangle}{\sqrt{2}} \right) = \frac{|x\rangle|0 \oplus f(x)\rangle - |x\rangle|1 \oplus f(x)\rangle}{\sqrt{2}}
$$

Now evaluate the target bit for both possible values of $f(x)$:

1. **If $f(x) = 0$:**

$$
\frac{|x\rangle|0\rangle - |x\rangle|1\rangle}{\sqrt{2}} = |x\rangle |-\rangle = (+1) |x\rangle |-\rangle
$$

2. **If $f(x) = 1$:**

$$
\frac{|x\rangle|1\rangle - |x\rangle|0\rangle}{\sqrt{2}} = - \left( \frac{|x\rangle|0\rangle - |x\rangle|1\rangle}{\sqrt{2}} \right) = -|x\rangle |-\rangle = (-1) |x\rangle |-\rangle
$$

Combining both cases:

$$
U_f |x\rangle |-\rangle = (-1)^{f(x)} |x\rangle |-\rangle
$$

The target qubit remains in state $|-\rangle$ completely unentangled, while the function output $f(x)$ is "kicked back" into the relative phase $(-1)^{f(x)}$ of the query register.

---

## 3. Taxonomy of Quantum Algorithmic Speedups

The algorithms explored in this repository represent the three major algorithmic families that power modern quantum computing:

```text
                                Quantum Algorithms
                                        │
        ┌───────────────────────────────┼───────────────────────────────┐
        ▼                               ▼                               ▼
1. Query & Hidden Structure   2. Amplitude Amplification     3. Quantum Phase Estimation
   (Exact Exponential)            (Quadratic Polynomial)         (Exponential Fourier)
   • Deutsch-Jozsa                • Grover Search                 • Quantum Fourier Transform (QFT)
   • Bernstein-Vazirani                                          • Quantum Phase Estimation (QPE)
                                                                 • VQE (Hybrid NISQ)
```

### Family 1: Hidden Structure & Query Algorithms

- **[Deutsch-Jozsa Algorithm](deutsch-jozsa.md):**
  - **Problem:** Given a promise that $f: \{0,1\}^n \to \{0,1\}$ is either *constant* (same output for all inputs) or *balanced* (outputs 0 for half of inputs, 1 for the other half), determine which it is.
  - **Complexity:** Quantum requires **1 query**; deterministic classical requires $2^{n-1} + 1$ queries.
  - **Mechanism:** Prepares an equal superposition with $H^{\otimes n}$, applies phase kickback, and applies $H^{\otimes n}$ again. If $f$ is constant, destructive interference eliminates all computational states except $|0\dots 0\rangle$.
- **[Bernstein-Vazirani Algorithm](bernstein-vazirani.md):**
  - **Problem:** Given an oracle computing $f(x) = s \cdot x \pmod 2$ for an unknown secret bitstring $s \in \{0,1\}^n$, find $s$.
  - **Complexity:** Quantum requires **1 query**; classical requires $n$ queries.
  - **Mechanism:** Interference reconstructs the entire bitstring $s$ in a single measurement of the query register.

### Family 2: Amplitude Amplification (Grover)

- **[Grover Search](grover-search.md):**
  - **Problem:** Find a marked item $\omega$ in an unstructured database of $N = 2^n$ items.
  - **Complexity:** Quantum requires $O(\sqrt{N})$ queries; classical randomized search requires $\Omega(N)$ queries (a provable **quadratic speedup**).
  - **Mechanism:** Iterative geometric rotation in a two-dimensional subspace. Each Grover iteration consists of an oracle phase flip followed by the Grover diffusion operator (inversion about the average amplitude).

### Family 3: Spectral Estimation & Fourier Transforms

- **[Quantum Fourier Transform (QFT)](quantum-fourier-transform.md):**
  - **Problem:** Perform the discrete Fourier transform on quantum state amplitudes:

$$
|j\rangle \mapsto \frac{1}{\sqrt{N}} \sum_{k=0}^{N-1} e^{2\pi i j k / N} |k\rangle
$$

  - **Complexity:** Uses $O(n^2)$ gates on $n$ qubits vs classical FFT requiring $O(n 2^n)$ operations.
- **[Quantum Phase Estimation (QPE)](quantum-phase-estimation.md):**
  - **Problem:** Given a unitary $U$ and an eigenstate $|u\rangle$ such that $U|u\rangle = e^{2\pi i \theta}|u\rangle$, estimate the unknown phase $\theta \in [0, 1)$ to $t$ bits of precision.
  - **Complexity:** Achieves polynomial scaling in precision; forms the algorithmic core of Shor's factoring algorithm, the HHL algorithm for linear systems, and quantum chemistry simulation.

### Family 4: Variational & Hybrid NISQ Algorithms

- **[Variational Quantum Eigensolver (VQE)](variational-quantum-eigensolver.md):**
  - **Problem:** Find the ground-state energy $E_0 = \min_{|\psi\rangle} \frac{\langle \psi|H|\psi\rangle}{\langle\psi|\psi\rangle}$ of a quantum Hamiltonian $H$.
  - **Design:** Hybrid quantum-classical optimization loop. A shallow parameterized quantum circuit (ansatz $|\psi(\vec{\theta})\rangle$) prepares the trial state and measures Pauli expectation values; a classical optimization algorithm updates $\vec{\theta}$ to minimize energy.

---

## 4. Comprehensive Algorithm Comparison Table

The six canonical algorithms implemented in this repository are summarized below:

| Algorithm | Problem Addressed | Quantum Queries / Depth | Classical Complexity | Speedup Type | Core Quantum Primitive | Experiment Link |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Deutsch-Jozsa** | Constant vs balanced test | $1$ query | $2^{n-1}+1$ queries | Exponential (exact) | Hadamard interference | [`experiments/deutsch-jozsa`](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/deutsch-jozsa) |
| **Bernstein-Vazirani** | Recover secret string $s$ | $1$ query | $n$ queries | Polynomial / Linear | Phase kickback | [`experiments/bernstein-vazirani`](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/bernstein-vazirani) |
| **Grover Search** | Unstructured database search | $O(\sqrt{N})$ | $O(N)$ | Quadratic | Amplitude amplification | [`experiments/grover-search`](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/grover-search) |
| **QFT** | Discrete Fourier transform | $O(n^2)$ gates | $O(n 2^n)$ ops | Exponential | Controlled phase rotations | [`experiments/quantum-fourier-transform`](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/quantum-fourier-transform) |
| **QPE** | Unitary eigenvalue phase | $O(t^2)$ gates | Exponential in $t$ | Exponential | Controlled-$U^{2^j}$ + $\mathrm{QFT}^\dagger$ | [`experiments/quantum-phase-estimation`](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/quantum-phase-estimation) |
| **VQE** | Hamiltonian ground state | Shallow ansatz layers | Exponential ($2^n \times 2^n$) | Heuristic NISQ | Variational principle | [`experiments/variational-quantum-eigensolver`](https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/variational-quantum-eigensolver) |

---

## 5. The Unified 4-Stage Algorithmic Blueprint

Almost every gate-based quantum algorithm conforms to a unified architectural flow:

```text
 ┌──────────────────────┐
 │ 1. State Preparation │ |00...0⟩ ──[ H⊗n ]──> Equal superposition of all 2ⁿ states
 └──────────┬───────────┘
            ▼
 ┌──────────────────────┐
 │ 2. Problem Encoding  │ System ──[ Oracle / Controlled-U ]──> Encodes problem structure into phases
 └──────────┬───────────┘
            ▼
 ┌──────────────────────┐
 │ 3. Interference Step │ Phases ──[ H⊗n / QFT† / Diffusion ]──> Translates phase patterns to amplitudes
 └──────────┬───────────┘
            ▼
 ┌──────────────────────┐
 │ 4. Readout & Classical│ Measure computational basis ──> Extracts solution with high probability
 └──────────────────────┘
```

1. **State Preparation:** The register is initialized in $|0\dots 0\rangle$ and placed in a uniform superposition via Hadamard gates $H^{\otimes n}$, initializing all computational basis paths simultaneously.
2. **Problem Encoding (Oracle):** A unitary interaction (or parameterized ansatz) evaluates the problem, encoding solutions into the **relative phases** of quantum states via phase kickback.
3. **Interference Transformation:** A change of basis (such as $H^{\otimes n}$, inverse Quantum Fourier Transform $\mathrm{QFT}^\dagger$, or the Grover diffusion operator) converts phase differences into **probability amplitude differences**.
4. **Measurement and Extraction:** Measuring in the computational basis collapses the wave function, returning the desired answer with high probability.

---

## 6. Multi-Ecosystem Implementation Strategy

A central objective of `quantum_ed` is providing side-by-side implementations across multiple major quantum programming frameworks:

- **NumPy (`experiments/*/numpy/`):** Pure linear algebra exposing raw state vectors, Kronecker products, and matrix multiplication without framework abstractions.
- **Qiskit (`experiments/*/qiskit/`):** IBM's Python SDK, targeting superconducting architectures and OpenQASM transpilation.
- **Q# (`experiments/*/qsharp/`):** Microsoft's quantum-specific language featuring native memory safety, adjoint operations, and clean register management.
- **OpenQASM 3 (`experiments/*/qasm/`):** The vendor-neutral quantum assembly language standard.
- **PennyLane (`experiments/*/pennylane/`):** Xanadu's differentiable programming framework for quantum machine learning and variational circuits.

For a detailed side-by-side syntax comparison, see the [Ecosystem Comparison Guide](language-comparison.md).

---

## 7. Worked Study Problems

### Problem 1 — Why Naive Parallelism Fails
**Problem:**
A student proposes an algorithm: "To find an input $x$ where $f(x)=1$, prepare the superposition $\frac{1}{\sqrt{N}}\sum_x |x\rangle$, evaluate the bit oracle $U_f$, and measure the query register."
Explain mathematically why this yields no speedup over classical random guessing.

**Solution:**
1. State after applying bit oracle to $\frac{1}{\sqrt{N}}\sum_x |x\rangle|0\rangle$:

$$
|\psi\rangle = \frac{1}{\sqrt{N}} \sum_{x=0}^{N-1} |x\rangle |f(x)\rangle
$$

2. Suppose there is exactly 1 solution $x^* \in \{0, \dots, N-1\}$ where $f(x^*) = 1$:

$$
|\psi\rangle = \frac{1}{\sqrt{N}} |x^*\rangle |1\rangle + \frac{1}{\sqrt{N}} \sum_{x \neq x^*} |x\rangle |0\rangle
$$

3. Measuring the query register:
   The probability of measuring the solution $x^*$ is:

$$
P(x^*) = \left| \frac{1}{\sqrt{N}} \right|^2 = \frac{1}{N}
$$

   This is identical to selecting an input at random in classical computation. Without an interference step (like Grover's diffusion operator), the quantum superposition offers zero speedup.

---

### Problem 2 — Classical Query Lower Bound for Deutsch-Jozsa
**Problem:**
Prove that a deterministic classical algorithm requires $2^{n-1} + 1$ queries in the worst case to determine whether a Boolean function $f: \{0,1\}^n \to \{0,1\}$ is constant or balanced.

**Solution:**
- The domain has $N = 2^n$ inputs.
- A balanced function evaluates to $0$ on exactly $2^{n-1}$ inputs and $1$ on $2^{n-1}$ inputs.
- A constant function evaluates to the same value on all $2^n$ inputs.
- If a classical algorithm evaluates $f$ on $k$ inputs and observes all $0$s:
  - If $k \le 2^{n-1}$, the function could still be balanced (the remaining $2^{n-1}$ inputs could all be $1$).
  - Only when $k = 2^{n-1} + 1$ and all outputs are $0$ is it mathematically impossible for $f$ to be balanced.
- Therefore, a deterministic classical algorithm requires $2^{n-1} + 1$ queries in the worst case, whereas the Deutsch-Jozsa quantum algorithm requires exactly **1 query**.

---

### Problem 3 — Grover Search Iterations
**Problem:**
In an unstructured database of size $N = 64$ ($n=6$ qubits) with $M = 1$ target solution, compute the optimal number of Grover iterations $R \approx \frac{\pi}{4}\sqrt{\frac{N}{M}}$.

**Solution:**
1. Compute the rotation angle $\theta$:

$$
\sin\theta = \frac{\sqrt{M}}{\sqrt{N}} = \frac{1}{\sqrt{64}} = \frac{1}{8} = 0.125 \implies \theta = \arcsin(0.125) \approx 0.12533\ \text{rad}
$$

2. Each Grover iteration rotates the state vector by $2\theta$:

$$
(2R + 1)\theta \approx \frac{\pi}{2} \implies R \approx \frac{\pi}{4\theta} - \frac{1}{2}
$$

$$
R \approx \frac{\pi}{4(0.12533)} - 0.5 \approx \frac{3.14159}{0.50133} - 0.5 \approx 6.26 - 0.5 = 5.76
$$

3. Rounding to the nearest integer gives $R = 6$ iterations.
After 6 iterations, the probability of measuring the target state is:

$$
P = \sin^2((2 \cdot 6 + 1)\theta) = \sin^2(13 \cdot 0.12533) = \sin^2(1.629\ \text{rad}) \approx \sin^2(93.3^\circ) \approx 0.9966 \quad (99.7\%)
$$

---

## 8. Next Steps

Explore the individual algorithm guides and experiments:

- [Deutsch-Jozsa Algorithm](deutsch-jozsa.md)
- [Bernstein-Vazirani Algorithm](bernstein-vazirani.md)
- [Grover Search](grover-search.md)
- [Quantum Fourier Transform](quantum-fourier-transform.md)
- [Quantum Phase Estimation](quantum-phase-estimation.md)
- [Variational Quantum Eigensolver](variational-quantum-eigensolver.md)
- [Multi-Language Comparison](language-comparison.md)
