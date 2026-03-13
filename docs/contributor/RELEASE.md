# Release Guide

PHILOSOPHY: Simple, Practical, Elegant

---

## Version Format

Semantic Versioning: `MAJOR.MINOR.PATCH`

- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)

Pre-release: `1.0.1-beta`

---

## Single Source of Truth

Only `pyproject.toml` maintains the version.

`__version__.py` reads from package metadata at runtime -- no manual sync needed.

---

## Release Process (Fully Automated)

NOTE: Normal workflow: Just push to main. That's it.

### Automated Release on Push

When you push to `main`, GitHub Actions automatically:
- Validates: Runs tests, lint, format checks
- Calculates: Determines version bump from commit messages
- Updates: Bumps version in `pyproject.toml`
- Generates: Creates changelog entries
- Commits: Creates release commit
- Tags: Creates git tag
- Publishes: Creates GitHub Release

NOTE: No manual steps required.

```bash
# Your workflow:
git commit -m "feat: add new feature"
git push origin main
# Done. CI/CD handles the rest.
```

### Manual Release (Advanced / Emergency Only)

For troubleshooting or special cases, you can run locally:

```bash
# Preview what version would be released
pdm run semantic-release version --print

# Dry run (no modifications)
pdm run semantic-release version --dry-run

# Force release (bypasses automatic calculation)
pdm run semantic-release version --bump major
```

---

## Project Management with PDM

All project commands use `pdm run`:

```bash
# Install dependencies
pdm install

# Run tests
pdm run pytest -v

# Format code
pdm run black src/ tests/
pdm run isort src/ tests/

# Lint
pdm run flake8 src/ tests/

# Run application
pdm run traceflux search "pattern" .
```

Why PDM: Manages virtual environment, dependencies, and command execution in one tool.

---

## Commit Message Convention

Releases are driven by Conventional Commits:

| Type | Example | SemVer Impact |
|------|---------|---------------|
| `feat` | `feat(cli): add search command` | MINOR |
| `fix` | `fix(scanner): handle empty input` | PATCH |
| `feat!` | `feat(api)!: change output format` | MAJOR |
| Others | `chore`, `docs`, `style`, `test` | None |

Full guide: See `.github/COMMIT_CONVENTION.md`

---

## CI/CD Pipeline

| Trigger | Jobs |
|---------|------|
| PR to main | test, lint |
| Push to main | test, lint, release (auto) |

Cost: ~5 minutes per run (single Python version)

Note: Release job runs on every push to main but only creates a release if commit messages warrant a version bump.

---

## Troubleshooting

### Build Command Fails (Tests/Lint)

Fix the reported issues, then re-run:
```bash
pdm run semantic-release version
```

### Tag Already Exists

```bash
git tag -d v1.0.1
git push origin :refs/tags/v1.0.1
pdm run semantic-release version
```

---

## Related Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | semantic-release config + version |
| `.github/COMMIT_CONVENTION.md` | Commit message guide |
| `.github/RELEASE_PROTOCOL.md` | Detailed release protocol |
| `CHANGELOG.md` | Auto-generated changelog |

---

LAST UPDATED: 2026-03-11
VERSION: 1.0.0
Tool: python-semantic-release
