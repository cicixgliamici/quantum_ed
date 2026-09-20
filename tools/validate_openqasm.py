"""Parse every declared OpenQASM 3 experiment with Qiskit."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from qiskit import qasm3

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def openqasm_sources() -> list[Path]:
    """Return OpenQASM entrypoints declared by experiment manifests."""
    sources: list[Path] = []
    for path in sorted((REPOSITORY_ROOT / "experiments").glob("*/experiment.json")):
        manifest = json.loads(path.read_text(encoding="utf-8"))
        sources.append(REPOSITORY_ROOT / manifest["implementations"]["openqasm"])
    return sources


def main() -> int:
    """Parse each source and fail immediately with its repository path."""
    for source in openqasm_sources():
        try:
            qasm3.load(source)
        except Exception as error:  # The importer exposes several version-specific errors.
            print(f"OpenQASM validation failed for {source.relative_to(REPOSITORY_ROOT)}: {error}")
            return 1
        print(f"Parsed {source.relative_to(REPOSITORY_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
