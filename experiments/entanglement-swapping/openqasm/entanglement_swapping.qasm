OPENQASM 3.0;
include "stdgates.inc";

qubit[4] qubits;
bit[2] result;

// One shared gate supports both the executable entrypoint and state diagnostics.
gate swap_entanglement alice, bob_left, bob_right, charlie {
    h alice;
    cx alice, bob_left;
    h bob_right;
    cx bob_right, charlie;
    cx bob_left, bob_right;
    h bob_left;
    // Coherent controls are the deferred representation of classical corrections.
    cx bob_right, charlie;
    cz bob_left, charlie;
}

swap_entanglement qubits[0], qubits[1], qubits[2], qubits[3];
result[0] = measure qubits[0];
result[1] = measure qubits[3];
