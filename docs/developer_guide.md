# Developer Guide

## Environment setup

```bash
uv venv
uv sync --all-extras --dev
source .venv/bin/activate
```

## Formatting and tests

```bash
uv run black .
uv run pytest
```

Run a single test by name:

```bash
uv run pytest -k test_package_manager_init_package_a_only
```

## Adding a new package

1. Create a package under `libs/` or `tests/package_*` using the `src/<name>/`
   layout.
2. Add the package to `[tool.uv.workspace]` and `[tool.uv.sources]` in the root
   `pyproject.toml`.
3. Register the package before creating a `SlangPackageManager` instance.

## Documentation

Sphinx uses Markdown via MyST. Build docs locally with:

```bash
uv run sphinx-build -b html docs docs/_build
```
