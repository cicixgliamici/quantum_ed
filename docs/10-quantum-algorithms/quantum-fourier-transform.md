# Quantum Fourier Transform (QFT)

The **Quantum Fourier Transform (QFT)** is the quantum mechanical analogue of the classical Discrete Fourier Transform (DFT). It is one of the most powerful algorithmic building blocks in quantum computation, serving as the mathematical engine underlying:

- **Quantum Phase Estimation (QPE)**
- **Shor's Factoring and Discrete Logarithm Algorithm**
- **Hidden Subgroup Problems (HSP)**
- **Quantum Counting and Amplitude Estimation**

While the classical Fast Fourier Transform (FFT) requires $O(n 2^n)$ arithmetic operations to process a vector of size $N = 2^n$, the QFT executes on an $n$-qubit quantum register in only **$O(n^2)$ quantum gates**, representing an exponential reduction in gate complexity.

---

## 1. Mathematical Definition

Let $N = 2^n$ denote the dimension of the state space of an $n$-qubit register. The computational basis states are denoted $|0\rangle, |1\rangle, \dots, |N-1\rangle$.

The **Quantum Fourier Transform** is the linear unitary operator $\operatorname{QFT}_N$ that maps each computational basis state $|j\rangle$ to an equal-magnitude superposition of basis states with Fourier phase factors:

$$
\operatorname{QFT}_N |j\rangle = \frac{1}{\sqrt{N}} \sum_{k=0}^{N-1} \omega^{j k} |k\rangle, \qquad \text{where } \omega = e^{2\pi i / N}
$$

When applied to an arbitrary quantum state $|\psi\rangle = \sum_{j=0}^{N-1} x_j |j\rangle$, the output is:

$$
\operatorname{QFT}_N |\psi\rangle = \sum_{k=0}^{N-1} y_k |k\rangle
$$

where the output amplitudes $y_k$ are precisely the discrete Fourier transform of the input amplitudes $x_j$:

$$
y_k = \frac{1}{\sqrt{N}} \sum_{j=0}^{N-1} x_j e^{2\pi i j k / N}
$$

### Unitarity

The QFT operator is strictly unitary ($\operatorname{QFT}^\dagger \operatorname{QFT} = I$). The matrix elements are:

$$
(\operatorname{QFT}_N)_{j, k} = \frac{1}{\sqrt{N}} e^{2\pi i j k / N}
$$

Because all columns are mutually orthonormal, total probability is strictly conserved.

---

## 2. Product Representation (The Circuit Factorization)

To implement the QFT using quantum gates, we must decompose the $2^n \times 2^n$ matrix into local gates acting on one and two qubits.

The breakthrough discovered by Coppersmith (1994) is that the QFT maps an arbitrary computational basis state into a **completely separable tensor product of individual qubit states**.

### Binary Fraction Notation

Write the integer $j \in \{0, \dots, 2^n - 1\}$ in binary notation:

$$
j = j_1 2^{n-1} + j_2 2^{n-2} + \dots + j_n 2^0 = j_1 j_2 \dots j_n, \quad j_l \in \{0, 1\}
$$

Define the binary fraction:

$$
0.j_l j_{l+1} \dots j_m = \sum_{r=l}^m j_r 2^{-(r - l + 1)} = \frac{j_l}{2} + \frac{j_{l+1}}{4} + \dots + \frac{j_m}{2^{m-l+1}}
$$

### Mathematical Derivation

Expand the basis state $|k\rangle = |k_1 k_2 \dots k_n\rangle$:

$$
\operatorname{QFT}_N |j\rangle = \frac{1}{\sqrt{2^n}} \sum_{k=0}^{2^n-1} e^{2\pi i j k / 2^n} |k\rangle
$$

Write $k = \sum_{l=1}^n k_l 2^{n-l}$:

$$
\operatorname{QFT}_N |j\rangle = \frac{1}{\sqrt{2^n}} \sum_{k_1=0}^1 \dots \sum_{k_n=0}^1 e^{2\pi i j \sum_{l=1}^n k_l 2^{-l}} |k_1 \dots k_n\rangle
$$

Factor the exponential of the sum into a product of exponentials:

$$
= \frac{1}{\sqrt{2^n}} \sum_{k_1=0}^1 \dots \sum_{k_n=0}^1 \bigotimes_{l=1}^n e^{2\pi i j k_l 2^{-l}} |k_l\rangle
$$

