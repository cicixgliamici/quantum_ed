"""Measurement utilities (intro level).

We start with computational basis measurement for 1 qubit.
Later we can generalize to n qubits and arbitrary bases.
"""

from __future__ import annotations
import numpy as np
from .states import normalize, ket0, ket1

def probs_comp_basis(ket: np.ndarray) -> tuple[float, float]:
    """Return probabilities (p0, p1) for measuring a qubit in {|0>,|1>} basis."""
    ket = normalize(ket)
    a = ket[0,0]
    b = ket[1,0]
    p0 = float((abs(a)**2).real)
    p1 = float((abs(b)**2).real)
    # numeric safety
    s = p0 + p1
    if s != 0:
        p0, p1 = p0/s, p1/s
    return p0, p1

def measure_comp_basis(ket: np.ndarray, rng: np.random.Generator | None = None) -> tuple[int, np.ndarray]:
    """Measure a qubit in computational basis.

    Returns (outcome, post_state).
    """
    if rng is None:
        rng = np.random.default_rng()
    p0, p1 = probs_comp_basis(ket)
    outcome = int(rng.random() >= p0)  # 0 with prob p0 else 1
    post = ket0() if outcome == 0 else ket1()
    return outcome, post
