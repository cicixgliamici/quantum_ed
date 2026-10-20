"""Execute notebook copies and add their rendered lessons to the MkDocs site."""

import logging
from pathlib import Path

import nbformat
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File, Files
from nbconvert import MarkdownExporter
from nbconvert.preprocessors import ExecutePreprocessor

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
LOGGER = logging.getLogger("mkdocs.notebooks")


def render_notebook(source: Path) -> tuple[str, dict[str, bytes]]:
    """Return executed Markdown and figures without modifying the source file."""
    notebook = nbformat.read(source, as_version=4)
    # Fail the build on execution errors; stale or partial results must not publish.
    executor = ExecutePreprocessor(timeout=120, kernel_name="python3")
    executor.preprocess(notebook, {"metadata": {"path": str(REPOSITORY_ROOT)}})
    exporter = MarkdownExporter()
    # Prefix figure names because every notebook shares the generated directory.
    markdown, resources = exporter.from_notebook_node(
        notebook, resources={"unique_key": source.stem}
    )
    links = (
        "[All notebooks](../notebooks.md) · "
        f"[Download the source notebook]({source.name})\n\n"
    )
    return links + markdown, resources.get("outputs", {})


def on_files(files: Files, config: MkDocsConfig, **kwargs) -> Files:
    """Register generated pages and assets before MkDocs resolves site links."""
    notebooks = sorted((REPOSITORY_ROOT / "notebooks").glob("*.ipynb"))
    if not notebooks:
        raise ValueError("No source notebooks found; refusing to publish an empty collection.")
    for source in notebooks:
        LOGGER.info("Executing notebook: %s", source.name)
        markdown, figures = render_notebook(source)
        files.append(File.generated(config, f"notebooks/{source.stem}.md", content=markdown))
        files.append(File.generated(config, f"notebooks/{source.name}", content=source.read_bytes()))
        for name, content in figures.items():
            files.append(File.generated(config, f"notebooks/{name}", content=content))
    # Keep lessons in the sidebar as well as the searchable overview page.
    for entry in config.nav:
        if entry.get("Notebooks") == "notebooks.md":
            entry["Notebooks"] = [{"Overview": "notebooks.md"}] + [
                {source.stem: f"notebooks/{source.stem}.md"} for source in notebooks
            ]
    return files


def on_page_markdown(markdown: str, page, **kwargs) -> str:
    """Build the overview from source filenames so its links cannot drift."""
    if page.file.src_uri != "notebooks.md":
        return markdown
    links = [
        f"- [{source.stem}](notebooks/{source.stem}.md)"
        for source in sorted((REPOSITORY_ROOT / "notebooks").glob("*.ipynb"))
    ]
    return markdown + "\n\n## Read the lessons\n\n" + "\n".join(links) + "\n"
