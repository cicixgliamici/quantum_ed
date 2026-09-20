"""Compile every declared Q# experiment in an isolated interpreter state."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Set telemetry policy before importing the QDK, which initializes its runtime.
os.environ.setdefault("QDK_PYTHON_TELEMETRY", "none")

from qdk import qsharp

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def qsharp_sources() -> list[Path]:
    """Return Q# entrypoints declared by experiment manifests."""
    sources: list[Path] = []
    for path in sorted((REPOSITORY_ROOT / "experiments").glob("*/experiment.json")):
        manifest = json.loads(path.read_text(encoding="utf-8"))
        sources.append(REPOSITORY_ROOT / manifest["implementations"]["qsharp"])
    return sources


def validate_source(source: Path) -> None:
    """Compile one standalone Q# file without leaking its Main operation."""
    # Each example defines Main, so a fresh interpreter avoids symbol collisions.
    qsharp.init()
    qsharp.eval(source.read_text(encoding="utf-8"))


def main() -> int:
    """Compile every source and print an actionable failure location."""
    for source in qsharp_sources():
        try:
            validate_source(source)
        except Exception as error:  # QDK exception classes can change across releases.
            print(f"Q# validation failed for {source.relative_to(REPOSITORY_ROOT)}: {error}")
            return 1
        print(f"Compiled {source.relative_to(REPOSITORY_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
