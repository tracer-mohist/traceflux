# Python Environment Configuration

PURPOSE: Document Python version and package management for traceflux.

---

## Python Version

Required: Python 3.10+

RECOMMENDED: Python 3.12 or 3.13

CONFIGURATION: `.python-version` file specifies the Python version for this project.

```bash
# Check current Python version
python --version

# Check project's required version
cat .python-version
```text

---

## Package Management

Tool: PDM (Python Dependency Manager)

Why PDM:
- Modern Python package management
- PEP 582 support (optional)
- Lock file for reproducible installs
- Virtual environment management

### Installation

```bash
# Install PDM (if not already installed)
curl -sSL https://pdm.fming.dev/install-pdm.py | python3 -

# Verify installation
pdm --version
```text

### Project Setup

```bash
# Install dependencies (creates .venv automatically)
pdm install

# Verify installation
pdm run traceflux --help
```text

### Running Commands

Always use `pdm run` for project commands:

```bash
# Run traceflux
pdm run traceflux "search query"

# Run tests
pdm run pytest

# Run pre-commit
pdm run pre-commit run --all-files

# Run linters
pdm run black src/
pdm run flake8 src/
```text

Why `pdm run`?
- Uses project's virtual environment
- Ensures consistent dependency versions
- Avoids polluting global Python environment

---

## Virtual Environment

Location: `.venv/` (project-local)

Management: PDM automatically manages the virtual environment.

```bash
# Show Python interpreter path
pdm info --python

# Show environment info
pdm info
```text

### Manual Activation (Optional)

```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Now you can run commands without `pdm run`
traceflux --help
pytest
```text

NOTE: Activation is optional. Using `pdm run` is recommended for clarity.

---

## Pre-commit Hooks

SETUP:

```bash
# Install pre-commit hooks (one-time)
pdm run pre-commit install

# Verify installation
ls -la .git/hooks/pre-commit
```text

Run manually:

```bash
# Run all hooks
pdm run pre-commit run --all-files

# Run specific hook
pdm run pre-commit run black
```text

CONFIGURATION: `.pre-commit-config.yaml`

---

## Common Issues

### Python Version Mismatch

PROBLEM: `RuntimeError: failed to find interpreter for python3.X`

SOLUTION:
```bash
# Check available Python versions
python3 --version
python3.12 --version  # If available

# Update .python-version if needed
echo "3.13" > .python-version

# Reinstall dependencies
rm -rf .venv
pdm install
```text

### Pre-commit Hook Failures

PROBLEM: Pre-commit hooks fail with interpreter errors.

SOLUTION:
```bash
# Clear pre-commit cache
rm -rf ~/.cache/pre-commit

# Reinstall hooks
pdm run pre-commit install --force
```text

### Dependency Conflicts

PROBLEM: `ResolutionImpossible` or version conflicts.

SOLUTION:
```bash
# Clear lock file and reinstall
rm pdm.lock
pdm install

# Or update specific dependency
pdm update package-name
```text

---

## For Contributors

QUICK START:

```bash
# 1. Clone repository
git clone https://github.com/tracer-mohist/traceflux.git
cd traceflux

# 2. Install dependencies
pdm install

# 3. Install pre-commit hooks
pdm run pre-commit install

# 4. Verify installation
pdm run traceflux --help
pdm run pytest
```text

Development Workflow:

```bash
# Make changes
# Edit src/traceflux/*.py

# Run tests
pdm run pytest

# Run quality checks
pdm run pre-commit run --all-files

# Commit (hooks run automatically)
git add .
git commit -m "feat: add new feature"

# Push
git push
```text

---

## Related Files

- `.python-version` - Python version specification
- `pyproject.toml` - Project configuration and dependencies
- `pdm.lock` - Locked dependency versions
- `.pre-commit-config.yaml` - Pre-commit hooks configuration
- `.venv/` - Virtual environment (auto-generated, not committed)

---

LAST UPDATED: 2026-03-11
STATUS: Active
