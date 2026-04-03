import numpy as np
from quantum_ed.linalg import is_unitary
from quantum_ed.gates import I, X, Y, Z, H, S, T, CNOT

def test_unitary_1q():
    for g in [I, X, Y, Z, H, S, T]:
        assert is_unitary(g)

def test_unitary_cnot():
    assert is_unitary(CNOT)
