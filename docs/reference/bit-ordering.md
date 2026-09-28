# Bit-Ordering Conventions in Quantum Software

One of the most persistent sources of confusion and subtle software bugs in quantum computing is **bit ordering** (endianness). Different quantum frameworks and textbook literature adopt opposing conventions for indexing qubits and printing measurement bitstrings.

Bit ordering is a **presentation and indexing convention**, not a physical difference in circuit execution. This reference provides an explicit guide to the conventions used in `quantum_ed`, Qiskit, Q#, OpenQASM 3, and PennyLane.

---

## 1. The Core Distinctions

To avoid ambiguity, always distinguish between three separate concepts:

1. **Qubit Wire Index:** Identifies a physical or virtual wire in a circuit diagram ($q_0, q_1, \dots$).
2. **Tensor Product Ordering:** Determines how multi-qubit matrices and state vectors are assembled via Kronecker products:

$$
|q_0\rangle \otimes |q_1\rangle \otimes \dots \otimes |q_{n-1}\rangle
$$

3. **Display String Order:** Determines how a framework formats a multi-qubit measurement outcome as a text string (e.g. `"001"` vs `"100"`).

---

## 2. Big-Endian vs Little-Endian

### Big-Endian (Most Significant Bit on the Left)

In **big-endian** (or lexicographic) ordering:

- Qubit 0 is the **most significant bit (MSB)**, corresponding to place value $2^{n-1}$.
- Qubit $n-1$ is the **least significant bit (LSB)**, corresponding to place value $2^0$.
- Basis state index:

$$
\text{index} = \sum_{j=0}^{n-1} q_j 2^{n - 1 - j}
$$

- State vector:

$$
|q_0 q_1 \dots q_{n-1}\rangle = |q_0\rangle \otimes |q_1\rangle \otimes \dots \otimes |q_{n-1}\rangle
$$

**Adopted by:** Standard physics textbooks (Nielsen & Chuang), **NumPy core in `quantum_ed`**, **PennyLane**, **Q#**, and **QuTiP**.

### Little-Endian (Least Significant Bit on the Left / Qiskit Convention)

In **little-endian** ordering (as adopted by **IBM Qiskit**):

- Qubit 0 is the **least significant bit (LSB)**, corresponding to place value $2^0$.
- Qubit $n-1$ is the **most significant bit (MSB)**, corresponding to place value $2^{n-1}$.
- Basis state index:

$$
\text{index} = \sum_{j=0}^{n-1} q_j 2^j
$$

- In Qiskit, when formatting measurement counts, the bit corresponding to qubit $n-1$ is printed on the leftmost side, and qubit 0 is on the rightmost side:

$$
\text{Printed String} = \text{"}q_{n-1} q_{n-2} \dots q_1 q_0\text{"}
$$

---

## 3. Comparison Lookup Tables

### Two-Qubit System ($n = 2$)

Consider the state where **qubit 0 is in state $|1\rangle$** and **qubit 1 is in state $|0\rangle$**:

| Framework | State Representation | State Vector Index | Display String | Place Value Formula |
| :--- | :--- | :--- | :--- | :--- |
| **NumPy (`quantum_ed`)** | $|10\rangle = |1\rangle \otimes |0\rangle$ | `index 2` ($2 \cdot 1 + 0$) | `[0, 0, 1, 0]` | $2 \cdot q_0 + q_1$ |
| **Q#** | `[One, Zero]` | `index 2` | `[1, 0]` | Lexicographic |
| **PennyLane** | `wires=[0, 1]` | `index 2` | `|10>` | Lexicographic |
| **Qiskit** | $|q_1 q_0\rangle = |01\rangle$ | `index 1` ($1 \cdot 1 + 2 \cdot 0$) | `"01"` ($q_1=0, q_0=1$) | $q_0 + 2 \cdot q_1$ |

### Three-Qubit Comprehensive Mapping ($n = 3$)

The table below maps the eight computational basis states across frameworks:

