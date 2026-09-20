"""Execute every declared NumPy experiment as a standalone entrypoint."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def numpy_sources() -> list[Path]:
    """Return NumPy entrypoints declared by experiment manifests."""
    sources: list[Path] = []
    for path in sorted((REPOSITORY_ROOT / "experiments").glob("*/experiment.json")):
        manifest = json.loads(path.read_text(encoding="utf-8"))
        sources.append(REPOSITORY_ROOT / manifest["implementations"]["numpy"])
    return sources


def main() -> int:
    """Execute each entrypoint and preserve its failure status."""
    for source in numpy_sources():
        result = subprocess.run(
            [sys.executable, str(source)],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"NumPy validation failed for {source.relative_to(REPOSITORY_ROOT)}")
            print(result.stderr)
            return result.returncode
        print(f"Executed {source.relative_to(REPOSITORY_ROOT)}: {result.stdout.strip()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
