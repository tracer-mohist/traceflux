# traceflux Todo

## Active (当前进行)

- [ ] **Phase 8: Release Automation Upgrade** (python-semantic-release)
  - [ ] **Step 1: Configuration** (30 min)
    - [ ] Add minimal config to pyproject.toml
    - [ ] Configure commit parser (angular)
    - [ ] Disable auto-publish (manual confirmation)
    - [ ] Disable PyPI publishing
  - [ ] **Step 2: Documentation** (30 min)
    - [ ] Add Conventional Commits guide to CONTRIBUTING.md
    - [ ] Update RELEASE.md with new workflow
    - [ ] Create commit examples
  - [ ] **Step 3: Testing** (1-2 releases)
    - [ ] Test version calculation
    - [ ] Test CHANGELOG generation
    - [ ] Test GitHub Release creation
    - [ ] Verify manual confirmation works
  - [ ] **Step 4: Evaluation**
    - [ ] Collect new contributor feedback
    - [ ] Assess maintainer experience
    - [ ] Decide: enable auto-publish or keep manual

- [ ] **Phase 7: Documentation Cleanup** (Simplify)
  - [ ] **Remove Redundant Files**
    - [ ] Delete RELEASE_NOTES.md (duplicate)
    - [ ] Delete RELEASE_NOTES_TEMPLATE.md (script has logic)
    - [ ] Delete INSTALLATION_TEST.md (temporary)
    - [ ] Delete docs/README.md (duplicate)
    - [ ] Delete docs/PROJECT-STATUS.md (outdated)
    - [ ] Delete docs/PYTHON-INFRASTRUCTURE-PLAN.md (outdated)
  - [ ] **Reorganize**
    - [ ] Create research/ directory
    - [ ] Move IMPLEMENTATION-DESIGN.md to research/
    - [ ] Merge TESTING.md (keep root version)
  - [ ] **Simplify Content**
    - [ ] Trim README.md to <200 lines
    - [ ] Ensure single responsibility per doc
    - [ ] Update all internal links

---

## Backlog (待办)

- [ ] **Phase 5C: Code Cleanup** (Optional)
  - [ ] Unified naming conventions
  - [ ] Extract large functions
  - [ ] Remove dead code
  - [ ] Simplify complex logic

- [ ] **Phase 5D: Test Quality** (Optional)
  - [ ] Ensure tests document behavior
  - [ ] Remove redundant tests
  - [ ] Improve test names
  - [ ] Add missing edge cases

- [ ] **Phase 5E: Final Review** (Optional)
  - [ ] Run linter (ruff/flake8)
  - [ ] Run formatter (black)
  - [ ] Verify all tests pass
  - [ ] Create release notes

---

## Deferred (延期)

- [ ] **Phase 4: Performance Optimization**
  - [x] Decision: Not pursuing
  - [x] Reason: UNIX philosophy — pipe with rg/grep for large files

---

## Completed ✅

- [x] **Phase 6: Release Automation & Security**
  - [x] #28 Security Audit & Documentation
  - [x] #29 Repository Foundation Files
  - [x] #30 Version Automation
  - [x] #31 GitHub Release Automation
  - [x] v1.0.0 released

- [x] **Phase 5: Code Quality & Maintainability**
  - [x] 5A Code Audit (9 modules reviewed)
  - [x] 5B Documentation & Refactoring (+1,100 lines)

- [x] **Phase 3: Core Features**
  - [x] Search
  - [x] Patterns
  - [x] Associations
  - [x] Index

- [x] **Phase 2: Infrastructure**
  - [x] CI/CD
  - [x] Git hooks
  - [x] Release script
  - [x] Documentation

- [x] **Phase 1: Foundation**
  - [x] Project initialization
  - [x] Core architecture
  - [x] Basic search
