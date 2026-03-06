# docs/PROJECT-STATUS.md
# traceflux Project Status Report

**Date**: 2026-03-06
**Status**: Design Complete, Ready for Implementation
**Goal**: UNIX philosophy lightweight text engine - noise filtering + associative search

---

## 1. Project Vision

### Core Purpose

traceflux = Lightweight text search engine

Key capabilities:
- Noise filtering (remove invalid punctuation, unreadable symbols)
- Associative search (discover related concepts, not just exact match)

Philosophy: UNIX style - simple, composable, focused

### Design Principles

1. Pure mathematics (characters, sequences, graphs - no linguistics)
2. One-pass scanning (O(n) efficiency)
3. Noise filtering (frequency + PageRank thresholds)
4. Divergent associations (show possibilities, not predictions)
5. Composable output (pipe to other tools)

---

## 2. Current Theoretical Foundation

### Completed Research

- `pure-math-foundation.md` - Characters, sequences, graphs (pure math) - Complete
- `frequency-lz-pagerank.md` - LZ77 patterns + weighted PageRank - Complete
- `divergent-associations.md` - Divergent display (not predictive) - Complete
- `lzwpagerank-autocomplete.md` - LZW dictionary + PageRank - Complete
- `cross-domain-inspiration.md` - LZ77, PageRank, Six Degrees synthesis - Complete
- `mathematical-formalization.md` - Unified mathematical framework - Complete
- `punctuation-namespace-index.md` - PNI (punctuation-based segmentation) - Complete
- `punctuation-context-tree.md` - PCT (tree structure by context) - Complete
- `advanced-algorithms.md` - LZMA, PageRank, BWT inspiration - Complete
- `ngram-explained.md` - N-gram basics (for comparison) - Complete
- `space-is-readable.md` - Space is content, not punctuation - Complete
- `character-level-analysis.md` - Character-level sequence analysis - Complete
- `search-flowchart.md` - Complete flow (list format) - Complete

Total: 13 research documents, ~100KB of theoretical work

---

## 3. Core Algorithm Design

### Phase 1: One-Pass Scanning (PNI + LZ77)

Input: Text T (raw character sequence)

Process:
1. Scan left-to-right (O(n))
2. Segment by punctuation (PNI)
   - Punctuation = non-alphanumeric (includes space, escapes)
   - Each segment: (pre_punct, content, post_punct)
3. Extract maximal repeated patterns (LZ77-style)
   - Pattern P is repeated iff |Occ(P, T)| >= 2
   - Store: Pattern -> [(doc_id, positions)]

Output:
- Pattern index: {pattern -> [(doc, positions)]}
- Filter: freq(P) < min_support -> discard (noise)

Mathematical basis: `pure-math-foundation.md`, `punctuation-namespace-index.md`

### Phase 2: Co-occurrence Graph Construction

Input: Pattern index from Phase 1

Process:
1. For each document:
   - Extract pattern sequence: [p1, p2, p3, ...]
   - Adjacent patterns co-occur: (p1, p2), (p2, p3), ...
2. Build graph:
   - Nodes: Patterns
   - Edges: Co-occurrence
   - Weights: Co-occurrence frequency

Output:
- Graph G = (V, E, w)
- V = patterns
- E = co-occurrence relationships
- w = edge weights

Mathematical basis: `mathematical-formalization.md`, `frequency-lz-pagerank.md`

### Phase 3: Weighted PageRank

Input: Co-occurrence graph G

Process:
1. Run weighted PageRank:
   PR(v) = (1-d)/N + d * sum_{u} PR(u) * w(u,v) / sum_{t} w(u,t)
2. Filter low-rank patterns:
   Keep P iff PR(P) >= threshold
3. Store ranks in index

Output:
- Enhanced index: {pattern -> [(doc, positions, PR_score)]}
- Filtered: Low-rank patterns discarded (noise)

Mathematical basis: `frequency-lz-pagerank.md`, `lzwpagerank-autocomplete.md`

### Phase 4: Associative Search (BFS)

Input:
- Query Q (character sequence)
- Index I = (patterns, graph, PR scores)

Process:
1. Find exact/partial matches for Q
2. BFS on graph (depth k=3-4):
   Assoc_k(Q) = {P | dist(Q, P) <= k}
3. Rank by:
   - PageRank (importance)
   - Distance (1, 2, 3 degrees)
   - Diversity (MMR - different branches)

Output:
- Direct matches (exact/partial)
- Associations (1, 2, 3 degrees with paths)
- Ranked by importance + diversity

Mathematical basis: `divergent-associations.md`, `advanced-algorithms.md`

---

## 4. Implementation Plan

### Language Decision

Chosen: Python 3.10+

Rationale:
- Simple, readable syntax
- No complex meta-design (unlike Rust/C++)
- Great for UNIX-style composition
- Rich standard library
- O(n) algorithm choice matters more than language speed

Rejected:
- C++ - Too much syntactic sugar
- Rust - Complex grammar meta-design
- C - Too low-level, manual memory management
- Go - GC pauses, larger binary
- Zig/Nim - Too new, risky ecosystems

### Timeline

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

## 5. Next Steps

### Immediate Actions

1. Commit existing research documents to git
2. Create project structure (src/, tests/, benches/)
3. Implement Phase 1 (PNI scanner)
4. Write tests for scanner

### Success Criteria

- v0.1.0 released within 10 weeks
- All 4 phases implemented
- Test coverage >= 80%
- Documentation complete

---

## Related Files

- `IMPLEMENTATION-DESIGN.md` - Detailed implementation design
- `../design/00-search-flowchart.md` - Search process flowchart
- `../research/01-foundations/` - Theoretical foundations
