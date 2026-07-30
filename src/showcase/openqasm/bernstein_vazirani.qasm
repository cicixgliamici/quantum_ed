OPENQASM 3.0;
include "stdgates.inc";

qubit[3] inputs;
qubit output;
bit[3] results;

// Prepare |-> on the output and uniform superposition on the inputs.
x output;
h inputs;
h output;

// Controls 0 and 2 encode the secret 101 in qubit-index order.
cx inputs[0], output;
cx inputs[2], output;

// The final H layer decodes the phase pattern into the state |101>.
h inputs;

// Each input qubit is measured into the classical bit with the same index.
results = measure inputs;
