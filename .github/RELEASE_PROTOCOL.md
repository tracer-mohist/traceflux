# Release Protocol

**Philosophy**: Simple, Practical, Elegant

This document defines the release process for traceflux. It serves as the single source of truth for all release-related activities.

---

## 1. Version Format

Semantic Versioning: `MAJOR.MINOR.PATCH`

| Component | When to Increment | Example |
|-----------|------------------|---------|
| **MAJOR** | Breaking changes | 1.0.0 → 2.0.0 |
| **MINOR** | New features (backward compatible) | 1.0.0 → 1.1.0 |
| **PATCH** | Bug fixes (backward compatible) | 1.0.0 → 1.0.1 |

**Pre-release**: `1.0.1-beta`, `1.0.1-rc.1`

---

## 2. Release Process

### Manual Release (Current)

```bash
# 1. Run release script
./scripts/release.sh 1.0.1

# 2. Review changes
git show

# 3. Push to trigger CI/CD
git push origin main --tags

# 4. CI/CD automatically:
#    - Runs tests
#    - Runs linting
#    - Creates GitHub Release
```

### Script Responsibilities

`scripts/release.sh` handles:
- ✅ Version validation (SemVer format)
- ✅ Update `pyproject.toml`
- ✅ Run tests (must pass)
- ✅ Create git commit
- ✅ Create git tag

### CI/CD Responsibilities

GitHub Actions handles:
- ✅ Run tests (Python 3.12)
- ✅ Run linting (black, isort, flake8)
- ✅ Create GitHub Release (on tag)
- ✅ Generate release notes

---

## 3. Single Source of Truth

**Version is maintained in**: `pyproject.toml` only

`src/traceflux/__version__.py` reads from package metadata at runtime — no manual sync needed.

```python
# __version__.py
import importlib.metadata

try:
    __version__ = importlib.metadata.version("traceflux")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0-dev"
```

---

## 4. Code Quality Standards

### Pre-commit Hooks

Enabled via: `git config core.hooksPath .githooks`

Checks performed:
1. Python syntax validation
2. Code formatting (black)
3. Import order (isort)
4. Linting (flake8)

### CI/CD Checks

All PRs and pushes must pass:
- ✅ `pytest -v` (all tests)
- ✅ `black --check` (formatting)
- ✅ `isort --check-only` (imports)
- ✅ `flake8` (linting)

---

## 5. Branch Protection

### main Branch

- ✅ Require pull request reviews
- ✅ Require status checks (CI/CD)
- ✅ Require branches to be up to date
- ❌ No force pushes
- ❌ No direct commits

### Feature Branches

- Short-lived (days, not weeks)
- Named: `feature/description` or `fix/description`
- Must pass CI before merge

---

## 6. Pull Request Guidelines

### Before Submitting

- [ ] Tests pass locally
- [ ] Code formatted (`black`, `isort`)
- [ ] Linting passes (`flake8`)
- [ ] Documentation updated (if needed)

### Review Process

1. CI/CD must pass
2. At least 1 maintainer approval
3. Address review feedback
4. Squash merge (keep history clean)

---

## 7. Emergency Procedures

### Hotfix Release

```bash
# 1. Create hotfix branch from tag
git checkout v1.0.0
git checkout -b hotfix/critical-bug

# 2. Fix, test, commit

# 3. Release with patch version
./scripts/release.sh 1.0.1
git push origin main --tags
```

### Rollback

```bash
# 1. Delete bad tag
git tag -d v1.0.1
git push origin :refs/tags/v1.0.1

# 2. Revert commit
git revert HEAD

# 3. Create new release
./scripts/release.sh 1.0.2
```

---

## 8. Automation Roadmap

### Current (Manual + Script)

- ✅ Version update scripted
- ✅ Tests automated
- ✅ Git operations scripted
- ✅ CI/CD automated
- ⚠️ Human decides version number

### Future (If Needed)

When release frequency > 2x/month, consider:
- Auto-calculate version from commit messages
- Auto-generate CHANGELOG
- Keep manual approval step

**Tool options** (evaluate when needed):
- release-please
- python-semantic-release
- Custom script enhancements

---

## 9. Related Files

| File | Purpose |
|------|---------|
| `scripts/release.sh` | Release automation script |
| `.githooks/pre-commit` | Pre-commit code quality checks |
| `.github/workflows/ci.yml` | CI/CD pipeline definition |
| `pyproject.toml` | Version source of truth |
| `src/traceflux/__version__.py` | Runtime version reading |
| `docs/RELEASE.md` | User-facing release guide |

---

## 10. Decision Records

### Why Manual Version Decision?

**Date**: 2026-03-07

**Why**: Early-stage project, release frequency low (< 2x/month)

**Alternatives considered**:
- release-please (rejected: over-engineering for current needs)
- semantic-release (rejected: too complex, black-box)

**Assumptions**:
- Release frequency will remain low
- Human judgment valuable for version numbers
- Can automate later when needed

**Review trigger**: Release frequency > 2x/month

### Why Single Python Version in CI?

**Date**: 2026-03-07

**Why**: Cost control (75% CI/CD cost reduction)

**Trade-off**: Less test coverage vs. faster feedback

**Assumptions**:
- Python 3.12 representative for compatibility
- Can add versions when users demand

---

**Last Updated**: 2026-03-07  
**Version**: 1.0.0  
**Status**: Active
