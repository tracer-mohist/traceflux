<!-- docs/RELEASE.md -->
# Release Guide

**Philosophy**: Simple, Practical, Elegant

---

## Version Format

Semantic Versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

**Pre-release**: `1.0.1-beta`

---

## Single Source of Truth

**Only `pyproject.toml` maintains the version.**

`__version__.py` reads from package metadata at runtime — no manual sync needed.

---

## Release Process (Fully Automated)

### Single Command Release

```bash
# Run release - everything is automated
pdm run semantic-release version
```

This automatically:
1. **Validates** - Runs tests, lint, format checks (via `build_command`)
2. **Calculates** - Determines version bump from commit messages
3. **Updates** - Bumps version in `pyproject.toml`
4. **Generates** - Creates changelog entries
5. **Commits** - Creates release commit
6. **Tags** - Creates git tag

### 2. Push to Publish

```bash
# Push triggers GitHub Release creation
git push origin main --tags
```

CI/CD will automatically create GitHub Release with changelog.

---

## Manual Override (If Needed)

### Preview Version Bump

```bash
# See what version would be released
pdm run semantic-release version --print
```

### Preview Changelog

```bash
# See changelog entries
pdm run semantic-release changelog --print
```

### Dry Run

```bash
# Test release without modifications
pdm run semantic-release version --dry-run
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

**Why PDM**: Manages virtual environment, dependencies, and command execution in one tool.

---

## Commit Message Convention

Releases are driven by Conventional Commits:

| Type | Example | SemVer Impact |
|------|---------|---------------|
| `feat` | `feat(cli): add search command` | MINOR |
| `fix` | `fix(scanner): handle empty input` | PATCH |
| `feat!` | `feat(api)!: change output format` | MAJOR |
| Others | `chore`, `docs`, `style`, `test` | None |

**Full guide**: See `.github/COMMIT_CONVENTION.md`

---

## CI/CD Pipeline

| Trigger | Jobs |
|---------|------|
| PR to main | test, lint |
| Push to main | test, lint |
| Tag v* | test, lint, release |

**Cost**: ~5 minutes per run (single Python version)

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

### Force Specific Version Bump

```bash
# Force major/minor/patch bump
pdm run semantic-release version --bump major
pdm run semantic-release version --bump minor
pdm run semantic-release version --bump patch
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

**Last Updated**: 2026-03-10  
**Version**: 1.0.0  
**Tool**: python-semantic-release
