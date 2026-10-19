import Std.Math.*;
import Std.Measurement.*;

/// Apply the three-qubit QFT to the basis state 001.
operation PrepareQft(inputValue : Int, qubits : Qubit[]) : Unit {
    // Logical integer labels use qubits[0] as the most significant bit.
    for wire in 0..2 {
        if (inputValue &&& (1 <<< (2 - wire))) != 0 {
            X(qubits[wire]);
        }
    }

    H(qubits[0]);
    Controlled R1([qubits[1]], (PI() / 2.0, qubits[0]));
    Controlled R1([qubits[2]], (PI() / 4.0, qubits[0]));
    H(qubits[1]);
    Controlled R1([qubits[2]], (PI() / 2.0, qubits[1]));
    H(qubits[2]);
    SWAP(qubits[0], qubits[2]);
}

/// Measure the same preparation inspected by the phase-sensitive validator.
operation Main() : Result[] {
    use qubits = Qubit[3];
    PrepareQft(1, qubits);

    // QFT phases produce a uniform computational-basis distribution here.
    return MResetEachZ(qubits);
}
