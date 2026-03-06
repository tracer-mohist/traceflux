# Research: Advanced Compression & Search Algorithms

**Date**: 2026-03-06  
**Status**: Algorithm Inspiration  
**Topic**: LZMA, PageRank, BWT — Inspiration for traceflux

---

## User's Hint

**N-gram may not be the best strategy.**

**References**:
1. **7z compression algorithm** — Award-winning algorithm
2. **Google's search algorithm** — Famous search technique

Let me recall and analyze these.

---

## 1. LZMA (Lempel-Ziv-Markov Algorithm)

### Background

**Used in**: 7z file format (7-Zip)

**Awards**:
- LZ77 (basis): IEEE Computer Society Golden Jubilee Award
- LZW: Various awards for data compression

**Key Idea**: **Dictionary-based compression with sliding window**

---

### Core Algorithm (LZ77/LZMA)

```
Instead of storing repeated data, store references:

Text: "hello hello world hello"

Naive storage:
  "hello hello world hello" (24 chars)

LZ77 compression:
  "hello" (5 chars)
  + <copy from 6 chars ago, length 5>  → "hello"
  + " world" (6 chars)
  + <copy from 17 chars ago, length 5> → "hello"

Result: "hello" + (offset=6, len=5) + " world" + (offset=17, len=5)
        Much smaller!
```

### Sliding Window + Dictionary

```
Position: 0    5    10   15   20
Text:     h e l l o   h e l l o   w o r l d   h e l l o
          │         │              │
          └─────────┘              │
          Already seen             │
                                   └─────────────┘
                                   Match found! (offset=17, len=5)

Algorithm:
  1. Maintain sliding window of recent text
  2. For each position, find longest match in window
  3. Output: (offset, length) or literal char
```

### Application to traceflux

```
Instead of n-grams, use LZ-style references:

Text: "proxy configuration proxy settings"

Index:
  "proxy " (literal, pos 0)
  "configuration" (literal, pos 6)
  " " (literal, pos 19)
  <match: offset=20, length=6>  → "proxy "
  "settings" (literal, pos 26)

Benefit:
  - Captures repeated patterns automatically
  - No fixed n-gram size
  - Variable-length patterns
  - Space-efficient
```

### Key Insight for Search

```
LZ77 finds: "This sequence appeared before at position X"

For search:
  - "proxy" appears at [0, 20, 100, 250]
  - "proxy config" appears at [0, 100] (longer pattern)
  - "proxy settings" appears at [20, 250] (longer pattern)

Instead of fixed n-grams, find **maximal repeated sequences**.
```

---

## 2. PageRank (Google's Algorithm)

### Background

**Created by**: Larry Page & Sergey Brin (1996)

**Purpose**: Rank web pages by importance

**Key Idea**: **Link structure as importance signal**

---

### Core Algorithm

```
Web as graph:
  Page A → Page B (A links to B)
  
PageRank:
  - A page is important if important pages link to it
  - Recursive definition
  
Formula:
  PR(A) = (1-d)/N + d * Σ(PR(Ti)/C(Ti))
  
  Where:
    PR(A) = PageRank of page A
    d = damping factor (0.85)
    N = total pages
    Ti = pages linking to A
    C(Ti) = number of outbound links from Ti
```

### Intuition

```
Page A has many inbound links → Important
Page B has few inbound links → Less important

But: One link from important page > many links from unimportant pages
```

### Application to traceflux

```
Text segments as "pages":
  Segment A: "proxy configuration"
  Segment B: "proxy settings"
  Segment C: "git proxy"

Co-occurrence as "links":
  If A and B appear in same document → A ↔ B (linked)
  
Segment "PageRank":
  - Segment appearing with many others → Important (hub)
  - Segment appearing with important segments → Important
  
Example:
  "proxy" appears with: config, settings, git, SSH, firewall...
  → High "rank" (central concept)
  
  "authentication" appears with: security, proxy, firewall...
  → Also high "rank"
  
  "xyz123" appears alone
  → Low "rank" (likely noise)
```

### Key Insight for Search

```
Not all segments are equal:
  - Some are "hubs" (appear with many others)
  - Some are "authorities" (linked by hubs)
  - Some are isolated (noise?)

Rank segments by "importance" in co-occurrence graph.
```

---

## 3. Burrows-Wheeler Transform (BWT)

### Background

**Created by**: Michael Burrows & David Wheeler (1994)

**Used in**: bzip2, gzip, modern compressors

**Key Idea**: **Reorder text to group similar contexts**

---

### Core Algorithm

```
Original: "banana"

All rotations:
  banana
  ananab
  nanaba
  anaban
  nabana
  abanan

Sort rotations:
  abanan
  anaban
  ananab
  banana  ← Original
  nabana
  nanaba

Take last column: "nnbaaa"

BWT("banana") = "nnbaaa"

Why? Similar contexts are grouped:
  "n" follows "a" multiple times → grouped together
```

### Application to traceflux