Distribute the sums into individual tensor product factors:

$$
= \frac{1}{\sqrt{2^n}} \bigotimes_{l=1}^n \left( \sum_{k_l=0}^1 e^{2\pi i j k_l 2^{-l}} |k_l\rangle \right) = \frac{1}{\sqrt{2^n}} \bigotimes_{l=1}^n \left( |0\rangle + e^{2\pi i j 2^{-l}} |1\rangle \right)
$$

Now evaluate the phase factor $e^{2\pi i j 2^{-l}}$:

$$
j 2^{-l} = \sum_{r=1}^n j_r 2^{n-l-r} = \underbrace{\sum_{r=1}^{n-l} j_r 2^{n-l-r}}_{\text{Integer Part}} + \underbrace{\sum_{r=n-l+1}^n j_r 2^{n-l-r}}_{\text{Fractional Part } 0.j_{n-l+1}\dots j_n}
$$

Since $e^{2\pi i \cdot (\text{integer})} = 1$, the integer part contributes nothing:

$$
e^{2\pi i j 2^{-l}} = e^{2\pi i (0.j_{n-l+1} j_{n-l+2} \dots j_n)}
$$

Substituting this back into the product yields the **QFT Product Representation**:

$$
\operatorname{QFT}|j_1 j_2 \dots j_n\rangle = \frac{1}{\sqrt{2^n}} \left( |0\rangle + e^{2\pi i 0.j_n} |1\rangle \right) \otimes \left( |0\rangle + e^{2\pi i 0.j_{n-1} j_n} |1\rangle \right) \otimes \dots \otimes \left( |0\rangle + e^{2\pi i 0.j_1 j_2 \dots j_n} |1\rangle \right)
$$

---

## 3. Circuit Architecture

The product representation directly reveals how to synthesize the QFT using standard quantum gates:

### Gate Components

1. **Hadamard Gate ($H$):**
   Acts on qubit $l$ in state $|j_l\rangle$:

$$
H|j_l\rangle = \frac{|0\rangle + (-1)^{j_l}|1\rangle}{\sqrt{2}} = \frac{|0\rangle + e^{2\pi i (0.j_l)}|1\rangle}{\sqrt{2}}
$$

2. **Controlled Phase Rotation Gate ($R_k$):**
   The single-qubit phase rotation gate is:

$$
R_k = \begin{bmatrix} 1 & 0 \\ 0 & e^{2\pi i / 2^k} \end{bmatrix}
$$

   Special cases:
   - $R_1 = Z = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$ ($\text{phase } \pi$)
   - $R_2 = S = \begin{bmatrix} 1 & 0 \\ 0 & i \end{bmatrix}$ ($\text{phase } \pi/2$)
   - $R_3 = T = \begin{bmatrix} 1 & 0 \\ 0 & e^{i\pi/4} \end{bmatrix}$ ($\text{phase } \pi/4$)

   When controlled by qubit $j_m$, the gate $C\text{-}R_k$ applies phase $e^{2\pi i / 2^k}$ if and only if $j_m = 1$, effectively appending $j_m$ to the binary fraction phase.

3. **SWAP Gates:**
   Notice that in the product formula, the first output qubit has phase $0.j_n$ (least significant bit), while the last output qubit has phase $0.j_1\dots j_n$ (most significant bit). A final layer of $\lfloor n/2 \rfloor$ SWAP gates reverses the wire order to match standard register conventions.

### Circuit Flow for $n$ Qubits

```text
|j₁⟩ ───[ H ]───[ R₂ ]───[ R₃ ]─── ... ───[ Rₙ ]───────────────────────── X ─── |OUT₁⟩
                  │        │                 │                             │
|j₂⟩ ─────────────●──────┼──────[ H ]─── ... ───[ Rₙ₋₁ ]─────────────────┼─── |OUT₂⟩
                           │                   │                           │
|j₃⟩ ──────────────────────●───────────────────┼────── ... ────────────────┼─── |OUT₃⟩
                                               │                           │
...                                            │                           │
|jₙ⟩ ──────────────────────────────────────────●────── ... ───[ H ]─────── X ─── |OUTₙ⟩
```

---

## 4. Complexity Analysis: $O(n^2)$ vs Classical $O(n 2^n)$

Let us count the total number of elementary gates in an $n$-qubit QFT circuit:

