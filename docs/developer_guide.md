# Developer Guide

## Environment setup

```bash
uv venv
uv sync --dev
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

## Package builds

The root workspace (`spm-workspace`) is a development umbrella that pulls in
library and test fixtures. It is not intended for release builds.

Build the `spm-slang` library package from the repo root with:

```bash
uv build libs/spm_slang
```

Build artifacts land under `libs/spm_slang/dist/`.

## Documentation

Sphinx uses Markdown via MyST. Build docs locally with:

```bash
uv run sphinx-build -b html docs docs/_build
```
