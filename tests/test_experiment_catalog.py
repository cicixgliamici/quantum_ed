"""Check contract changes reach both catalogs without overwriting manual prose."""

import json

import pytest

from tools import experiment_catalog


@pytest.fixture
def catalog_repository(tmp_path):
    experiment = tmp_path / "experiments/example"
    experiment.mkdir(parents=True)
    (experiment / "README.md").write_text("# Example\n", encoding="utf-8")
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "theory.md").write_text("# Example theory\n", encoding="utf-8")
    manifest = {
        "name": "example", "theory": "docs/theory.md",
        "expected_result": "P(0 | input) = 1",
        "implementations": {"numpy": "example.py", "pennylane": "model.py"},
    }
    (experiment / "experiment.json").write_text(json.dumps(manifest), encoding="utf-8")
    for relative in experiment_catalog.CATALOG_DOCUMENTS:
        (tmp_path / relative).write_text(
            "Manual introduction\n" + experiment_catalog.START_MARKER + "\nstale\n"
            + experiment_catalog.END_MARKER + "\nManual conclusion\n", encoding="utf-8"
        )
    return tmp_path


def test_catalogs_follow_contracts_and_preserve_manual_content(catalog_repository):
    updates = experiment_catalog.catalog_updates(catalog_repository)
    assert len(updates) == 2
    for path, content in updates.items():
        assert content.startswith("Manual introduction\n")
        assert content.endswith("\nManual conclusion\n")
        assert "NumPy, PennyLane" in content
        assert "P(0 &#124; input) = 1" in content
        path.write_text(content, encoding="utf-8")
    assert experiment_catalog.catalog_updates(catalog_repository) == {}

    manifest_path = catalog_repository / "experiments/example/experiment.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["expected_result"] = "Updated scientific claim"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    changed = experiment_catalog.catalog_updates(catalog_repository)
    assert len(changed) == 2
    assert all("Updated scientific claim" in content for content in changed.values())


def test_website_and_repository_use_their_own_link_roots(catalog_repository):
    website = experiment_catalog.render_catalog(catalog_repository, website=True)
    repository = experiment_catalog.render_catalog(catalog_repository, website=False)
    assert "](theory.md)" in website
    assert "github.com/cicixgliamici/quantum_ed/tree/main/experiments/example" in website
    assert "](../docs/theory.md)" in repository
    assert "](example/README.md)" in repository


@pytest.mark.parametrize("document", ["No markers", "<!-- experiment-catalog:start -->"])
def test_missing_markers_fail_instead_of_replacing_manual_prose(document):
    with pytest.raises(ValueError, match="exactly one pair"):
        experiment_catalog.updated_document(document, "generated table")
