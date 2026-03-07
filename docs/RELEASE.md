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

## Release Process

### 1. Run Release Script

```bash
./scripts/release.sh 1.0.1
```

This will:
1. Update `pyproject.toml`
2. Run tests (must pass)
3. Create commit and tag

### 2. Review

```bash
git show
```

### 3. Push

```bash
git push origin main --tags
```

### 4. CI/CD Creates Release

GitHub Actions will:
1. Run tests
2. Run linting
3. Create GitHub Release with auto-generated notes

---

## Manual Release (Fallback)

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

Fix the issue, re-run script.

### Tag Exists

```bash
git tag -d v1.0.1
git push origin :refs/tags/v1.0.1
./scripts/release.sh 1.0.1
```

---

**Last Updated**: 2026-03-07  
**Version**: 1.0.0
