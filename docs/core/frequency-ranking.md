# Frequency Ranking

Purpose: Weight patterns by occurrence and structural importance.

NOTE: Consolidated from research/01-foundations/ (2026-03-11)

---

## Core Principle

Frequency is the simplest numerical metric - it captures importance, redundancy, and signal vs noise.

---

## Frequency Definition

### Raw Frequency

For pattern p in corpus C:

freq(p, C) = count of (document, position) pairs where p appears

### Example

Corpus C = {
  T_1 = "proxy config proxy",
  T_2 = "proxy settings",
  T_3 = "proxy config"
}

freq("proxy", C) = 4   (appears 4 times total)
freq("config", C) = 2
freq("settings", C) = 1

Normalized frequency:
freq_norm("proxy", C) = 4 / 3 ~= 1.33 (per document)

---

## Why Frequency is Fundamental

### Captures Multiple Signals

Frequency captures:
  1. Importance (high freq = important)
  2. Redundancy (high freq = repeated)
  3. Signal vs Noise (low freq = likely noise)

### Properties

- Simple to compute: O(n)
- Easy to understand: count
- Universal: applies to any pattern type
- Comparable: same scale across patterns

---

## Frequency-Based Filtering

### Minimum Support Threshold

Keep pattern p if: freq(p, C) >= min_support

Example (min_support = 2):
  "proxy" (freq=4) -> Keep
  "config" (freq=2) -> Keep
  "settings" (freq=1) -> Filter (likely noise)

### Adaptive Thresholds

Global threshold: min_support = 2 (for all patterns)

Position-weighted:
  - Start of text: min_support = 1 (more important)
  - Middle: min_support = 2
  - End: min_support = 2

Length-weighted:
  - Short patterns (1-2 chars): min_support = 5
  - Medium (3-5 chars): min_support = 2
  - Long (6+ chars): min_support = 1

---

## LZW Compression for Pattern Discovery

### LZW Basics

LZW (Lempel-Ziv-Welch) compression discovers repeated patterns automatically.

### How It Works

Text: "proxy config proxy settings"

Step 1: Initialize dictionary with single characters

Step 2: Scan text, add new patterns to dictionary
  "pr" -> new, add to dict
  "ro" -> new, add to dict
  "proxy" -> new, add to dict
  ...

Step 3: When pattern repeats, use dictionary reference
  Second "proxy" -> reference existing entry

### Benefits for TraceFlux

1. Automatic pattern discovery
   - No need to pre-define n-gram size
   - Discovers patterns of any length

2. Efficient storage
   - Repeated patterns stored once
   - Reference by ID

3. Frequency tracking
   - Each dictionary entry has frequency count
   - High-frequency patterns = important

---

## PageRank for Structural Importance

### Why PageRank?

Raw frequency is not enough. Position and context matter.

Example:
  "proxy" appears 100 times
    - 90 times in footer (less important)
    - 10 times in title (very important)

PageRank captures:
  - Position importance (title > footer)
  - Link structure (citations, references)
  - Recursive importance

### Weighted PageRank

For pattern p:

PR(p) = (1 - d) / N + d * sum(PR(q) / out_degree(q))
                                 for all q linking to p

Where:
  d = damping factor (0.85)
  N = total patterns
  q = patterns that co-occur with p

### Application to Text

Co-occurrence graph:
  - Nodes: patterns (n-grams, segments)
  - Edges: patterns appear in same document/segment
  - Weight: frequency of co-occurrence

PageRank on this graph:
  - Patterns co-occurring with important patterns become important
  - Captures semantic relationships

---

## Combined Scoring

### Final Score Formula

score(p) = alpha * freq_norm(p) + beta * pagerank(p) + gamma * pos_weight(p)

Where:
  alpha, beta, gamma = weights (sum to 1.0)
  freq_norm = normalized frequency
  pagerank = structural importance
  pos_weight = boost for start/end positions

### Example Weights

For search autocomplete:
  alpha = 0.5 (frequency matters most)
  beta = 0.3 (structure matters)
  gamma = 0.2 (position matters)

For document ranking:
  alpha = 0.3
  beta = 0.5 (structure matters more)
  gamma = 0.2

---

## Implementation Reference

See: [frequency-ranking-impl.md](./frequency-ranking-impl.md)

- Frequency index implementation
- PageRank computation
- Combined scoring function

---

## Related

- [N-gram Analysis](./ngram-analysis.md) - Pattern extraction
- [Mathematical Model](./mathematical-model.md) - Formal definitions
- [Autocomplete](../algorithms/autocomplete.md) - Application
- [Implementation](./frequency-ranking-impl.md) - Code examples

---

Last Updated: 2026-03-11
Source Files: 2026-03-06_frequency-lz-pagerank*.md
