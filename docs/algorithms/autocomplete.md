# Autocomplete Engine

**Purpose**: Real-time search suggestions using LZW + PageRank.

**NOTE**: Consolidated from research/01-foundations/ (2026-03-11)

---

## Overview

Autocomplete uses LZW dictionary compression for pattern discovery and PageRank for ranking suggestions.

---

## LZW Dictionary for Pattern Discovery

### How LZW Works

```text
Input: "hello hello world hello"

LZW builds dictionary dynamically:
  1. Read "h" -> not in dict, add "h" (code 0)
  2. Read "he" -> not in dict, add "he" (code 1)
  3. Read "hel" -> not in dict, add "hel" (code 2)
  4. Read "hell" -> not in dict, add "hell" (code 3)
  5. Read "hello" -> not in dict, add "hello" (code 4)
  6. Read "hello " -> not in dict, add "hello " (code 5)
  7. Read " " -> in dict, output code
  8. Read "he" -> in dict! Output code 1
  ...

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
```

### Key Insight

**LZW dictionary = Natural pattern index!**

- Automatically discovers repeated patterns
- No need to pre-define n-gram size
- Patterns of any length are captured

---

## LZW vs N-gram

| Aspect | N-gram | LZW |
|--------|--------|-----|
| Pattern size | Fixed (n) | Variable (discovered) |
| Dictionary | Implicit (all n-grams) | Explicit (frequent patterns) |
| Memory | O(|Σ|^n) | O(number of patterns) |
| Discovery | Exhaustive | Adaptive |

### When to Use Each

```text
N-gram:
  - Small n (2-3): Fuzzy matching, typo tolerance
  - Large n (5+): Exact phrase matching

LZW:
  - Autocomplete: Discovers common prefixes
  - Compression: Efficient storage
  - Pattern mining: Finds frequent substrings
```

---

## PageRank for Ranking

### Why PageRank?

Raw frequency is not enough for autocomplete.

```text
Example:
  "proxy" appears 100 times
    - 90 times in footer (less important)
    - 10 times in title (very important)

PageRank captures:
  - Position importance
  - Co-occurrence structure
  - Recursive importance
```

### Co-occurrence Graph

```text
Build graph from LZW dictionary:
  - Nodes: dictionary entries (patterns)
  - Edges: patterns co-occur in same context
  - Weight: frequency of co-occurrence

Run PageRank on this graph.
```

---

## Autocomplete Algorithm

### Step 1: Build LZW Dictionary

```python
def build_lzw_dict(texts):
    """Build LZW dictionary from corpus."""
    dictionary = {}
    code = 0
    current = ""
    
    for text in texts:
        for char in text:
            candidate = current + char
            if candidate in dictionary:
                current = candidate
            else:
                dictionary[code] = current + char
                code += 1
                current = char
    
    return dictionary
```

### Step 2: Build Co-occurrence Graph

```python
def build_cooccurrence_graph(dictionary, texts):
    """Build co-occurrence graph from dictionary."""
    graph = defaultdict(lambda: defaultdict(float))
    
    for text in texts:
        # Find all dictionary entries in text
        entries = find_entries(dictionary, text)
        
        # Add edges between co-occurring entries
        for i, e1 in enumerate(entries):
            for e2 in entries[i+1:i+5]:  # Window of 5
                graph[e1][e2] += 1
                graph[e2][e1] += 1
    
    return graph
```

### Step 3: Compute PageRank

```python
def compute_pagerank(graph, damping=0.85, iterations=20):
    """Compute PageRank on co-occurrence graph."""
    nodes = list(graph.keys())
    N = len(nodes)
    pr = {node: 1.0 / N for node in nodes}
    
    for _ in range(iterations):
        new_pr = {}
        for node in nodes:
            rank_sum = sum(
                pr[neighbor] / sum(graph[neighbor].values())
                for neighbor in graph
                if node in graph[neighbor]
            )
            new_pr[node] = (1 - damping) / N + damping * rank_sum
        pr = new_pr
    
    return pr
```

### Step 4: Autocomplete Query

```python
def autocomplete(query, dictionary, pagerank, top_k=5):
    """
    Get autocomplete suggestions for query.
    
    Returns: List of (suggestion, score) tuples
    """
    # Find all dictionary entries starting with query
    candidates = [
        (code, entry) for code, entry in dictionary.items()
        if entry.startswith(query)
    ]
    
    # Score by PageRank
    scored = [
        (entry, pagerank.get(code, 0))
        for code, entry in candidates
    ]
    
    # Sort by score, return top-k
    return sorted(scored, key=lambda x: -x[1])[:top_k]
```

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
  8: "proxy con",
  9: "proxy conf",
  10: "proxy confi",
  11: "proxy config",
  ...
}
```

### Autocomplete "prox"

```text
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
```

---

## Optimization

### Incremental Updates

```text
Problem: Rebuilding LZW dictionary is expensive.

Solution: Incremental updates
  - Add new patterns as they appear
  - Merge dictionaries periodically
  - Use rolling window for recent data
```

### Memory Efficiency

```text
Problem: Large dictionaries consume memory.

Solutions:
  1. Frequency threshold: Only keep patterns with freq >= 2
  2. Length limit: Max pattern length = 20 chars
  3. LRU cache: Keep most recently used entries
  4. Compression: Store dictionary entries compressed
```

---

## Related

- [Frequency Ranking](../core/frequency-ranking.md) - LZW + PageRank theory
- [N-gram Analysis](../core/ngram-analysis.md) - Alternative pattern extraction
- [Divergent Search](./divergent-search.md) - Non-obvious associations

---

**Last Updated**: 2026-03-11  
**Source Files**: `2026-03-06_lzwpagerank-autocomplete*.md`
