"""Check environment evidence and reject installation modes that hide packaging errors."""

import hashlib
import json
from pathlib import Path
import tomllib
from importlib.metadata import PackagePath
from types import SimpleNamespace

import pytest

from tools import environment_report


def test_wheel_rejects_tutorials_from_an_old_build_directory():
    distribution = SimpleNamespace(files=[
        PackagePath("quantum_ed/states.py"),
        PackagePath("showcase/qiskit/00_first_circuit.py"),
    ])
    with pytest.raises(ValueError, match="Clean build/lib"):
        environment_report.validate_wheel_contents(distribution)


def test_wheel_accepts_library_modules_and_distribution_metadata():
    distribution = SimpleNamespace(files=[
        PackagePath("quantum_ed/__init__.py"),
        PackagePath("quantum_ed/viz/bloch.py"),
        PackagePath("quantum_ed-0.1.0.dist-info/METADATA"),
    ])
    environment_report.validate_wheel_contents(distribution)


def test_bootstrap_resolver_matches_the_project_requirement():
    root = Path(__file__).resolve().parents[1]
    project = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    bootstrap = [line for line in (root / "tools/uv-requirement.txt").read_text().splitlines()
                 if line and not line.startswith("#")]
    assert bootstrap == [f"uv{project['tool']['uv']['required-version']}"]


def test_lock_fingerprint_is_stable_across_git_line_endings(tmp_path, monkeypatch):
    monkeypatch.setattr(environment_report, "REPOSITORY_ROOT", tmp_path)
    lockfile = tmp_path / "uv.lock"
    contents = b"version = 1\nrevision = 5\n"
    lockfile.write_bytes(contents)
    expected = environment_report.lock_fingerprint()
    lockfile.write_bytes(contents.replace(b"\n", b"\r\n"))
    assert environment_report.lock_fingerprint() == expected
    assert expected == hashlib.sha256(contents).hexdigest()


@pytest.mark.parametrize("editable,inside_environment", [(True, True), (False, False)])
def test_wheel_verification_rejects_editable_or_source_tree_imports(
    tmp_path, monkeypatch, editable, inside_environment
):
    import quantum_ed

    class Distribution:
        version = "0.1.0"

        def read_text(self, name):
            return json.dumps({"dir_info": {"editable": editable}})

    prefix = tmp_path / "venv"
    module_path = (prefix if inside_environment else tmp_path / "src") / "quantum_ed/__init__.py"
    monkeypatch.setattr(quantum_ed, "__file__", str(module_path))
    monkeypatch.setattr(environment_report.sys, "prefix", str(prefix))
    monkeypatch.setattr(environment_report.metadata, "distribution", lambda name: Distribution())
    with pytest.raises(ValueError, match="noneditable"):
        environment_report.project_installation(require_wheel=True)
