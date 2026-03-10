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

## Release Process (Automated with semantic-release)

### 1. Calculate Next Version

```bash
# Preview version bump based on commit messages
semantic-release version --print
```

This analyzes commits since last tag and suggests:
- `patch` for `fix:` commits
- `minor` for `feat:` commits
- `major` for `feat!:` or `BREAKING CHANGE`

### 2. Generate Changelog (Preview)

```bash
# Preview changelog
semantic-release changelog --print
```

### 3. Create Release (Manual Confirmation)

```bash
# Run release (updates version, creates tag, generates changelog)
semantic-release version

# Review changes
git show

# Push to trigger GitHub Release
git push origin main --tags
```

### 4. Publish to GitHub Release

```bash
# After push, create GitHub Release with notes
semantic-release publish
```

**NOTE**: Current config has `upload_to_release = false` for manual control.

---

## Manual Release (Fallback)

If semantic-release is unavailable:

```bash
# 1. Update pyproject.toml
sed -i 's/^version = ".*"/version = "1.0.1"/' pyproject.toml

# 2. Commit and tag
git add pyproject.toml
git commit -m "Release v1.0.1"
git tag -a "v1.0.1" -m "Release v1.0.1"

# 3. Push
git push origin main --tags
```

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

### Tests Fail

Fix the issue, re-run `semantic-release version`.

### Tag Exists

```bash
git tag -d v1.0.1
git push origin :refs/tags/v1.0.1
semantic-release version
```

### Preview Without Changes

```bash
# Dry-run mode (no file modifications)
semantic-release version --dry-run
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
