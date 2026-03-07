# traceflux Testing Strategy

> "Tests consolidate the logic we are confident in, not prove the program is correct."

---

## Philosophy

### What Tests Are For

1. **Verify necessary conditions** — If the program is correct, these tests must pass
2. **Consolidate confidence** — Anchor the logic we trust
3. **Document behavior** — Explain what the system does in human language
4. **Catch regressions** — Alert when critical logic breaks

### What Tests Are NOT For

1. ❌ Prove the program is completely correct (mathematically impossible)
2. ❌ Cover every input path (input space is infinite)
3. ❌ Test implementation details (these change with refactoring)
4. ❌ Inflate coverage numbers (vanity metrics)

---

## Limited Testing Principles

### Core Insight

**Test efficiency = Information gain / Cost**

Maximize information gain, minimize maintenance cost.

### Input Space Partitioning

```
I = I_u ∪ I_c ∪ I_i ∪ I_e ∪ I_untested
```

We acknowledge `I_untested` exists and always will.

Focus on `T ∩ C_ε` — tests covering inputs with importance > threshold.

**Importance = User-perceived impact × Failure severity**

---

## Four Test Types

### 1. Unit Tests (`*.unit.test.*`)

**Purpose**: Verify function logic correctness

**Scope**: Individual functions, isolated from dependencies

**Quantity**: Proportional to logical complexity (cyclomatic complexity)

**Example**:
```python
def test_pagerank_convergence():
    # Scenario: PageRank runs on a connected graph
    # Expected: Scores converge to stable distribution summing to 1.0
    # If fails: All association rankings are wrong
    graph = CooccurrenceGraph()
    graph.add_cooccurrence("A", "B", weight=5)
    graph.add_cooccurrence("B", "C", weight=3)
    
    scores = compute_pagerank(graph, max_iterations=100)
    
    assert abs(sum(scores.values()) - 1.0) < 0.001
```

**Keep when**:
- Tests core algorithm logic
- Failure would affect all downstream features
- Logic is non-trivial (not just getters/setters)

**Remove when**:
- Tests Python built-in behavior (`char.isalnum()`)
- Tests trivial property access
- Information gain ≈ 0

---

### 2. Component Tests (`*.component.test.*`)

**Purpose**: Verify component contract implementation

**Scope**: Public interfaces, main scenarios + critical exceptions

**Quantity**: Cover all public interface main scenarios

**Example**:
```python
def test_search_command_with_json_output():
    # Scenario: User wants machine-readable output for piping to jq
    # Expected: Valid JSON with query, results, total_matches
    # If fails: Users can't compose traceflux with other tools
    result = main(["search", "hello", str(tmp_path), "--json"])
    output = json.loads(capsys.readouterr().out)
    
    assert "query" in output
    assert "results" in output
    assert "total_matches" in output
```

**Keep when**:
- Tests user-facing interface
- Documents expected behavior
- Failure breaks user workflows

---

### 3. Integration Tests (`*.integration.test.*`)

**Purpose**: Verify critical data flows between components

**Scope**: Actually used component combinations only

**Quantity**: Limited to real integration points

**Example**:
```python
def test_full_pipeline_basic():
    # Scenario: User runs traceflux end-to-end
    # Expected: Text → patterns → graph → associations
    # If fails: Core value proposition broken
    text = "proxy config proxy settings proxychains config"
    
    scanner = Scanner()
    detector = PatternDetector(min_support=2)
    patterns = detector.find_patterns(text)
    
    graph = CooccurrenceGraph()
    graph.add_document_cooccurrences(list(patterns.keys()), window_size=3)
    
    assert graph.node_count() >= 1
```

**Keep when**:
- Tests real data flow
- Catches interface mismatches
- Validates component contracts together

---

### 4. E2E Tests (`*.e2e.test.*`)

**Purpose**: Verify core user value

**Scope**: Complete user workflows, business-impacting

**Quantity**: 5-15 tests maximum (must choose carefully)

