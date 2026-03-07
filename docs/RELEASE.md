# Release Guide

**Purpose**: Document the release process for traceflux.

**Audience**: Maintainers and contributors.

---

## Version Numbering

traceflux follows [Semantic Versioning](https://semver.org/):

```
MAJOR.MINOR.PATCH
```

| Component | When to Increment | Example |
|-----------|------------------|---------|
| **MAJOR** | Breaking changes | 1.0.0 → 2.0.0 |
| **MINOR** | New features (backward compatible) | 1.0.0 → 1.1.0 |
| **PATCH** | Bug fixes (backward compatible) | 1.0.0 → 1.0.1 |

**Pre-release versions**:
- `1.0.1-alpha` - Early testing
- `1.0.1-beta` - Feature complete, testing
- `1.0.1-rc.1` - Release candidate

---

## Release Process

### Step 1: Prepare Release

**Update CHANGELOG.md**:
```markdown
## [1.0.1] - 2026-03-07

### Added
- New feature description

### Changed
- Changed behavior description

### Fixed
- Bug fix description
```

**Update version in documentation** if needed.

### Step 2: Run Release Script

```bash
cd /home/openclaw/tracer/dev-repo/traceflux
./scripts/release.sh 1.0.1
```

This script:
1. ✅ Validates version format (SemVer)
2. ✅ Updates `pyproject.toml`
3. ✅ Updates `src/traceflux/__version__.py`
4. ✅ Verifies version consistency
5. ✅ Runs tests (must pass)
6. ✅ Creates git commit
7. ✅ Creates git tag

### Step 3: Review Changes

```bash
git show
git tag -l
```

Verify:
- [ ] Version updated correctly
- [ ] Tests passed
- [ ] Commit message is clear
- [ ] Tag created

### Step 4: Push to GitHub

```bash
git push origin main --tags
```

This triggers CI/CD pipeline:
1. 🧪 Tests run on Python 3.10-3.13
2. 🔍 Linting checks (black, flake8, isort, mypy)
3. 📦 Package build
4. 🚀 GitHub Release creation

### Step 5: Verify Release

**Check GitHub Release**:
- Visit: https://github.com/tracer-mohist/traceflux/releases
- Verify release notes

**Test installation** (from source):
```bash
git clone https://github.com/tracer-mohist/traceflux.git
cd traceflux
pip install -e .
traceflux --version
```

---

## Manual Release (Fallback)

If the release script fails:

### Manual Version Update

```bash
# Update pyproject.toml
sed -i 's/^version = ".*"/version = "1.0.1"/' pyproject.toml

# Update __version__.py
cat > src/traceflux/__version__.py <<EOF
__version__ = "1.0.1"
__version_info__ = (1, 0, 1)
EOF

# Verify
grep '^version = ' pyproject.toml
grep '^__version__ = ' src/traceflux/__version__.py
```

### Manual Commit and Tag

```bash
git add -A
git commit -m "Release v1.0.1"
git tag -a "v1.0.1" -m "Release v1.0.1"
git push origin main --tags
```

---

## CI/CD Pipeline

### Triggers

| Event | Branch/Tag | Actions |
|-------|------------|---------|
| Push | `main` | Test, Lint |
| Pull Request | `main` | Test, Lint |
| Tag | `v*` | Test, Lint, GitHub Release |

### Jobs

1. **test** - Run tests (Python 3.12)
2. **lint** - Code quality checks (black, isort, flake8)
3. **release** - Create GitHub Release (tag only)

### Secrets Required

None required for GitHub Releases only.

---

## Hotfix Release

For urgent bug fixes:

1. Create branch from latest release tag:
   ```bash
   git checkout v1.0.0
   git checkout -b hotfix/critical-bug
   ```

2. Fix the bug, add test

3. Release with patch version:
   ```bash
   ./scripts/release.sh 1.0.1
   git push origin main --tags
   ```

---

## Troubleshooting

### Tests Fail During Release

**Problem**: Release script aborts due to test failure.

**Solution**:
1. Fix the failing tests
2. Commit the fix
3. Re-run release script

### Tag Already Exists

**Problem**: `Tag v1.0.1 already exists`

**Solution**:
```bash
# Delete local tag
git tag -d v1.0.1

# Delete remote tag (if pushed)
git push origin :refs/tags/v1.0.1

# Re-run release script
./scripts/release.sh 1.0.1
```

### Version Mismatch

**Problem**: `pyproject.toml` and `__version__.py` don't match.

**Solution**:
```bash
# Check current versions
grep '^version = ' pyproject.toml
grep '^__version__ = ' src/traceflux/__version__.py

# Manually sync if needed
# Then re-run release script
```

### CI/CD Fails After Push

**Problem**: GitHub Actions workflow fails.

**Solution**:
1. Check workflow logs on GitHub
2. Fix the issue locally
3. Commit and push fix
4. CI/CD will re-run automatically

---

## Related Files

| File | Purpose |
|------|---------|
| `scripts/release.sh` | Release automation script |
| `.github/workflows/ci.yml` | CI/CD pipeline definition |
| `.githooks/pre-commit` | Pre-commit code quality checks |
| `CHANGELOG.md` | Version history |
| `pyproject.toml` | Package configuration |
| `src/traceflux/__version__.py` | Version information |

---

**Last Updated**: 2026-03-07  
**Version**: 1.0.0
