### 2. PNI as Partition

```text
PNI partitions text by context pairs:
  ⋃_{(pre,post)} PNI(pre, post) = All segments
  PNI(pre_1, post_1) INTERSECT PNI(pre_2, post_2) = ∅ if (pre_1,post_1) != (pre_2,post_2)

Mathematical property:
  PNI is a partition of segments (disjoint, complete)
```

### 3. LZ Patterns as Compression

```text
Patterns = Maximal repeated substrings

Compression ratio:
  CR = |T| / |PI| (original size / indexed size)

Higher CR = more redundancy = better compression
```

### 4. PageRank as Eigenvector

```text
PageRank r is principal eigenvector of Mᵀ:
  r = d * Mᵀ * r + (1-d)/|V| * 1⃗

Mathematical property:
  r exists and unique (Perron-Frobenius theorem)
```

### 5. Six Degrees as Graph Property

```text
Small-world property:
  L ≈ log(n) / log(k)

For text co-occurrence graphs:
  n = number of patterns
  k = average co-occurrence degree

Expected: L ≈ 3-4 (short paths exist)
```

---

## 10. Summary: Unified View

```text
Text T
  ↓ (φ_0_1: punctuation segmentation)
Segments with context pairs
  ↓ (φ_1_2: pattern extraction)
Patterns (maximal repeats)
  ↓ (φ_2_3: co-occurrence)
Graph G = (Patterns, Edges)
  ↓ (PageRank)
Importance scores
  ↓ (BFS)
Associations (k-degree)

All expressed in: Set theory, Graph theory, Linear algebra
```

---

STATUS: Mathematical formalization complete
NEXT: Implement based on mathematical definitions
PHILOSOPHY: Pure mathematics unifies all algorithms
