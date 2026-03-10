# Release Protocol

Purpose: Automated release process with python-semantic-release.

Philosophy: Simple, Practical, Elegant

---

## Version Format

Semantic Versioning: MAJOR.MINOR.PATCH

- MAJOR: Breaking changes (1.0.0 -> 2.0.0)
- MINOR: New features, backward compatible (1.0.0 -> 1.1.0)
- PATCH: Bug fixes, backward compatible (1.0.0 -> 1.0.1)

Pre-release: 1.0.1-beta, 1.0.1-rc.1

---

## Automated Release Process

### Contributor Workflow

1. Write code
2. Commit with Conventional Commits (feat, fix, chore, etc.)
3. Open pull request
4. Merge to main

### CI/CD Automation

On push to main, GitHub Actions:
1. Runs tests (pytest)
2. Runs lint (black, isort, flake8)
3. Calculates version from commit messages
4. Updates pyproject.toml
5. Creates git tag
6. Generates CHANGELOG
7. Creates GitHub Release

### Manual Confirmation (Current)

Configuration: upload_to_release = false

After automated version calculation:
```bash
# Review calculated version
git show

# Confirm and publish
pdm run semantic-release publish
git push --follow-tags
```

This provides a safety valve while automation is new.

Future: Enable auto-publish when confident.

---

## Conventional Commits

Version calculation depends on commit types:

- feat: MINOR bump (1.0.0 -> 1.1.0)
- fix: PATCH bump (1.0.0 -> 1.0.1)
- chore, docs, style, test, refactor: No version bump

REFERENCE: .github/COMMIT_CONVENTION.md

Example:
```bash
git commit -m "feat(cli): add search command"
git commit -m "fix(scanner): handle empty input"
git commit -m "chore(scripts): add release.sh"
```

---

## Single Source of Truth

Version is maintained in: pyproject.toml only

src/traceflux/__version__.py reads from package metadata at runtime.

```python
# src/traceflux/__version__.py
import importlib.metadata

try:
    __version__ = importlib.metadata.version("traceflux")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0-dev"
```

---

## CI/CD Workflows

### pr-check.yml

Trigger: Pull request to main

Jobs:
- commitlint: Validates commit message format

### test.yml

Trigger: Pull request or push to main

Jobs:
- test: Pytest with PDM
- lint: Black, isort, flake8 with PDM

### cd.yml

Trigger: Push to main

Jobs:
- release: python-semantic-release automation

---

## Code Quality Standards

### Pre-commit Hooks

Enabled via: git config core.hooksPath .githooks

Checks:
- Python syntax validation
- Code formatting (black)
- Import order (isort)
- Linting (flake8)

### CI/CD Checks

All PRs and pushes must pass:
- pytest -v (all tests)
- black --check (formatting)
- isort --check-only (imports)
- flake8 (linting)

---

## Branch Protection

### main Branch

- Require pull request reviews
- Require status checks (CI/CD)
- Require branches to be up to date
- No force pushes
- No direct commits

### Feature Branches

- Short-lived (days, not weeks)
- Named: issue/number-description or feature/description
- Must pass CI before merge

---

## Emergency Procedures

### Hotfix Release

```bash
# 1. Create hotfix branch from tag
git checkout v1.0.0
git checkout -b hotfix/critical-bug

# 2. Fix, test, commit with "fix" type
git commit -m "fix: critical bug description"

# 3. Push to trigger CI/CD
git push origin main
```

CI/CD will auto-calculate version (1.0.0 -> 1.0.1) and create release.

### Rollback

```bash
# 1. Delete bad tag
git tag -d v1.0.1
git push origin :refs/tags/v1.0.1

# 2. Revert commit
git revert HEAD

# 3. Push to trigger new release
git push origin main
```

---

## Related Files

- .github/workflows/pr-check.yml — PR validation
- .github/workflows/test.yml — Test and lint
- .github/workflows/cd.yml — Release automation
- pyproject.toml — Version source of truth
- .github/COMMIT_CONVENTION.md — Commit message guide
- CONTRIBUTING.md — Contributor guidelines

---

Last Updated: 2026-03-10
Status: Automated with manual confirmation
