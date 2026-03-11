# Testing Philosophy

Purpose: Core principles for testing traceflux.

REFERENCE: CONTRIBUTING.md (how to contribute)
REFERENCE: docs/PHILOSOPHY.md (design philosophy)

---

## Core Principle: Information Gain / Cost

Maximize information gained per test written. Not all tests are equal.

Questions before writing a test:
1. What failure mode does this catch?
2. How likely is this failure?
3. What is the maintenance cost?
4. Is there a cheaper way to get this confidence?

---

## Necessary vs Sufficient

### Necessary Tests (must have)

- Core functionality broken - user cannot complete primary task
- Silent failures - wrong results without error
- Regression risks - frequently modified code

### Sufficient Tests (nice to have)

- Edge cases with low probability
- Implementation details (test behavior, not internals)
- Third-party library behavior

---

## What We Test

### Core Search and Discovery

Search must find text in files. This is the primary use case.

Associations must return meaningful results. This is the differentiator from grep.

### Semantic Segmentation

IP addresses should not split (127.0.0.1 stays intact). Semantic meaning must be preserved.

### Real Corpus Validation

Tests must include real Python files, logs, and documentation. Synthetic tests can pass while real usage fails.

### Pipeline Integration

UNIX pipe support must work. traceflux must compose with other tools.

---

## What We Do NOT Test

### Third-Party Libraries

Do not test that json.load works. Python stdlib is tested by CPython team.

### Implementation Details

Do not test internal variable names or private methods. Refactoring should not break tests.

### Every Edge Case

Do not test empty file, 1-byte file, 1GB file. Test representative cases only.

### Performance Benchmarks

Do not assert search completes in under 100ms. Flaky on CI, premature optimization.

### Abandoned Features

Do not test indexing, caching, parallel processing. These were abandoned per UNIX philosophy.

---

## Test Quality Principles

### 1. Tests Should Not Break on Refactoring

BAD: Tests internal implementation
```python
assert scanner._tokens[0] == "proxy"
```

GOOD: Tests behavior
```python
results = search("proxy", file)
assert len(results) > 0
```

### 2. Tests Should Be Understandable Without Comments

BAD: Requires comment to understand
```python
def test_foo():
    # Check that the thing works with the stuff
    assert func(x) == y
```

GOOD: Self-documenting
```python
def test_search_finds_occurrences():
    results = search("proxy", "test.txt")
    assert len(results) > 0
```

### 3. Tests Should Fail Clearly

BAD: Unclear failure
```python
assert len(results) == expected
```

GOOD: Clear failure message
```python
assert len(results) == expected, f"Expected {expected} results, got {len(results)}"
```

### 4. Tests Should Be Fast

Fast test: under 100ms. Slow tests discourage running tests frequently.

---

## Lessons Learned

### Lesson 1: Tests Pass Does Not Mean Software Works

Problem: 193 tests passing, but traceflux search returned no results.

Cause: Search used PatternDetector (complex) instead of direct scanning.

Fix: Rewrote search to work like grep.

Action: Added real corpus tests.

### Lesson 2: Simple Is Better Than Over-engineered

Problem: Search was broken, associations returned empty.

Cause: Over-engineered architecture.

Fix: Simple direct text scanning.

Lesson: Simple things should be simple.

### Lesson 3: Semantic Understanding Matters

Problem: 127.0.0.1 segmented as 127, 0, 0, 1.

Impact: Lost all semantic meaning.

Fix: Context-aware segmentation.

Lesson: Algorithms must respect real-world semantics.

---

## Related Documents

- CONTRIBUTING.md — How to contribute (includes test guidelines)
- docs/PHILOSOPHY.md — Design philosophy
- docs/TESTING.md — Running tests (quick reference)

---

Last Updated: 2026-03-10
