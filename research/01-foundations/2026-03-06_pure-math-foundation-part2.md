## 4. Repetition Detection (LZ77 Style)

### Repeated Substring

DEFINITION-12-(REPEATED-SUBSTRING):
```text
S is repeated in T iff:
  |Occ(S, T)| >= 2

Maximal repeated:
  S is maximal repeated iff:
    ∀S' SUPERSET S (S' is superstring of S), |Occ(S', T)| < |Occ(S, T)|
```

EXAMPLE:
```text
T = "hello hello world hello"

S = "hello"
Occ(S, T) = {0, 6, 18}
|Occ(S, T)| = 3 >= 2 -> S is repeated

S' = "hello " (with space)
Occ(S', T) = {0, 6}
|Occ(S', T)| = 2 >= 2 -> S' is also repeated

S'' = "hello w"
Occ(S'', T) = {0}
|Occ(S'', T)| = 1 < 2 -> S'' is NOT repeated

Maximal repeated: "hello " (cannot extend further with >=2 occurrences)
```

---

### LZ77 Factorization

DEFINITION-13-(LZ77-FACTORIZATION):
```text
For text T, the LZ77 factorization is:

T = f_1 . f_2 . ... . f_k

Where each factor fᵢ is either:
  1. A single character (literal), or
  2. A reference (offset, length) to previous occurrence

Formally:
  fᵢ = (0, c)        if c is new (literal)
  fᵢ = (d, ℓ)        if T[pos:pos+ℓ] occurred before at distance d
```

EXAMPLE:
```text
T = "hello hello world"

LZ77 factorization:
  f_1 = (0, 'h')      literal
  f_2 = (0, 'e')      literal
  f_3 = (0, 'l')      literal
  f_4 = (0, 'l')      literal
  f_5 = (0, 'o')      literal
  f_6 = (0, ' ')      literal
  f_7 = (6, 5)        reference: copy 5 chars from 6 positions back ("hello")
  f_8 = (0, ' ')      literal
  f_9 = (0, 'w')      literal
  f_1_0 = (0, 'o')     literal
  f_1_1 = (0, 'r')     literal
  f_1_2 = (0, 'l')     literal
  f_1_3 = (0, 'd')     literal

Pattern index (byproduct):
  "hello" -> {0, 6}
  " " -> {5, 11}
  "world" -> {12}
```

---

## 5. Sequence Graph (Pure Co-occurrence)

### Adjacency Graph

DEFINITION-14-(ADJACENCY-GRAPH):
```text
For text T, the character adjacency graph is:

G_adj = (SIGMA, E, w)

Where:
  - SIGMA = characters (vertices)
  - E = {(cᵢ, cᵢ_+_1) | 0 <= i < n-1} (edges)
  - w(cᵢ, cⱼ) = |{i | T[i] = cᵢ and T[i+1] = cⱼ}| (edge weight)

Interpretation: w(cᵢ, cⱼ) = how many times cⱼ follows cᵢ
```

EXAMPLE:
```text
T = "hello"

G_adj:
  Vertices: {h, e, l, o}
  Edges:
    (h, e): 1
    (e, l): 1
    (l, l): 1
    (l, o): 1
```

---

### k-gram Graph

DEFINITION-15-(K-GRAM-GRAPH):
```text
For text T and integer k >= 1:

G_k = (V_k, E_k, w_k)

Where:
  - V_k = {T[i:i+k] | 0 <= i <= n-k} (all k-grams as vertices)
  - E_k = {(gᵢ, gᵢ_+_1) | gᵢ = T[i:i+k], gᵢ_+_1 = T[i+1:i+1+k]} (adjacent k-grams)
  - w_k(gᵢ, gⱼ) = |{pos | gᵢ at pos, gⱼ at pos+1}| (co-occurrence count)
```

EXAMPLE:
```text
T = "hello hello", k = 2

V_2 = {"he", "el", "ll", "lo", "o ", " h"}
E_2:
  "he" -> "el": 2
  "el" -> "ll": 2
  "ll" -> "lo": 2
  "lo" -> "o ": 2
  "o " -> " h": 1
  " h" -> "he": 1
```

---

## 6. PageRank on Sequence Graph

### Standard PageRank (Pure Graph)

DEFINITION-16-(PAGERANK):
```text
For graph G = (V, E, w):

PR(v) = (1-d)/|V| + d * SIGMA_{u: (u,v)INE} PR(u) * w(u,v) / SIGMA_{t: (u,t)INE} w(u,t)

Where:
  - d = damping factor (typically 0.85)
  - w(u,v) = edge weight
  - PR(v) = stationary probability of random walk at v

Matrix form:
  r = (1-d)/N * 1⃗ + d * Mᵀ * r
  Mᵢⱼ = w(i,j) / SIGMA_k w(i,k)
```

---

### PageRank on k-gram Graph

APPLICATION:
```text
For G_k (k-gram graph):

PR(g) = importance of k-gram g

Interpretation:
  High PR(g) = g appears in many contexts
  Low PR(g) = g appears in few contexts (possibly noise)

Filter:
  Keep g iff PR(g) >= threshold
```

EXAMPLE:
```text
T = "hello hello world"

G_2 PageRank:
  PR("he") = 0.25
  PR("el") = 0.25
  PR("ll") = 0.25
  PR("lo") = 0.15
  PR("o ") = 0.05
  PR(" w") = 0.03
  PR("wo") = 0.02

Filter (threshold = 0.1):
  Keep: "he", "el", "ll", "lo"
  Discard: "o ", " w", "wo" (low rank, possibly noise)
```

---

## 7. Association Discovery (Pure BFS)

### k-Degree Association

DEFINITION-17-(K-DEGREE-ASSOCIATION):
```text
For query sequence Q and graph G:

Assoc_k(Q, G) = {v IN V | dist(Q, v) <= k}

Where:
  - dist(Q, v) = shortest path length from Q to v
  - k = maximum degrees (typically 3-4)

Path:
  Path(Q, v) = ⟨Q = v_0, v_1, ..., vₘ = v⟩
  Where (vᵢ, vᵢ_+_1) IN E for all i
```

ALGORITHM-(BFS):
```text
BFS(G, Q, k):
  visited = {Q}
  queue = [(Q, 0, [Q])]  // (node, degree, path)
  results = []

  while queue not empty:
    (v, deg, path) = dequeue()
    if deg >= k: continue

    for (v, neighbor) in E:
      if neighbor not in visited:
        visited.add(neighbor)
        new_path = path + [neighbor]
        results.append((neighbor, deg+1, new_path))
        enqueue((neighbor, deg+1, new_path))

  return results
```

---
