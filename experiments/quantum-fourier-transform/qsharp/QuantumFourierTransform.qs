import Std.Math.*;
import Std.Measurement.*;

/// Apply the three-qubit QFT to the basis state 001.
operation Main() : Result[] {
    use qubits = Qubit[3];
    X(qubits[0]);

    H(qubits[0]);
    Controlled R1([qubits[1]], (PI() / 2.0, qubits[0]));
    Controlled R1([qubits[2]], (PI() / 4.0, qubits[0]));
    H(qubits[1]);
    Controlled R1([qubits[2]], (PI() / 2.0, qubits[1]));
    H(qubits[2]);
    SWAP(qubits[0], qubits[2]);

    // QFT phases produce a uniform computational-basis distribution here.
    return MResetEachZ(qubits);
}
