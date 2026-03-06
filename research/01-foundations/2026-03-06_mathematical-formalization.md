# Research: Mathematical Formalization

**Date**: 2026-03-06  
**Status**: Mathematical Model Design  
**Topic**: Unified mathematical framework for all algorithms

---

## Goal: Unified Mathematical Framework

Express all algorithms in pure mathematics:
- N-gram
- Punctuation Namespace Index (PNI)
- LZ77 pattern detection
- PageRank
- Six Degrees of Separation

**Language**: Set theory, Graph theory, Information theory

---

## 1. Fundamental Definitions

### Text as Sequence

**Definition 1 (Text Sequence)**:
```
A text T is a finite sequence of characters:
  T = ⟨c₀, c₁, c₂, ..., cₙ₋₁⟩

Where:
  - cᵢ ∈ Σ (alphabet, e.g., Unicode)
  - n = |T| (length of T)
  - pos(cᵢ) = i (position of character cᵢ)
```

**Example**:
```
T = "hello"
T = ⟨'h', 'e', 'l', 'l', 'o'⟩
|T| = 5
pos('h') = 0, pos('e') = 1, ..., pos('o') = 4
```

---

### Subsequence and Substring

**Definition 2 (Substring)**:
```
A substring of T from position i to j (inclusive):
  T[i:j] = ⟨cᵢ, cᵢ₊₁, ..., cⱼ⟩

Where 0 ≤ i ≤ j < n
```

**Definition 3 (Subsequence)**:
```
A subsequence S of T:
  S = ⟨cᵢ₁, cᵢ₂, ..., cᵢₖ⟩

Where 0 ≤ i₁ < i₂ < ... < iₖ < n
```

**Key Difference**:
- Substring: contiguous (连续)
- Subsequence: not necessarily contiguous (不连续)

---

### Punctuation Set

**Definition 4 (Punctuation Set)**:
```
Let P ⊂ Σ be the set of punctuation characters.

P = {c ∈ Σ | c is punctuation}

Examples:
  P includes: , . ! ? ; : " ' ( ) [ ] { } space tab newline ...
  P excludes: a-z, A-Z, 0-9, Unicode letters
```

**Complement**:
```
Let R = Σ \ P be the set of readable characters.
```

---

## 2. N-gram Mathematical Model

### Definition

**Definition 5 (N-gram)**:
```
The set of n-grams of text T:
  Gₙ(T) = {T[i:i+n] | 0 ≤ i ≤ |T| - n}

Cardinality:
  |Gₙ(T)| = |T| - n + 1
```

**Example**:
```
T = "hello", n = 2

G₂(T) = {"he", "el", "ll", "lo"}
|G₂(T)| = 5 - 2 + 1 = 4
```

---

### N-gram Index

**Definition 6 (N-gram Inverted Index)**:
```
For a corpus C = {T₁, T₂, ..., Tₘ}:

Iₙ: Gₙ(C) → 𝒫(D × ℕ)

Where:
  - Gₙ(C) = ⋃ᵢ Gₙ(Tᵢ) (all n-grams in corpus)
  - D = {1, 2, ..., m} (document IDs)
  - 𝒫 is power set
  - Iₙ(g) = {(d, pos) | g appears at pos in Tₔ}
```

**Example**:
```
C = {T₁="hello", T₂="hallo"}

I₂("ll") = {(1, 2), (2, 2)}  // "ll" at position 2 in both docs
I₂("he") = {(1, 0)}          // "he" only in T₁
I₂("ha") = {(2, 0)}          // "ha" only in T₂
```

---

### N-gram Similarity

**Definition 7 (Jaccard Similarity on N-grams)**:
```
For texts T₁, T₂:

simₙ(T₁, T₂) = |Gₙ(T₁) ∩ Gₙ(T₂)| / |Gₙ(T₁) ∪ Gₙ(T₂)|

Properties:
  - 0 ≤ simₙ(T₁, T₂) ≤ 1
  - simₙ(T₁, T₂) = 1 iff Gₙ(T₁) = Gₙ(T₂)
  - simₙ(T₁, T₂) = 0 iff Gₙ(T₁) ∩ Gₙ(T₂) = ∅
```

**Example**:
```
T₁ = "hello", T₂ = "hallo", n = 2

G₂(T₁) = {"he", "el", "ll", "lo"}
G₂(T₂) = {"ha", "al", "ll", "lo"}

G₂(T₁) ∩ G₂(T₂) = {"ll", "lo"}  (size 2)
G₂(T₁) ∪ G₂(T₂) = {"he", "el", "ll", "lo", "ha", "al"}  (size 6)

sim₂(T₁, T₂) = 2/6 = 1/3 ≈ 0.33
```

---

## 3. Punctuation Namespace Index (PNI) Mathematical Model

### Punctuation Segmentation

**Definition 8 (Punctuation Positions)**:
```
For text T, the set of punctuation positions:
  PPos(T) = {i | T[i] ∈ P, 0 ≤ i < |T|}

Ordered: PPos(T) = {p₀, p₁, ..., pₖ₋₁} where p₀ < p₁ < ... < pₖ₋₁
```

