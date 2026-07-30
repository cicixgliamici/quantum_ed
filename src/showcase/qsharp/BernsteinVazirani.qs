import Std.Measurement.*;

/// Recover the hidden string 101 in qubit-index order.
operation Main() : Result[] {
    // Array indexes define the documented secret-bit order.
    use inputs = Qubit[3];
    use output = Qubit();

    // The output starts in |-> so target flips become relative phases.
    X(output);

    // A uniform input superposition lets one oracle call encode every bit.
    for input in inputs {
        H(input);
    }
    H(output);

    // Controls 0 and 2 encode the nonzero bits of the secret.
    CNOT(inputs[0], output);
    CNOT(inputs[2], output);

    // The second Hadamard layer maps the phase pattern to |101>.
    for input in inputs {
        H(input);
    }

    // Measurement returns [One, Zero, One] in input-array order.
    let results = MResetEach(inputs);
    Reset(output);
    return results;
}
