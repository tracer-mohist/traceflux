# Research: Cross-Domain Algorithm Inspiration

**Date**: 2026-03-06  
**Status**: Deep Analysis — Cross-Domain Inspiration  
**Topic**: How to borrow LZ77, PageRank, Six Degrees for text search

---

## Core Question

**How to truly "cross-apply" (触类旁通) algorithms from different domains?**

Not just: "Use LZ77 for compression"  
But: "What is the **essence** of LZ77, and how does it apply to search?"

---

## Pattern: Cross-Domain Inspiration

### Six Degrees of Separation (Social Network → Text Search)

```
Original Domain: Social networks
  - Nodes: People
  - Edges: Friendships
  - Insight: Any two people connected by ~6 steps

Cross-Apply to Text:
  - Nodes: Words/Patterns
  - Edges: Co-occurrence
  - Insight: Any two words connected by ~3-4 steps

Essence Extracted:
  "Small-world networks have short path lengths"
  
Applied:
  Build co-occurrence graph, BFS to find associations
```

### Key Steps for Cross-Application

```
1. Understand original algorithm (what problem does it solve?)
2. Extract essence (mathematical/core principle)
3. Map domains (what corresponds to what?)
4. Adapt algorithm (modify for new context)
5. Validate (does it work?)
```

---

## LZ77: From Compression to Search

### Original Problem (Compression)

```
Problem: Reduce file size

LZ77 Solution:
  - Find repeated sequences
  - Store once + references
  - "hello hello" → "hello" + <ref: offset=6, len=5>

Core Principle:
  "Redundancy exists; exploit it"
```

### Essence Extraction

```
Mathematical Core:
  - Text has repeated substrings
  - Finding repeats = O(n) with suffix tree
  - Reference = (offset, length) tuple

Abstract Form:
  For sequence S:
    Find all maximal repeated substrings R
    For each R: store (first_occurrence, all_other_occurrences)
```

### Domain Mapping

| Compression | Text Search |
|-------------|-------------|
| Repeated sequence | Repeated pattern |
| Offset | Position in document |
| Length | Pattern length |
| Dictionary | Pattern index |
| Compress | Index |

### Adapted Algorithm (PNI + LZ)

```
Original LZ77:
  For each position i:
    Find longest match in window [i-w, i)
    Output: (offset, length) or literal

Adapted for Search:
  For each document:
    Find all maximal repeated patterns
    For each pattern P:
      Index: P → [(doc_id, positions)]
    
  Result: Pattern → Documents index

Example:
  Doc 1: "proxy configuration proxy settings"
  Doc 2: "proxy settings proxy config"
  
  Patterns found:
    "proxy" → [(doc1, [0, 20]), (doc2, [0, 15])]
    " configuration" → [(doc1, [6])]
    " settings" → [(doc1, [20]), (doc2, [15])]
    " config" → [(doc2, [20])]
```

### Key Insight (触类旁通)

```
LZ77 Essence: "Find what repeats, store references"

For Search:
  - Repeats = Patterns worth indexing
  - References = Where they appear
  - Benefit: Only index meaningful patterns (repeats), not noise (unique)

Filtering:
  - Pattern appears 1 time → Likely noise, skip
  - Pattern appears 5+ times → Likely meaningful, index
```

---

## PageRank: From Web Ranking to Pattern Ranking

### Original Problem (Web Ranking)

```
Problem: Which web pages are important?

PageRank Solution:
  - Web as graph (pages = nodes, links = edges)
  - Recursive: Important pages link to important pages
  - Formula: PR(A) = Σ(PR(Ti) / C(Ti))

Core Principle:
  "Structure reveals importance"
```

### Essence Extraction

```
Mathematical Core:
  - Graph G = (V, E)
  - Random walk on G
  - Stationary distribution = importance
  
Abstract Form:
  For graph G:
    Initialize: rank(v) = 1/N for all v
    Iterate: rank(v) = Σ(rank(u) / out_degree(u)) for u → v
    Converge: ranks stabilize
```

### Domain Mapping

| Web Search | Text Search |
|------------|-------------|
| Web page | Pattern/Segment |
| Hyperlink | Co-occurrence |
| In-degree | Number of co-occurring patterns |
| PageRank | Pattern importance |

### Adapted Algorithm (PatternRank)

```
Original PageRank:
  For each page P:
    PR(P) = (1-d)/N + d * Σ(PR(Ti) / C(Ti))
    Where Ti link to P

Adapted for Patterns:
  For each pattern P:
    Rank(P) = (1-d)/N + d * Σ(Rank(Ci) / cooccur_count(Ci))
    Where Ci co-occur with P

Example:
  Patterns: "proxy", "config", "settings", "git", "SSH"
  
  Co-occurrence graph:
    "proxy" ↔ "config" (10 times)
    "proxy" ↔ "settings" (8 times)
    "proxy" ↔ "git" (5 times)
    "proxy" ↔ "SSH" (3 times)
    "config" ↔ "settings" (6 times)
  
  After PageRank:
    "proxy": 0.35 (hub, co-occurs with many)
    "config": 0.25
    "settings": 0.20
    "git": 0.12
    "SSH": 0.08
  
  Use: Filter low-rank patterns (noise), sort results by rank
```

### Key Insight (触类旁通)

```
PageRank Essence: "Graph structure reveals node importance"

For Search:
  - Co-occurrence = "links" between patterns
  - Patterns co-occurring with many others = "hubs"
  - Benefit: Distinguish signal (high-rank) from noise (low-rank)

Filtering:
  - Rank < 0.01 → Likely noise, filter
  - Rank > 0.1 → Likely meaningful, prioritize
```

---

## Six Degrees: From Social Networks to Association Discovery

