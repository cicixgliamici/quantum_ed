/// Teleport |1> using coherent controls in place of classical corrections.
operation Main() : Result {
    use qubits = Qubit[3];

    // Qubit 0 is the message; qubits 1 and 2 form the communication resource.
    X(qubits[0]);
    H(qubits[1]);
    CNOT(qubits[1], qubits[2]);

    // Alice performs the Bell-basis interaction on her two qubits.
    CNOT(qubits[0], qubits[1]);
    H(qubits[0]);

    // Quantum controls are the deferred form of the two classical corrections.
    CNOT(qubits[1], qubits[2]);
    CZ(qubits[0], qubits[2]);

    // Bob's qubit deterministically contains the original state |1>.
    let result = M(qubits[2]);
    ResetAll(qubits);
    return result;
}