**Example**:
```python
def test_explore_codebase_workflow():
    # Scenario: Developer exploring unfamiliar codebase
    # Workflow: Run traceflux associations "proxy" src/
    # Expected: Discovers proxychains, HTTP_PROXY, git config
    # Value: Finds unknown related concepts
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create sample codebase
        (Path(tmpdir) / "main.py").write_text("""
def main():
    config = load_config()
    proxy = setup_proxy(config)
    run(proxy)
""")
        # Run traceflux
        all_text = Path(tmpdir).read_text()
        # ... full pipeline
        
        # Should find associations
        assert result.query == "proxy"
```

**Keep when**:
- Tests complete user workflow
- Failure means product is unusable
- Directly validates value proposition

**Remove when**:
- Overlaps with other E2E tests
- Tests edge cases (move to integration/unit)
- More than 15 tests (prioritize)

---

## Current Test Inventory

### File Structure

```
tests/
├── test_scanner_unit.py          # Unit: Scanner logic
├── test_patterns_unit.py         # Unit: Pattern detection
├── test_index_unit.py            # Unit: Index operations
├── test_graph_unit.py            # Unit: Graph operations
├── test_pagerank_unit.py         # Unit: PageRank algorithm
├── test_associations_unit.py     # Unit: Association search
├── test_associations_integration.py  # Integration: Association pipeline
├── test_pipeline_integration.py  # Integration: Full data flow
└── test_cli_component.py         # Component: CLI interface
```

### Test Count

- **Total**: ~172 tests
- **Coverage**: 91%

### Assessment

| Category | Current | Target | Status |
|----------|---------|--------|--------|
| Unit tests | ~100 | ~80 | ⚠️ Slightly high |
| Component tests | ~40 | ~30 | ✅ Good |
| Integration tests | ~20 | ~20 | ✅ Good |
| E2E tests | ~10 | 5-15 | ✅ Good |

---

## Test Quality Checklist

Before adding a test, ask:

1. **If I don't run this test, does it affect confidence in key logic?**
   - No → Don't add

2. **When this test fails, do I need to fix it immediately?**
   - No → Not a critical test

3. **Three months from now, will I understand why this test exists?**
   - No → Add better documentation

4. **Where would the system break if I delete this test?**
   - Can't answer → Test may be redundant

5. **Am I testing logic, or implementation details?**
   - Implementation → Refactor test

---

## Naming Convention

```
tests/
├── test_<module>_unit.py         # Unit tests
├── test_<module>_component.py    # Component tests
├── test_<module>_integration.py  # Integration tests
└── test_<workflow>_e2e.py        # E2E tests
```

**Examples**:
- `test_pagerank_unit.py` — PageRank algorithm logic
- `test_cli_component.py` — CLI interface behavior
- `test_pipeline_integration.py` — Full data flow
- `test_explore_workflow_e2e.py` — User exploration workflow

---

## Maintenance Strategy

### When to Update Tests

1. **Behavior changes** → Update tests to match new behavior
2. **Implementation changes** → Tests should NOT need updates (if they do, they're testing implementation)
3. **New feature** → Add tests for critical logic only
4. **Bug fix** → Add regression test if bug was user-impacting

### When to Remove Tests

1. **Low information gain** — Tests Python built-ins
2. **Redundant** — Covered by other tests
3. **Implementation detail** — Breaks with refactoring
4. **Unclear purpose** — Can't explain why it exists

### Quarterly Review

Every quarter, review tests:
- Remove tests that no longer provide value
- Add tests for new critical paths
- Update documentation for unclear tests

---

## Context and Limitations

### Applicable To

- ✅ Business systems
- ✅ Developer tools (like traceflux)
- ✅ Exploratory/iterative projects
- ✅ Non-safety-critical software

### Not Applicable To

- ❌ Safety-critical systems (aviation, medical)
- ❌ Life-critical systems
- ❌ Financial core systems (trading, settlement)

### Complementary Mechanisms

Testing alone is not enough. Combine with:

1. **Monitoring** — Catch issues in production
2. **Fast rollback** — Recover quickly from failures
3. **User feedback** — Real-world validation
4. **Code review** — Human verification

---

## References

- `docs/PHILOSOPHY.md` — traceflux design philosophy
- `/share/testing/design/limited-testing-boundaries.exp.md` — Theoretical framework
- Kent Beck — Test Pyramid
- Kent C. Dodds — Testing Trophy

---

_"Tests are anchors, not proofs."_
