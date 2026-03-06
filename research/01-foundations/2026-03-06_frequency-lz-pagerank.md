# Research: Frequency, LZ77 Indexing, and Weighted PageRank

**Date**: 2026-03-06  
**Status**: Critical Analysis  
**Topic**: Frequency as basic metric, LZ77 vs N-gram, Weighted PageRank

---

## 1. Frequency as Basic Metric

### User's Insight

> "某种组合的出现次数是最简单使用的数值化"
> 
> (Frequency of occurrence is the simplest numerical metric)

---

### Mathematical Formalization

**Definition (Frequency)**:
```
For pattern p in corpus C:

freq(p, C) = |{(d, pos) | p appears at pos in Tₔ}|

Normalized frequency:
freq_norm(p, C) = freq(p, C) / |C|
```

**Example**:
```
C = {
  T₁ = "proxy config proxy",
  T₂ = "proxy settings",
  T₃ = "proxy config"
}

freq("proxy", C) = 4  (appears 4 times total)
freq("config", C) = 2
freq("settings", C) = 1

freq_norm("proxy", C) = 4 / 3 ≈ 1.33 (per document)
```

---

### Why Frequency is Fundamental

```
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

```
Filter by frequency threshold:

Keep pattern p if: freq(p, C) ≥ min_support

Example:
  min_support = 2
  
  "proxy" (freq=4) → Keep ✓
  "config" (freq=2) → Keep ✓
  "settings" (freq=1) → Filter ✗ (likely noise)
```

---

## 2. N-gram vs LZ77 for Indexing

### User's Question

> "对于 n-gram 评价，LZ77 是否更合适索引？"
> 
> (For n-gram evaluation, is LZ77 more suitable for indexing?)

---

### Critical Analysis: N-gram Index Problems

**Problem 1: Redundancy**
```
Text: "hello hello hello"

2-gram index:
  "he" → [0, 6, 12]
  "el" → [1, 7, 13]
  "ll" → [2, 8, 14]
  "lo" → [3, 9, 15]
  "o " → [4, 10, 16]

Stored: 5 entries × 3 positions = 15 integers

But: "hello" repeats 3 times — redundancy not captured!
```

**Problem 2: Fixed Size**
```
"hello" and "hello world" treated same:

2-grams of "hello": ["he", "el", "ll", "lo"]
2-grams of "hello world": ["he", "el", "ll", "lo", "o ", " w", "wo", "or", "rl", "ld"]

No distinction between short and long patterns!
```

**Problem 3: Fragmentation**
```
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

**Advantage 1: Natural Patterns**
```
Text: "hello hello world hello"

LZ77 finds:
  "hello" → [0, 6, 18]  (maximal repeat)
  " world" → [12]       (unique)

Index:
  "hello" → [0, 6, 18]
  " world" → [12]

Stored: 2 entries (vs 5+ for n-gram)
```

**Advantage 2: Variable Length**
```
Patterns have natural lengths:
  "hello" (5 chars)
  "hello world" (11 chars)
  "world" (5 chars)

Not artificially cut to fixed n!
```

**Advantage 3: Compression = Indexing**
```
LZ77 compression:
  "hello hello world hello"
  → "hello" + <ref: offset=6, len=5> + " world" + <ref: offset=18, len=5>

Index is compression byproduct:
  Pattern "hello" → positions [0, 6, 18]
  
Benefit: Index size proportional to unique patterns, not text length!
```

---

### Mathematical Comparison

**N-gram Index Size**:
```
|Iₙ| = O(|C| × max_n)

Where:
  |C| = corpus size
  max_n = maximum n-gram size

Example: |C| = 1MB, max_n = 5
  |Iₙ| ≈ 5MB (5× expansion)
```

**LZ77 Index Size**:
```
|I_LZ| = O(|Unique Patterns|)

Where:
  |Unique Patterns| << |C| (for redundant text)

Example: |C| = 1MB, unique patterns = 100KB
  |I_LZ| ≈ 100KB (10× compression)
```

**Conclusion**: LZ77 index is exponentially smaller for redundant text!

---

### Hybrid Approach: PNI + LZ77

