OPENQASM 3.0;
include "stdgates.inc";

qubit[3] inputs;
qubit ancilla;
bit[3] results;

// X followed by H prepares the output in |-> for phase kickback.
x ancilla;

// A register-wide H creates a uniform superposition of all inputs.
h inputs;
h ancilla;

// This controlled-X implements the balanced function f(x) = x_0.
cx inputs[0], ancilla;

// Interference maps the oracle's phase pattern to measurable bits.
h inputs;

// The output is intentionally omitted because it carries no classification.
results = measure inputs;
