# traceflux Testing Philosophy

> **Tests consolidate confidence, but real usage validates value.**

---

## Testing Philosophy

### Core Principle: Information Gain / Cost

We maximize **information gained per test written**. Not all tests are equal.

**Questions before writing a test**:
1. What failure mode does this catch?
2. How likely is this failure?
3. What's the maintenance cost?
4. Is there a cheaper way to get this confidence?

### Necessary vs Sufficient

**Necessary tests** (must have):
- Core functionality broken → user can't complete primary task
- Silent failures → wrong results without error
- Regression risks → frequently modified code

**Sufficient tests** (nice to have):
- Edge cases with low probability
- Implementation details (test behavior, not internals)
- Third-party library behavior

### Limited Testing Strategy

| Test Type | Count | Purpose | Example |
|-----------|-------|---------|---------|
| **Unit** | ~150 | Individual components | Scanner, Graph, PageRank |
| **Component** | ~40 | Module integration | CLI + Scanner + Index |
| **Integration** | ~3 | Data flow end-to-end | Pipeline: file → tokens → associations |
| **E2E** | ~10 | Real user workflows | "Explore codebase via associations" |

**Total**: ~200 tests, <30 seconds, 92%+ coverage

---

## What We Test (And Why)

### ✅ Test: Core Search & Discovery

```python
def test_search_finds_occurrences():
    """Search must find text in files."""
    # Why: Primary use case - if this breaks, tool is useless

def test_associations_discovers_related_terms():
    """Associations must return meaningful results."""
    # Why: Differentiator from grep - core value proposition
```

### ✅ Test: Semantic Segmentation

```python
def test_ip_addresses_stay_intact():
    """127.0.0.1 should not split into [127, 0, 0, 1]."""
    # Why: Semantic meaning lost if split - breaks real usage
```

### ✅ Test: Real Corpus Validation

```python
def test_search_python_code():
    """Search works on actual Python files."""
    # Why: Synthetic tests pass, real usage fails (learned from bug)
```

### ✅ Test: Pipeline Integration

```python
def test_stdin_pipe_support():
    """cat file | traceflux search 'term' - works."""
    # Why: UNIX philosophy - must compose with other tools
```

---

## What We DON'T Test (And Why)

### ❌ Don't Test: Third-Party Libraries

```python
# DON'T: Test that json.load() works
# Why: Python stdlib is tested by CPython team
```

### ❌ Don't Test: Implementation Details

```python
# DON'T: Test internal variable names or private methods
# Why: Refactoring should not break tests - test behavior, not structure
```

### ❌ Don't Test: Every Edge Case

```python
# DON'T: Test empty file, 1-byte file, 1GB file, etc.
# Why: Diminishing returns - test representative cases
```

### ❌ Don't Test: Performance Benchmarks (Currently)

```python
# DON'T: Assert search completes in <100ms
# Why: Flaky on CI, premature optimization (Phase 4 abandoned)
```

### ❌ Don't Test: Phase 4 Features

```python
# DON'T: Indexing, caching, parallel processing
# Why: Abandoned per UNIX philosophy decision (issue #6)
```

---

## Test Organization

### File Naming

```
tests/
├── test_scanner_unit.py          # Unit tests for scanner.py
├── test_graph_unit.py            # Unit tests for graph.py
├── test_associations_integration.py  # Integration tests
├── test_real_corpus_e2e.py       # E2E tests with real data
└── test_explore_workflow_e2e.py  # E2E user workflows
```

### Naming Pattern

- `*.unit.test.py` or `test_*_unit.py` — Unit tests
- `*.integration.test.py` or `test_*_integration.py` — Integration tests
- `*.e2e.test.py` or `test_*_e2e.py` — E2E tests

### Directory Structure

```
traceflux/
├── src/traceflux/
│   ├── scanner.py
│   ├── graph.py
│   └── cli.py
├── tests/
│   ├── test_scanner_unit.py
│   ├── test_graph_unit.py
│   └── test_real_corpus_e2e.py
├── test_corpus/
│   ├── python_code.py
│   ├── error.log
│   └── README.md
└── TESTING.md
```

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

### Coverage Targets

- **Overall**: 90%+
- **Core modules** (scanner, graph, associations): 95%+
- **CLI**: 85%+ (UI logic less critical)

### CI/CD Integration (Future)

```yaml
# .github/workflows/test.yml (not yet implemented)
- run: pytest --cov=src/traceflux --cov-report=xml
- upload coverage to Codecov
```

---

## Test Quality Principles

### 1. Tests Should Not Break on Refactoring

```python
# BAD: Tests internal implementation
assert scanner._tokens[0] == "proxy"

# GOOD: Tests behavior
results = search("proxy", file)
assert len(results) > 0
```

### 2. Tests Should Be Understandable Without Comments

```python
# BAD: Requires comment to understand
def test_foo():
    # Check that the thing works with the stuff
    assert func(x) == y

# GOOD: Self-documenting
def test_search_finds_occurrences():
    results = search("proxy", "test.txt")
    assert len(results) > 0
```

### 3. Tests Should Fail Clearly

```python
# BAD: Unclear failure
assert len(results) == expected

# GOOD: Clear failure message
assert len(results) == expected, f"Expected {expected} results, got {len(results)}: {results}"
```

### 4. Tests Should Be Fast

```python
# BAD: Slow test (>1 second)
# GOOD: Fast test (<100ms)
# Why: Slow tests discourage running tests frequently
```

---

## E2E Test Scenarios (Completed)

### 1. Code Exploration Workflow ✅

```python
def test_e2e_code_exploration():
    """User searches 'PageRank', discovers related modules."""
    # Implemented in: test_explore_workflow_e2e.py
```

### 2. Documentation Navigation ✅

```python
def test_e2e_docs_navigation():
    """User searches 'proxy' in docs, finds proxychains config."""
    # Implemented in: test_real_corpus_e2e.py
```

### 3. Research Note Discovery ✅

```python
def test_e2e_note_discovery():
    """User follows association chain, finds unexpected connections."""
    # Implemented in: test_explore_workflow_e2e.py
```

### 4. Real Corpus Validation ✅

```python
def test_search_python_code(): ...
def test_search_log_files(): ...
def test_search_markdown_docs(): ...
# Implemented in: test_real_corpus_e2e.py (9 tests)
```

---

## Lessons Learned

### Lesson 1: Tests Pass ≠ Software Works

**Problem**: 193 tests passing, but `traceflux search` returned no results.

**Cause**: Search used PatternDetector (complex) instead of direct scanning.

**Fix**: Rewrote search to work like grep.

**Lesson**: Need real-world E2E tests, not just synthetic unit tests.

**Action**: Added 9 real corpus tests.

---

### Lesson 2: Simple > Over-engineered

**Problem**: Search was broken, associations returned empty.

**Cause**: Over-engineered architecture (PatternDetector, complex pipelines).

**Fix**: Simple direct text scanning.

**Lesson**: Simple things should be simple.

---

### Lesson 3: Semantic Understanding Matters

**Problem**: "127.0.0.1" segmented as ["127", "0", "0", "1"].

**Impact**: Lost all semantic meaning.

**Fix**: Context-aware segmentation (preserve IPs, versions, identifiers).

**Lesson**: Algorithms must respect real-world semantics.

---

## Related Documents

- `README.md` — Project overview and quick start
- `docs/` — Detailed documentation
- `memory/` — Development session logs (in workspace memory)

---

**Last Updated**: 2026-03-07  
**Status**: Complete — All test philosophy documented
