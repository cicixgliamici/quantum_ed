# Implementation comparison: Qiskit, Q#, and OpenQASM 3

The three showcase implementations describe the same circuits at different
levels of abstraction. This comparison focuses on the concepts visible in the
Deutsch-Jozsa and Bernstein-Vazirani examples.

## The role of each ecosystem

| Ecosystem | Primary role in this repository | Abstraction level |
| --- | --- | --- |
| Qiskit | Build, simulate, inspect, and post-process circuits from Python | High-level SDK |
| Q# | Express quantum operations with explicit qubit ownership | Quantum programming language |
| OpenQASM 3 | Describe gates, registers, and measurements in a portable circuit format | Low-level quantum/classical IR |

They are complementary rather than interchangeable in every context. Qiskit
includes host-language workflow and result processing, Q# models a quantum
program as typed operations, and OpenQASM 3 describes the executable circuit
most directly.

## Concept mapping

| Concept | Qiskit | Q# | OpenQASM 3 |
| --- | --- | --- | --- |
| Allocate three inputs | `QuantumCircuit(4, 3)` | `use inputs = Qubit[3];` | `qubit[3] inputs;` |
| Allocate classical results | Part of `QuantumCircuit(4, 3)` | Return type `Result[]` | `bit[3] results;` |
| Apply Hadamard to a register | `circuit.h(range(3))` | `for input in inputs { H(input); }` | `h inputs;` |
| Apply controlled-X | `circuit.cx(0, 3)` | `CNOT(inputs[0], output);` | `cx inputs[0], output;` |
| Measure inputs | `circuit.measure(...)` | `MResetEach(inputs)` | `results = measure inputs;` |
| Execute locally | `StatevectorSampler` | QDK simulator | Provider/tool dependent |
| Process counts | Python dictionary | Host or returned results | Outside this circuit file |

## Qiskit: circuit plus workflow

Qiskit is embedded in Python. This makes it natural to keep circuit
construction, simulation, visualization, and classical post-processing in one
file.

```python
sampler = StatevectorSampler(seed=42)
result = sampler.run([circuit], shots=128).result()
counts = result[0].data.c.get_counts()
```

The circuit is quantum, while Python controls execution and interprets the
result. This is why the Qiskit examples can directly print `balanced` or the
recovered secret.

The tradeoff is that some behavior belongs to the SDK rather than the circuit
itself. Register names, result containers, backend selection, and bit-string
display order must be understood alongside the gate sequence.

## Q#: operations and qubit lifetime

Q# makes allocation and cleanup part of the program:

```qsharp
use inputs = Qubit[3];
use output = Qubit();
// ...
let results = MResetEach(inputs);
Reset(output);
```

The `use` scope communicates ownership: the operation receives fresh qubits
and must leave them safe to release. Explicit reset is therefore not incidental
cleanup; it documents the quantum resource lifecycle.

Q# also distinguishes quantum results from ordinary Boolean values through the
`Result` type. The examples return measurements and leave display or repeated
execution to the surrounding QDK environment.

## OpenQASM 3: the circuit made explicit

OpenQASM 3 exposes registers and instructions with little host-language
machinery:

```qasm
qubit[3] inputs;
qubit output;
bit[3] results;

h inputs;
cx inputs[0], output;
results = measure inputs;
```

This makes the physical structure easy to review. Register-wide gate
broadcasting, classical storage, and measurement are visible in a compact
form.

The source intentionally does not choose a simulator, shot count, noise model,
or result visualization. Those concerns belong to the toolchain that consumes
the OpenQASM file.

## The same quantum pattern

Both algorithms use this sequence:

1. Prepare the output qubit in $|-\rangle$.
2. Put the input register into uniform superposition.
3. Call the oracle once.
4. Apply Hadamard gates to the inputs.
5. Measure the inputs.

Only the oracle and classical interpretation change:

| Algorithm | Oracle used in the showcase | Interpretation |
| --- | --- | --- |
| Deutsch-Jozsa | $f(x)=x_0$ | All zeros means constant; otherwise balanced |
| Bernstein-Vazirani | $f_s(x)=s\cdot x$ with $s=101$ | The measurement is the secret |

This separation is deliberate. It shows that an algorithm is more than its
gate skeleton: the promise on the oracle and the meaning assigned to the
measurement are part of the specification.

## Bit-order conventions

Bit order is the most visible source of apparent disagreement:

- Q# returns the `Result[]` in input-array order.
- Qiskit count strings conventionally display the highest classical index on
  the left.
- OpenQASM maps `inputs[j]` to `results[j]`, while the consuming tool decides
  how the complete register is printed.

For the Deutsch-Jozsa example, the physical results are
$x_0=1,x_1=0,x_2=0$. Q# presents this as `[One, Zero, Zero]`; Qiskit prints
`001`. Both describe the same measured bits.

The Bernstein-Vazirani secret `101` is symmetric under reversal, which makes
the example pleasant to read but does not remove the underlying convention.

## Which representation should a reviewer inspect?

- Inspect **Qiskit** to see an end-to-end executable experiment.
- Inspect **Q#** to see structured quantum control and resource ownership.
- Inspect **OpenQASM 3** to see the circuit with minimal framework overhead.

Reading the three versions side by side separates the algorithm's invariant
logic from ecosystem-specific syntax.
