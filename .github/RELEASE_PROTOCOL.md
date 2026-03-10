# Release Protocol

Purpose: Automated release process with python-semantic-release.

Philosophy: Simple, Practical, Elegant

Last Updated: 2026-03-10

---

## Version Format

Semantic Versioning: MAJOR.MINOR.PATCH

- MAJOR: Breaking changes (1.0.0 -> 2.0.0)
- PATCH: Bug fixes, backward compatible (1.0.0 -> 1.0.1)
- MINOR: New features, backward compatible (1.0.0 -> 1.1.0)

Pre-release: 1.0.1-beta, 1.0.1-rc.1

---

## Automated Release Process

### Workflow

1. Developer writes code
2. Commit with Conventional Commits (feat, fix, chore, etc.)
3. Open pull request
4. Merge to main
5. CI/CD automatically:
   - Runs tests (pytest)
   - Runs lint (black, isort, flake8)
   - Calculates version from commit messages
   - Updates pyproject.toml
   - Creates git tag
   - Generates CHANGELOG
   - Builds package
   - Creates GitHub Release with artifacts

### No Manual Steps

Release is fully automated. No manual confirmation needed.

---

## Conventional Commits

Version calculation depends on commit types:

| Type | Version Bump | Example |
|------|-------------|---------|
| feat | MINOR (1.0.0 -> 1.1.0) | feat(cli): add search command |
| fix | PATCH (1.0.0 -> 1.0.1) | fix(scanner): handle empty input |
| perf | PATCH | perf(index): improve search speed |
| chore, docs, style, test, refactor, build, ci | No bump | chore: update config |

REFERENCE: .github/COMMIT_CONVENTION.md for full guide.

---

## CI/CD Workflows

### pr-check.yml

Trigger: Pull request

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
  - Calculate version
  - Update pyproject.toml
  - Create git tag
  - Build package (pdm build)
  - Upload artifacts to GitHub Release
  - Create GitHub Release

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

## Code Quality Standards

### Pre-commit Hooks

Enabled via pre-commit framework.

Hooks run automatically before commit:
- trailing-whitespace
- end-of-file-fixer
- check-yaml
- check-json
- black (format check)
- isort (import order)
- flake8 (linting)

Install: `pdm run pre-commit install`

### CI/CD Checks

All PRs and pushes must pass:
- pytest -v (all tests)
- black --check (formatting)
- isort --check-only (imports)
- flake8 (linting)
- commitlint (commit message format)

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

- .github/workflows/pr-check.yml - PR validation
- .github/workflows/test.yml - Test and lint
- .github/workflows/cd.yml - Release automation
- pyproject.toml - Version source of truth
- .github/COMMIT_CONVENTION.md - Commit message guide
- CONTRIBUTING.md - Contributor guidelines
- .pre-commit-config.yaml - Pre-commit hooks config

---

Status: Automated (no manual confirmation)
