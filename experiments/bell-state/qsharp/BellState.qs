/// Prepare, measure, and release a Bell pair.
operation Main() : (Result, Result) {
    // Q# owns the lifetime of qubits allocated inside a use block.
    use qubits = Qubit[2];

    // H creates superposition; CNOT converts it into Bell correlations.
    H(qubits[0]);
    CNOT(qubits[0], qubits[1]);

    // Individual measurements preserve the relationship between array indexes.
    let results = (M(qubits[0]), M(qubits[1]));

    // Explicit reset documents the lifecycle expected by quantum simulators.
    ResetAll(qubits);
    return results;
}
