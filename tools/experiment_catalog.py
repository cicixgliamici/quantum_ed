"""Generate repository and website experiment tables from the same contracts."""

import argparse
import json
from pathlib import Path
import sys

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
START_MARKER = "<!-- experiment-catalog:start -->"
END_MARKER = "<!-- experiment-catalog:end -->"
ECOSYSTEM_LABELS = {
    "numpy": "NumPy", "qiskit": "Qiskit", "pennylane": "PennyLane",
    "qsharp": "Q#", "openqasm": "OpenQASM 3",
}
CATALOG_DOCUMENTS = ("experiments/README.md", "docs/experiments.md")


def table_cell(text: str) -> str:
    """Keep contract text inside one Markdown table cell."""
    return " ".join(text.split()).replace("|", "&#124;")


def render_catalog(root: Path, *, website: bool) -> str:
    """Use each manifest's theory, declared ecosystems, and expected result."""
    rows = ["| Experiment | Theory | Implementations | Expected result |",
            "| --- | --- | --- | --- |"]
    for path in sorted((root / "experiments").glob("*/experiment.json")):
        manifest = json.loads(path.read_text(encoding="utf-8"))
        title = (path.parent / "README.md").read_text(encoding="utf-8").splitlines()[0].removeprefix("# ")
        theory = Path(manifest["theory"])
        theory_title = (root / theory).read_text(encoding="utf-8").splitlines()[0].removeprefix("# ")
        # Website links stay inside the rendered theory; source stays on GitHub.
        if website:
            source = f"https://github.com/cicixgliamici/quantum_ed/tree/main/experiments/{manifest['name']}"
            theory_link = theory.relative_to("docs").as_posix()
        else:
            source = f"{manifest['name']}/README.md"
            theory_link = "../" + theory.as_posix()
        ecosystems = ", ".join(label for name, label in ECOSYSTEM_LABELS.items()
                               if name in manifest["implementations"])
        rows.append(f"| [{table_cell(title)}]({source}) | [{table_cell(theory_title)}]({theory_link}) "
                    f"| {ecosystems} | {table_cell(manifest['expected_result'])} |")
    return "\n".join(rows)


def updated_document(document: str, table: str) -> str:
    """Replace only the marked table, preserving the surrounding explanation."""
    if document.count(START_MARKER) != 1 or document.count(END_MARKER) != 1:
        raise ValueError("Expected exactly one pair of experiment catalog markers")
    before, remainder = document.split(START_MARKER)
    _, after = remainder.split(END_MARKER)
    return before + START_MARKER + "\n\n" + table + "\n\n" + END_MARKER + after


def catalog_updates(root: Path) -> dict[Path, str]:
    """Return changed documents so CI can detect drift without rewriting files."""
    updates = {}
    for relative in CATALOG_DOCUMENTS:
        path = root / relative
        current = path.read_text(encoding="utf-8")
        expected = updated_document(current, render_catalog(root, website=relative.startswith("docs/")))
        if current != expected:
            updates[path] = expected
    return updates


def main() -> int:
    """Refresh only on explicit request; the default command checks freshness."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Refresh the marked tables")
    arguments = parser.parse_args()
    updates = catalog_updates(REPOSITORY_ROOT)
    for path, content in updates.items():
        if arguments.write:
            path.write_text(content, encoding="utf-8")
        print(f"{'Updated' if arguments.write else 'Stale'}: {path.relative_to(REPOSITORY_ROOT)}")
    if updates and not arguments.write:
        print("Run python tools/experiment_catalog.py --write to refresh the catalogs.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
