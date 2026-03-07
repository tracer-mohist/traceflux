# traceflux Development Tasks

**Purpose**: Track development tasks, improvements, and releases for traceflux.

**Last Updated**: 2026-03-07

---

## Phase 6: Release Automation & Security

### Dependencies

```
#60 (Security Audit) 
  ↓
#61 (Git History Cleanup) 
  ↓
#62 (Repository Foundation Files) 
  ↓
#63 (Version Automation) 
  ↓
#64 (GitHub Release Automation)
```

---

## Tasks

### #60 Security Audit & Documentation ⏳ Current

**Priority**: Critical  
**Status**: In Progress  
**Dependencies**: None

**Tasks**:
- [x] Identify email leakage in git history
- [ ] Create SECURITY.md
- [ ] Document security best practices
- [ ] Review code for sensitive data

**Acceptance Criteria**:
1. SECURITY.md created with clear guidelines
2. No sensitive data in codebase
3. Security contact method documented

---

### #61 Git History Cleanup

**Priority**: Critical  
**Status**: Pending  
**Dependencies**: #60

**Tasks**:
- [ ] Rewrite git history to replace `tracer.mohist@outlook.com` with GitHub noreply email
- [ ] Force push to remote repository
- [ ] Verify all commits use `265808142+tracer-mohist@users.noreply.github.com`
- [ ] Document the cleanup in CHANGELOG.md

**Technical Details**:
```bash
# Affected commits (4 commits with real email):
cbab197a - a1a3181e

# Use git filter-branch or git rebase -i
git filter-branch --env-filter '
export GIT_AUTHOR_EMAIL="265808142+tracer-mohist@users.noreply.github.com"
export GIT_COMMITTER_EMAIL="265808142+tracer-mohist@users.noreply.github.com"
' --tag-name-filter cat -- --all
```

**Acceptance Criteria**:
1. Zero commits with `tracer.mohist@outlook.com`
2. All commits use GitHub noreply email
3. Remote repository updated (force push)
4. Git history intact (no lost commits)

**Warning**: This rewrites history. Coordinate with any collaborators.

---

### #62 Repository Foundation Files

**Priority**: High  
**Status**: Pending  
**Dependencies**: #61

**Tasks**:
- [ ] Update README.md
  - Remove pip installation (only pipx recommended)
  - Add security badge
  - Add contributor guidelines link
- [ ] Create CONTRIBUTING.md
  - How to contribute
  - Code style guidelines
  - PR process
  - Issue reporting
- [ ] Create CODE_OF_CONDUCT.md
  - Use Contributor Covenant
  - Enforcement guidelines
- [ ] Create SECURITY.md (part of #60)
  - Reporting vulnerabilities
  - Security best practices
  - Contact method
- [ ] Verify LICENSE exists (MIT - already present)

**Acceptance Criteria**:
1. All 5 files present (README, LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY)
2. README.md updated with pipx-only installation
3. CONTRIBUTING.md clear and actionable
4. CODE_OF_CONDUCT.md uses standard template
5. SECURITY.md includes reporting process

---

### #63 Version Automation

**Priority**: High  
**Status**: Pending  
**Dependencies**: #62

**Tasks**:
- [ ] Define version source of truth
  - Single file (e.g., `src/traceflux/__version__.py` or `pyproject.toml`)
  - Auto-sync between files
- [ ] Implement semantic versioning
  - MAJOR.MINOR.PATCH format
  - Version bump script or tool
- [ ] Git tag integration
  - Tags match version (v1.0.0, v1.1.0, etc.)
  - Automated tag creation on release
- [ ] Version display
  - `traceflux --version` reads from source
  - Consistent across CLI and package

**Implementation Options**:

**Option A: Single Source (Recommended)**
```python
# src/traceflux/__version__.py
__version__ = "1.0.0"

# pyproject.toml references it (or vice versa)
# pyproject.toml
[project]
version = "1.0.0"  # Manually sync or use dynamic version
```

**Option B: Automated Sync**
```bash
# Use bump2version or similar tool
bump2version patch  # 1.0.0 -> 1.0.1
bump2version minor  # 1.0.1 -> 1.1.0
bump2version major  # 1.1.0 -> 2.0.0
```

**Acceptance Criteria**:
1. Single source of truth for version
2. `traceflux --version` works correctly
3. Version can be bumped easily
4. Git tags match version numbers

---

### #64 GitHub Release Automation

**Priority**: High  
**Status**: Pending  
**Dependencies**: #63

**Tasks**:
- [ ] Create release notes template
  - What's Changed
  - New Features
  - Bug Fixes
  - Breaking Changes
  - Contributors
- [ ] Automate release creation
  - Script using `gh release create`
  - Auto-generate changelog from git history
  - Attach binaries if needed
- [ ] Integrate with version system
  - Release tag = version tag
  - Automatic version bump after release
- [ ] Document release process
  - Step-by-step guide
  - Checklist for releases

**Release Script Example**:
```bash
#!/bin/bash
# scripts/release.sh

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "Usage: $0 <version>"
    exit 1
fi

# Create git tag
git tag -a "v$VERSION" -m "Release v$VERSION"

# Create GitHub release
gh release create "v$VERSION" \
  --title "v$VERSION" \
  --notes-file RELEASE_NOTES.md \
  --generate-notes

# Push tag
git push origin "v$VERSION"
```

**Acceptance Criteria**:
1. Release notes template exists
2. Release script works (`scripts/release.sh`)
3. `gh release create` integrated
4. Release process documented
5. First release (v1.0.0) created successfully

---

## Future Phases (Backlog)

### Phase 5C: Code Cleanup (Optional)
- [ ] Unified naming conventions
- [ ] Extract large functions
- [ ] Remove dead code
- [ ] Simplify complex logic

### Phase 5D: Test Quality (Optional)
- [ ] Ensure tests document behavior
- [ ] Remove redundant tests
- [ ] Improve test names
- [ ] Add missing edge cases

### Phase 5E: Final Review (Optional)
- [ ] Run linter (ruff/flake8)
- [ ] Run formatter (black)
- [ ] Verify all tests pass
- [ ] Create release notes

### Phase 4: Performance Optimization (Deferred)
**Decision**: Not pursuing. UNIX philosophy — pipe with rg/grep for large files.

---

## Completed Phases

### ✅ Phase 5A: Code Audit
- Reviewed all 9 modules
- Created detailed audit report
- Identified priorities

### ✅ Phase 5B: Documentation & Refactoring
- **5B.1**: Refactored cli.py (602 lines → 7 modules)
- **5B.2**: patterns.py documentation (+265 lines)
- **5B.3**: pagerank.py documentation (+499 lines)
- **5B.4**: associations.py documentation (+336 lines)
- **Total**: +1,100 lines of documentation

### ✅ Phase 60: Security Foundation (Partial)
- Identified email leakage (4 commits)
- pyproject.toml updated (removed email)
- Git configured with noreply email

---

## Quick Reference

### Git History Cleanup
```bash
# Check current emails
git log --all --format="%ae" | sort | uniq -c

# After cleanup, verify
git log --all --format="%ae" | grep -v "noreply.github.com"
# Should return nothing
```

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version bumped
- [ ] Git tag created
- [ ] GitHub release created
- [ ] Announcement (if needed)

---

**Related**:
- `docs/PROJECT-STATUS.md` - Detailed project status
- `docs/TESTING.md` - Testing philosophy
- `docs/INSTALLATION.md` - Installation guide
- `docs/OUTPUT-FORMAT.md` - Output format specification
