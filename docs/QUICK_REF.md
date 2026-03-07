# Quick Reference

**Common commands and workflows for traceflux development.**

---

## Development Setup

```bash
# Clone and install
git clone https://github.com/tracer-mohist/traceflux.git
cd traceflux
pip install -e ".[dev]"

# Enable git hooks
git config core.hooksPath .githooks

# Install code quality tools
pip install black flake8 isort mypy
```

---

## Daily Development

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=traceflux --cov-report=term-missing

# Format code
black src/ tests/
isort src/ tests/

# Check code quality
black --check src/ tests/
flake8 --max-line-length=100 --ignore=E501,W503 src/ tests/
```

---

## Release Workflow

```bash
# 1. Update CHANGELOG.md
# Edit CHANGELOG.md with changes

# 2. Run release script
./scripts/release.sh 1.0.1

# 3. Review changes
git show

# 4. Push to GitHub
git push origin main --tags

# CI/CD will automatically:
# - Run tests
# - Check code quality
# - Build package
# - Create GitHub Release
# - Publish to PyPI (if configured)
```

---

## Pull Request Workflow

```bash
# 1. Create branch
git checkout main
git checkout -b feature/my-feature

# 2. Make changes, test, commit
# (pre-commit hooks run automatically)

# 3. Push to fork
git push origin feature/my-feature

# 4. Open PR on GitHub
# Use the PR template
```

---

## Troubleshooting

### Pre-commit hook fails

```bash
# Format code
black src/ tests/
isort src/ tests/

# Re-commit
git add .
git commit
```

### Tests fail

```bash
# Run specific test
pytest tests/test_file.py::test_function -v

# Run all tests
pytest -v
```

### Version mismatch

```bash
# Check versions
grep '^version = ' pyproject.toml
grep '^__version__ = ' src/traceflux/__version__.py

# Re-run release script
./scripts/release.sh <version>
```

---

## File Locations

| File | Purpose |
|------|---------|
| `scripts/release.sh` | Release automation |
| `.githooks/pre-commit` | Pre-commit checks |
| `.github/workflows/ci.yml` | CI/CD pipeline |
| `CHANGELOG.md` | Version history |
| `docs/RELEASE.md` | Release guide |
| `pyproject.toml` | Package config |

---

## Links

- [Release Guide](RELEASE.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [GitHub Actions](https://github.com/tracer-mohist/traceflux/actions)
- [PyPI Package](https://pypi.org/project/traceflux/)
