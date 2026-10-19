# Input contracts and normalization

The core toolkit uses finite numeric NumPy arrays. Qubit registers have
dimension `2**n`, with `n >= 1`. Invalid physical inputs raise `ValueError`
with an explanation instead of being silently repaired.

## State vectors

State vectors have shape `(2**n, 1)`. Flat vectors and row vectors are rejected,
except that `fidelity_pure` retains its documented flat-vector convenience.
`probs_comp_basis`, `measure_comp_basis`, and `bloch_vector` support exactly
one qubit, so they require shape `(2, 1)`.

Normalization is intentional only in these operations:

| Function | Normalization policy |
| --- | --- |
| `normalize` | Rescales a nonzero column vector to unit norm |
| `probs_comp_basis`, `measure_comp_basis` | Normalize the single-qubit input before computing probabilities |
| `bloch_vector` | Normalizes the single-qubit input before computing coordinates |
| `rho_from_ket`, `fidelity_pure` | Require unit norm; call `normalize` explicitly if rescaling is intended |
| `apply` | Preserves the scale implied by the supplied linear operator |

For example, `probs_comp_basis(np.array([[3.0], [4.0]]))` returns
`(0.36, 0.64)`. Passing a four-amplitude register raises `ValueError`;
it cannot be interpreted as a single qubit by dropping amplitudes.

`normalize` rejects norms less than or equal to `atol` (default `1e-12`).
Its tolerance must be finite and nonnegative; `atol=0` still rejects the zero
vector. Internal scaling avoids overflow when normalizing very large finite
amplitudes. Inputs are not modified.

## Density matrices

Density matrices must be square with dimension `2**n`, Hermitian, trace one,
and positive semidefinite. These conditions use absolute tolerance `1e-10`
and no relative tolerance; eigenvalues as small as `-1e-10` are accepted as
numerical roundoff. Pure-state normalization uses the same absolute tolerance.

Noise channels and `is_density_matrix` support only `(2, 2)` states.
`partial_trace_two_qubits` requires `(4, 4)` and `keep=0` or `keep=1`.
Fidelity and trace distance require matching dimensions. Partial trace does
not renormalize its result: valid input already has trace one.

`is_density_matrix` is a predicate: it returns `False` for invalid states
or invalid tolerances. Operations raise `ValueError` instead.

## Operators and scalar parameters

`apply` requires a finite square operator matching the state dimension.
It does not enforce unitarity, because observables and projectors are also
useful in the learning material. It neither validates nor restores unit norm.

Rotation/Bloch angles must be finite real scalars (radians). Noise
probabilities must also lie in `[0, 1]`. Complex values, arrays, and booleans
are rejected as scalar parameters, even if conversion would be possible.

The helpers in `quantum_ed.linalg` remain general linear-algebra primitives;
they do not enforce physical-state contracts. Use `rho_from_ket` when a
validated density matrix is required, and `projector` for a raw outer product.
