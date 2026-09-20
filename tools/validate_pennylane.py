"""Execute every declared PennyLane experiment entrypoint."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def sources() -> list[Path]:
    """Return optional PennyLane entrypoints declared by manifests."""
    entrypoints: list[Path] = []
    for path in sorted((REPOSITORY_ROOT / "experiments").glob("*/experiment.json")):
        manifest = json.loads(path.read_text(encoding="utf-8"))
        relative_path = manifest["implementations"].get("pennylane")
        if relative_path:
            entrypoints.append(REPOSITORY_ROOT / relative_path)
    return entrypoints


def main() -> int:
    """Execute each entrypoint in a separate process."""
    for source in sources():
        result = subprocess.run(
            [sys.executable, str(source)],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"PennyLane validation failed for {source.relative_to(REPOSITORY_ROOT)}")
            print(result.stderr)
            return result.returncode
        print(f"Executed {source.relative_to(REPOSITORY_ROOT)}: {result.stdout.strip()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
