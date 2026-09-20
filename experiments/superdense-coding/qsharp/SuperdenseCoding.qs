import Std.Measurement.*;

/// Transmit the logical message 10 through a shared Bell pair.
operation Main() : Result[] {
    use qubits = Qubit[2];

    // Alice and Bob share Phi-plus before communication begins.
    H(qubits[0]);
    CNOT(qubits[0], qubits[1]);

    // The first message bit is one, so Alice changes the Bell-state phase.
    // The second bit is zero, so no X operation is required.
    Z(qubits[0]);

    // Bob decodes the Bell state after receiving Alice's qubit.
    CNOT(qubits[0], qubits[1]);
    H(qubits[0]);

    // Array order reports the phase bit followed by the flip bit: 10.
    return MResetEachZ(qubits);
}