**Definition 9 (Segments)**:
```
Segments of T (split by punctuation):
  Seg(T) = {T[pᵢ₊₁:pᵢ₊₁] | 0 ≤ i < k-1}

Where:
  - p₋₁ = -1 (before start)
  - pₖ = |T| (after end)
  - Each segment sⱼ = T[pⱼ₋₁+1 : pⱼ]
```

**Example**:
```
T = "hello, world!"
P = {',', '!', ...}

PPos(T) = {5, 12}  // ',' at 5, '!' at 12

Seg(T) = {
  s₀ = T[0:5] = "hello",
  s₁ = T[6:12] = " world"
}
```

---

### Punctuation Context Pair

**Definition 10 (Context Pair)**:
```
For segment sᵢ at position [start, end):

context(sᵢ) = (pre, post)

Where:
  - pre = T[start-1] if start > 0, else ⊥ (START marker)
  - post = T[end] if end < |T|, else ⊤ (END marker)
```

**Example**:
```
T = "hello, world!"

s₀ = "hello" at [0, 5):
  context(s₀) = (⊥, ',')

s₁ = " world" at [6, 12):
  context(s₁) = (',', '!')
```

---

### PNI Index

**Definition 11 (Punctuation Namespace Index)**:
```
PNI: (Context Pair) → 𝒫(Segment × DocID × Position)

PNI(pre, post) = {(s, d, pos) | context(s) = (pre, post), s ∈ Tₔ at pos}
```

**Example**:
```
Corpus:
  T₁ = "hello, world!"
  T₂ = "hi, world!"

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

**Definition 12 (Context Hash)**:
```
hash: (Context Pair) → ℕ

hash(pre, post) = some deterministic function

Properties:
  - hash(pre₁, post₁) = hash(pre₂, post₂) iff (pre₁, post₁) = (pre₂, post₂)
  - Used for O(1) lookup in PNI
```

---

## 4. LZ77 Pattern Detection Mathematical Model

### Repeated Substring

**Definition 13 (Repeated Substring)**:
```
A substring s is repeated in T if:
  |{pos | T[pos:pos+|s|] = s}| ≥ 2

Let Occ(s, T) = {pos | T[pos:pos+|s|] = s} be the occurrence set.

s is repeated iff |Occ(s, T)| ≥ 2
```

**Example**:
```
T = "hello hello world"

s = "hello"
Occ(s, T) = {0, 6}
|Occ(s, T)| = 2 ≥ 2 → s is repeated