```
Instead of storing text as-is:
  "hello world hello"

BWT-like reordering:
  Group by context:
    "hello" appears before " world" (twice)
    "hello" appears at start (twice)
  
  Index by context, not position.
```

### Key Insight for Search

```
BWT groups characters with similar **following context**.

For search:
  - Group segments by punctuation context (pre, post)
  - Similar contexts → similar meaning?
  - Efficient compression of index
```

---

## Synthesis: Hybrid Approach for traceflux

### Combining Ideas

```
1. LZMA-style pattern detection
   - Find maximal repeated sequences
   - Variable-length patterns (not fixed n-grams)
   - Store (offset, length) references

2. PageRank-style importance ranking
   - Build co-occurrence graph
   - Rank segments by "importance"
   - Filter low-rank (noise)

3. BWT-style context grouping
   - Group by punctuation context (pre, post)
   - Efficient index structure
   - Fast context-based queries
```

---

## Proposed Algorithm: PNI + LZ + PageRank

### Phase 1: Punctuation Namespace Index (PNI)

```
One-pass scan, segment by punctuation:

"Hello, world! How are you?"
  → [("S", ","), "Hello"]
  → [(",", "!"), " world"]
  → [("!", "?"), " How are you"]
```

### Phase 2: LZ-Style Pattern Detection

```
Find maximal repeated sequences:

Document 1: "proxy configuration"
Document 2: "proxy settings"
Document 3: "proxy configuration"

Patterns:
  "proxy" → appears 3 times (at positions [...])
  "proxy config" → appears 2 times
  "configuration" → appears 2 times

Store as:
  Pattern: "proxy" → [doc1:0, doc2:0, doc3:0]
  Pattern: " config" → [doc1:6, doc3:6]
  Pattern: " settings" → [doc2:6]
```

### Phase 3: PageRank on Co-occurrence Graph

```
Build graph:
  Nodes: Patterns ("proxy", "config", "settings")
  Edges: Co-occur in same document

Rank:
  "proxy" → High rank (appears with many patterns)
  "config" → Medium rank
  "settings" → Medium rank

Use rank to:
  - Filter low-rank patterns (noise)
  - Sort search results by importance
```

---

## Comparison: N-gram vs LZ-Style

| Aspect | N-gram | LZ-Style |
|--------|--------|----------|
| **Pattern size** | Fixed (2, 3, 4 chars) | Variable (finds natural patterns) |
| **Storage** | All n-grams (redundant) | Only repeated patterns (efficient) |
| **Discovery** | Sliding window | Longest match |
| **Example** | "he", "el", "ll", "lo" | "hello" (once) + references |
| **Efficiency** | O(n × max_n) | O(n) with suffix tree |
| **Noise** | Many unique n-grams | Only repeated patterns |

---

## Key Insights

### 1. LZ77: Find Natural Patterns

```
Instead of fixed n-grams:
  "h", "he", "hel", "hell", "hello", "ello", "llo", "lo", "o"

Find maximal repeats:
  "hello" (appears 5 times)
  "world" (appears 3 times)
  "hello world" (appears 2 times)

Benefit: Natural patterns, not arbitrary cuts.
```

### 2. PageRank: Importance Matters

```
Not all patterns are equal:
  "proxy" (appears with 20 other patterns) → Important
  "xyz123" (appears alone) → Likely noise

Rank patterns by co-occurrence diversity.
```

### 3. BWT: Context Groups

```
Group by punctuation context:
  ("S", ",") → Patterns starting sentences, ending with comma
  (",", "!") → Patterns between comma and exclamation

Efficient indexing by context.
```

---

## Implementation Considerations

### Suffix Tree for LZ-Style

```python
# Suffix tree finds all repeated substrings in O(n)

Text: "hello hello world"

Suffix tree:
  Root
  ├── "hello hello world"
  ├── "ello hello world"
  ├── "llo hello world"
  ├── ...
  └── "world"

Repeated patterns:
  "hello" (appears twice)
  "ello" (appears twice)
  ...

Efficient: O(n) to build, O(m) to query
```

### PageRank on Co-occurrence

```python
# Build co-occurrence graph
graph = defaultdict(set)
for doc in documents:
    patterns = extract_patterns(doc)
    for p1 in patterns:
        for p2 in patterns:
            if p1 != p2:
                graph[p1].add(p2)

# Run PageRank
ranks = pagerank(graph)

# Filter low-rank (noise)
meaningful = [p for p in patterns if ranks[p] > threshold]
```

---

## Next Steps

1. **Research LZMA more deeply** — Understand exact algorithm
2. **Implement suffix tree** — For O(n) pattern detection
3. **Combine with PNI** — Punctuation namespaces + LZ patterns
4. **Add PageRank** — Rank patterns by importance
5. **Test vs n-gram** — Compare effectiveness

---

**Status**: Algorithm inspiration gathered  
**Next**: Deep dive into LZMA implementation, design hybrid approach  
**Philosophy**: Natural patterns (LZ) + Importance (PageRank) + Context (PNI)