```
Phase 1: PNI Segmentation
  "Hello, world! How are you?"
  → [("S", ","), "Hello"]
  → [(",", "!"), " world"]
  → [("!", "?"), " How are you"]

Phase 2: LZ77 Pattern Detection (within each namespace)
  Namespace ("S", ","):
    "Hello" appears 5 times → Pattern
    "Hi" appears 3 times → Pattern
    "Greetings" appears 1 time → Filter (noise)

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

**Benefit**: 
- PNI provides context (namespace)
- LZ77 provides patterns (natural units)
- Frequency provides filtering (noise removal)

---

## 3. Weighted PageRank for Patterns

### User's Question

> "PageRank 分析引用或者包含权重？"
> 
> (PageRank analysis: include citation/containment weights?)

---

### Standard PageRank (Unweighted)

```
PR(v) = (1-d)/N + d * Σ_{u→v} PR(u) / out_degree(u)

Problem: All links treated equally!

Example:
  Pattern A co-occurs with B once: A → B (weight 1)
  Pattern A co-occurs with C 100 times: A → C (weight 100)

Standard PageRank: Both links have same influence!
```

---

### Weighted PageRank (With Co-occurrence Frequency)

**Definition (Weighted PageRank)**:
```
WPR(v) = (1-d)/N + d * Σ_{u} WPR(u) * w(u,v) / Σ_{t} w(u,t)

Where:
  w(u,v) = co-occurrence frequency of u and v
  Σ_{t} w(u,t) = total co-occurrences of u with all patterns
```

**Intuition**:
```
A link from u to v is stronger if:
  - u and v co-occur frequently (high w(u,v))
  - u doesn't co-occur with many others (low Σ_{t} w(u,t))

Analogy:
  - Academic citation: 100 citations from one paper > 1 citation each from 100 papers
  - Social network: Best friend's recommendation > acquaintance's recommendation
```

---

### Example: Weighted vs Unweighted

```
Patterns: A, B, C, D

Co-occurrences:
  A ↔ B: 1 time
  A ↔ C: 100 times
  B ↔ D: 50 times
  C ↔ D: 1 time

Unweighted PageRank:
  A → B (weight 1)
  A → C (weight 1)
  B and C treated equally!

Weighted PageRank:
  A → B (weight 1/101 ≈ 0.01)
  A → C (weight 100/101 ≈ 0.99)
  C gets 99× more influence from A than B!
```

---

### Containment Weight (New Idea)

**Insight**: Patterns can contain other patterns!

```
"hello world" contains "hello" and "world"

Containment as weight:
  "hello world" → "hello" (containment weight = 1)
  "hello world" → "world" (containment weight = 1)
```

**Definition (Containment Weight)**:
```
w_contain(p_parent, p_child) = 1 if p_child ⊂ p_parent, else 0

Where p_child ⊂ p_parent means p_child is substring of p_parent
```

**Extended Weighted PageRank**:
```
EWPR(v) = (1-d)/N + d * (
  Σ_{u} EWPR(u) * w_cooccur(u,v) / Σ_{t} w_cooccur(u,t)  +
  Σ_{u} EWPR(u) * w_contain(u,v) / Σ_{t} w_contain(u,t)
)

Combines:
  - Co-occurrence weight (semantic relatedness)
  - Containment weight (hierarchical relationship)
```

---

### Example: Co-occurrence + Containment

```
Patterns:
  A = "proxy"
  B = "proxy configuration"
  C = "proxy settings"
  D = "git proxy"

Co-occurrence weights:
  A ↔ B: 10 times
  A ↔ C: 8 times
  A ↔ D: 5 times

Containment weights:
  B → A: 1 (B contains A)
  C → A: 1 (C contains A)

Extended PageRank:
  A receives from:
    - B (co-occur: 10, contain: 1)
    - C (co-occur: 8, contain: 1)
    - D (co-occur: 5, contain: 0)
  
  A is important because:
    - Co-occurs with many patterns (hub)
    - Contained in longer patterns (fundamental concept)
```

---

## 4. Unified Scoring Formula

### Combining All Metrics

```
Score(p) = α * freq_norm(p) + β * WPR(p) + γ * specificity(p)

Where:
  freq_norm(p) = freq(p) / max_freq (normalized frequency)
  WPR(p) = weighted PageRank (importance)
  specificity(p) = |p| / avg_length (longer = more specific)
  α + β + γ = 1 (weights)