| Qubit States $(q_0, q_1, q_2)$ | Standard Big-Endian Ket | NumPy / PennyLane Index | Qiskit Ket $|q_2 q_1 q_0\rangle$ | Qiskit Printed String |
| :---: | :---: | :---: | :---: | :---: |
| $(0, 0, 0)$ | $|000\rangle$ | `0` | $|000\rangle$ | `"000"` |
| $(0, 0, 1)$ | $|001\rangle$ | `1` | $|100\rangle$ | `"100"` |
| $(0, 1, 0)$ | $|010\rangle$ | `2` | $|010\rangle$ | `"010"` |
| $(0, 1, 1)$ | $|011\rangle$ | `3` | $|110\rangle$ | `"110"` |
| $(1, 0, 0)$ | $|100\rangle$ | `4` | $|001\rangle$ | `"001"` |
| $(1, 0, 1)$ | $|101\rangle$ | `5` | $|101\rangle$ | `"101"` |
| $(1, 1, 0)$ | $|110\rangle$ | `6` | $|011\rangle$ | `"011"` |
| $(1, 1, 1)$ | $|111\rangle$ | `7` | $|111\rangle$ | `"111"` |

Notice that states like $(1, 0, 0)$ (where only qubit 0 is active) correspond to state-vector index 4 in NumPy and PennyLane, but are printed as `"001"` in Qiskit counts dictionaries!

---

## 4. Controlled Gate Matrix Ordering

Endianness directly affects the matrix representation of two-qubit controlled gates.

### CNOT Matrix in Standard (Big-Endian) Convention

With qubit 0 as control and qubit 1 as target, the basis states are ordered $|00\rangle, |01\rangle, |10\rangle, |11\rangle$:

$$
\mathrm{CNOT}_{0 \to 1} = \begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 0 & 1 \\
0 & 0 & 1 & 0
\end{bmatrix}
$$

If control and target are reversed (qubit 1 is control, qubit 0 is target):

$$
\mathrm{CNOT}_{1 \to 0} = \begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & 0 & 0 & 1 \\
0 & 0 & 1 & 0 \\
0 & 1 & 0 & 0
\end{bmatrix}
$$

In Qiskit's internal operator representations, these matrices appear swapped because Qiskit treats qubit 0 as the rightmost factor ($q_1 \otimes q_0$).

---

## 5. Converting Across Frameworks in Python

Here is a Python utility to convert between Qiskit counts strings and NumPy state-vector indices:

```python
def qiskit_string_to_big_endian_index(bitstring: str) -> int:
    """Convert Qiskit's reversed bitstring into a standard big-endian index.
    
    In Qiskit, bitstring = 'q_{n-1}...q_1 q_0'.
    In Big-Endian, index = sum_{j=0}^{n-1} q_j * 2^{n - 1 - j}.
    """
    # Reverse string to get q_0, q_1, ..., q_{n-1}
    qubit_values = [int(b) for b in reversed(bitstring)]
    n = len(qubit_values)
    
    idx = 0
    for j, val in enumerate(qubit_values):
        idx += val * (1 << (n - 1 - j))
    return idx

def qiskit_counts_to_standard_probs(counts: dict[str, int]) -> dict[str, float]:
    """Convert a Qiskit counts dictionary to standard big-endian bitstrings."""
    total_shots = sum(counts.values())
    standard_counts = {}
    for bitstring, count in counts.items():
        # Reverse bitstring so q_0 is on the left
        std_bitstring = bitstring[::-1]
        standard_counts[std_bitstring] = count / total_shots
    return standard_counts

# Example: Qiskit reports result '001' (qubit 0 is 1, qubits 1 and 2 are 0)
qiskit_out = "001"
std_idx = qiskit_string_to_big_endian_index(qiskit_out)
print(f"Qiskit '{qiskit_out}' -> Big-Endian Index: {std_idx}")  # Index 4 (|100>)
```

---

## 6. Summary Rules for `quantum_ed`

When exploring this repository:

1. **Analytical derivations and NumPy code** use **Big-Endian** ordering:
   Qubit 0 is always the leftmost qubit ($|q_0 q_1 \dots\rangle$).
2. **Qiskit experiments** format printed outputs with qubit 0 on the **right**:
   Every experiment README explicitly documents the expected bitstring in both formats.
3. **Q# and OpenQASM 3** map `q[j]` to `c[j]` using matching indices, preserving wire order directly in result arrays.
