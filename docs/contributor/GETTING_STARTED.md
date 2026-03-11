# Getting Started as a Contributor

Welcome! This guide helps you get started with traceflux development.

---

## 5-Minute Setup

### 1. Fork and Clone

```bash
# Fork on GitHub (via web UI)

# Clone your fork
git clone https://github.com/YOUR_USERNAME/traceflux.git
cd traceflux
```text

### 2. Install for Development

```bash
# Install with dev dependencies (pdm manages venv automatically)
pdm install

# Verify installation
pdm run traceflux --help
```text

### 3. Enable Git Hooks

```bash
# Enable pre-commit hooks (runs quality checks before commit)
pdm run pre-commit install

# Test hooks
echo "# Test" > test.py
git add test.py
git commit -m "Test commit"
# Should run pre-commit checks
```text

### 4. Run Tests

```bash
# Run all tests
pdm run pytest

# Run with coverage
pdm run pytest --cov=src/traceflux --cov-report=term-missing

# Run specific test
pdm run pytest tests/test_scanner_unit.py -v
```text

---

## Your First Contribution

### Step 1: Find Something to Work On

GOOD FIRST ISSUES:
- Look for `good first issue` label on GitHub
- Check `TASKS.md` for planned features
- Fix a bug you encountered

### Step 2: Create a Branch

```bash
# From main branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```text

### Step 3: Make Changes

```bash
# Edit code
# Add tests (important!)
# Run tests locally
pdm run pytest

# Check code quality
pdm run black src/ tests/
pdm run isort src/ tests/
pdm run flake8 src/ tests/
```text

### Step 4: Commit

```bash
# Git hooks run automatically
git add .
git commit -m "feat: add your feature description"

# If hooks fail, fix issues and try again
```text

### Step 5: Push and Create PR

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create PR on GitHub
# - Use the PR template
# - Link to related issues
# - Describe what you changed
```text

---

## Development Guidelines

### Code Style

We use automated tools to ensure consistency:

| Tool | Purpose | Command |
|------|---------|---------|
| black | Code formatting | `black src/ tests/` |
| isort | Import sorting | `isort src/ tests/` |
| flake8 | Linting | `flake8 src/ tests/` |

Pre-commit hooks run these automatically -- you don't need to remember!

### Testing

RULE: New features need tests.

```python
# tests/test_your_feature.py
def test_your_feature():
    """Test your feature works correctly."""
    result = your_function()
    assert result == expected_value
```text

Run tests before committing:
```bash
pdm run pytest tests/test_your_feature.py -v
```text

### Documentation

UPDATE DOCUMENTATION IF YOU:
- Add a new feature
- Change behavior
- Fix a bug that affects users

DOCUMENTATION FILES:
- `README.md` -- Overview and quick start
- `docs/INSTALLATION.md` -- Installation guide
- `docs/QUICK_REF.md` -- Quick reference
- `docs/TESTING.md` -- Testing guide

---

## Common Tasks

### Add a New Feature

```bash
# 1. Create branch
git checkout -b feature/new-feature

# 2. Implement feature
# Edit src/traceflux/your_module.py

# 3. Add tests
# Edit tests/test_your_module.py

# 4. Run tests
pdm run pytest

# 5. Commit and push
git add .
git commit -m "feat: add new feature"
git push origin feature/new-feature
```text

### Fix a Bug

```bash
# 1. Create branch
git checkout -b fix/bug-description

# 2. Fix bug
# Edit relevant files

# 3. Add regression test
# Make sure bug doesn't come back

# 4. Run all tests
pdm run pytest

# 5. Commit and push
git add .
git commit -m "fix: describe the bug fix"
git push origin fix/bug-description
```text

### Update Documentation

```bash
# 1. Create branch
git checkout -b docs/update-description

# 2. Edit documentation
# Edit README.md or docs/*.md

# 3. No tests needed (usually)

# 4. Commit and push
git add .
git commit -m "docs: improve description of X"
git push origin docs/update-description
```text

---

## Troubleshooting

### Pre-commit Hooks Fail

PROBLEM: Pre-commit hooks reject your commit.

SOLUTION:
```bash
# See what failed
git commit
# Read error message

# Fix the issue
# (format code, fix linting, etc.)

# Try again
git add .
git commit
```text

### Tests Fail

PROBLEM: Tests fail locally.

SOLUTION:
```bash
# Run failing test with verbose output
pdm run pytest tests/test_failing.py -v

# Read error message
# Fix the issue
# Re-run tests
```text

### Can't Push to Repository

PROBLEM: Permission denied when pushing.

SOLUTION:
```bash
# Make sure you forked the repository
# Push to your fork, not upstream
git push origin your-branch

# Then create PR from your fork to upstream
```text

---

## Project Structure

```bash
traceflux/
├── src/traceflux/          # Source code
│   ├── __init__.py
│   ├── cli.py              # Command-line interface
│   ├── search.py           # Search logic
│   └── associations.py     # Association engine
├── tests/                  # Tests
│   ├── test_cli.py
│   ├── test_search.py
│   └── test_associations.py
├── docs/                   # Documentation
│   ├── user/               # User guides
│   ├── contributor/        # Contributor guides (this file)
│   └── internal/           # Internal documentation
├── scripts/                # Utility scripts
├── .github/                # GitHub configuration
│   ├── workflows/          # CI/CD
│   ├── RELEASE_PROTOCOL.md # Release process
│   └── pull_request_template.md
└── pyproject.toml          # Package configuration
```text

---

## Resources

### Documentation

- [Installation Guide](user/INSTALLATION.md)
- [Usage Guide](user/USAGE.md)
- [Testing Philosophy](TESTING-PHILOSOPHY.md)
- [Release Protocol](../.github/RELEASE_PROTOCOL.md)

### Tools

- [pytest](https://docs.pytest.org/) -- Testing framework
- [black](https://black.readthedocs.io/) -- Code formatter
- [isort](https://pycqa.github.io/isort/) -- Import sorter
- [flake8](https://flake8.pycqa.org/) -- Linter

### Communication

- GitHub Issues -- Bug reports, feature requests
- Pull Requests -- Code contributions
- Discussions -- Questions, ideas (if enabled)

---

## Questions?

COMMON QUESTIONS:

Q: Do I need to install all dev tools?
A: No! Pre-commit hooks run automatically. Just install with `pip install -e ".[dev]"`.

Q: How do I know what to work on?
A: Check GitHub issues with `good first issue` label, or ask in a comment.

Q: Can I submit a PR without an issue?
A: Yes! But for large changes, please open an issue first to discuss.

Q: How long does review take?
A: Usually within a few days. Be patient!

---

Welcome to the community!

Don't worry about making mistakes -- that's how we learn. Just start contributing!
