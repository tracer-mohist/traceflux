# traceflux Todo

Last Updated: 2026-03-10

---

## Phase 8: Release Automation (In Progress)

### Completed

- [x] Step 1: Configuration
  - pyproject.toml semantic_release config
  - branches.main configuration
  - commit_parser_options
  - upload_to_release = true (auto-publish enabled)

- [x] Step 2: Documentation
  - Conventional Commits guide (CONTRIBUTING.md)
  - Local testing (.github/PHASE2-TEST-REPORT.md)
  - RELEASE_PROTOCOL.md updated
  - COMMIT-EXAMPLES.md created

- [x] Step 3: CI/CD Migration
  - pr-check.yml (commitlint)
  - test.yml (pytest + lint with PDM)
  - cd.yml (python-semantic-release + build)
  - Deleted old ci.yml
  - .commitlintrc.json

- [x] Step 4: Pre-commit Framework
  - Added pre-commit dev dependency
  - Created .pre-commit-config.yaml
  - Installed hooks
  - Removed .githooks/

### Remaining

- [ ] Test CI/CD workflows on branch
- [ ] Verify auto-publish works
- [ ] Create first automated release

---

## Phase 7: Documentation Cleanup (Complete)

- [x] Removed 8 redundant files
- [x] Created docs/USAGE.md, ARCHITECTURE.md, USE-CASES.md, TESTING-PHILOSOPHY.md
- [x] Trimmed README.md to 80 lines
- [x] Simplified TESTING.md

---

## Backlog (Optional)

### Phase 5C: Code Cleanup

- [ ] Unified naming conventions
- [ ] Extract large functions
- [ ] Remove dead code

### Phase 5D: Test Quality

- [ ] Ensure tests document behavior
- [ ] Improve test names
- [ ] Add missing edge cases

---

## Principle

Focus on completing Phase 8. Optional phases (5C, 5D) can be deferred.

---
