# Repository tools

Run tools from the repository root using `uv run --no-sync python tools/<name>.py`.
Install the dependency profile described by each command's documentation first.

| Tool | Purpose |
| --- | --- |
| [verify_repository.py](verify_repository.py) | Validate experiment contracts, source links, and generated catalogs |
| [validate_experiments.py](validate_experiments.py) | Compare declared ecosystem implementations with analytical references |
| [environment_report.py](environment_report.py) | Record versions and verify the installed package |
| [check_math_blocks.py](check_math_blocks.py) | Report indented display-math delimiters for manual review |
| [experiment_catalog.py](experiment_catalog.py) | Refresh the experiment tables from their manifests |

The ecosystem-specific `validate_*.py` commands offer narrower entrypoints;
`experiment_checks.py` contains shared scientific assertions.
`notebook_docs.py` is a MkDocs hook, not a standalone command.
It also saves the executed copies to `build/executed-notebooks/` for CI review.

## Documentation maintenance

```bash
uv run --no-sync python tools/experiment_catalog.py --write
uv run --no-sync python tools/verify_repository.py
uv run --no-sync python tools/check_math_blocks.py
```

The math checker never edits documents because indentation can carry list
structure. The former one-off `scratch/` rewriting scripts are retained in Git
history; current maintenance uses explicit, reviewable commands here.
