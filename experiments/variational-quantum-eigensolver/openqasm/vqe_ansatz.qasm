OPENQASM 3.0;
include "stdgates.inc";

qubit qubit_under_test;
bit result;

// The classical optimizer has selected theta=pi for the RY ansatz.
ry(pi) qubit_under_test;
result = measure qubit_under_test;
