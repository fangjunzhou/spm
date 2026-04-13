# AGENTS.md

## Repository Summary
- Project: spm.slang (Slang package manager)
- Language: Python 3.12+
- Workspace: uv workspace with packages in `libs/*` and `tests/*`
- Primary library: `libs/spm_slang`
- Test suite: `tests/spm_test`
- Fixture packages: `tests/package_*` (for testing dependency graphs)

## Environment Setup
- Recommended: use `uv` and the workspace config in `pyproject.toml`
- Create venv: `uv venv` (creates `.venv` in repo root)
- Install workspace deps: `uv sync --all-groups`
- Activate venv: `source .venv/bin/activate`

## Build Commands
- Build workspace sdist/wheel: `uv run python -m build`
- Build a single package (example): `uv run python -m build libs/spm_slang`
- Build documentation: `uv run sphinx -b html docs docs/_build/html`
- Publish dry-run: `uv run python -m twine check dist/*`

## Lint / Format Commands
- Format with Black: `uv run black .`
- Check formatting only: `uv run black --check .`
- No dedicated lint config (ruff cache exists but no config file)

## Test Commands
- Run all tests: `uv run pytest`
- Run test module: `uv run pytest tests/spm_test/src/spm_test/test_package_manager_init_package_a_only.py`
- Run single test by name: `uv run pytest -k test_package_manager_init_package_a_only`
- Run with verbose output: `uv run pytest -vv`
- Stop on first failure: `uv run pytest -x`
- Quieter output: `uv run pytest -q`

## Test Selection Tips
- Use `-k` for substring matching across tests
- Use `-x` to stop on first failure
- Use `-q` for quieter output when iterating
- Prefer `-vv` when diagnosing ordering issues

## Dependency Management
- Workspace dependencies live in root `pyproject.toml`
- Package-specific deps live in each package `pyproject.toml`
- When adding a new package, add it to `[tool.uv.workspace]` members
- Keep `[tool.uv.sources]` in sync with workspace packages

## Packaging Layout
- Each package uses `src/<package_name>/` layout
- Keep package metadata in `pyproject.toml` next to `src/`
- Fixture packages live in `tests/package_*`
- Primary tests live in `tests/spm_test/src/spm_test/`

## Nix Dev Shell (Optional)
- Enter shell: `nix develop`
- The shell expects `.venv` to already exist
- macOS: automatically unsets SDKROOT and NIX_* env vars to avoid build issues

## Cursor / Copilot Rules
- No `.cursor/rules/`, `.cursorrules`, or `.github/copilot-instructions.md` files found

## Code Style Guidelines

### General
- Use Python 3.12 features when helpful (e.g., `type[...]`, `|` unions)
- Start new modules with `from __future__ import annotations` when appropriate
- Use f-strings for string interpolation
- Keep code concise and readable; avoid unnecessary abstractions
- Prefer pure functions where possible; keep side effects explicit
- Avoid `print`; use logging for diagnostics

### Formatting
- Follow Black formatting defaults (no custom line length configured)
- Use 4-space indentation
- Keep line lengths reasonable; rely on Black to wrap long expressions

### Imports
- Order imports by group:
  1. Standard library (`typing`, `logging`, `collections`, etc.)
  2. Third-party packages (`slangpy`, etc.)
  3. Local project imports (`spm_slang`, `package_a`, etc.)
- Separate groups with a blank line
- Avoid unused imports; remove them promptly

### Typing
- Provide type hints for all public functions, methods, and class attributes
- Use `TypedDict` for structured configs (see `DeviceConfiguration`)
- Use precise collection types (`list`, `dict`, `Sequence`) rather than `Any`
- Prefer `Optional[T]` or `T | None` for nullable values

### Naming Conventions
- Modules and packages: `snake_case`
- Classes: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Avoid single-letter names unless in tight, local scopes

### Error Handling
- Raise `ValueError` for invalid inputs or inconsistent state
- Prefer clear error messages with actionable context
- Detect and fail early for invalid dependency graphs or missing packages

### Logging
- Use module-level logger: `logger = logging.getLogger(__name__)`
- Log at `debug` for diagnostic info
- Avoid logging sensitive data or large objects

### Documentation
- Use concise docstrings for public classes and methods
- Prefer short summary + `:return:`/`:param:` style when needed
- Keep inline comments minimal; code should be self-explanatory

## Project Structure
- `libs/spm_slang/src/spm_slang/`: core package manager logic
  - `package.py`: `SlangPackage` base class
  - `package_manager.py`: `SlangPackageManager` and `DeviceConfiguration`
- `tests/package_*`: fixture packages used for dependency tests
- `tests/spm_test/src/spm_test/`: pytest suite validating dependency ordering

## Slang-Specific Conventions
- `SlangPackage` subclasses must implement:
  - `name()` (unique package name)
  - `shader_paths()` (list of shader paths)
  - `build()` (returns a `spy.Module`)
- Register packages before instantiating `SlangPackageManager`
- Ensure dependencies are registered and resolvable; cycles are errors

## Package Manager Behavior
- Packages are built in topological dependency order
- The module map keys are package names
- The package registry is the `packages` dict in `spm_slang.package_manager`
- Avoid side effects during module import; register packages explicitly
- Use `NotImplementedError` for required abstract methods

## Testing Patterns
- Tests clear the `packages` registry before each test: `packages.clear()`
- Register packages via `SlangPackageManager.register_package(PackageClass)`
- Assert on `manager.module_map` length and contents
- Use `logger.info()` for diagnostic output during tests

## Preferred Workflows
- Make changes in `libs/spm_slang/src/spm_slang/`
- Add or update tests in `tests/spm_test/src/spm_test/`
- Run `uv run pytest` before submitting changes
- Run `uv run black .` if files were modified

## Quick Sanity Checks
- Bytecode check: `uv run python -m compileall libs/spm_slang`
- Focused tests: `uv run pytest -k package_manager`
- Keep checks minimal unless requested

## Notes for Agents
- Keep edits minimal and consistent with existing patterns
- Do not add new tools or configs unless explicitly requested
- If unsure about build/test tooling, prefer `uv run` commands
