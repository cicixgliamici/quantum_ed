# Website publishing

Quantum-Ed is prepared for publication at
[cicixgliamici.github.io/quantum_ed](https://cicixgliamici.github.io/quantum_ed/).
The source is the Markdown in `docs/`; MkDocs Material generates the website.
Generated HTML stays out of Git so reviews focus on source changes.

## Enable GitHub Pages

1. Push the website configuration and
   [publishing workflow](https://github.com/cicixgliamici/quantum_ed/blob/main/.github/workflows/pages.yml)
   to `main`.
2. Open the repository's **Settings → Pages**.
3. Under **Build and deployment → Source**, select **GitHub Actions**.
4. Open **Actions → Publish documentation → Run workflow**, select `main`,
   and start the workflow. Later pushes to `main` publish automatically.
5. Wait for both the build and deployment jobs to succeed. The deployment
   summary links to the published website.

This follows GitHub's
[custom workflow publishing procedure](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
The deployment job requests Pages and identity-token permissions; the build
job only reads repository contents. No personal access token is needed.

## Preview a documentation change

From the repository root:

```bash
python -m pip install -r tools/uv-requirement.txt
uv sync --locked --extra docs --no-editable
uv run --no-sync python tools/verify_repository.py
uv run --no-sync python -m mkdocs build --strict
uv run --no-sync python -m mkdocs serve
```

Open the local address printed by MkDocs. Check navigation, search, equations,
and narrow-screen layout before publishing. Pull requests also run a strict
documentation build in the Quality workflow, without deploying a preview.

## What visitors can use

The website provides theory, study figures, downloadable CSV/JSON evidence,
and [executed notebook lessons](../notebooks.md) with code, results, and plots.
Notebook pages and figure assets are generated during each MkDocs build;
source notebooks are never overwritten. Each lesson includes a source download.

Python and quantum SDK examples run in a local environment; GitHub Pages
serves static files and does not execute those programs for visitors.

## Diagnose a failed publication

- If Pages is not configured, select **GitHub Actions** as the source and rerun
  the workflow.
- If the build fails, reproduce the strict build locally and fix the reported
  Markdown, configuration, or link warning.
- If deployment is waiting, inspect the `github-pages` environment's protection
  rules and allow deployment from `main`.
- If the repository is renamed or moved, update `site_url` and `repo_url` in
  `mkdocs.yml`, then review links to source files.

Only a successful deployment confirms that the public URL is live.
