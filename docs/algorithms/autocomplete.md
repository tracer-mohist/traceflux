# Autocomplete Engine

Purpose: Real-time search suggestions using LZW + PageRank.

NOTE: Consolidated from research/01-foundations/ (2026-03-11)

---

## Overview

Autocomplete uses LZW dictionary compression for pattern discovery and PageRank for ranking suggestions.

---

## LZW Dictionary for Pattern Discovery

### How LZW Works

Input: "hello hello world hello"

LZW builds dictionary dynamically:
  1. Read "h" -> not in dict, add "h" (code 0)
  2. Read "he" -> not in dict, add "he" (code 1)
  3. Read "hel" -> not in dict, add "hel" (code 2)
  4. Read "hell" -> not in dict, add "hell" (code 3)
  5. Read "hello" -> not in dict, add "hello" (code 4)
  6. Read "hello " -> not in dict, add "hello " (code 5)

Dictionary:
  {
    0: "h",
    1: "he",
    2: "hel",
    3: "hell",
    4: "hello",
    5: "hello ",
    ...
  }

### Key Insight

LZW dictionary = Natural pattern index!

- Automatically discovers repeated patterns
- No need to pre-define n-gram size
- Patterns of any length are captured

---

## LZW vs N-gram

| Aspect | N-gram | LZW |
|--------|--------|-----|
| Pattern size | Fixed (n) | Variable (discovered) |
| Dictionary | Implicit (all n-grams) | Explicit (frequent patterns) |
| Memory | O(Sigma^n) | O(number of patterns) |
| Discovery | Exhaustive | Adaptive |

### When to Use Each

N-gram:
  - Small n (2-3): Fuzzy matching, typo tolerance
  - Large n (5+): Exact phrase matching

LZW:
  - Autocomplete: Discovers common prefixes
  - Compression: Efficient storage
  - Pattern mining: Finds frequent substrings

---

## PageRank for Ranking

### Why PageRank?

Raw frequency is not enough for autocomplete.

Example:
  "proxy" appears 100 times
    - 90 times in footer (less important)
    - 10 times in title (very important)

PageRank captures:
  - Position importance
  - Co-occurrence structure
  - Recursive importance

### Co-occurrence Graph

Build graph from LZW dictionary:
  - Nodes: dictionary entries (patterns)
  - Edges: patterns co-occur in same context
  - Weight: frequency of co-occurrence

Run PageRank on this graph.

---

## Autocomplete Algorithm

### Step 1: Build LZW Dictionary

See: [autocomplete-implementation.md](./autocomplete-implementation.md)

### Step 2: Build Co-occurrence Graph

See: [autocomplete-implementation.md](./autocomplete-implementation.md)

### Step 3: Compute PageRank

See: [autocomplete-implementation.md](./autocomplete-implementation.md)

### Step 4: Autocomplete Query

See: [autocomplete-implementation.md](./autocomplete-implementation.md)

---

## Example

### Input Corpus

```text
[
  "proxy configuration for office",
  "proxy settings for home",
  "proxy config proxy settings",
  "direct connection no proxy"
]
```

### LZW Dictionary (partial)

```text
{
  0: "p",
  1: "pr",
  2: "pro",
  3: "prox",
  4: "proxy",
  5: "proxy ",
  6: "proxy c",
  7: "proxy co",
  ...
}
```

### Autocomplete "prox"

Query: "prox"

Candidates:
  "proxy" (PR: 0.15)
  "proxy " (PR: 0.12)
  "proxy c" (PR: 0.08)
  "proxy config" (PR: 0.06)
  "proxy settings" (PR: 0.05)

Results (top 3):
  1. "proxy" (0.15)
  2. "proxy " (0.12)
  3. "proxy c" (0.08)

---

## Optimization

### Incremental Updates

Problem: Rebuilding LZW dictionary is expensive.

Solution: Incremental updates
  - Add new patterns as they appear
  - Merge dictionaries periodically
  - Use rolling window for recent data

### Memory Efficiency

Problem: Large dictionaries consume memory.

Solutions:
  1. Frequency threshold: Only keep patterns with freq >= 2
  2. Length limit: Max pattern length = 20 chars
  3. LRU cache: Keep most recently used entries
  4. Compression: Store dictionary entries compressed

---

## Related

- [Frequency Ranking](../core/frequency-ranking.md) - LZW + PageRank theory
- [N-gram Analysis](../core/ngram-analysis.md) - Alternative pattern extraction
- [Divergent Search](./divergent-search.md) - Non-obvious associations
- [Implementation](./autocomplete-implementation.md) - Code examples

---

Last Updated: 2026-03-11
Source Files: 2026-03-06_lzwpagerank-autocomplete*.md
