# Frequency Ranking

**Purpose**: Weight patterns by occurrence and structural importance.

**NOTE**: Consolidated from research/01-foundations/ (2026-03-11)

---

## Core Principle

**Frequency is the simplest numerical metric** — it captures importance, redundancy, and signal vs noise.

---

## Frequency Definition

### Raw Frequency

```text
For pattern p in corpus C:

freq(p, C) = count of (document, position) pairs where p appears
```

### Example

```text
Corpus C = {
  T_1 = "proxy config proxy",
  T_2 = "proxy settings",
  T_3 = "proxy config"
}

freq("proxy", C) = 4   (appears 4 times total)
freq("config", C) = 2
freq("settings", C) = 1

Normalized frequency:
freq_norm("proxy", C) = 4 / 3 ≈ 1.33 (per document)
```

---

## Why Frequency is Fundamental

### Captures Multiple Signals

```text
Frequency captures:
  1. Importance (high freq = important)
  2. Redundancy (high freq = repeated)
  3. Signal vs Noise (low freq = likely noise)
```

### Properties

```text
- Simple to compute: O(n)
- Easy to understand: count
- Universal: applies to any pattern type
- Comparable: same scale across patterns
```

---

## Frequency-Based Filtering

### Minimum Support Threshold

```text
Keep pattern p if: freq(p, C) >= min_support

Example (min_support = 2):
  "proxy" (freq=4) -> Keep
  "config" (freq=2) -> Keep
  "settings" (freq=1) -> Filter (likely noise)
```

### Adaptive Thresholds

```text
Global threshold: min_support = 2 (for all patterns)

Position-weighted:
  - Start of text: min_support = 1 (more important)
  - Middle: min_support = 2
  - End: min_support = 2

Length-weighted:
  - Short patterns (1-2 chars): min_support = 5 (common, need higher bar)
  - Medium (3-5 chars): min_support = 2
  - Long (6+ chars): min_support = 1 (rare, keep all)
```

---

## LZW Compression for Pattern Discovery

### LZW Basics

LZW (Lempel-Ziv-Welch) compression discovers repeated patterns automatically.

### How It Works

```text
Text: "proxy config proxy settings"

Step 1: Initialize dictionary with single characters
  Dictionary: {p, r, o, x, y,  , c, o, n, f, i, g, s, e, t, l, n, g}

Step 2: Scan text, add new patterns to dictionary
  "pr" -> new, add to dict
  "ro" -> new, add to dict
  "ox" -> new, add to dict
  ...
  "proxy" -> new, add to dict
  "proxy " -> new, add to dict
  "proxy c" -> new, add to dict
  ...

Step 3: When pattern repeats, use dictionary reference
  Second "proxy" -> reference existing entry
```

### Benefits for TraceFlux

```text
1. Automatic pattern discovery
   - No need to pre-define n-gram size
   - Discovers patterns of any length

2. Efficient storage
   - Repeated patterns stored once
   - Reference by ID

3. Frequency tracking
   - Each dictionary entry has frequency count
   - High-frequency patterns = important
```

---

## PageRank for Structural Importance

### Why PageRank?

Raw frequency is not enough. Position and context matter.

```text
Example:
  "proxy" appears 100 times
    - 90 times in footer (less important)
    - 10 times in title (very important)

PageRank captures:
  - Position importance (title > footer)
  - Link structure (citations, references)
  - Recursive importance (important pages link to important pages)
```

### Weighted PageRank

```text
For pattern p:

PR(p) = (1 - d) / N + d * Σ(PR(q) / out_degree(q))
                     for all q linking to p

Where:
  d = damping factor (0.85)
  N = total patterns
  q = patterns that co-occur with p
```

### Application to Text

```text
Co-occurrence graph:
  - Nodes: patterns (n-grams, segments)
  - Edges: patterns appear in same document/segment
  - Weight: frequency of co-occurrence

PageRank on this graph:
  - Patterns co-occurring with important patterns become important
  - Captures semantic relationships
```

---

## Combined Scoring

### Final Score Formula

```text
score(p) = α * freq_norm(p) + β * pagerank(p) + γ * position_weight(p)

Where:
  α, β, γ = weights (sum to 1.0)
  freq_norm = normalized frequency
  pagerank = structural importance
  position_weight = boost for start/end positions
```

### Example Weights

```text
For search autocomplete:
  α = 0.5 (frequency matters most)
  β = 0.3 (structure matters)
  γ = 0.2 (position matters)

For document ranking:
  α = 0.3
  β = 0.5 (structure matters more)
  γ = 0.2
```

---

## Implementation

### Frequency Index

```python
from collections import defaultdict

class FrequencyIndex:
    def __init__(self, min_support=2):
        self.min_support = min_support
        self.frequency = defaultdict(int)

    def add_text(self, text):
        """Add text to frequency index."""
        # Count all substrings (or use n-grams)
        for i in range(len(text)):
            for j in range(i + 1, min(i + 10, len(text) + 1)):
                pattern = text[i:j]
                self.frequency[pattern] += 1

    def get_frequent(self):
        """Get patterns meeting minimum support."""
        return {
            p: f for p, f in self.frequency.items()
            if f >= self.min_support
        }
```

### PageRank Integration

```python
def compute_pagerank(cooccurrence_graph, damping=0.85, iterations=20):
    """
    Compute PageRank on co-occurrence graph.

    Args:
        cooccurrence_graph: dict {pattern: {neighbor: weight}}
        damping: damping factor
        iterations: number of iterations

    Returns: dict {pattern: pagerank_score}
    """
    nodes = list(cooccurrence_graph.keys())
    N = len(nodes)

    # Initialize
    pr = {node: 1.0 / N for node in nodes}

    # Iterate
    for _ in range(iterations):
        new_pr = {}
        for node in nodes:
            rank_sum = sum(
                pr[neighbor] / sum(cooccurrence_graph[neighbor].values())
                for neighbor in cooccurrence_graph
                if node in cooccurrence_graph[neighbor]
            )
            new_pr[node] = (1 - damping) / N + damping * rank_sum
        pr = new_pr

    return pr
```

---

## Related

- [N-gram Analysis](./ngram-analysis.md) - Pattern extraction
- [Mathematical Model](./mathematical-model.md) - Formal definitions
- [Autocomplete](../algorithms/autocomplete.md) - Application

---

**Last Updated**: 2026-03-11
**Source Files**: `2026-03-06_frequency-lz-pagerank*.md`
