import numpy as np
from quantum_ed.states import ket0, ket1, normalize
from quantum_ed.measurement import probs_comp_basis

def test_probs_basis_states():
    p0, p1 = probs_comp_basis(ket0())
    assert abs(p0 - 1.0) < 1e-12 and abs(p1 - 0.0) < 1e-12

    p0, p1 = probs_comp_basis(ket1())
    assert abs(p0 - 0.0) < 1e-12 and abs(p1 - 1.0) < 1e-12

def test_probs_superposition():
    psi = normalize(np.array([[1.0],[1.0]], dtype=complex))
    p0, p1 = probs_comp_basis(psi)
    assert abs(p0 - 0.5) < 1e-12 and abs(p1 - 0.5) < 1e-12
