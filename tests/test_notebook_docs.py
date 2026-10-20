"""Check that published notebook results are fresh and failures stop export."""

import pytest

nbformat = pytest.importorskip("nbformat")
pytest.importorskip("mkdocs")
pytest.importorskip("nbconvert")
pytest.importorskip("ipykernel")

from nbclient.exceptions import CellExecutionError

from tools.notebook_docs import render_notebook


def test_render_executes_cells_extracts_figures_and_preserves_source(tmp_path):
    source = tmp_path / "example.ipynb"
    notebook = nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell(
        "%matplotlib inline\n"
        "import matplotlib.pyplot as plt\n"
        "print(6 * 7)\n"
        "plt.plot([0, 1], [0, 1])\n"
        "plt.show()"
    )])
    nbformat.write(notebook, source)
    original = source.read_bytes()

    markdown, figures = render_notebook(source)

    assert "42" in markdown
    assert "[Download the source notebook](example.ipynb)" in markdown
    assert figures
    assert all(name.startswith("example_") for name in figures)
    assert any(content.startswith(b"\x89PNG") for content in figures.values())
    assert source.read_bytes() == original


def test_execution_errors_prevent_publication(tmp_path):
    source = tmp_path / "broken.ipynb"
    notebook = nbformat.v4.new_notebook(cells=[
        nbformat.v4.new_code_cell("raise ValueError('invalid scientific result')")
    ])
    nbformat.write(notebook, source)

    with pytest.raises(CellExecutionError, match="invalid scientific result"):
        render_notebook(source)