Typical weights:
  α = 0.4 (frequency)
  β = 0.4 (PageRank)
  γ = 0.2 (specificity)
```

---

### Frequency Discounting

**Problem**: High frequency ≠ always important

```
"the" appears 10000 times (stop word, not important)
"proxy" appears 100 times (important concept)

Need: Frequency discounting
```

**Solution: TF-IDF Style Discounting**
```
freq_discounted(p) = freq(p) / log(1 + docs_containing(p))

Where:
  docs_containing(p) = number of documents containing p

Intuition:
  - If p appears in ALL documents → less informative
  - If p appears in FEW documents → more informative
```

---

## 5. Mathematical Comparison

### N-gram Index vs LZ77 Index

| Metric | N-gram | LZ77 | Winner |
|--------|--------|------|--------|
| **Index Size** | O(|C| × max_n) | O(|Unique Patterns|) | LZ77 |
| **Pattern Discovery** | Fixed size | Variable (natural) | LZ77 |
| **Frequency Counting** | Per n-gram | Per pattern | LZ77 |
| **Query Speed** | O(1) lookup | O(log n) tree | N-gram |
| **Noise Filtering** | Hard (all n-grams stored) | Easy (freq threshold) | LZ77 |
| **Context Preservation** | Lost (fragmented) | Preserved (PNI) | PNI+LZ77 |

---

### Unweighted vs Weighted PageRank

| Metric | Unweighted | Weighted | Winner |
|--------|------------|----------|--------|
| **Co-occurrence Strength** | Ignored | Captured | Weighted |
| **Containment** | Ignored | Captured | Weighted |
| **Computation** | O(k·|E|) | O(k·|E|) | Tie |
| **Accuracy** | Lower | Higher | Weighted |
| **Interpretability** | Simple | Richer | Weighted |

---

## 6. Recommended Approach

### Final Design: PNI + LZ77 + Weighted PageRank

```
Phase 1: PNI Segmentation (O(n))
  Split by punctuation, record context pairs

Phase 2: LZ77 Pattern Detection (O(n))
  Find maximal repeated patterns in each namespace
  Filter: freq(p) < min_support → discard

Phase 3: Co-occurrence Graph Construction
  Nodes: Patterns
  Edges: Co-occurrence in same document
  Weights: Co-occurrence frequency + containment

Phase 4: Weighted PageRank (O(k·|E|))
  Compute EWPR for all patterns
  Filter: EWPR(p) < threshold → discard (noise)

Phase 5: Index Construction
  Index: Pattern → [(doc_id, positions, EWPR_score)]
  Query: O(log n) lookup + BFS for associations
```

---

### Key Formulas

**Frequency**:
```
freq(p) = |{(d, pos) | p appears at pos in Tₔ}|
```

**Weighted PageRank**:
```
WPR(p) = (1-d)/N + d * Σ_{q} WPR(q) * w(q,p) / Σ_{r} w(q,r)
```

**Combined Score**:
```
Score(p) = 0.4 * freq_norm(p) + 0.4 * WPR(p) + 0.2 * specificity(p)
```

**Association Discovery**:
```
Assocₖ(query) = {p | dist(query, p) ≤ k} via BFS on co-occurrence graph
```

---

## 7. Key Insights

### 1. Frequency is Foundation
```
All metrics build on frequency:
  - Raw frequency → importance signal
  - Normalized frequency → comparable across patterns
  - Discounted frequency → informativeness

But: Frequency alone is not enough!
```

### 2. LZ77 > N-gram for Indexing
```
LZ77 advantages:
  - Natural patterns (not arbitrary cuts)
  - Variable length (captures semantics)
  - Smaller index (compression = indexing)
  - Easy filtering (frequency threshold)
```

### 3. Weighted PageRank Captures Richness
```
Unweighted: All links equal
Weighted: Strong co-occurrences matter more
Containment: Hierarchical relationships

Result: Better importance estimation
```

### 4. Hybrid Approach Best
```
PNI (context) + LZ77 (patterns) + WPR (ranking)
= Best of all worlds
```

---

**Status**: Critical analysis complete, recommended design finalized  
**Next**: Implement PNI + LZ77 + Weighted PageRank  
**Philosophy**: Frequency is foundation, but context and structure matter
