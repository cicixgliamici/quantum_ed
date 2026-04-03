"""Bloch sphere plotting (minimal matplotlib).

We intentionally keep this light; notebooks can call this helper.
"""

from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt

def plot_bloch_vector(r: np.ndarray, ax=None):
    """Plot a Bloch vector r = [x,y,z] on a Bloch sphere."""
    r = np.asarray(r, dtype=float)
    if r.shape != (3,):
        raise ValueError("r must have shape (3,)")

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

    # sphere wireframe
    u = np.linspace(0, 2*np.pi, 40)
    v = np.linspace(0, np.pi, 20)
    xs = np.outer(np.cos(u), np.sin(v))
    ys = np.outer(np.sin(u), np.sin(v))
    zs = np.outer(np.ones_like(u), np.cos(v))
    ax.plot_wireframe(xs, ys, zs, linewidth=0.5, alpha=0.3)

    # axes
    ax.plot([-1,1],[0,0],[0,0], linewidth=1)
    ax.plot([0,0],[-1,1],[0,0], linewidth=1)
    ax.plot([0,0],[0,0],[-1,1], linewidth=1)

    # vector
    ax.quiver(0,0,0, r[0], r[1], r[2], length=1.0, normalize=False)

    ax.set_xlim(-1,1); ax.set_ylim(-1,1); ax.set_zlim(-1,1)
    ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")
    ax.set_title("Bloch sphere")
    return ax
