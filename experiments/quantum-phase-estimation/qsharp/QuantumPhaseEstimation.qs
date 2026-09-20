import Std.Math.*;
import Std.Measurement.*;

/// Apply quantum phase estimation for the T gate on eigenstate |1>.
operation Main() : Result[] {
    use counting = Qubit[3];
    use target = Qubit();

    // Prepare target in eigenstate |1>
    X(target);

    // Initialize counting register in uniform superposition
    for q in counting {
        H(q);
    }

    // Controlled-U^(2^j) operations
    Controlled R1([counting[0]], (PI() / 4.0, target));
    Controlled R1([counting[1]], (PI() / 2.0, target));
    Controlled R1([counting[2]], (PI(), target));

    // Inverse QFT on counting register
    SWAP(counting[0], counting[2]);
    H(counting[0]);
    Controlled R1([counting[1]], (-PI() / 2.0, counting[0]));
    Controlled R1([counting[2]], (-PI() / 4.0, counting[0]));
    H(counting[1]);
    Controlled R1([counting[2]], (-PI() / 2.0, counting[1]));
    H(counting[2]);

    // Reset target qubit before release
    Reset(target);

    // Measure counting register: returns [One, Zero, Zero] for counting[0]=One
    return MResetEachZ(counting);
}
