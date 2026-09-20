OPENQASM 3.0;
include "stdgates.inc";

qubit[2] qubits;
bit[2] results;

h qubits;
cz qubits[0], qubits[1];

// Diffusion reflects amplitudes about their mean.
h qubits;
x qubits;
cz qubits[0], qubits[1];
x qubits;
h qubits;
results = measure qubits;
