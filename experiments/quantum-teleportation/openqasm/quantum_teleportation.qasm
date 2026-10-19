OPENQASM 3.0;
include "stdgates.inc";

qubit[3] qubits;
bit result;

// A reusable gate lets validation inspect arbitrary messages with the same protocol.
gate teleport message, alice, bob {
    h alice;
    cx alice, bob;
    // Alice's Bell-basis interaction precedes the deferred corrections.
    cx message, alice;
    h message;
    cx alice, bob;
    cz message, bob;
}

// The portable entrypoint keeps |1> as its default message.
x qubits[0];
teleport qubits[0], qubits[1], qubits[2];

// Bob's target qubit deterministically contains |1>.
result = measure qubits[2];
