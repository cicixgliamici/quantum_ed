import numpy as np
from quantum_ed.channels import depolarize_rho, dephase_rho, is_density_matrix

def test_depolarize_trace():
    rho = np.array([[1,0],[0,0]], dtype=complex)
    out = depolarize_rho(rho, p=0.2)
    assert np.allclose(np.trace(out), 1.0)
    assert is_density_matrix(out)

def test_dephase_offdiag():
    rho = np.array([[0.5,0.5],[0.5,0.5]], dtype=complex)
    out = dephase_rho(rho, p=1.0)
    assert abs(out[0,1]) < 1e-12
    assert abs(out[1,0]) < 1e-12
    assert np.allclose(np.trace(out), 1.0)
