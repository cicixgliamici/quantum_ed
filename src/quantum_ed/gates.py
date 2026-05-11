"""Common quantum gates (NumPy matrices).

Conventions:
- States are column vectors |psi> with shape (2^n, 1)
- Gates are square matrices U with shape (2^n, 2^n)
- Apply gate: |psi'> = U |psi>

The module intentionally keeps the matrices explicit so that the
mathematical definitions remain easy to inspect.
"""

from __future__ import annotations

import numpy as np

from .linalg import kron as _kron

I = np.array([[1, 0], [0, 1]], dtype=complex)

X = np.array([[0, 1], [1, 0]], dtype=complex)

Y = np.array([[0, -1j], [1j, 0]], dtype=complex)

Z = np.array([[1, 0], [0, -1]], dtype=complex)

H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)

S = np.array([[1, 0], [0, 1j]], dtype=complex)

T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)

CNOT = np.array(
    [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
    ],
    dtype=complex,
)

CZ = np.array(
    [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, -1],
    ],
    dtype=complex,
)

SWAP = np.array(
    [
        [1, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
    ],
    dtype=complex,
)


def rx(theta: float) -> np.ndarray:
    """Return the one-qubit rotation Rx(theta)."""
    c = np.cos(theta / 2)
    s = np.sin(theta / 2)
    return np.array([[c, -1j * s], [-1j * s, c]], dtype=complex)


def ry(theta: float) -> np.ndarray:
    """Return the one-qubit rotation Ry(theta)."""
    c = np.cos(theta / 2)
    s = np.sin(theta / 2)
    return np.array([[c, -s], [s, c]], dtype=complex)


def rz(theta: float) -> np.ndarray:
    """Return the one-qubit rotation Rz(theta)."""
    return np.array(
        [[np.exp(-1j * theta / 2), 0], [0, np.exp(1j * theta / 2)]],
        dtype=complex,
    )


def kron_n(*ops: np.ndarray) -> np.ndarray:
    """Kronecker product for building n-qubit operators."""
    return _kron(*ops)


def apply(U: np.ndarray, ket: np.ndarray) -> np.ndarray:
    """Apply gate U to state ket."""
    return U @ ket
