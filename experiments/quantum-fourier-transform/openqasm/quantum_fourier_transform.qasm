OPENQASM 3.0;
include "stdgates.inc";

qubit[3] qubits;
bit[3] results;

x qubits[0];
h qubits[0];
cp(pi / 2) qubits[1], qubits[0];
cp(pi / 4) qubits[2], qubits[0];
h qubits[1];
cp(pi / 2) qubits[2], qubits[1];
h qubits[2];
swap qubits[0], qubits[2];
results = measure qubits;