### Original Problem (Social Networks)

```
Problem: How are people connected?

Six Degrees Solution:
  - Small-world network property
  - Average path length ≈ 6
  - Formula: L ≈ log(N) / log(k)

Core Principle:
  "Networks have short paths between nodes"
```

### Essence Extraction

```
Mathematical Core:
  - Graph G = (V, E)
  - High clustering + short paths
  - BFS finds shortest paths
  
Abstract Form:
  For graph G, start node S:
    BFS to depth D
    Return all nodes within D steps
    Path = [S, N1, N2, ..., Nd]
```

### Domain Mapping

| Social Network | Text Search |
|----------------|-------------|
| Person | Pattern/Word |
| Friendship | Co-occurrence |
| Social circle | Topic cluster |
| 6 degrees | 3-4 word associations |

### Adapted Algorithm (Association BFS)

```
Original Six Degrees:
  Start from person P
  BFS to depth 6
  Return all reachable people

Adapted for Search:
  Start from query pattern Q
  BFS to depth 3-4 on co-occurrence graph
  Return all reachable patterns with paths

Example:
  Query: "proxy"
  
  Co-occurrence graph:
    "proxy" — "config" — "security" — "authentication"
       │         │
       │         └— "environment"
       │
       └— "git" — "SSH"
  
  BFS (depth=3):
    1°: "config", "git"
    2°: "security", "environment", "SSH"
    3°: "authentication", "firewall"
  
  Output:
    "proxy" → "config" → "security" → "authentication"
    (3-step association path)
```

### Key Insight (触类旁通)

```
Six Degrees Essence: "Short paths exist between distant nodes"

For Search:
  - Distant patterns connected via intermediates
  - 3-4 steps can reach "far" concepts
  - Benefit: Discover non-obvious associations

Discovery:
  User searches "proxy"
  Discovers: "proxy" → "config" → "security" → "authentication"
  Insight: "Oh, proxy relates to authentication!"
```

---

## Synthesis: Unified Algorithm

### Combining All Three

```
Phase 1: LZ-Style Pattern Detection
  - Find all maximal repeated patterns
  - Filter: single-occurrence patterns (noise)
  - Output: Pattern → [(doc, positions)]

Phase 2: PageRank-Style Ranking
  - Build co-occurrence graph
  - Run PatternRank algorithm
  - Output: Pattern → Rank(score)

Phase 3: Six-Degrees-Style Association
  - For query Q, BFS on co-occurrence graph
  - Depth=3-4
  - Output: Associations with paths

Result:
  Query: "proxy"
  
  Direct matches:
    "proxy" (rank=0.35, appears in [doc1, doc2, doc5])
  
  Associations (1°):
    "config" (rank=0.25, co-occurs 10 times)
    "git" (rank=0.12, co-occurs 5 times)
  
  Associations (2°):
    "security" (rank=0.18, via "config")
    "SSH" (rank=0.08, via "git")
  
  Associations (3°):
    "authentication" (rank=0.15, via "security")
```

---

## Comparison: Before vs After Cross-Application

### Before (N-gram Only)

```
Index: All 2-grams, 3-grams, 4-grams

Query: "proxy"
Match: Exact 2-grams containing "proxy"
Result: Limited, no associations, no ranking
```

### After (LZ + PageRank + Six Degrees)

```
Index: Maximal repeated patterns + ranks + co-occurrence graph

Query: "proxy"
Match: 
  - Exact patterns containing "proxy"
  - Ranked by importance
  - Associations via BFS (1°, 2°, 3°)

Result: Rich, ranked, associative discovery
```

---

## Key Principles for Cross-Domain Inspiration

### 1. Extract Mathematical Essence

```
Don't: "LZ77 compresses files"
Do: "LZ77 finds repeated substrings and stores references"

Abstract: Pattern detection + reference storage
```

### 2. Map Domain Concepts

```
Create mapping table:
  Source Domain → Target Domain
  Web page → Pattern
  Link → Co-occurrence
  Person → Word
  Friendship → Co-occurrence
```

### 3. Adapt, Don't Copy

```
Original PageRank:
  PR(P) = Σ(PR(Ti) / C(Ti))

Adapted PatternRank:
  Rank(P) = Σ(Rank(Ci) / cooccur_count(Ci))

Same structure, different semantics
```

### 4. Validate with Examples

```
Test on real data:
  - Does LZ-style pattern detection find meaningful patterns?
  - Does PatternRank distinguish signal from noise?
  - Does Six-Degrees BFS find useful associations?
```

---

## Philosophical Reflection

### Why Cross-Domain Works

```
Different domains, same mathematical structures:
  - Social networks ≈ Co-occurrence graphs
  - Web links ≈ Pattern co-occurrences
  - Text repeats ≈ Compression opportunities

Mathematics is universal; domains are just interpretations.
```

### The Art of 触类旁通

```
类 (Category): Recognize similar structures
通 (Connect): Map concepts between domains
旁 (Side): Explore adjacent possibilities
通 (Through): Achieve deep understanding

Process:
  1. Understand deep structure (not surface details)
  2. Recognize patterns across domains
  3. Adapt, don't copy blindly
  4. Validate in new context
```

---

## Next Steps

1. **Implement LZ-style pattern detection** — Suffix tree for O(n)
2. **Implement PatternRank** — Adapt PageRank formula
3. **Implement Association BFS** — Six-degrees style discovery
4. **Test on real corpus** — Validate cross-domain inspiration
5. **Iterate** — Refine based on results

---

**Status**: Cross-domain analysis complete  
**Next**: Implement unified algorithm (LZ + PageRank + Six Degrees)  
**Philosophy**: Extract essence, map domains, adapt, validate
