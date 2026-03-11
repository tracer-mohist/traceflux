### PatternRank (Adapted for Text)

DEFINITION-18-(PATTERNRANK):
```text
For co-occurrence graph G:

Rank(p) = (1-d)/|V| + d * SIGMA_{q: (q,p)INE} Rank(q) * w(q,p) / SIGMA_{r} w(q,r)

Where:
  - w(q,p) = co-occurrence count of q and p
  - SIGMA_{r} w(q,r) = total co-occurrences of q with all patterns
```

INTUITION:
```text
A pattern is important if:
  - Important patterns co-occur with it
  - Co-occurrence is frequent (high weight)
```

---

## 6. Six Degrees Mathematical Model

### Graph Distance

DEFINITION-19-(PATH):
```text
A path from u to v in graph G:
  Path(u, v) = ⟨v_0, v_1, ..., v_k⟩

Where:
  - v_0 = u
  - v_k = v
  - (vᵢ, vᵢ_+_1) IN E for all 0 <= i < k

Length: |Path| = k (number of edges)
```

DEFINITION-20-(SHORTEST-PATH-DISTANCE):
```text
dist(u, v) = min{|Path(u, v)|}

If no path exists: dist(u, v) = INF
```

---

### Average Path Length

DEFINITION-21-(AVERAGE-PATH-LENGTH):
```text
For graph G with n vertices:

L = (1 / (n*(n-1))) * SIGMA_{u!=v} dist(u, v)

For small-world networks: L ≈ log(n) / log(k)

Where k = average degree
```

EXAMPLE:
```text
Social network:
  n = 7 billion (world population)
  k = 1000 (average person knows ~1000 people)

  L ≈ log(7x10^9) / log(1000)
  L ≈ 22.8 / 3 ≈ 7.6

  -> ~6-8 degrees (matches empirical findings!)
```

---

### Association Discovery via BFS

DEFINITION-22-(K-DEGREE-ASSOCIATIONS):
```text
For query pattern q and graph G:

Assoc_k(q) = {p IN V | dist(q, p) <= k}

With paths:
  AssocPaths_k(q) = {Path(q, p) | p IN Assoc_k(q)}
```

ALGORITHM-(BFS):
```text
BFS(G, q, k):
  visited = {q}
  queue = [(q, 0, [q])]  // (node, degree, path)
  results = []

  while queue not empty:
    (v, deg, path) = dequeue()
    if deg >= k: continue

    for neighbor in neighbors(v):
      if neighbor not in visited:
        visited.add(neighbor)
        new_path = path + [neighbor]
        results.append((neighbor, deg+1, new_path))
        enqueue((neighbor, deg+1, new_path))

  return results
```

---

## 7. Unified Mathematical Framework

### Text as Multi-Layer Structure

DEFINITION-23-(TEXT-MULTI-LAYER):
```text
Text T has multiple representations:

Layer 0 (Character): T = ⟨c_0, c_1, ..., c_n_-_1⟩
Layer 1 (Segment): Seg(T) = {s_0, s_1, ..., sₘ}
Layer 2 (Pattern): Patterns(T) = {p_0, p_1, ..., p_k}
Layer 3 (Graph): G = (Patterns, Co-occurrence)
```

MAPPINGS:
```text
φ_0_1: Layer 0 -> Layer 1 (punctuation segmentation)
φ_1_2: Layer 1 -> Layer 2 (pattern extraction)
φ_2_3: Layer 2 -> Layer 3 (co-occurrence graph)
```

---

### Unified Index Structure

DEFINITION-24-(UNIFIED-INDEX):
```text
Index I = (PNI, PI, CG, PR)

Where:
  - PNI: Punctuation Namespace Index (Def 11)
  - PI: Pattern Index (Def 15)
  - CG: Co-occurrence Graph (Def 16)
  - PR: PatternRank scores (Def 18)

Query Q:
  1. Lookup PNI for context-matched segments
  2. Lookup PI for pattern matches
  3. Traverse CG for associations (BFS)
  4. Rank by PR scores
```

---

### Query Processing (Mathematical)

DEFINITION-25-(QUERY-RESULT):
```text
For query q and index I:

Result(q, I) = {(p, score, path) | p IN Patterns}

Where:
  - score = α * exact_match(p, q) + β * PR(p) + γ * assoc_score(p, q)
  - path = Path from q to p in CG (if exists)
  - α + β + γ = 1 (weights)

Ranking: Sort by score descending
```

---

## 8. Complexity Analysis

### Time Complexity

| Operation | Algorithm | Complexity |
|-----------|-----------|------------|
| N-gram extraction | Sliding window | O(n) |
| PNI construction | One-pass scan | O(n) |
| Pattern detection | Suffix tree | O(n) |
| PageRank | Power iteration | O(k.\|E\|) |
| BFS (k-degree) | Breadth-first | O(k.d^k) |

Where:
- n = text length
- k = iterations / BFS depth
- d = average graph degree

---

### Space Complexity

| Structure | Space |
|-----------|-------|
| N-gram index | O(n.max_n) |
| PNI | O(n) |
| Pattern index | O(n) (only repeats) |
| Co-occurrence graph | O(\|V\| + \|E\|) |

---

## 9. Key Mathematical Insights

### 1. N-gram as Sliding Window

```text
G_n(T) = {T[i:i+n] | 0 <= i <= |T|-n}

Mathematical property:
  |G_n(T)| = |T| - n + 1 (linear in |T|)
```
