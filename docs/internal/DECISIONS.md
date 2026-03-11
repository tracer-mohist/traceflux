# Infrastructure Decisions

Purpose: Record key infrastructure decisions for traceflux.

Last Updated: 2026-03-10

---

## Decision Records

### 1. Package Manager: PDM

Date: 2026-03-10

Decision: Use PDM as primary package manager.

Why:
- Modern Python package manager (PEP 582 support)
- Lock file for reproducible builds
- Virtual environment management
- Compatible with setuptools build backend

Alternatives Considered:
- pip only (rejected - no lock file)
- Poetry (rejected - PDM is more modern)

ASSUMPTIONS:
- Single developer or small team
- Need reproducible builds

---

### 2. Release Automation: python-semantic-release

Date: 2026-03-10

Decision: Use python-semantic-release v10.5.3 for automated releases.

Why:
- Automatic version calculation from Conventional Commits
- Automatic CHANGELOG generation
- GitHub Release creation
- Well-maintained, official Python implementation

CONFIGURATION:
- upload_to_release = true (auto-publish enabled)
- upload_to_pypi = false (GitHub Releases only)
- branches.main.match = "(main|master)"

Alternatives Considered:
- Manual releases (rejected - too much cognitive load)
- release-please (rejected - python-semantic-release is more flexible)

ASSUMPTIONS:
- Conventional Commits will be followed
- GitHub Releases sufficient (no PyPI needed)

---

### 3. Pre-commit Framework

Date: 2026-03-10

Decision: Use pre-commit framework instead of custom .githooks/.

Why:
- Standard Python community tool
- Declarative configuration (.pre-commit-config.yaml)
- Automatic hook environment management
- Cross-platform (Windows/macOS/Linux)
- PDM integration

Hooks Configured:
- pre-commit-hooks (trailing-whitespace, end-of-file-fixer, check-yaml, check-json)
- black (format check)
- isort (import order)
- flake8 (linting)

Alternatives Considered:
- Custom .githooks/ scripts (rejected - not cross-platform, harder to maintain)

ASSUMPTIONS:
- Developers will run `pdm run pre-commit install`
- CI/CD also runs these checks

---

### 4. CI/CD Structure

Date: 2026-03-10

Decision: Three-workflow structure (pr-check, test, cd).

Why:
- Separation of concerns
- Fast feedback on PRs (commitlint only)
- Full test suite on push/PR
- Automated release on main push

WORKFLOWS:
- pr-check.yml: commitlint on PR
- test.yml: pytest + lint on push/PR
- cd.yml: release automation on main push

Alternatives Considered:
- Single workflow (rejected - slower feedback)
- Two workflows (rejected - PR checks should be fastest)

ASSUMPTIONS:
- GitHub Actions minutes are sufficient
- Most PRs are small (commitlint is fast)

---

### 5. No PyPI Publishing

Date: 2026-03-10

Decision: Publish to GitHub Releases only, not PyPI.

Why:
- CLI tool, users can install from GitHub
- Simpler release process
- No PyPI credentials management
- GitHub Releases include build artifacts

Alternatives Considered:
- PyPI publishing (rejected - adds complexity for minimal benefit)

ASSUMPTIONS:
- Users are comfortable with `pipx install git+https://...`
- No need for PyPI discovery

---

### 6. Documentation Structure

Date: 2026-03-10

Decision: README.md as index.html, detailed docs in docs/.

Why:
- README.md should be short (80 lines)
- Detailed content in separate files
- Clear separation: concepts (docs/) vs procedures (workflow/)

STRUCTURE:
- README.md (80 lines) - Quick start, links
- docs/USAGE.md - Command reference
- docs/ARCHITECTURE.md - How it works
- docs/USE-CASES.md - Real-world examples
- docs/TESTING-PHILOSOPHY.md - Testing principles
- docs/PHILOSOPHY.md - Design philosophy

Alternatives Considered:
- Single large README (rejected - hard to navigate)
- Wiki (rejected - GitHub wiki is separate from repo)

ASSUMPTIONS:
- Users prefer short README
- Detailed docs are linkable

---

### 7. Conventional Commits

Date: 2026-03-10

Decision: Use Conventional Commits v1.0.0 with specific type mappings.

Type Mappings:
- feat -> MINOR
- fix, perf -> PATCH
- chore, docs, style, test, refactor, ci, build -> No bump

Why:
- Machine-readable history
- Automatic version calculation
- Clear intent in commit messages
- Enables automation

Alternatives Considered:
- Angular commits (rejected - conventional is more flexible)
- No convention (rejected - enables automation)

ASSUMPTIONS:
- Contributors will follow convention
- commitlint will enforce on PRs

---

## Related Files

- pyproject.toml - Configuration
- .pre-commit-config.yaml - Pre-commit hooks
- .github/workflows/ - CI/CD workflows
- .github/RELEASE_PROTOCOL.md - Release process
- .github/COMMIT-EXAMPLES.md - Commit examples
- CONTRIBUTING.md - Contribution guidelines

---

## Review Schedule

Review these decisions:
- After first automated release
- After contributor feedback
- Every 3 months

---

Last Updated: 2026-03-10
