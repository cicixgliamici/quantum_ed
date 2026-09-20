import Std.Measurement.*;

/// Find the marked state 11 with one two-qubit Grover iteration.
operation Main() : Result[] {
    use qubits = Qubit[2];
    H(qubits[0]);
    H(qubits[1]);

    // CZ is the phase oracle for the marked state 11.
    CZ(qubits[0], qubits[1]);

    // This gate sequence implements reflection about the uniform state.
    H(qubits[0]);
    H(qubits[1]);
    X(qubits[0]);
    X(qubits[1]);
    CZ(qubits[0], qubits[1]);
    X(qubits[0]);
    X(qubits[1]);
    H(qubits[0]);
    H(qubits[1]);
    return MResetEachZ(qubits);
}
