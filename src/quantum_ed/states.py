"""State vectors and Bloch sphere utilities."""

from __future__ import annotations
import numpy as np
from ._validation import real_scalar, state_vector, tolerance

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
    """Normalize a finite qubit column vector; reject norms <= atol.

    This is an explicit rescaling operation, not a physical state evolution.
    """
    ket = state_vector(ket)
    atol = tolerance(atol)
    # Convert integers before abs: the smallest signed integer cannot be negated.
    ket = ket.astype(complex)
    # Scaling first avoids overflow/underflow when squaring finite amplitudes.
    scale = float(np.max(np.maximum(np.abs(ket.real), np.abs(ket.imag))))
    if scale == 0:
        raise ValueError("Cannot normalize a near-zero vector.")
    scaled = ket / scale
    scaled_norm = float(np.linalg.norm(scaled))
    if scale <= atol / scaled_norm:
        raise ValueError("Cannot normalize a near-zero vector.")
    return scaled / scaled_norm

def bloch_vector(ket: np.ndarray) -> np.ndarray:
    """Return the Bloch vector r for a *pure* qubit state |psi>.

    For a density matrix rho:
      r_i = Tr(rho * sigma_i)
    For a pure state, rho = |psi><psi|.

    Returns: np.array([rx, ry, rz]) as floats.
    """
    # Bloch coordinates describe one qubit; normalization is intentional here.
    ket = normalize(state_vector(ket, dimension=2))
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
    theta = real_scalar(theta, "theta")
    phi = real_scalar(phi, "phi")
    a = np.cos(theta/2.0)
    b = np.exp(1j*phi) * np.sin(theta/2.0)
    return normalize(np.array([[a],[b]], dtype=complex))
