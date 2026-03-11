# Testing Quick Reference

Purpose: How to run tests and write new tests.

REFERENCE: docs/TESTING-PHILOSOPHY.md (testing principles)
REFERENCE: CONTRIBUTING.md (contribution guidelines)

---

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/traceflux --cov-report=term-missing

# Run specific test file
pytest tests/test_real_corpus_e2e.py

# Run specific test function
pytest tests/test_scanner_unit.py::test_ip_address_segmentation

# Run tests matching pattern
pytest -k "semantic"
```

### With PDM

```bash
pdm run pytest
pdm run pytest --cov=src/traceflux
```

---

## Test Organization

### File Naming

```text
tests/
├── test_scanner_unit.py          # Unit tests for scanner.py
├── test_graph_unit.py            # Unit tests for graph.py
├── test_associations_integration.py  # Integration tests
├── test_real_corpus_e2e.py       # E2E tests with real data
└── test_explore_workflow_e2e.py  # E2E user workflows
```

### Naming Pattern

- test_*_unit.py - Unit tests
- test_*_integration.py - Integration tests
- test_*_e2e.py - E2E tests

---

## Writing Tests

### Follow Testing Philosophy

REFERENCE: docs/TESTING-PHILOSOPHY.md

Key principles:
1. Test behavior, not implementation
2. Tests should be self-documenting
3. Tests should fail clearly
4. Tests should be fast (under 100ms)

### What to Test

- Core search and discovery
- Semantic segmentation (IP addresses, versions)
- Real corpus validation
- Pipeline integration (UNIX pipes)

### What NOT to Test

- Third-party libraries
- Implementation details
- Every edge case
- Performance benchmarks

---

## Test Quality Checklist

Before submitting a test:

- [ ] Test name describes what is being tested
- [ ] Test fails clearly with useful error message
- [ ] Test runs fast (under 100ms)
- [ ] Test does not depend on internal implementation
- [ ] Test uses real data when possible

---

## CI/CD

Tests run automatically on:
- Pull requests to main
- Pushes to main branch

All tests must pass before merge.

---

## Related Documents

- docs/TESTING-PHILOSOPHY.md - Core testing principles
- CONTRIBUTING.md - How to contribute
- docs/PHILOSOPHY.md - Design philosophy

---

Last Updated: 2026-03-10
