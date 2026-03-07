# traceflux Python Project Infrastructure Plan

**Date**: 2026-03-07  
**Problem**: traceflux lacks Python project best practices (versioning, CI/CD, quality checks)

---

## 🎯 Current State

### What We Have
- ✅ `pyproject.toml` (basic structure)
- ✅ Version: `1.0.0` (static)
- ✅ Tests: 202 tests, 92%+ coverage
- ✅ Zero dependencies (pure stdlib)

### What's Missing
- ❌ Version automation (manual updates)
- ❌ CI/CD pipeline (no GitHub Actions)
- ❌ Code quality checks (no linting/formatting)
- ❌ Release automation (manual process)
- ❌ PyPI publishing (if needed later)

---

## 💡 Proposed Solutions

### 1. Version Management

#### Option A: bump2version (Recommended for simplicity)

**What**: Simple version bumping tool

**Setup**:
```toml
# pyproject.toml
[tool.bumpversion]
current_version = "1.0.0"
commit = true
tag = true

[[tool.bumpversion.files]]
filename = "src/traceflux/__version__.py"

[[tool.bumpversion.files]]
filename = "pyproject.toml"
```

**Usage**:
```bash
bump-my-version patch  # 1.0.0 → 1.0.1
bump-my-version minor  # 1.0.0 → 1.1.0
bump-my-version major  # 1.0.0 → 2.0.0
```

**Pros**:
- ✅ Simple, explicit
- ✅ Works with existing structure
- ✅ No magic

**Cons**:
- ⚠️ Manual step required
- ⚠️ Extra dependency

---

#### Option B: setuptools-scm (Automatic from git tags)

**What**: Version from git tags automatically

**Setup**:
```toml
# pyproject.toml
[project]
dynamic = ["version"]

[tool.setuptools_scm]
write_to = "src/traceflux/_version.py"
```

**Usage**:
```bash
git tag v1.0.0
git push --tags
# Version automatically set to 1.0.0
```

**Pros**:
- ✅ Single source of truth (git tag)
- ✅ No manual version updates
- ✅ Standard in Python ecosystem

**Cons**:
- ⚠️ Requires git at build time
- ⚠️ Slightly more complex

---

#### **Recommendation**: Option B (setuptools-scm)

**Why**: 
- Git tags are already the release mechanism
- Eliminates manual version updates
- Industry standard for Python projects

---

### 2. Code Quality

#### Tools

| Tool | Purpose | Config |
|------|---------|--------|
| **ruff** | Linting (fast) | `pyproject.toml` |
| **black** | Formatting | `pyproject.toml` |
| **mypy** | Type checking | `pyproject.toml` |

#### Configuration

```toml
# pyproject.toml

[tool.ruff]
line-length = 100
target-version = "py310"
select = ["E", "F", "W", "I", "N", "UP"]

[tool.black]
line-length = 100
target-version = ["py310", "py311", "py312", "py313"]

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false  # Gradual typing
```

#### Pre-commit Hooks (Optional)

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
      - id: ruff-format
  
  - repo: https://github.com/psf/black
    rev: 24.2.0
    hooks:
      - id: black
```

---

### 3. CI/CD Pipeline (GitHub Actions)

#### Workflow Structure

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  release:
    types: [published]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12", "3.13"]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
      
      - name: Run tests
        run: |
          pytest --cov=traceflux --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      
      - name: Install tools
        run: |
          pip install ruff black mypy
      
      - name: Lint
        run: ruff check src/
      
      - name: Format check
        run: black --check src/
      
      - name: Type check
        run: mypy src/

  release:
    needs: [test, quality]
    if: github.event_name == 'release'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      
      - name: Build
        run: |
          pip install build
          python -m build
      
      - name: Upload to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
```

---

### 4. Release Automation

#### Manual Release Process (Current)

```bash
# 1. Update version (if not using setuptools-scm)
# 2. Commit
# 3. Tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# 4. Create GitHub release
gh release create v1.0.0 --generate-notes

# 5. Build and publish (optional)
python -m build
twine upload dist/*
```

