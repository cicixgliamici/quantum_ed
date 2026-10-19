/// Teleport |1> using coherent controls in place of classical corrections.
operation PrepareTeleportation(theta : Double, phi : Double, qubits : Qubit[]) : Unit {

    // Qubit 0 is the message; qubits 1 and 2 form the communication resource.
    // Ry followed by R1 prepares cos(theta/2)|0> + exp(i phi)sin(theta/2)|1>.
    Ry(theta, qubits[0]);
    R1(phi, qubits[0]);
    H(qubits[1]);
    CNOT(qubits[1], qubits[2]);

    // Alice performs the Bell-basis interaction on her two qubits.
    CNOT(qubits[0], qubits[1]);
    H(qubits[0]);

    // Quantum controls are the deferred form of the two classical corrections.
    CNOT(qubits[1], qubits[2]);
    CZ(qubits[0], qubits[2]);
}

/// Keep the portable entrypoint's default message |1>.
operation Main() : Result {
    use qubits = Qubit[3];
    PrepareTeleportation(Std.Math.PI(), 0.0, qubits);

    // Bob's qubit deterministically contains the original state |1>.
    let result = M(qubits[2]);
    ResetAll(qubits);
    return result;
}
