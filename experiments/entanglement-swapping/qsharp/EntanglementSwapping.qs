/// Use the same four-wire preparation for sampling and full-state diagnostics.
operation PrepareSwapping(qubits : Qubit[]) : Unit {
    H(qubits[0]);
    CNOT(qubits[0], qubits[1]);
    H(qubits[2]);
    CNOT(qubits[2], qubits[3]);

    // Bob holds qubits 1 and 2; these gates change to the Bell-measurement basis.
    CNOT(qubits[1], qubits[2]);
    H(qubits[1]);

    // Deferred controls model classical feed-forward, not remote physical gates.
    CNOT(qubits[2], qubits[3]);
    CZ(qubits[1], qubits[3]);
}

/// Return only Alice and Charlie's terminal results in that explicit order.
operation Main() : (Result, Result) {
    use qubits = Qubit[4];
    PrepareSwapping(qubits);
    let results = (M(qubits[0]), M(qubits[3]));
    ResetAll(qubits);
    return results;
}
