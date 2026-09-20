import Std.Math.*;

/// Prepare the optimal RY(pi)|0> ansatz for the Hamiltonian Z.
operation Main() : Result {
    use qubit = Qubit();
    Ry(PI(), qubit);
    let result = M(qubit);
    Reset(qubit);
    return result;
}
