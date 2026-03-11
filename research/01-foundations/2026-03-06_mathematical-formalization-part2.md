### Punctuation Context Pair

DEFINITION-10-(CONTEXT-PAIR):
```text
For segment sᵢ at position [start, end):

context(sᵢ) = (pre, post)

Where:
  - pre = T[start-1] if start > 0, else ⊥ (START marker)
  - post = T[end] if end < |T|, else ⊤ (END marker)
```

EXAMPLE:
```text
T = "hello, world!"

s_0 = "hello" at [0, 5):
  context(s_0) = (⊥, ',')

s_1 = " world" at [6, 12):
  context(s_1) = (',', '!')
```

---

### PNI Index

DEFINITION-11-(PUNCTUATION-NAMESPACE-INDEX):
```text
PNI: (Context Pair) -> 𝒫(Segment x DocID x Position)

PNI(pre, post) = {(s, d, pos) | context(s) = (pre, post), s IN Tₔ at pos}
```

EXAMPLE:
```text
Corpus:
  T_1 = "hello, world!"
  T_2 = "hi, world!"

PNI(⊥, ',') = {
  ("hello", 1, 0),
  ("hi", 2, 0)
}

PNI(',', '!') = {
  (" world", 1, 6),
  (" world", 2, 3)
}
```

---

### Context Pair Hash

DEFINITION-12-(CONTEXT-HASH):
```text
hash: (Context Pair) -> ℕ

hash(pre, post) = some deterministic function

Properties:
  - hash(pre_1, post_1) = hash(pre_2, post_2) iff (pre_1, post_1) = (pre_2, post_2)
  - Used for O(1) lookup in PNI
```

---

## 4. LZ77 Pattern Detection Mathematical Model

### Repeated Substring

DEFINITION-13-(REPEATED-SUBSTRING):
```text
A substring s is repeated in T if:
  |{pos | T[pos:pos+|s|] = s}| >= 2

Let Occ(s, T) = {pos | T[pos:pos+|s|] = s} be the occurrence set.

s is repeated iff |Occ(s, T)| >= 2
```

EXAMPLE:
```text
T = "hello hello world"

s = "hello"
Occ(s, T) = {0, 6}
|Occ(s, T)| = 2 >= 2 -> s is repeated

s = "world"
Occ(s, T) = {12}
|Occ(s, T)| = 1 < 2 -> s is NOT repeated
```

---

### Maximal Repeated Substring

DEFINITION-14-(MAXIMAL-REPEATED-SUBSTRING):
```text
A repeated substring s is maximal if:
  ∀s' SUPERSET s (s' is a superstring of s), |Occ(s', T)| < |Occ(s, T)|

In other words: cannot extend s without reducing occurrences.
```

EXAMPLE:
```text
T = "hello hello world hello"

s = "hello"
Occ(s, T) = {0, 6, 18}

s' = "hello " (with space)
Occ(s', T) = {0, 6}  // "hello " at 0 and 6, but not at 18 (end of string)

s is NOT maximal (can extend to "hello" and still have 2+ occurrences)

s'' = " hello" (with leading space)
Occ(s'', T) = {5, 17}
s'' is maximal (cannot extend further)
```

---

### Pattern Index (LZ-Style)

DEFINITION-15-(PATTERN-INDEX):
```text
For corpus C = {T_1, ..., Tₘ}:

PI: Pattern -> 𝒫(DocID x Positions)

PI(p) = {(d, Occ(p, Tₔ)) | |Occ(p, Tₔ)| >= 1}

Filter: Only include patterns with |Occ(p, C)| >= min_support
```

EXAMPLE:
```text
C = {
  T_1 = "proxy configuration",
  T_2 = "proxy settings",
  T_3 = "proxy configuration"
}

PI("proxy") = {
  (1, {0}),
  (2, {0}),
  (3, {0})
}

PI(" configuration") = {
  (1, {6}),
  (3, {6})
}
```

---

## 5. PageRank Mathematical Model

### Graph Representation

DEFINITION-16-(CO-OCCURRENCE-GRAPH):
```text
G = (V, E, w)

Where:
  - V = {patterns} (vertices)
  - E ⊆ V x V (edges)
  - w: E -> ℕ (edge weight = co-occurrence count)

Edge exists: (u, v) IN E iff u and v co-occur in some document
```

EXAMPLE:
```text
Patterns: {"proxy", "config", "settings"}

Co-occurrences:
  "proxy" & "config": 10 times
  "proxy" & "settings": 8 times
  "config" & "settings": 6 times

G = (
  V = {"proxy", "config", "settings"},
  E = {("proxy","config"), ("proxy","settings"), ("config","settings")},
  w("proxy","config") = 10,
  w("proxy","settings") = 8,
  w("config","settings") = 6
)
```

---

### PageRank Formula

DEFINITION-17-(PAGERANK):
```text
For graph G = (V, E):

PR(v) = (1-d)/|V| + d * SIGMA_{u: (u,v)INE} PR(u) / out_degree(u)

Where:
  - d = damping factor (typically 0.85)
  - out_degree(u) = |{v | (u,v) IN E}|
  - PR(v) = stationary probability of random walk at v
```

MATRIX-FORM:
```text
Let M be the transition matrix:
  Mᵢⱼ = 1/out_degree(i) if (i,j) IN E, else 0

PageRank vector r:
  r = (1-d)/|V| * 1⃗ + d * Mᵀ * r

Solution: r = (1-d)/|V| * (I - d*Mᵀ)^-^1 * 1⃗
```

---
