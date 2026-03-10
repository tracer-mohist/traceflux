# TODO: CI/CD Migration Plan

Purpose: Migrate traceflux CI/CD to proper abstraction layer design.

Last Updated: 2026-03-10

REFERENCE: AGENTS.md (analysis and decisions)
REFERENCE: ~/tracer/dev-repo/llm-api-scope/.github/workflows/ (reference implementation)
REFERENCE: .github/PHASE2-TEST-REPORT.md (Phase 2 test results)

---

## Problem Summary

### Current State

- Package Manager: PDM (local development)
- CI Workflow: Uses pip (ignores pdm.lock)
- Release Automation: python-semantic-release configured but not integrated
- CI Release Job: Uses softprops/action-gh-release (only creates Release page, no version automation)

### Core Issues

1. **Abstraction Layer Failure**: Contributors must understand versioning and release process
2. **Inconsistency**: Local uses PDM, CI uses pip
3. **Half-Automation**: python-semantic-release configured but CI does not use it
4. **Transition State**: Phase 8 in progress, not complete

---

## Migration Goals

### Goal 1: Complete Abstraction Layer

Contributor experience after migration:
- Write code
- Commit with Conventional Commits (feat, fix, chore)
- Open PR
- Done (no version decisions, no release commands)

CI/CD handles automatically:
- Version calculation from commit type
- pyproject.toml update
- Git tag creation
- CHANGELOG generation
- GitHub Release creation

### Goal 2: PDM Consistency

- Local development: pdm install --dev
- CI: pdm install --dev (same as local)
- Benefit: Reproducible builds, consistent dependencies

### Goal 3: Proper Tool Naming

- Python package: python-semantic-release
- CLI command: semantic-release
- GitHub Action: python-semantic-release/python-semantic-release@v10.5.3

---

## Task List

### Phase 1: Documentation Cleanup (Priority: High) - COMPLETE

- [x] **1.1**: Update AGENTS.md with correct terminology
- [x] **1.2**: Create this migration plan
- [x] **1.3**: Update .github/RELEASE_PROTOCOL.md (deferred to Phase 3)
- [x] **1.4**: Update CONTRIBUTING.md (complete)
- [x] **1.5**: Rewrite README.md (remove tables, emoji, specific numbers)
- [x] **1.6**: Create docs/TESTING-PHILOSOPHY.md (extract philosophy)
- [x] **1.7**: Simplify TESTING.md (quick reference only)
- [x] **1.8**: Delete RELEASE_ANNOUNCEMENT.md (redundant with GitHub Releases)

### Phase 2: Local Testing (Priority: High) - COMPLETE

- [x] **2.1**: Test python-semantic-release locally with PDM
  - Installed python-semantic-release 10.5.3
- [x] **2.2**: Verify version calculation
  - feat commit -> MINOR bump (1.1.0 -> 1.2.0) PASS
  - fix commit -> PATCH bump PASS
- [x] **2.3**: Test CHANGELOG generation
  - CHANGELOG.md generated successfully
- [x] **2.4**: Document local testing results
  - Report: .github/PHASE2-TEST-REPORT.md

**Configuration Fixes Applied**:
- Updated branch config: `branch = "main"` -> `[tool.semantic_release.branches.main]`
- Synced pyproject.toml version: 1.0.0 -> 1.1.0 (match tag v1.1.0)

### Phase 3: CI Workflow Restructure (Priority: High) - NEXT

- [ ] **3.1**: Create .github/workflows/pr-check.yml
  - Trigger: pull_request
  - Job: commitlint (wagoid/commitlint-github-action)
  - Purpose: Fast feedback on PR commit messages

- [ ] **3.2**: Create .github/workflows/test.yml
  - Trigger: pull_request, push main
  - Jobs: test (pytest), lint (black, isort, flake8)
  - Use PDM: pdm install --dev, pdm run pytest

- [ ] **3.3**: Create .github/workflows/cd.yml
  - Trigger: push main
  - Job: release (python-semantic-release)
  - Use official action: python-semantic-release/python-semantic-release@v10.5.3
  - Configure: git_committer_name, git_committer_email, build: false
  - Add concurrency control

- [ ] **3.4**: Delete old .github/workflows/ci.yml
  - After new workflows tested and working

### Phase 4: Integration Testing (Priority: Medium)

- [ ] **4.1**: Test full workflow on development branch
- [ ] **4.2**: Test concurrency control
- [ ] **4.3**: Test conditional execution
- [ ] **4.4**: Document integration test results

### Phase 5: Migration to Main (Priority: Medium)

- [ ] **5.1**: Backup current CI configuration
- [ ] **5.2**: Merge new workflows to main
- [ ] **5.3**: Delete old ci.yml
- [ ] **5.4**: Verify main branch CI/CD works
- [ ] **5.5**: Create first automated release

### Phase 6: Evaluation (Priority: Low)

- [ ] **6.1**: Collect contributor feedback
- [ ] **6.2**: Measure CI performance
- [ ] **6.3**: Decide on manual confirmation
- [ ] **6.4**: Update documentation

---

## Dependencies

```
Phase 1 (Docs) -> Phase 2 (Local Test) -> Phase 3 (CI Restructure)
                                              |
                                              v
Phase 6 (Evaluation) <- Phase 5 (Main) <- Phase 4 (Integration Test)
```

---

## Success Criteria

- [ ] Contributors can commit without thinking about versions
- [ ] CI uses PDM (consistent with local)
- [ ] python-semantic-release integrated in CI
- [ ] Automated version calculation working
- [ ] Automated CHANGELOG generation working
- [ ] Automated GitHub Release creation working
- [ ] No CI/CD downtime during migration
- [ ] Documentation updated and accurate

---

## Related Files

- AGENTS.md - Analysis and decisions
- .github/workflows/ci.yml - Current CI (to be replaced)
- .github/RELEASE_PROTOCOL.md - Release process (to be updated)
- CONTRIBUTING.md - Contributor guide (to be updated)
- pyproject.toml - python-semantic-release config
- .github/PHASE2-TEST-REPORT.md - Phase 2 test results
- ~/tracer/dev-repo/llm-api-scope/.github/workflows/ - Reference implementation

---

Principle: Complete the transition. Half-automation is more confusing than no automation.
