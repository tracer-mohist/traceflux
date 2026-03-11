# Research: Cross-Domain Algorithm Inspiration

DATE: 2026-03-06
STATUS: Deep Analysis -- Cross-Domain Inspiration
TOPIC: How to borrow LZ77, PageRank, Six Degrees for text search

---

## Core Question

> HOW-TO-TRULY-"CROSS-APPLY"-()-ALGORITHMS-FROM-DIFFERENT-DOMAINS?

Not just: "Use LZ77 for compression"
But: "What is the ESSENCE of LZ77, and how does it apply to search?"

---

## Pattern: Cross-Domain Inspiration

### Six Degrees of Separation (Social Network -> Text Search)

```text
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

```text
1. Understand original algorithm (what problem does it solve?)
2. Extract essence (mathematical/core principle)
3. Map domains (what corresponds to what?)
4. Adapt algorithm (modify for new context)
5. Validate (does it work?)
```

---

## LZ77: From Compression to Search

### Original Problem (Compression)

```text
Problem: Reduce file size

LZ77 Solution:
  - Find repeated sequences
  - Store once + references
  - "hello hello" -> "hello" + <ref: offset=6, len=5>

Core Principle:
  "Redundancy exists; exploit it"
```

### Essence Extraction

```text
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

```text
Original LZ77:
  For each position i:
    Find longest match in window [i-w, i)
    Output: (offset, length) or literal

Adapted for Search:
  For each document:
    Find all maximal repeated patterns
    For each pattern P:
      Index: P -> [(doc_id, positions)]

  Result: Pattern -> Documents index

Example:
  Doc 1: "proxy configuration proxy settings"
  Doc 2: "proxy settings proxy config"

  Patterns found:
    "proxy" -> [(doc1, [0, 20]), (doc2, [0, 15])]
    " configuration" -> [(doc1, [6])]
    " settings" -> [(doc1, [20]), (doc2, [15])]
    " config" -> [(doc2, [20])]
```

### Key Insight ()

```text
LZ77 Essence: "Find what repeats, store references"

For Search:
  - Repeats = Patterns worth indexing
  - References = Where they appear
  - Benefit: Only index meaningful patterns (repeats), not noise (unique)

Filtering:
  - Pattern appears 1 time -> Likely noise, skip
  - Pattern appears 5+ times -> Likely meaningful, index
```

---

## PageRank: From Web Ranking to Pattern Ranking

### Original Problem (Web Ranking)

```text
Problem: Which web pages are important?

PageRank Solution:
  - Web as graph (pages = nodes, links = edges)
  - Recursive: Important pages link to important pages
  - Formula: PR(A) = SIGMA(PR(Ti) / C(Ti))

Core Principle:
  "Structure reveals importance"
```

### Essence Extraction

```text
Mathematical Core:
  - Graph G = (V, E)
  - Random walk on G
  - Stationary distribution = importance

Abstract Form:
  For graph G:
    Initialize: rank(v) = 1/N for all v
    Iterate: rank(v) = SIGMA(rank(u) / out_degree(u)) for u -> v
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

```text
Original PageRank:
  For each page P:
    PR(P) = (1-d)/N + d * SIGMA(PR(Ti) / C(Ti))
    Where Ti link to P

Adapted for Patterns:
  For each pattern P:
    Rank(P) = (1-d)/N + d * SIGMA(Rank(Ci) / cooccur_count(Ci))
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