1. **Gate count per wire:**
   - Wire 1 requires 1 Hadamard and $(n-1)$ controlled rotations = $n$ gates.
   - Wire 2 requires 1 Hadamard and $(n-2)$ controlled rotations = $(n-1)$ gates.
   - Wire $l$ requires 1 Hadamard and $(n-l)$ controlled rotations = $(n-l+1)$ gates.
   - Wire $n$ requires 1 Hadamard = $1$ gate.
2. **Sum of phase and Hadamard gates:**

$$
\sum_{l=1}^n l = \frac{n(n+1)}{2}
$$

3. **Reversal SWAP gates:**
   $\lfloor n/2 \rfloor$ SWAP gates (each decomposable into 3 CNOTs).

Total gate complexity:

$$
N_{\mathrm{gates}} = \frac{n(n+1)}{2} + \left\lfloor \frac{n}{2} \right\rfloor = O(n^2)
$$

### Comparison Table

| Property | Classical FFT (Cooley-Tukey) | Quantum Fourier Transform (QFT) |
| :--- | :--- | :--- |
| **Input Data** | Classical vector $\vec{x} \in \mathbb{C}^N$ | Quantum state $|\psi\rangle = \sum x_j |j\rangle$ |
| **Operation Count** | $\Theta(N \log N) = \Theta(n 2^n)$ ops | $O(n^2)$ quantum gates |
| **For $n = 30$ ($N \approx 10^9$)** | $\approx 3 \times 10^{10}$ FLOPs | $\approx 465$ gates |
| **For $n = 100$ ($N \approx 10^{30}$)** | Physically impossible ($> 10^{32}$ ops) | $\approx 5,050$ gates |
| **Output Accessibility** | Full vector accessible simultaneously | Sampled probabilistically upon readout |

> [!NOTE]
> The exponential gate reduction does not permit computing the classical FFT of arbitrary data faster, because preparing an arbitrary classical vector into $2^n$ quantum amplitudes requires $\Omega(2^n)$ operations. The true power of QFT arises when intermediate states inside quantum algorithms naturally possess periodic phase structures.

---

## 5. The Inverse QFT ($\mathrm{QFT}^\dagger$)

Because quantum computation is reversible, the inverse transform $\operatorname{QFT}^\dagger = \operatorname{QFT}^{-1}$ is implemented by:

1. Inverting the sequence of gates (executing the circuit from right to left).
2. Replacing every rotation angle $\theta$ with $-\theta$ (taking the adjoint $R_k^\dagger$):

$$
R_k^\dagger = \begin{bmatrix} 1 & 0 \\ 0 & e^{-2\pi i / 2^k} \end{bmatrix}
$$

In Quantum Phase Estimation, $\mathrm{QFT}^\dagger$ transforms phases created by controlled-$U$ operations back into computational basis bitstrings that can be measured directly.

---

## 6. Worked Example: 3-Qubit QFT ($N = 8$)

Consider $n = 3$ qubits ($N = 8$). The basis states are $|000\rangle, \dots, |111\rangle$.

### Transform of State $|000\rangle$

For $j = 0$ ($j_1=0, j_2=0, j_3=0$):

$$
\operatorname{QFT}|000\rangle = \frac{1}{\sqrt{8}} (|0\rangle + |1\rangle) \otimes (|0\rangle + |1\rangle) \otimes (|0\rangle + |1\rangle) = |+\rangle \otimes |+\rangle \otimes |+\rangle
$$

The QFT of the all-zero state is the uniform superposition of all 8 computational basis states with equal phase.

### Transform of State $|100\rangle$ ($j = 4$)

In binary, $j = 4$ corresponds to $j_1=1, j_2=0, j_3=0$:
- Binary fractions:
  - $0.j_3 = 0.0_2 = 0$
  - $0.j_2 j_3 = 0.00_2 = 0$
  - $0.j_1 j_2 j_3 = 0.100_2 = 1/2 \implies e^{2\pi i (1/2)} = e^{i\pi} = -1$

Substituting into the product formula:

$$
\operatorname{QFT}|100\rangle = \frac{1}{\sqrt{8}} (|0\rangle + |1\rangle) \otimes (|0\rangle + |1\rangle) \otimes (|0\rangle - |1\rangle) = |+\rangle |+\rangle |-\rangle
$$

---

