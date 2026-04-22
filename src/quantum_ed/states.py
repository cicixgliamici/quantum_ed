"""State vectors and Bloch sphere utilities."""

from __future__ import annotations
import numpy as np
from .linalg import dagger

StateVector = np.ndarray

def ket0() -> np.ndarray:
    return np.array([[1.0],[0.0]], dtype=complex)

def ket1() -> np.ndarray:
    return np.array([[0.0],[1.0]], dtype=complex)

def basis_00() -> StateVector:
    """Return the two-qubit basis state |00>."""
    return np.kron(ket0(), ket0())


def basis_01() -> StateVector:
    """Return the two-qubit basis state |01>."""
    return np.kron(ket0(), ket1())


def basis_10() -> StateVector:
    """Return the two-qubit basis state |10>."""
    return np.kron(ket1(), ket0())


def basis_11() -> StateVector:
    """Return the two-qubit basis state |11>."""
    return np.kron(ket1(), ket1())


def bell_phi_plus() -> StateVector:
    """Return the Bell state (|00> + |11>) / sqrt(2)."""
    return (1 / np.sqrt(2)) * np.array([[1], [0], [0], [1]], dtype=complex)


def bell_phi_minus() -> StateVector:
    """Return the Bell state (|00> - |11>) / sqrt(2)."""
    return (1 / np.sqrt(2)) * np.array([[1], [0], [0], [-1]], dtype=complex)


def bell_psi_plus() -> StateVector:
    """Return the Bell state (|01> + |10>) / sqrt(2)."""
    return (1 / np.sqrt(2)) * np.array([[0], [1], [1], [0]], dtype=complex)


def bell_psi_minus() -> StateVector:
    """Return the Bell state (|01> - |10>) / sqrt(2)."""
    return (1 / np.sqrt(2)) * np.array([[0], [1], [-1], [0]], dtype=complex)

def normalize(ket: np.ndarray, atol: float = 1e-12) -> np.ndarray:
    """Normalize a ket; raise if norm is ~0."""
    nrm = np.sqrt((dagger(ket) @ ket).item())
    if abs(nrm) < atol:
        raise ValueError("Cannot normalize a near-zero vector.")
    return ket / nrm

def bloch_vector(ket: np.ndarray) -> np.ndarray:
    """Return the Bloch vector r for a *pure* qubit state |psi>.

    For a density matrix rho:
      r_i = Tr(rho * sigma_i)
    For a pure state, rho = |psi><psi|.

    Returns: np.array([rx, ry, rz]) as floats.
    """
    ket = normalize(ket)
    a = ket[0,0]
    b = ket[1,0]
    # Standard formula
    rx = 2.0 * np.real(np.conjugate(a) * b)
    ry = 2.0 * np.imag(np.conjugate(a) * b)
    rz = (abs(a)**2 - abs(b)**2).real
    return np.array([rx, ry, rz], dtype=float)

def state_from_bloch(theta: float, phi: float) -> np.ndarray:
    """Create a pure qubit state from Bloch angles (theta, phi).

    |psi> = cos(theta/2)|0> + e^{i phi} sin(theta/2)|1>
    """
    a = np.cos(theta/2.0)
    b = np.exp(1j*phi) * np.sin(theta/2.0)
    return normalize(np.array([[a],[b]], dtype=complex))