#### Automated Release (With GitHub Actions)

Triggered by release publication:
- Auto-build wheels
- Auto-publish to PyPI (if configured)
- Auto-upload to GitHub release

---

### 5. Project Structure Updates

```
traceflux/
├── .github/
│   └── workflows/
│       ├── ci.yml           # CI/CD pipeline
│       └── release.yml      # Release automation
├── src/
│   └── traceflux/
│       ├── __init__.py
│       ├── __version__.py   # Or use setuptools-scm
│       └── ...
├── tests/
├── .pre-commit-config.yaml  # Optional: pre-commit hooks
├── pyproject.toml
├── README.md
├── CHANGELOG.md             # Auto-generated or manual
└── ...
```

---

## 📋 Implementation Plan

### Phase 1: Code Quality (Immediate)

- [ ] Add ruff configuration
- [ ] Add black configuration
- [ ] Run initial formatting
- [ ] Fix any linting issues

**Time**: 1-2 hours

---

### Phase 2: CI/CD Pipeline (High Priority)

- [ ] Create `.github/workflows/ci.yml`
- [ ] Configure test matrix (3.10-3.13)
- [ ] Add code quality checks
- [ ] Set up Codecov (optional)

**Time**: 2-3 hours

---

### Phase 3: Version Management (Medium Priority)

- [ ] Choose: bump2version vs setuptools-scm
- [ ] Configure in `pyproject.toml`
- [ ] Update `__version__.py` if needed
- [ ] Test version detection

**Time**: 1 hour

---

### Phase 4: Release Automation (Optional)

- [ ] Create PyPI account (if publishing)
- [ ] Add PyPI API token to GitHub secrets
- [ ] Configure release workflow
- [ ] Test with test.pypi.org

**Time**: 2 hours

---

### Phase 5: Documentation (Ongoing)

- [ ] Add CONTRIBUTING.md section on development setup
- [ ] Document release process
- [ ] Add badges to README (CI status, coverage, version)

**Time**: 1 hour

---

## 🎯 Recommendations

### Must Have (v1.0.1)

1. **CI/CD pipeline** - Automated testing on PR/merge
2. **Code quality** - ruff + black
3. **Python version matrix** - Test 3.10-3.13

### Should Have (v1.1.0)

1. **Version automation** - setuptools-scm
2. **Coverage tracking** - Codecov integration
3. **Type checking** - mypy (gradual)

### Nice to Have (Future)

1. **PyPI publishing** - If there's demand
2. **Pre-commit hooks** - For local development
3. **Changelog automation** - From commit messages

---

## 📊 Comparison: Before vs After

| Aspect | Before | After |
|--------|--------|-------|
| **Version** | Manual | Auto from git tags |
| **Testing** | Local only | CI on every PR |
| **Quality** | None | ruff + black + mypy |
| **Release** | Manual | Semi-automated |
| **PyPI** | No | Optional |
| **Confidence** | Medium | High |

---

## 🚀 Quick Start (If Approved)

```bash
cd /home/openclaw/tracer/dev-repo/traceflux

# 1. Install dev tools
pip install ruff black mypy pytest pytest-cov

# 2. Format code
black src/ tests/
ruff check --fix src/ tests/

# 3. Run tests
pytest --cov=traceflux

# 4. Create CI workflow
# (Create .github/workflows/ci.yml)

# 5. Commit and push
git add -A
git commit -m "ci: Add GitHub Actions CI/CD pipeline"
git push
```

---

## 💭 Philosophical Consideration

**Question**: Does adding CI/CD violate traceflux's UNIX philosophy?

**Answer**: No, it enhances it:
- ✅ **Do one thing well**: CI tests, code runs
- ✅ **Composability**: GitHub Actions compose workflows
- ✅ **Simplicity**: Automated checks prevent complexity creep
- ✅ **Clarity**: CI status is clear to all contributors

**Principle**: Automation is not bloat—it's reliability.

---

**Decision Needed**: Should I proceed with implementation?

---

**Last Updated**: 2026-03-07  
**Status**: Proposal (awaiting decision)
