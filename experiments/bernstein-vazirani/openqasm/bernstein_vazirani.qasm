OPENQASM 3.0;
include "stdgates.inc";

qubit[3] inputs;
qubit ancilla;
bit[3] results;

// Prepare |-> on the output and uniform superposition on the inputs.
x ancilla;
h inputs;
h ancilla;

// Controls 0 and 2 encode the secret 101 in qubit-index order.
cx inputs[0], ancilla;
cx inputs[2], ancilla;

// The final H layer decodes the phase pattern into the state |101>.
h inputs;

// Each input qubit is measured into the classical bit with the same index.
results = measure inputs;
