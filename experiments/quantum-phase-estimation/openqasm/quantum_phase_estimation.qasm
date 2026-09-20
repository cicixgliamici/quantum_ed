OPENQASM 3.0;
include "stdgates.inc";

qubit[3] counting;
qubit target;
bit[3] results;

// Prepare target in eigenstate |1>
x target;

// Initialize counting register in uniform superposition
h counting[0];
h counting[1];
h counting[2];

// Controlled-U^(2^j) operations
cp(pi / 4) counting[0], target;
cp(pi / 2) counting[1], target;
cp(pi) counting[2], target;

// Inverse QFT on counting register
swap counting[0], counting[2];
h counting[0];
cp(-pi / 2) counting[1], counting[0];
cp(-pi / 4) counting[2], counting[0];
h counting[1];
cp(-pi / 2) counting[2], counting[1];
h counting[2];

results = measure counting;
