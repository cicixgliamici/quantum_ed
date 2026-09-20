"""Validate experiment contracts and local Markdown links."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS_ROOT = REPOSITORY_ROOT / "experiments"
REQUIRED_ECOSYSTEMS = {"numpy", "qiskit", "qsharp", "openqasm"}
OPTIONAL_ECOSYSTEMS = {"pennylane"}
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
EXPERIMENT_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def load_manifest(path: Path) -> dict[str, Any]:
    """Load one experiment manifest and report malformed JSON clearly."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read {path.relative_to(REPOSITORY_ROOT)}: {error}") from error


def validate_manifest(path: Path) -> list[str]:
    """Return contract violations for one experiment manifest."""
    manifest = load_manifest(path)
    experiment_dir = path.parent
    errors: list[str] = []

    required_fields = {
        "schema_version",
        "name",
        "category",
        "theory",
        "expected_result",
        "implementations",
    }
    manifest_fields = set(manifest)
    missing_fields = required_fields - manifest_fields
    if missing_fields:
        errors.append(f"{path}: missing fields {sorted(missing_fields)}")
        return errors
    extra_fields = manifest_fields - required_fields
    if extra_fields:
        errors.append(f"{path}: unknown fields {sorted(extra_fields)}")

    if manifest["schema_version"] != 1:
        errors.append(f"{path}: unsupported schema_version")
    if manifest["name"] != experiment_dir.name:
        errors.append(f"{path}: name must match directory {experiment_dir.name!r}")
    if not isinstance(manifest["name"], str) or not EXPERIMENT_NAME.fullmatch(manifest["name"]):
        errors.append(f"{path}: name must use lowercase kebab-case")
    if not isinstance(manifest["category"], str) or not manifest["category"].strip():
        errors.append(f"{path}: category cannot be empty")

    readme = experiment_dir / "README.md"
    if not readme.is_file():
        errors.append(f"{experiment_dir}: README.md is required")

    theory = REPOSITORY_ROOT / str(manifest["theory"])
    if not theory.is_file():
        errors.append(f"{path}: theory file does not exist: {manifest['theory']}")

    implementations = manifest["implementations"]
    if not isinstance(implementations, dict):
        errors.append(f"{path}: implementations must be an object")
        return errors

    ecosystems = set(implementations)
    missing_ecosystems = REQUIRED_ECOSYSTEMS - ecosystems
    unknown_ecosystems = ecosystems - REQUIRED_ECOSYSTEMS - OPTIONAL_ECOSYSTEMS
    if missing_ecosystems:
        errors.append(f"{path}: missing implementations {sorted(missing_ecosystems)}")
    if unknown_ecosystems:
        errors.append(f"{path}: unknown implementations {sorted(unknown_ecosystems)}")

    for ecosystem, relative_path in implementations.items():
        if not isinstance(relative_path, str):
            errors.append(f"{path}: {ecosystem} source must be a string")
            continue
        source = REPOSITORY_ROOT / relative_path
        if not source.is_file():
            errors.append(f"{path}: missing {ecosystem} source: {relative_path}")
        if source.parent.name != ecosystem:
            errors.append(f"{path}: {ecosystem} source must be inside its ecosystem directory")

    if not str(manifest["expected_result"]).strip():
        errors.append(f"{path}: expected_result cannot be empty")
    return errors


def is_external_link(target: str) -> bool:
    """Return whether a Markdown target is intentionally not local."""
    return target.startswith(("http://", "https://", "mailto:", "#"))


def validate_markdown_links(path: Path) -> list[str]:
    """Return broken local links found in one Markdown document."""
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    for match in MARKDOWN_LINK.finditer(text):
        target = match.group(1).strip()
        if is_external_link(target):
            continue

        # Anchors do not affect whether the referenced local file exists.
        file_target = target.split("#", maxsplit=1)[0]
        if file_target and not (path.parent / file_target).resolve().exists():
            relative_document = path.relative_to(REPOSITORY_ROOT)
            errors.append(f"{relative_document}: broken link {target!r}")
    return errors


def collect_errors() -> list[str]:
    """Run every repository-level structural validation."""
    errors: list[str] = []
    manifests = sorted(EXPERIMENTS_ROOT.glob("*/experiment.json"))
    experiment_dirs = sorted(path for path in EXPERIMENTS_ROOT.iterdir() if path.is_dir())

    if len(manifests) != len(experiment_dirs):
        errors.append("every experiment directory must contain experiment.json")
    for manifest in manifests:
        errors.extend(validate_manifest(manifest))
    for document in REPOSITORY_ROOT.rglob("*.md"):
        if ".git" not in document.parts and ".venv" not in document.parts:
            errors.extend(validate_markdown_links(document))
    return errors


def main() -> int:
    """Print a concise validation report and return a process status."""
    try:
        errors = collect_errors()
    except ValueError as error:
        errors = [str(error)]

    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    experiment_count = len(list(EXPERIMENTS_ROOT.glob("*/experiment.json")))
    print(f"Repository validation passed for {experiment_count} experiments.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
