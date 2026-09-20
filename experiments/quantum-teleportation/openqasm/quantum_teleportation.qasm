OPENQASM 3.0;
include "stdgates.inc";

qubit[3] qubits;
bit result;

// Qubit 0 is |1>; qubits 1 and 2 become the shared Bell pair.
x qubits[0];
h qubits[1];
cx qubits[1], qubits[2];
barrier qubits;

// Alice performs the Bell-basis interaction.
cx qubits[0], qubits[1];
h qubits[0];

// Coherent controls defer measurement and classical feed-forward.
cx qubits[1], qubits[2];
cz qubits[0], qubits[2];
barrier qubits;

// Bob's target qubit deterministically contains |1>.
result = measure qubits[2];
