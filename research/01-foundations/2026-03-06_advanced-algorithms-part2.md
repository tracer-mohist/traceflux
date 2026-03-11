### Application to traceflux

```text
Instead of storing text as-is:
  "hello world hello"

BWT-like reordering:
  Group by context:
    "hello" appears before " world" (twice)
    "hello" appears at start (twice)

  Index by context, not position.
```

### Key Insight for Search

```text
BWT groups characters with similar **following context**.

For search:
  - Group segments by punctuation context (pre, post)
  - Similar contexts -> similar meaning?
  - Efficient compression of index
```

---

## Synthesis: Hybrid Approach for traceflux

### Combining Ideas

```text
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

```text
One-pass scan, segment by punctuation:

"Hello, world! How are you?"
  -> [("S", ","), "Hello"]
  -> [(",", "!"), " world"]
  -> [("!", "?"), " How are you"]
```

### Phase 2: LZ-Style Pattern Detection

```text
Find maximal repeated sequences:

Document 1: "proxy configuration"
Document 2: "proxy settings"
Document 3: "proxy configuration"

Patterns:
  "proxy" -> appears 3 times (at positions [...])
  "proxy config" -> appears 2 times
  "configuration" -> appears 2 times

Store as:
  Pattern: "proxy" -> [doc1:0, doc2:0, doc3:0]
  Pattern: " config" -> [doc1:6, doc3:6]
  Pattern: " settings" -> [doc2:6]
```

### Phase 3: PageRank on Co-occurrence Graph

```text
Build graph:
  Nodes: Patterns ("proxy", "config", "settings")
  Edges: Co-occur in same document

Rank:
  "proxy" -> High rank (appears with many patterns)
  "config" -> Medium rank
  "settings" -> Medium rank

Use rank to:
  - Filter low-rank patterns (noise)
  - Sort search results by importance
```

---

## Comparison: N-gram vs LZ-Style

| Aspect | N-gram | LZ-Style |
|--------|--------|----------|
| PATTERN-SIZE | Fixed (2, 3, 4 chars) | Variable (finds natural patterns) |
| STORAGE | All n-grams (redundant) | Only repeated patterns (efficient) |
| DISCOVERY | Sliding window | Longest match |
| EXAMPLE | "he", "el", "ll", "lo" | "hello" (once) + references |
| EFFICIENCY | O(n x max_n) | O(n) with suffix tree |
| NOISE | Many unique n-grams | Only repeated patterns |

---

## Key Insights

### 1. LZ77: Find Natural Patterns

```text
Instead of fixed n-grams:
  "h", "he", "hel", "hell", "hello", "ello", "llo", "lo", "o"

Find maximal repeats:
  "hello" (appears 5 times)
  "world" (appears 3 times)
  "hello world" (appears 2 times)

Benefit: Natural patterns, not arbitrary cuts.
```

### 2. PageRank: Importance Matters

```text
Not all patterns are equal:
  "proxy" (appears with 20 other patterns) -> Important
  "xyz123" (appears alone) -> Likely noise

Rank patterns by co-occurrence diversity.
```

### 3. BWT: Context Groups

```text
Group by punctuation context:
  ("S", ",") -> Patterns starting sentences, ending with comma
  (",", "!") -> Patterns between comma and exclamation

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
  +-- "hello hello world"
  +-- "ello hello world"
  +-- "llo hello world"
  +-- ...
  +-- "world"

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

1. RESEARCH-LZMA-MORE-DEEPLY -- Understand exact algorithm
2. IMPLEMENT-SUFFIX-TREE -- For O(n) pattern detection
3. COMBINE-WITH-PNI -- Punctuation namespaces + LZ patterns
4. ADD-PAGERANK -- Rank patterns by importance
5. TEST-VS-N-GRAM -- Compare effectiveness

---

STATUS: Algorithm inspiration gathered
NEXT: Deep dive into LZMA implementation, design hybrid approach
PHILOSOPHY: Natural patterns (LZ) + Importance (PageRank) + Context (PNI)
