"""Prevent stale source links from bypassing the local documentation checker."""

from tools import verify_repository


def test_own_repository_source_links_resolve_queries_and_line_anchors(tmp_path, monkeypatch):
    monkeypatch.setattr(verify_repository, "REPOSITORY_ROOT", tmp_path)
    (tmp_path / "example.py").write_text("pass\n", encoding="utf-8")
    document = tmp_path / "README.md"
    document.write_text(
        "[source](https://github.com/cicixgliamici/quantum_ed/blob/main/example.py?plain=1#L1)",
        encoding="utf-8")
    assert verify_repository.validate_markdown_links(document) == []


def test_missing_own_repository_source_is_reported(tmp_path, monkeypatch):
    monkeypatch.setattr(verify_repository, "REPOSITORY_ROOT", tmp_path)
    document = tmp_path / "README.md"
    document.write_text(
        "[source](https://github.com/cicixgliamici/quantum_ed/blob/main/missing.py)", encoding="utf-8")
    errors = verify_repository.validate_markdown_links(document)
    assert len(errors) == 1
    assert "broken repository source link" in errors[0]


def test_external_papers_and_other_branches_remain_external():
    assert verify_repository.repository_source_target("https://arxiv.org/abs/1801.00862") is None
    assert verify_repository.repository_source_target(
        "https://github.com/cicixgliamici/quantum_ed/blob/other/example.py") is None


def test_generated_and_virtual_environment_docs_are_not_scanned(tmp_path, monkeypatch):
    monkeypatch.setattr(verify_repository, "REPOSITORY_ROOT", tmp_path)
    source = tmp_path / "docs"
    source.mkdir()
    (source / "README.md").write_text("Source documentation", encoding="utf-8")
    generated = tmp_path / "build"
    generated.mkdir()
    (generated / "README.md").write_text("Third-party documentation", encoding="utf-8")
    environment = tmp_path / "custom-environment"
    environment.mkdir()
    (environment / "pyvenv.cfg").write_text("home = example", encoding="utf-8")
    (environment / "README.md").write_text("Third-party documentation", encoding="utf-8")
    assert verify_repository.markdown_documents() == [source / "README.md"]
