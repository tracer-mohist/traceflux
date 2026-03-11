## 6. Recommended Approach

### Final Design: PNI + LZ77 + Weighted PageRank

```text
Phase 1: PNI Segmentation (O(n))
  Split by punctuation, record context pairs

Phase 2: LZ77 Pattern Detection (O(n))
  Find maximal repeated patterns in each namespace
  Filter: freq(p) < min_support -> discard

Phase 3: Co-occurrence Graph Construction
  Nodes: Patterns
  Edges: Co-occurrence in same document
  Weights: Co-occurrence frequency + containment

Phase 4: Weighted PageRank (O(k.|E|))
  Compute EWPR for all patterns
  Filter: EWPR(p) < threshold -> discard (noise)

Phase 5: Index Construction
  Index: Pattern -> [(doc_id, positions, EWPR_score)]
  Query: O(log n) lookup + BFS for associations
```

---

### Key Formulas

FREQUENCY:
```text
freq(p) = |{(d, pos) | p appears at pos in Tₔ}|
```

WEIGHTED-PAGERANK:
```text
WPR(p) = (1-d)/N + d * SIGMA_{q} WPR(q) * w(q,p) / SIGMA_{r} w(q,r)
```

COMBINED-SCORE:
```text
Score(p) = 0.4 * freq_norm(p) + 0.4 * WPR(p) + 0.2 * specificity(p)
```

ASSOCIATION-DISCOVERY:
```text
Assoc_k(query) = {p | dist(query, p) <= k} via BFS on co-occurrence graph
```

---

## 7. Key Insights

### 1. Frequency is Foundation
```text
All metrics build on frequency:
  - Raw frequency -> importance signal
  - Normalized frequency -> comparable across patterns
  - Discounted frequency -> informativeness

But: Frequency alone is not enough!
```

### 2. LZ77 > N-gram for Indexing
```text
LZ77 advantages:
  - Natural patterns (not arbitrary cuts)
  - Variable length (captures semantics)
  - Smaller index (compression = indexing)
  - Easy filtering (frequency threshold)
```

### 3. Weighted PageRank Captures Richness
```text
Unweighted: All links equal
Weighted: Strong co-occurrences matter more
Containment: Hierarchical relationships

Result: Better importance estimation
```

### 4. Hybrid Approach Best
```text
PNI (context) + LZ77 (patterns) + WPR (ranking)
= Best of all worlds
```

---

STATUS: Critical analysis complete, recommended design finalized
NEXT: Implement PNI + LZ77 + Weighted PageRank
PHILOSOPHY: Frequency is foundation, but context and structure matter
