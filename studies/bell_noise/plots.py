"""Export readable scientific figures using a noninteractive Matplotlib backend."""

from pathlib import Path

import matplotlib

# Batch generation must work on CI without a display or notebook kernel.
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .metrics import measure_state
from .numpy_model import CHANNELS, noisy_bell_state
from .theory import DEPOLARIZING_THRESHOLD

COLORS = {"dephasing": "#007e87", "depolarizing": "#4568b0", "amplitude_damping": "#c05c15"}
LABELS = {"dephasing": "Dephasing", "depolarizing": "Depolarizing", "amplitude_damping": "Amplitude damping"}
STYLE = {"font.family": "DejaVu Sans", "font.size": 11, "axes.spines.top": False,
         "axes.spines.right": False, "svg.hashsalt": "quantum-ed-bell-noise"}


def save_figure(figure, output_dir: Path, name: str) -> None:
    """Keep raster previews and scalable exports with stable SVG identifiers."""
    figure.savefig(output_dir / f"{name}.png", dpi=220, facecolor="white")
    figure.savefig(output_dir / f"{name}.svg", facecolor="white", metadata={"Date": None})
    plt.close(figure)


def plot_channel(axis, rows: list[dict], channel: str, metric: str) -> None:
    """Use sparse SDK markers to reveal overlap without covering the curves."""
    numpy_rows = [row for row in rows if row["model"] == "numpy" and row["channel"] == channel]
    sdk_rows = [row for row in rows if row["model"] == "pennylane" and row["channel"] == channel]
    linestyle = "--" if channel == "amplitude_damping" else "-"
    axis.plot([row["probability"] for row in numpy_rows], [row[metric] for row in numpy_rows],
              label=LABELS[channel], color=COLORS[channel], linestyle=linestyle, linewidth=2.2)
    if sdk_rows:
        stride = max(1, (len(sdk_rows) - 1) // 10)
        sampled = sdk_rows[::stride]
        marker = "s" if channel == "amplitude_damping" else "o"
        axis.scatter([row["probability"] for row in sampled], [row[metric] for row in sampled],
                     edgecolors=COLORS[channel], facecolors="none", marker=marker, s=32, zorder=3)


def plot_metrics(rows: list[dict], output_dir: Path) -> None:
    """Show why fidelity, entanglement, and purity answer different questions."""
    with plt.rc_context(STYLE):
        figure, axes = plt.subplots(1, 3, figsize=(14.4, 4.8))
        metrics = [("fidelity", "Fidelity to the Bell pair", (-0.02, 1.04)),
                   ("negativity", "Entanglement negativity", (-0.015, 0.525)),
                   ("purity", "Purity", (0.22, 1.04))]
        for axis, (metric, title, limits) in zip(axes, metrics):
            for channel in CHANNELS:
                plot_channel(axis, rows, channel, metric)
            axis.set(title=title, xlabel="Local noise strength p", ylim=limits, xlim=(0, 1))
            axis.grid(alpha=0.17)
        axes[0].legend(frameon=False, loc="lower left", fontsize=10)
        axes[1].axvline(DEPOLARIZING_THRESHOLD, color="#64748b", linewidth=1, linestyle=":")
        axes[1].text(DEPOLARIZING_THRESHOLD + 0.025, 0.45, "$p_* \\approx 0.423$", fontsize=10)
        figure.suptitle("One Bell pair, three independent local noise models", fontsize=16, weight="bold", y=0.98)
        caption = ("Lines: NumPy  |  Open markers: PennyLane  |  Dashed: amplitude damping"
                   if any(row["model"] == "pennylane" for row in rows)
                   else "Lines: NumPy only  |  Dashed: amplitude damping  |  SDK comparison not performed")
        figure.text(0.5, 0.015, caption, ha="center", fontsize=10, color="#475569")
        figure.tight_layout(rect=(0, 0.055, 1, 0.91))
        save_figure(figure, output_dir, "metrics")


def plot_coherence(output_dir: Path) -> None:
    """Keep all heatmaps on the same scale and show unchanged Z-basis probabilities."""
    with plt.rc_context(STYLE):
        figure, axes = plt.subplots(2, 3, figsize=(11.7, 7), layout="constrained")
        labels = ["00", "01", "10", "11"]
        for column, probability in enumerate((0, 0.5, 1)):
            state = noisy_bell_state("dephasing", probability)
            metrics = measure_state(state)
            axis = axes[0, column]
            image = axis.imshow(np.abs(state), vmin=0, vmax=0.5, cmap="viridis")
            axis.set(xticks=range(4), yticks=range(4), xticklabels=labels, yticklabels=labels,
                     title=f"p = {probability:g}   |   F = {metrics['fidelity']:.3f}   |   N = {metrics['negativity']:.3f}")
            for row in range(4):
                for col in range(4):
                    value = abs(state[row, col])
                    axis.text(col, row, f"{value:.3g}", ha="center", va="center",
                              color="black" if value > 0.3 else "white", fontsize=10)
            axes[1, column].bar(labels, np.diag(state).real, color=COLORS["dephasing"], width=0.62)
            axes[1, column].set(ylim=(0, 0.6), xlabel="Z-basis outcome", ylabel="Probability")
            axes[1, column].grid(axis="y", alpha=0.17)
        figure.colorbar(image, ax=list(axes[0]), shrink=0.8, label="Density-matrix magnitude")
        figure.suptitle("Identical Z-basis probabilities can hide lost entanglement", fontsize=15, weight="bold")
        save_figure(figure, output_dir, "coherence")