## 7. Python Implementation with NumPy

```python
import numpy as np

def qft_matrix(n: int) -> np.ndarray:
    """Construct the exact 2^n x 2^n QFT unitary matrix."""
    N = 1 << n
    omega = np.exp(2j * np.pi / N)
    j, k = np.indices((N, N))
    return (1.0 / np.sqrt(N)) * (omega ** (j * k))

# Verify unitarity for 3 qubits (8x8)
U_qft = qft_matrix(3)
assert np.allclose(U_qft @ np.conjugate(U_qft).T, np.eye(8))

# Test transform of |100> (index 4)
ket_4 = np.zeros(8, dtype=complex)
ket_4[4] = 1.0

fourier_state = U_qft @ ket_4
print("Amplitudes of QFT|4>:\n", np.round(fourier_state, 4))
```

---

## 8. Multi-Ecosystem Showcase

The 3-qubit QFT circuit is implemented across all five supported environments in the repository:

- [NumPy Implementation](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/quantum-fourier-transform/numpy/quantum_fourier_transform.py)
- [Qiskit Circuit](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/quantum-fourier-transform/qiskit/quantum_fourier_transform.py)
- [Q# Program](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/quantum-fourier-transform/qsharp/QuantumFourierTransform.qs)
- [OpenQASM 3](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/quantum-fourier-transform/openqasm/quantum_fourier_transform.qasm)
- [PennyLane](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/quantum-fourier-transform/pennylane/quantum_fourier_transform.py)

---

## 9. Worked Exercises

### Exercise 1 — 1-Qubit QFT is Hadamard
**Problem:**
Show that for $n = 1$ qubit ($N = 2$), the Quantum Fourier Transform operator is identical to the Hadamard gate $H$.

**Solution:**
For $N = 2$, $\omega = e^{2\pi i / 2} = e^{i\pi} = -1$.
Compute matrix elements $(\operatorname{QFT}_2)_{j, k} = \frac{1}{\sqrt{2}} (-1)^{j \cdot k}$ for $j, k \in \{0, 1\}$:
- $j=0, k=0 \implies (-1)^0 = 1$
- $j=0, k=1 \implies (-1)^0 = 1$
- $j=1, k=0 \implies (-1)^0 = 1$
- $j=1, k=1 \implies (-1)^1 = -1$

Assembling into matrix form:

$$
\operatorname{QFT}_2 = \frac{1}{\sqrt{2}} \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix} = H
$$

Thus, the single-qubit QFT is exactly the Hadamard gate.

---

### Exercise 2 — Orthonormality Proof
**Problem:**
Prove that the columns of the QFT matrix are mutually orthonormal, showing that $\operatorname{QFT}_N$ is unitary for any $N$.

**Solution:**
Let $|\psi_j\rangle = \operatorname{QFT}_N |j\rangle = \frac{1}{\sqrt{N}}\sum_{k=0}^{N-1} e^{2\pi i j k / N} |k\rangle$.
Compute the inner product $\langle \psi_m | \psi_j \rangle$:

$$
\langle \psi_m | \psi_j \rangle = \frac{1}{N} \sum_{k=0}^{N-1} e^{-2\pi i m k / N} e^{2\pi i j k / N} = \frac{1}{N} \sum_{k=0}^{N-1} e^{2\pi i (j - m) k / N}
$$

1. If $j = m$:

$$
\frac{1}{N} \sum_{k=0}^{N-1} 1 = \frac{N}{N} = 1
$$

2. If $j \neq m$:
   Let $r = e^{2\pi i (j - m)/N} \neq 1$. Using the geometric series formula:

$$
\sum_{k=0}^{N-1} r^k = \frac{1 - r^N}{1 - r} = \frac{1 - e^{2\pi i (j - m)}}{1 - r} = \frac{1 - 1}{1 - r} = 0
$$

Therefore, $\langle \psi_m | \psi_j \rangle = \delta_{m, j}$, which proves that $\operatorname{QFT}_N$ is unitary.

---

## 10. Next Steps

- [Quantum Phase Estimation](quantum-phase-estimation.md) — see how the inverse QFT resolves unknown eigenvalue phases
- [Shor's Algorithm Overview](https://github.com/cicixgliamici/quantum_ed/blob/main/experiments/quantum-phase-estimation/README.md)
- [Grover Search](grover-search.md) — explore amplitude amplification
