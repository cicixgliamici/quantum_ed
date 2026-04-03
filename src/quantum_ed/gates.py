"""Common quantum gates (NumPy matrices).

Conventions:
- States are column vectors |psi> with shape (2^n, 1)
- Gates are square matrices U with shape (2^n, 2^n)
- Apply gate: |psi'> = U |psi>
"""

from __future__ import annotations
import numpy as np
from .linalg import kron as _kron

I = np.array([[1,0],[0,1]], dtype=complex)
X = np.array([[0,1],[1,0]], dtype=complex)
Y = np.array([[0,-1j],[1j,0]], dtype=complex)
Z = np.array([[1,0],[0,-1]], dtype=complex)

H = (1/np.sqrt(2))*np.array([[1,1],[1,-1]], dtype=complex)

S = np.array([[1,0],[0,1j]], dtype=complex)
T = np.array([[1,0],[0,np.exp(1j*np.pi/4)]], dtype=complex)

CNOT = np.array([
    [1,0,0,0],
    [0,1,0,0],
    [0,0,0,1],
    [0,0,1,0],
], dtype=complex)

def kron_n(*ops: np.ndarray) -> np.ndarray:
    """Kronecker product for building n-qubit operators."""
    return _kron(*ops)

def apply(U: np.ndarray, ket: np.ndarray) -> np.ndarray:
    """Apply gate U to state ket."""
    return U @ ket
