## 3. Weighted PageRank for Patterns

### User's Question

> "PageRank ?"
>
> (PageRank analysis: include citation/containment weights?)

---

### Standard PageRank (Unweighted)

```text
PR(v) = (1-d)/N + d * SIGMA_{u->v} PR(u) / out_degree(u)

Problem: All links treated equally!

Example:
  Pattern A co-occurs with B once: A -> B (weight 1)
  Pattern A co-occurs with C 100 times: A -> C (weight 100)

Standard PageRank: Both links have same influence!
```

---

### Weighted PageRank (With Co-occurrence Frequency)

DEFINITION-(WEIGHTED-PAGERANK):
```text
WPR(v) = (1-d)/N + d * SIGMA_{u} WPR(u) * w(u,v) / SIGMA_{t} w(u,t)

Where:
  w(u,v) = co-occurrence frequency of u and v
  SIGMA_{t} w(u,t) = total co-occurrences of u with all patterns
```

INTUITION:
```text
A link from u to v is stronger if:
  - u and v co-occur frequently (high w(u,v))
  - u doesn't co-occur with many others (low SIGMA_{t} w(u,t))

Analogy:
  - Academic citation: 100 citations from one paper > 1 citation each from 100 papers
  - Social network: Best friend's recommendation > acquaintance's recommendation
```

---

### Example: Weighted vs Unweighted

```text
Patterns: A, B, C, D

Co-occurrences:
  A ↔ B: 1 time
  A ↔ C: 100 times
  B ↔ D: 50 times
  C ↔ D: 1 time

Unweighted PageRank:
  A -> B (weight 1)
  A -> C (weight 1)
  B and C treated equally!

Weighted PageRank:
  A -> B (weight 1/101 ≈ 0.01)
  A -> C (weight 100/101 ≈ 0.99)
  C gets 99x more influence from A than B!
```

---

### Containment Weight (New Idea)

INSIGHT: Patterns can contain other patterns!

```text
"hello world" contains "hello" and "world"

Containment as weight:
  "hello world" -> "hello" (containment weight = 1)
  "hello world" -> "world" (containment weight = 1)
```

DEFINITION-(CONTAINMENT-WEIGHT):
```text
w_contain(p_parent, p_child) = 1 if p_child SUBSET p_parent, else 0

Where p_child SUBSET p_parent means p_child is substring of p_parent
```

EXTENDED-WEIGHTED-PAGERANK:
```text
EWPR(v) = (1-d)/N + d * (
  SIGMA_{u} EWPR(u) * w_cooccur(u,v) / SIGMA_{t} w_cooccur(u,t)  +
  SIGMA_{u} EWPR(u) * w_contain(u,v) / SIGMA_{t} w_contain(u,t)
)

Combines:
  - Co-occurrence weight (semantic relatedness)
  - Containment weight (hierarchical relationship)
```

---

### Example: Co-occurrence + Containment

```text
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
  B -> A: 1 (B contains A)
  C -> A: 1 (C contains A)

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

```text
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

PROBLEM: High frequency != always important

```text
"the" appears 10000 times (stop word, not important)
"proxy" appears 100 times (important concept)

Need: Frequency discounting
```

SOLUTION:-TF-IDF-STYLE-DISCOUNTING
```text
freq_discounted(p) = freq(p) / log(1 + docs_containing(p))

Where:
  docs_containing(p) = number of documents containing p

Intuition:
  - If p appears in ALL documents -> less informative
  - If p appears in FEW documents -> more informative
```

---

## 5. Mathematical Comparison

### N-gram Index vs LZ77 Index

| Metric | N-gram | LZ77 | Winner |
|--------|--------|------|--------|
| INDEX-SIZE | O(|C| x max_n) | O(|Unique Patterns|) | LZ77 |
| PATTERN-DISCOVERY | Fixed size | Variable (natural) | LZ77 |
| FREQUENCY-COUNTING | Per n-gram | Per pattern | LZ77 |
| QUERY-SPEED | O(1) lookup | O(log n) tree | N-gram |
| NOISE-FILTERING | Hard (all n-grams stored) | Easy (freq threshold) | LZ77 |
| CONTEXT-PRESERVATION | Lost (fragmented) | Preserved (PNI) | PNI+LZ77 |

---

### Unweighted vs Weighted PageRank

| Metric | Unweighted | Weighted | Winner |
|--------|------------|----------|--------|
| CO-OCCURRENCE-STRENGTH | Ignored | Captured | Weighted |
| CONTAINMENT | Ignored | Captured | Weighted |
| COMPUTATION | O(k.|E|) | O(k.|E|) | Tie |
| ACCURACY | Lower | Higher | Weighted |
| INTERPRETABILITY | Simple | Richer | Weighted |

---
