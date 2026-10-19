"""Validate the Bell-noise sweep and export data, figures, and provenance."""

from __future__ import annotations

import argparse
import csv
import importlib.metadata
import json
from pathlib import Path
import platform

import numpy as np

from .metrics import measure_state
from .numpy_model import CHANNELS, noisy_bell_state
from .theory import DEPOLARIZING_THRESHOLD, predicted_metrics, predicted_state

ABSOLUTE_TOLERANCE = 1e-10
DEFAULT_OUTPUT = Path(__file__).resolve().parents[2] / "docs" / "assets" / "bell-noise"


def simulation_models(include_pennylane: bool) -> dict:
    """Never silently replace an unavailable independent comparison model."""
    models = {"numpy": noisy_bell_state}
    if include_pennylane:
        try:
            from .pennylane_model import noisy_bell_state as sdk_state
        except ModuleNotFoundError as error:
            raise RuntimeError('Install .[pennylane] or explicitly pass --numpy-only') from error
        models["pennylane"] = sdk_state
    return models


def evaluate_point(channel: str, probability: float, models: dict) -> list[dict]:
    """Check full matrices and independent metric formulas at each grid point."""
    expected_state = predicted_state(channel, probability)
    expected_metrics = predicted_metrics(channel, probability)
    states = {name: np.asarray(model(channel, probability)) for name, model in models.items()}
    pair_error = (float(np.max(np.abs(states["numpy"] - states["pennylane"])))
                  if "pennylane" in states else None)
    if pair_error is not None and pair_error > ABSOLUTE_TOLERANCE:
        raise AssertionError(f"Framework mismatch: {channel}, p={probability}: {pair_error}")
    rows = []
    for model, state in states.items():
        metrics = measure_state(state)  # Also checks physicality of every state.
        matrix_error = float(np.max(np.abs(state - expected_state)))
        metric_error = max(abs(metrics[key] - value) for key, value in expected_metrics.items())
        if max(matrix_error, metric_error) > ABSOLUTE_TOLERANCE:
            raise AssertionError(f"Theory mismatch: {model}/{channel}, p={probability}")
        rows.append({"channel": channel, "probability": probability, "model": model,
                     **metrics, "theory_matrix_max_abs_error": matrix_error,
                     "theory_metric_max_abs_error": metric_error,
                     "framework_matrix_max_abs_error": pair_error})
    return rows


def collect_results(points: int = 101, include_pennylane: bool = True) -> list[dict]:
    """Use an endpoint-inclusive deterministic grid; exact simulation needs no seed."""
    if isinstance(points, bool) or not isinstance(points, int) or points < 3:
        raise ValueError("points must be an integer of at least 3")
    models = simulation_models(include_pennylane)
    rows = []
    for channel in CHANNELS:
        for probability in np.linspace(0, 1, points):
            rows.extend(evaluate_point(channel, float(probability), models))
    return rows


def build_summary(rows: list[dict], points: int) -> dict:
    """Record measured agreement and distinguish a grid bracket from an exact threshold."""
    models = sorted({row["model"] for row in rows})
    versions = {name: importlib.metadata.version(name) for name in ["numpy", "scipy", "matplotlib"]}
    if "pennylane" in models:
        versions["pennylane"] = importlib.metadata.version("pennylane")
    depolarized = [row for row in rows if row["model"] == "numpy" and row["channel"] == "depolarizing"]
    entangled = [row["probability"] for row in depolarized if row["negativity"] > ABSOLUTE_TOLERANCE]
    separable = [row["probability"] for row in depolarized if row["negativity"] <= ABSOLUTE_TOLERANCE]
    return {
        "schema_version": 1, "models": models, "channels": list(CHANNELS),
        "points_per_channel": points, "states_checked": len(rows),
        "simulation": "exact density matrices; independent identical local channels; one application per wire",
        "wire_order": "q0 q1", "absolute_tolerance": ABSOLUTE_TOLERANCE,
        "theory_matrix_max_abs_error": max(row["theory_matrix_max_abs_error"] for row in rows),
        "theory_metric_max_abs_error": max(row["theory_metric_max_abs_error"] for row in rows),
        "framework_matrix_max_abs_error": (max(row["framework_matrix_max_abs_error"] for row in rows)
                                            if "pennylane" in models else None),
        "depolarizing_transition": {"analytical_threshold": float(DEPOLARIZING_THRESHOLD),
                                    "grid_last_entangled": max(entangled),
                                    "grid_first_numerically_separable": min(separable)},
        "environment": {"python": platform.python_version(), "packages": versions},
        "command": "python -m studies.bell_noise.run_study",
        "parameters": {"points": points, "numpy_only": "pennylane" not in models},
    }


def export_results(rows: list[dict], summary: dict, output_dir: Path) -> None:
    """Write reviewable source data alongside the standalone figures."""
    from .plots import plot_coherence, plot_metrics

    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "results.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    plot_metrics(rows, output_dir)
    plot_coherence(output_dir)


def main() -> None:
    """Require full comparison by default, with an explicit lightweight alternative."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--points", type=int, default=101)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--numpy-only", action="store_true")
    arguments = parser.parse_args()
    rows = collect_results(arguments.points, not arguments.numpy_only)
    summary = build_summary(rows, arguments.points)
    export_results(rows, summary, arguments.output_dir)
    print(f"Validated {len(rows)} states; models: {', '.join(summary['models'])}")
    print(f"Maximum theory matrix error: {summary['theory_matrix_max_abs_error']:.3e}")
    if summary["framework_matrix_max_abs_error"] is not None:
        print(f"Maximum NumPy/PennyLane matrix error: {summary['framework_matrix_max_abs_error']:.3e}")
    else:
        print("NumPy-only run: cross-framework comparison was not performed.")
    print(f"Artifacts: {arguments.output_dir.resolve()}")


if __name__ == "__main__":
    main()
