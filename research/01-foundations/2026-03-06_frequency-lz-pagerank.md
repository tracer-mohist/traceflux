# Research: Frequency, LZ77 Indexing, and Weighted PageRank

DATE: 2026-03-06
STATUS: Critical Analysis
TOPIC: Frequency as basic metric, LZ77 vs N-gram, Weighted PageRank

---

## 1. Frequency as Basic Metric

### User's Insight

> ""
>
> (Frequency of occurrence is the simplest numerical metric)

---

### Mathematical Formalization

DEFINITION-(FREQUENCY):
```text
For pattern p in corpus C:

freq(p, C) = |{(d, pos) | p appears at pos in Tₔ}|

Normalized frequency:
freq_norm(p, C) = freq(p, C) / |C|
```

EXAMPLE:
```text
C = {
  T_1 = "proxy config proxy",
  T_2 = "proxy settings",
  T_3 = "proxy config"
}

freq("proxy", C) = 4  (appears 4 times total)
freq("config", C) = 2
freq("settings", C) = 1

freq_norm("proxy", C) = 4 / 3 ≈ 1.33 (per document)
```

---

### Why Frequency is Fundamental

```text
Frequency captures:
  1. Importance (high freq = important)
  2. Redundancy (high freq = repeated)
  3. Signal vs Noise (low freq = likely noise)

Properties:
  - Simple to compute: O(n)
  - Easy to understand: count
  - Universal: applies to any pattern type
  - Comparable: same scale across patterns
```

---

### Frequency-Based Filtering

```text
Filter by frequency threshold:

Keep pattern p if: freq(p, C) >= min_support

Example:
  min_support = 2

  "proxy" (freq=4) -> Keep
  "config" (freq=2) -> Keep
  "settings" (freq=1) -> Filter  (likely noise)
```

---

## 2. N-gram vs LZ77 for Indexing

### User's Question

> " n-gram ,LZ77 ?"
>
> (For n-gram evaluation, is LZ77 more suitable for indexing?)

---

### Critical Analysis: N-gram Index Problems

PROBLEM-1:-REDUNDANCY
```text
Text: "hello hello hello"

2-gram index:
  "he" -> [0, 6, 12]
  "el" -> [1, 7, 13]
  "ll" -> [2, 8, 14]
  "lo" -> [3, 9, 15]
  "o " -> [4, 10, 16]

Stored: 5 entries x 3 positions = 15 integers

But: "hello" repeats 3 times -- redundancy not captured!
```

PROBLEM-2:-FIXED-SIZE
```text
"hello" and "hello world" treated same:

2-grams of "hello": ["he", "el", "ll", "lo"]
2-grams of "hello world": ["he", "el", "ll", "lo", "o ", " w", "wo", "or", "rl", "ld"]

No distinction between short and long patterns!
```

PROBLEM-3:-FRAGMENTATION
```text
"hello hello" indexed as:
  "he": [0, 6]
  "el": [1, 7]
  "ll": [2, 8]
  "lo": [3, 9]

But: "hello" as a unit is lost!
Cannot directly query "find all 'hello'"
```

---

### LZ77 Index Advantages

ADVANTAGE-1:-NATURAL-PATTERNS
```text
Text: "hello hello world hello"

LZ77 finds:
  "hello" -> [0, 6, 18]  (maximal repeat)
  " world" -> [12]       (unique)

Index:
  "hello" -> [0, 6, 18]
  " world" -> [12]

Stored: 2 entries (vs 5+ for n-gram)
```

ADVANTAGE-2:-VARIABLE-LENGTH
```text
Patterns have natural lengths:
  "hello" (5 chars)
  "hello world" (11 chars)
  "world" (5 chars)

Not artificially cut to fixed n!
```

ADVANTAGE-3:-COMPRESSION-=-INDEXING
```text
LZ77 compression:
  "hello hello world hello"
  -> "hello" + <ref: offset=6, len=5> + " world" + <ref: offset=18, len=5>

Index is compression byproduct:
  Pattern "hello" -> positions [0, 6, 18]

Benefit: Index size proportional to unique patterns, not text length!
```

---

### Mathematical Comparison

N-GRAM-INDEX-SIZE:
```text
|I_n| = O(|C| x max_n)

Where:
  |C| = corpus size
  max_n = maximum n-gram size

Example: |C| = 1MB, max_n = 5
  |I_n| ≈ 5MB (5x expansion)
```

LZ77-INDEX-SIZE:
```text
|I_LZ| = O(|Unique Patterns|)

Where:
  |Unique Patterns| << |C| (for redundant text)

Example: |C| = 1MB, unique patterns = 100KB
  |I_LZ| ≈ 100KB (10x compression)
```

CONCLUSION: LZ77 index is exponentially smaller for redundant text!

---

### Hybrid Approach: PNI + LZ77

```text
Phase 1: PNI Segmentation
  "Hello, world! How are you?"
  -> [("S", ","), "Hello"]
  -> [(",", "!"), " world"]
  -> [("!", "?"), " How are you"]

Phase 2: LZ77 Pattern Detection (within each namespace)
  Namespace ("S", ","):
    "Hello" appears 5 times -> Pattern
    "Hi" appears 3 times -> Pattern
    "Greetings" appears 1 time -> Filter (noise)

Phase 3: Index by Namespace + Pattern
  Index:
    ("S", ","): {
      "Hello": [doc1:0, doc3:10, doc5:5],
      "Hi": [doc2:0, doc4:5, doc6:0]
    }
    (",", "!"): {
      " world": [doc1:6, doc2:3, ...]
    }
```

BENEFIT:
- PNI provides context (namespace)
- LZ77 provides patterns (natural units)
- Frequency provides filtering (noise removal)

---
