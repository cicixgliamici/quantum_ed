OPENQASM 3.0;
include "stdgates.inc";

qubit[2] qubits;
bit[2] results;

// H creates superposition on qubit 0.
h qubits[0];

// CNOT correlates qubit 1 with qubit 0 to create Phi-plus.
cx qubits[0], qubits[1];

// Register-wide measurement maps qubit j to classical bit j.
results = measure qubits;
