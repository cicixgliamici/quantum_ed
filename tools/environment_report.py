"""Record the actual interpreter, installed distributions, and lockfile fingerprint."""

from __future__ import annotations

import argparse
import hashlib
from importlib import metadata
import json
from pathlib import Path
import platform
import sys

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def lock_fingerprint() -> str:
    """Normalize Git line endings so Windows and Linux identify the same lock."""
    contents = (REPOSITORY_ROOT / "uv.lock").read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(contents).hexdigest()


def project_installation(require_wheel: bool) -> dict:
    """Reject source-tree imports when a normal package installation is required."""
    import quantum_ed

    distribution = metadata.distribution("quantum-ed")
    direct_url = json.loads(distribution.read_text("direct_url.json") or "{}")
    editable = direct_url.get("dir_info", {}).get("editable", False)
    module_path = Path(quantum_ed.__file__).resolve()
    in_environment = module_path.is_relative_to(Path(sys.prefix).resolve())
    if require_wheel and (editable or not in_environment):
        raise ValueError(f"Expected a noneditable package inside {sys.prefix}; imported {module_path}")
    return {"version": distribution.version, "editable": editable,
            "inside_environment": in_environment}


def build_report(require_wheel: bool = False) -> dict:
    """Inventory installed packages, not just the intended dependency versions."""
    packages = {distribution.metadata["Name"].lower().replace("_", "-"): distribution.version
                for distribution in metadata.distributions() if distribution.metadata["Name"]}
    return {
        "schema_version": 1,
        "python": {"version": platform.python_version(), "implementation": platform.python_implementation()},
        "platform": {"system": platform.system(), "release": platform.release(), "machine": platform.machine()},
        "lock_sha256_lf": lock_fingerprint(),
        "project": project_installation(require_wheel),
        "packages": dict(sorted(packages.items())),
    }


def main() -> None:
    """Use --require-wheel with isolated Python to check CI's installation mode."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("build/reproducibility/environment.json"))
    parser.add_argument("--require-wheel", action="store_true")
    arguments = parser.parse_args()
    report = build_report(arguments.require_wheel)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Recorded Python {report['python']['version']} and {len(report['packages'])} packages")
    print(f"Noneditable environment installation: {not report['project']['editable'] and report['project']['inside_environment']}")
    print(f"Environment report: {arguments.output}")


if __name__ == "__main__":
    main()
