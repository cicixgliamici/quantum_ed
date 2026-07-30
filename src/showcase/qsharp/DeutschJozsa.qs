import Std.Measurement.*;

/// Classify the promised function f(x) = x_0 with Deutsch-Jozsa.
operation Main() : Result[] {
    // Three inputs plus one output match the oracle signature U_f|x>|y>.
    use inputs = Qubit[3];
    use output = Qubit();

    // X and H prepare |->, the phase-kickback eigenstate of X.
    X(output);

    // The inputs must cover every computational basis state coherently.
    for input in inputs {
        H(input);
    }
    H(output);

    // This controlled-X implements a balanced oracle.
    CNOT(inputs[0], output);

    // Interference reveals whether the oracle phases cancel.
    for input in inputs {
        H(input);
    }

    // MResetEach measures in array order and safely returns inputs to |0>.
    let results = MResetEach(inputs);

    // The unmeasured output must also be reset before leaving its use scope.
    Reset(output);
    return results;
}