s = "world"
Occ(s, T) = {12}
|Occ(s, T)| = 1 < 2 → s is NOT repeated
```

---

### Maximal Repeated Substring

**Definition 14 (Maximal Repeated Substring)**:
```
A repeated substring s is maximal if:
  ∀s' ⊃ s (s' is a superstring of s), |Occ(s', T)| < |Occ(s, T)|

In other words: cannot extend s without reducing occurrences.
```

**Example**:
```
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

**Definition 15 (Pattern Index)**:
```
For corpus C = {T₁, ..., Tₘ}:

PI: Pattern → 𝒫(DocID × Positions)

PI(p) = {(d, Occ(p, Tₔ)) | |Occ(p, Tₔ)| ≥ 1}

Filter: Only include patterns with |Occ(p, C)| ≥ min_support
```

**Example**:
```
C = {
  T₁ = "proxy configuration",
  T₂ = "proxy settings",
  T₃ = "proxy configuration"
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

**Definition 16 (Co-occurrence Graph)**:
```
G = (V, E, w)

Where:
  - V = {patterns} (vertices)
  - E ⊆ V × V (edges)
  - w: E → ℕ (edge weight = co-occurrence count)

Edge exists: (u, v) ∈ E iff u and v co-occur in some document
```

**Example**:
```
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

**Definition 17 (PageRank)**:
```
For graph G = (V, E):

PR(v) = (1-d)/|V| + d * Σ_{u: (u,v)∈E} PR(u) / out_degree(u)

Where:
  - d = damping factor (typically 0.85)
  - out_degree(u) = |{v | (u,v) ∈ E}|
  - PR(v) = stationary probability of random walk at v
```

**Matrix Form**:
```
Let M be the transition matrix:
  Mᵢⱼ = 1/out_degree(i) if (i,j) ∈ E, else 0

PageRank vector r:
  r = (1-d)/|V| * 1⃗ + d * Mᵀ * r

Solution: r = (1-d)/|V| * (I - d*Mᵀ)⁻¹ * 1⃗
```

---

### PatternRank (Adapted for Text)

**Definition 18 (PatternRank)**:
```
For co-occurrence graph G:

Rank(p) = (1-d)/|V| + d * Σ_{q: (q,p)∈E} Rank(q) * w(q,p) / Σ_{r} w(q,r)

Where:
  - w(q,p) = co-occurrence count of q and p
  - Σ_{r} w(q,r) = total co-occurrences of q with all patterns
```

**Intuition**:
```
A pattern is important if:
  - Important patterns co-occur with it
  - Co-occurrence is frequent (high weight)
```

---

## 6. Six Degrees Mathematical Model

### Graph Distance

**Definition 19 (Path)**:
```
A path from u to v in graph G:
  Path(u, v) = ⟨v₀, v₁, ..., vₖ⟩

Where:
  - v₀ = u
  - vₖ = v
  - (vᵢ, vᵢ₊₁) ∈ E for all 0 ≤ i < k

Length: |Path| = k (number of edges)
```

**Definition 20 (Shortest Path Distance)**:
```
dist(u, v) = min{|Path(u, v)|}

If no path exists: dist(u, v) = ∞
```

---

### Average Path Length

**Definition 21 (Average Path Length)**:
```
For graph G with n vertices:

L = (1 / (n*(n-1))) * Σ_{u≠v} dist(u, v)

For small-world networks: L ≈ log(n) / log(k)

Where k = average degree
```

**Example**:
```
Social network:
  n = 7 billion (world population)
  k = 1000 (average person knows ~1000 people)
  
  L ≈ log(7×10⁹) / log(1000)
  L ≈ 22.8 / 3 ≈ 7.6

  → ~6-8 degrees (matches empirical findings!)
```

---

### Association Discovery via BFS

**Definition 22 (k-Degree Associations)**:
```
For query pattern q and graph G:

Assocₖ(q) = {p ∈ V | dist(q, p) ≤ k}

With paths:
  AssocPathsₖ(q) = {Path(q, p) | p ∈ Assocₖ(q)}
```

**Algorithm (BFS)**:
```
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

**Definition 23 (Text Multi-Layer)**:
```
Text T has multiple representations:

Layer 0 (Character): T = ⟨c₀, c₁, ..., cₙ₋₁⟩
Layer 1 (Segment): Seg(T) = {s₀, s₁, ..., sₘ}
Layer 2 (Pattern): Patterns(T) = {p₀, p₁, ..., pₖ}
Layer 3 (Graph): G = (Patterns, Co-occurrence)
```

**Mappings**:
```
φ₀₁: Layer 0 → Layer 1 (punctuation segmentation)
φ₁₂: Layer 1 → Layer 2 (pattern extraction)
φ₂₃: Layer 2 → Layer 3 (co-occurrence graph)
```

---

### Unified Index Structure

**Definition 24 (Unified Index)**:
```
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

**Definition 25 (Query Result)**:
```
For query q and index I:

Result(q, I) = {(p, score, path) | p ∈ Patterns}

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
| PageRank | Power iteration | O(k·\|E\|) |
| BFS (k-degree) | Breadth-first | O(k·dᵏ) |

Where:
- n = text length
- k = iterations / BFS depth
- d = average graph degree

---

### Space Complexity

| Structure | Space |
|-----------|-------|
| N-gram index | O(n·max_n) |
| PNI | O(n) |
| Pattern index | O(n) (only repeats) |
| Co-occurrence graph | O(\|V\| + \|E\|) |

---

## 9. Key Mathematical Insights

### 1. N-gram as Sliding Window

```
Gₙ(T) = {T[i:i+n] | 0 ≤ i ≤ |T|-n}

Mathematical property:
  |Gₙ(T)| = |T| - n + 1 (linear in |T|)
```

### 2. PNI as Partition

```
PNI partitions text by context pairs:
  ⋃_{(pre,post)} PNI(pre, post) = All segments
  PNI(pre₁, post₁) ∩ PNI(pre₂, post₂) = ∅ if (pre₁,post₁) ≠ (pre₂,post₂)

Mathematical property:
  PNI is a partition of segments (disjoint, complete)
```

### 3. LZ Patterns as Compression

```
Patterns = Maximal repeated substrings

Compression ratio:
  CR = |T| / |PI| (original size / indexed size)

Higher CR = more redundancy = better compression
```

### 4. PageRank as Eigenvector

```
PageRank r is principal eigenvector of Mᵀ:
  r = d * Mᵀ * r + (1-d)/|V| * 1⃗

Mathematical property:
  r exists and unique (Perron-Frobenius theorem)
```

### 5. Six Degrees as Graph Property

```
Small-world property:
  L ≈ log(n) / log(k)

For text co-occurrence graphs:
  n = number of patterns
  k = average co-occurrence degree
  
Expected: L ≈ 3-4 (short paths exist)
```

---

## 10. Summary: Unified View

```
Text T
  ↓ (φ₀₁: punctuation segmentation)
Segments with context pairs
  ↓ (φ₁₂: pattern extraction)
Patterns (maximal repeats)
  ↓ (φ₂₃: co-occurrence)
Graph G = (Patterns, Edges)
  ↓ (PageRank)
Importance scores
  ↓ (BFS)
Associations (k-degree)

All expressed in: Set theory, Graph theory, Linear algebra
```

---

**Status**: Mathematical formalization complete  
**Next**: Implement based on mathematical definitions  
**Philosophy**: Pure mathematics unifies all algorithms
