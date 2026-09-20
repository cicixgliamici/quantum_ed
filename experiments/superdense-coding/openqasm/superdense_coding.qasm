OPENQASM 3.0;
include "stdgates.inc";

qubit[2] qubits;
bit[2] results;

// Alice and Bob share Phi-plus before the message is encoded.
h qubits[0];
cx qubits[0], qubits[1];
barrier qubits;

// Z encodes phase bit 1; omitting X encodes flip bit 0.
z qubits[0];
barrier qubits;

// Bob maps the four Bell states to distinct computational-basis states.
cx qubits[0], qubits[1];
h qubits[0];

// Index order is phase bit then flip bit: results[0]=1, results[1]=0.
results[0] = measure qubits[0];
results[1] = measure qubits[1];
