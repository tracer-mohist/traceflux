# docs/IMPLEMENTATION-DESIGN.md
# traceflux Implementation Design (Python Only)

**Date**: 2026-03-06
**Status**: Ready for Implementation
**Decision**: Python only - simple, readable, UNIX philosophy aligned

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

```
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

---

## 4. Module Specifications

### scanner.py - PNI One-Pass Scanner

Purpose: Segment text by punctuation, extract character sequences

Input: Raw text (UTF-8 string)

Output: List of segments, each containing:
- pre_punct: Punctuation before content
- content: Alphanumeric sequence
- post_punct: Punctuation after content
- position: Start position in original text

Algorithm:
1. Iterate through characters left-to-right
2. Classify each char: alphanumeric or punctuation
3. Group consecutive alphanumerics as content
4. Track punctuation boundaries
5. Emit segments with positions

Complexity: O(n) time, O(n) space

### patterns.py - LZ77 Pattern Detection

Purpose: Find maximal repeated patterns

Input: List of segments from scanner

Output: Pattern index: {pattern: [(doc_id, positions)]}

Algorithm:
1. Build suffix array for each document
2. Find maximal repeats (appear >= 2 times)
3. Filter by minimum support (freq < threshold -> noise)
4. Store pattern -> positions mapping

Complexity: O(n log n) time (suffix array construction)

### index.py - Pattern Index

Purpose: Store and serialize pattern index

Data Structures:
- In-memory: Dict[pattern, List[(doc_id, positions)]]
- On-disk: JSON or MessagePack serialization

Operations:
- add(pattern, doc_id, positions)
- get(pattern) -> List[(doc_id, positions)]
- save(path)
- load(path)

### graph.py - Co-occurrence Graph

Purpose: Build graph of pattern relationships

Input: Pattern index

Output: Graph G = (V, E, w)
- V: Patterns (nodes)
- E: Co-occurrence edges
- w: Edge weights (co-occurrence frequency)

Algorithm:
1. For each document, get pattern sequence
2. For each adjacent pair (p1, p2), increment edge weight
3. Store as adjacency list: {node: {neighbor: weight}}

Complexity: O(n * k) where k = avg patterns per doc

### pagerank.py - Weighted PageRank

Purpose: Rank patterns by importance

Input: Co-occurrence graph

Output: Dict[pattern, score]

Algorithm:
1. Initialize: PR(p) = 1/N for all patterns
2. Iterate until convergence:
   PR(p) = (1-d)/N + d * sum_{q} PR(q) * w(q,p) / sum_{t} w(q,t)
3. Filter: Keep patterns with PR >= threshold

Parameters:
- d: Damping factor (default 0.85)
- threshold: Minimum PageRank (default 0.001)
- max_iter: Maximum iterations (default 100)

### associations.py - BFS Association Finder

Purpose: Find related patterns for a query

Input:
- Query pattern
- Co-occurrence graph
- Pattern index

Output: List of associations with metadata:
- pattern: The related pattern
- degree: Distance from query (1, 2, 3)
- path: Path through graph
- score: Combined score (PageRank + distance)

Algorithm:
1. BFS from query pattern (max depth = 3)
2. Track paths and degrees
3. Score by PageRank and inverse distance
4. Return top-k associations

### mmr.py - Maximal Marginal Relevance

Purpose: Diversify association results

Input: List of associations

Output: Ranked list with diversity

Algorithm:
1. Score each association:
   score = lambda * relevance - (1-lambda) * similarity_to_selected
2. Greedily select highest score
3. Update similarities
4. Repeat until k items selected

Parameters:
- lambda: Balance relevance vs diversity (default 0.7)

---

## 5. CLI Design

### Basic Usage

```bash
# Index documents
traceflux index ./docs/*.md -o index.json

# Search
traceflux search "proxy" -i index.json

# Associative search
traceflux search "proxy" -i index.json --associations --depth 3

# Pipe output
traceflux search "config" | grep -A 5 "associations"
```

### Command Structure

Commands:
- `index` - Build index from documents
- `search` - Search index
- `stats` - Show index statistics

Common Options:
- `-i, --index` - Index file path
- `-o, --output` - Output file path
- `--depth` - Association depth (default 3)
- `--top-k` - Top k results (default 10)
- `--verbose` - Verbose output

---

## 6. Testing Strategy

### Unit Tests

Each module has corresponding test file:
- test_scanner.py - Test segmentation logic
- test_patterns.py - Test pattern detection
- test_graph.py - Test graph construction
- test_pagerank.py - Test PageRank convergence
- test_associations.py - Test BFS traversal
- test_mmr.py - Test diversity ranking

### Integration Tests

Test end-to-end workflows:
- Index small corpus, search, verify results
- Test noise filtering (ensure low-freq patterns filtered)
- Test multi-language support (Chinese, English, mixed)

### Performance Tests

Benchmark critical paths:
- Scanner throughput (MB/s)
- Pattern detection latency
- PageRank convergence time
- Association query latency

---

## 7. Success Criteria

### Functional

- Index 1GB text in < 10 minutes
- Search latency < 100ms (cached index)
- Association discovery finds related concepts
- Noise filtering removes irrelevant matches

### Non-Functional

- Code coverage >= 80%
- Documentation complete
- CLI intuitive and composable
- Cross-platform (Linux, macOS, Windows)

---

## Related Files

- `PROJECT-STATUS.md` - Overall project status
- `../design/00-search-flowchart.md` - Search process flowchart
- `../research/01-foundations/` - Theoretical foundations
