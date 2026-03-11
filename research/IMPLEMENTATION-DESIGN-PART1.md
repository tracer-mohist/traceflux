# traceflux Implementation Design (Python Only)

DATE: 2026-03-06
STATUS: Ready for Implementation
DECISION: Python only - simple, readable, UNIX philosophy aligned

---

## 1. Language Philosophy Decision

### Why Python Only

User's Design Philosophy:
- Simplicity over complexity
- Readable syntax
- No syntactic sugar (C++ problem)
- No complex meta-design (Rust problem)

Rejected Languages:
- C++ - Too much syntactic sugar, complex
- Rust - Complex grammar meta-design, steep learning curve
- C - Too low-level, manual memory management
- Go - GC pauses, larger binary
- Zig/Nim - Too new, risky ecosystems

Chosen Language:
- Python - Simple, readable, composable

### Alignment with UNIX Philosophy

UNIX Philosophy:
- Simple is better than complex
- Readable is better than obscure
- Composable is better than monolithic

Python Matches:
- Clear, explicit syntax
- Easy to read and understand
- Great for piping and composition
- Rich standard library

### Performance Considerations

Concern: Python is slower than Rust/C

Mitigation:
1. O(n) algorithms (correct algorithm > fast language)
2. Profile and optimize hot paths
3. Use efficient data structures
4. For extreme performance: optional C extensions later

Truth: Most text search is I/O bound, not CPU bound. Algorithm choice matters more than language.

---

## 2. Revised Implementation Plan

### Single-Phase: Python Production

Timeline: 8-10 weeks to v0.1.0

Week 1-2: Core Scanning
- PNI scanner (one-pass, O(n))
- Pattern index
- Basic CLI

Week 3-4: Pattern Detection
- LZ77-style maximal repeats
- Suffix array implementation
- Frequency filtering

Week 5-6: Graph and PageRank
- Co-occurrence graph
- Weighted PageRank
- Noise filtering

Week 7-8: Associations and Polish
- BFS association finder
- Divergent display (MMR)
- Output formatting
- Testing and documentation

Week 9-10: Optimization
- Profile hot paths
- Optimize critical sections
- Benchmark
- Release v0.1.0

---

## 3. Project Structure (Python)

```text
traceflux/
  pyproject.toml
  README.md
  LICENSE (MIT)
  .gitignore

  src/traceflux/
    __init__.py         # Version, exports
    cli.py              # CLI entry point
    scanner.py          # PNI one-pass scanner
    patterns.py         # LZ77 pattern detection
    index.py            # Pattern index + serialization
    graph.py            # Co-occurrence graph
    pagerank.py         # Weighted PageRank
    associations.py     # BFS association finder
    mmr.py              # Maximal Marginal Relevance
    utils.py            # Utilities (hashing, etc.)

  tests/
    test_scanner.py
    test_patterns.py
    test_graph.py
    test_pagerank.py
    test_associations.py
    test_mmr.py

  docs/
    PROJECT-STATUS.md
    IMPLEMENTATION-DESIGN.md
    00-search-flowchart.md
    PERFORMANCE.md

  research/01-foundations/
    (13 research documents)

  examples/
    basic_search.py
    associative_search.py
    noise_filtering.py

  benches/
    bench_scanner.py
    bench_patterns.py
    bench_pagerank.py
```
