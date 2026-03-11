### Key Insight ()

```text
PageRank Essence: "Graph structure reveals node importance"

For Search:
  - Co-occurrence = "links" between patterns
  - Patterns co-occurring with many others = "hubs"
  - Benefit: Distinguish signal (high-rank) from noise (low-rank)

Filtering:
  - Rank < 0.01 -> Likely noise, filter
  - Rank > 0.1 -> Likely meaningful, prioritize
```

---

## Six Degrees: From Social Networks to Association Discovery

### Original Problem (Social Networks)

```text
Problem: How are people connected?

Six Degrees Solution:
  - Small-world network property
  - Average path length ≈ 6
  - Formula: L ≈ log(N) / log(k)

Core Principle:
  "Networks have short paths between nodes"
```

### Essence Extraction

```text
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

```text
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
    "proxy" -- "config" -- "security" -- "authentication"
       |         |
       |         +-- "environment"
       |
       +-- "git" -- "SSH"

  BFS (depth=3):
    1deg: "config", "git"
    2deg: "security", "environment", "SSH"
    3deg: "authentication", "firewall"

  Output:
    "proxy" -> "config" -> "security" -> "authentication"
    (3-step association path)
```

### Key Insight ()

```text
Six Degrees Essence: "Short paths exist between distant nodes"

For Search:
  - Distant patterns connected via intermediates
  - 3-4 steps can reach "far" concepts
  - Benefit: Discover non-obvious associations

Discovery:
  User searches "proxy"
  Discovers: "proxy" -> "config" -> "security" -> "authentication"
  Insight: "Oh, proxy relates to authentication!"
```

---

## Synthesis: Unified Algorithm

### Combining All Three

```text
Phase 1: LZ-Style Pattern Detection
  - Find all maximal repeated patterns
  - Filter: single-occurrence patterns (noise)
  - Output: Pattern -> [(doc, positions)]

Phase 2: PageRank-Style Ranking
  - Build co-occurrence graph
  - Run PatternRank algorithm
  - Output: Pattern -> Rank(score)

Phase 3: Six-Degrees-Style Association
  - For query Q, BFS on co-occurrence graph
  - Depth=3-4
  - Output: Associations with paths

Result:
  Query: "proxy"

  Direct matches:
    "proxy" (rank=0.35, appears in [doc1, doc2, doc5])

  Associations (1deg):
    "config" (rank=0.25, co-occurs 10 times)
    "git" (rank=0.12, co-occurs 5 times)

  Associations (2deg):
    "security" (rank=0.18, via "config")
    "SSH" (rank=0.08, via "git")

  Associations (3deg):
    "authentication" (rank=0.15, via "security")
```

---

## Comparison: Before vs After Cross-Application

### Before (N-gram Only)

```text
Index: All 2-grams, 3-grams, 4-grams

Query: "proxy"
Match: Exact 2-grams containing "proxy"
Result: Limited, no associations, no ranking
```

### After (LZ + PageRank + Six Degrees)

```text
Index: Maximal repeated patterns + ranks + co-occurrence graph

Query: "proxy"
Match:
  - Exact patterns containing "proxy"
  - Ranked by importance
  - Associations via BFS (1deg, 2deg, 3deg)

Result: Rich, ranked, associative discovery
```

---

## Key Principles for Cross-Domain Inspiration

### 1. Extract Mathematical Essence

```text
Don't: "LZ77 compresses files"
Do: "LZ77 finds repeated substrings and stores references"

Abstract: Pattern detection + reference storage
```

### 2. Map Domain Concepts

```text
Create mapping table:
  Source Domain -> Target Domain
  Web page -> Pattern
  Link -> Co-occurrence
  Person -> Word
  Friendship -> Co-occurrence
```

### 3. Adapt, Don't Copy

```text
Original PageRank:
  PR(P) = SIGMA(PR(Ti) / C(Ti))

Adapted PatternRank:
  Rank(P) = SIGMA(Rank(Ci) / cooccur_count(Ci))

Same structure, different semantics
```
