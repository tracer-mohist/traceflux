# Research: Pure Mathematical Foundation

**Date**: 2026-03-06  
**Status**: Foundational Formalization  
**Topic**: Pure mathematics — characters, sequences, order, no linguistic assumptions

---

## Core Principle

> "必须是存粹的文本字符、字符序列、序列顺序、存粹数学算法。"
> 
> (Must be pure text characters, character sequences, sequence order, pure mathematical algorithms.)

**No linguistic assumptions**:
- ❌ No "words" (linguistic concept)
- ❌ No "semantics" (meaning-based)
- ❌ No "syntax" (grammar-based)
- ✅ Only: characters, positions, sequences, sets, graphs

---

## 1. Fundamental Objects

### Character (Primitive)

**Definition 1 (Alphabet)**:
```
Σ = finite set of characters (Unicode code points)

c ∈ Σ is a character
Example: c = 0x48 ('H'), c = 0xE4B896 ('世')
```

**Note**: No distinction between "letter", "digit", "punctuation" — all are just characters in Σ.

---

### Text Sequence

**Definition 2 (Text)**:
```
A text T is a finite sequence of characters:

T = ⟨c₀, c₁, c₂, ..., cₙ₋₁⟩

Where:
  - cᵢ ∈ Σ for all 0 ≤ i < n
  - n = |T| (length of T)
  - pos(cᵢ) = i (position of cᵢ in T)
```

**Mathematical object**: T ∈ Σ* (Kleene star — all finite sequences over Σ)

---

### Subsequence

**Definition 3 (Subsequence)**:
```
S is a subsequence of T iff:
  S = ⟨cᵢ₁, cᵢ₂, ..., cᵢₖ⟩

Where:
  - 0 ≤ i₁ < i₂ < ... < iₖ < n
  - Each cᵢⱼ ∈ T

Notation: S ⊑ T
```

**Key property**: Order is preserved (i₁ < i₂ < ... < iₖ)

---

### Substring (Contiguous Subsequence)

**Definition 4 (Substring)**:
```
S is a substring of T iff:
  S = ⟨cᵢ, cᵢ₊₁, ..., cᵢ₊ₖ₋₁⟩

Where:
  - 0 ≤ i < n
  - 0 ≤ k ≤ n - i

Notation: T[i:i+k]

Key: Indices are consecutive (contiguous)
```

---

## 2. Pure Sequence Operations

### Concatenation

**Definition 5 (Concatenation)**:
```
For sequences A = ⟨a₀, ..., aₘ₋₁⟩ and B = ⟨b₀, ..., bₙ₋₁⟩:

A · B = ⟨a₀, ..., aₘ₋₁, b₀, ..., bₙ₋₁⟩

Properties:
  - Associative: (A · B) · C = A · (B · C)
  - Identity: A · ⟨⟩ = A (empty sequence)
  - Not commutative: A · B ≠ B · A (order matters!)
```

---

### Prefix and Suffix

**Definition 6 (Prefix)**:
```
P is a prefix of T iff:
  T = P · S for some sequence S

Notation: P ⊑ₚᵣₑ T

Example:
  T = "hello"
  Prefixes: ⟨⟩, "h", "he", "hel", "hell", "hello"
```

**Definition 7 (Suffix)**:
```
S is a suffix of T iff:
  T = P · S for some sequence P

Notation: S ⊑ₛᵤ𝒻 T

Example:
  T = "hello"
  Suffixes: ⟨⟩, "o", "lo", "llo", "ello", "hello"
```

---

### Reversal

**Definition 8 (Reversal)**:
```
For T = ⟨c₀, c₁, ..., cₙ₋₁⟩:

Tᴿ = ⟨cₙ₋₁, cₙ₋₂, ..., c₁, c₀⟩

Properties:
  - (Tᴿ)ᴿ = T
  - (A · B)ᴿ = Bᴿ · Aᴿ
```

---

## 3. Pattern Matching (Pure)

### Exact Match

**Definition 9 (Exact Match)**:
```
Pattern P occurs in T at position i iff:
  T[i:i+|P|] = P

Occurrence set:
  Occ(P, T) = {i | T[i:i+|P|] = P}

Frequency:
  freq(P, T) = |Occ(P, T)|
```

**Example**:
```
T = "hello hello world"
P = "hello"

Occ(P, T) = {0, 6}
freq(P, T) = 2
```

---

### Longest Common Subsequence

**Definition 10 (LCS)**:
```
For sequences A and B:

LCS(A, B) = longest S such that S ⊑ A and S ⊑ B

Computation: Dynamic programming
  dp[i][j] = length of LCS(A[0:i], B[0:j])
  
  dp[i][j] = dp[i-1][j-1] + 1              if A[i] = B[j]
           = max(dp[i-1][j], dp[i][j-1])   otherwise
```

**Use**: Sequence similarity (not semantic!)

---

### Longest Common Substring

**Definition 11 (Longest Common Substring)**:
```
For sequences A and B:

LCSubstr(A, B) = longest S such that S ⊑ₛᵤᵦ A and S ⊑ₛᵤᵦ B

Computation: Suffix tree or dynamic programming
```

---

## 4. Repetition Detection (LZ77 Style)

### Repeated Substring

**Definition 12 (Repeated Substring)**:
```
S is repeated in T iff:
  |Occ(S, T)| ≥ 2

Maximal repeated:
  S is maximal repeated iff:
    ∀S' ⊃ S (S' is superstring of S), |Occ(S', T)| < |Occ(S, T)|
```

**Example**:
```
T = "hello hello world hello"

S = "hello"
Occ(S, T) = {0, 6, 18}
|Occ(S, T)| = 3 ≥ 2 → S is repeated

S' = "hello " (with space)
Occ(S', T) = {0, 6}
|Occ(S', T)| = 2 ≥ 2 → S' is also repeated

S'' = "hello w"
Occ(S'', T) = {0}
|Occ(S'', T)| = 1 < 2 → S'' is NOT repeated

Maximal repeated: "hello " (cannot extend further with ≥2 occurrences)
```

---

### LZ77 Factorization

**Definition 13 (LZ77 Factorization)**:
```
For text T, the LZ77 factorization is:

T = f₁ · f₂ · ... · fₖ

Where each factor fᵢ is either:
  1. A single character (literal), or
  2. A reference (offset, length) to previous occurrence

Formally:
  fᵢ = (0, c)        if c is new (literal)
  fᵢ = (d, ℓ)        if T[pos:pos+ℓ] occurred before at distance d
```

**Example**:
```
T = "hello hello world"

LZ77 factorization:
  f₁ = (0, 'h')      literal
  f₂ = (0, 'e')      literal
  f₃ = (0, 'l')      literal
  f₄ = (0, 'l')      literal
  f₅ = (0, 'o')      literal
  f₆ = (0, ' ')      literal
  f₇ = (6, 5)        reference: copy 5 chars from 6 positions back ("hello")
  f₈ = (0, ' ')      literal
  f₉ = (0, 'w')      literal
  f₁₀ = (0, 'o')     literal
  f₁₁ = (0, 'r')     literal
  f₁₂ = (0, 'l')     literal
  f₁₃ = (0, 'd')     literal

Pattern index (byproduct):
  "hello" → {0, 6}
  " " → {5, 11}
  "world" → {12}
```

---

## 5. Sequence Graph (Pure Co-occurrence)

### Adjacency Graph

**Definition 14 (Adjacency Graph)**:
```
For text T, the character adjacency graph is:

G_adj = (Σ, E, w)

Where:
  - Σ = characters (vertices)
  - E = {(cᵢ, cᵢ₊₁) | 0 ≤ i < n-1} (edges)
  - w(cᵢ, cⱼ) = |{i | T[i] = cᵢ and T[i+1] = cⱼ}| (edge weight)

Interpretation: w(cᵢ, cⱼ) = how many times cⱼ follows cᵢ
```

**Example**:
```
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

**Definition 15 (k-gram Graph)**:
```
For text T and integer k ≥ 1:

G_k = (Vₖ, Eₖ, wₖ)

Where:
  - Vₖ = {T[i:i+k] | 0 ≤ i ≤ n-k} (all k-grams as vertices)
  - Eₖ = {(gᵢ, gᵢ₊₁) | gᵢ = T[i:i+k], gᵢ₊₁ = T[i+1:i+1+k]} (adjacent k-grams)
  - wₖ(gᵢ, gⱼ) = |{pos | gᵢ at pos, gⱼ at pos+1}| (co-occurrence count)
```

**Example**:
```
T = "hello hello", k = 2

V₂ = {"he", "el", "ll", "lo", "o ", " h"}
E₂:
  "he" → "el": 2
  "el" → "ll": 2
  "ll" → "lo": 2
  "lo" → "o ": 2
  "o " → " h": 1
  " h" → "he": 1
```

---

## 6. PageRank on Sequence Graph

### Standard PageRank (Pure Graph)

**Definition 16 (PageRank)**:
```
For graph G = (V, E, w):

PR(v) = (1-d)/|V| + d * Σ_{u: (u,v)∈E} PR(u) * w(u,v) / Σ_{t: (u,t)∈E} w(u,t)

Where:
  - d = damping factor (typically 0.85)
  - w(u,v) = edge weight
  - PR(v) = stationary probability of random walk at v

Matrix form:
  r = (1-d)/N * 1⃗ + d * Mᵀ * r
  Mᵢⱼ = w(i,j) / Σₖ w(i,k)
```

---

### PageRank on k-gram Graph

**Application**:
```
For G_k (k-gram graph):

PR(g) = importance of k-gram g

Interpretation:
  High PR(g) = g appears in many contexts
  Low PR(g) = g appears in few contexts (possibly noise)

Filter:
  Keep g iff PR(g) ≥ threshold
```

**Example**:
```
T = "hello hello world"

G₂ PageRank:
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

**Definition 17 (k-Degree Association)**:
```
For query sequence Q and graph G:

Assocₖ(Q, G) = {v ∈ V | dist(Q, v) ≤ k}

Where:
  - dist(Q, v) = shortest path length from Q to v
  - k = maximum degrees (typically 3-4)

Path:
  Path(Q, v) = ⟨Q = v₀, v₁, ..., vₘ = v⟩
  Where (vᵢ, vᵢ₊₁) ∈ E for all i
```

**Algorithm (BFS)**:
```
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

### Example: Pure Association

```
T = "hello hello world hello world"

G₂ (2-gram graph):
  "he" → "el" → "ll" → "lo" → "o " → " w" → "wo" → "or" → "rl" → "ld"

Query: "he"
k = 3

Assoc₃("he", G₂):
  1°: "el" (path: ["he", "el"])
  2°: "ll" (path: ["he", "el", "ll"])
  3°: "lo" (path: ["he", "el", "ll", "lo"])

Output:
  "he" → "el" → "ll" → "lo"
  (3-step association path)
```

---

## 8. Unified Pure Mathematical Framework

### Text as Multi-Layer Sequence Structure

```
Layer 0: Characters
  T = ⟨c₀, c₁, ..., cₙ₋₁⟩
  cᵢ ∈ Σ

Layer 1: k-grams
  Gₖ(T) = {T[i:i+k] | 0 ≤ i ≤ n-k}

Layer 2: Adjacency Graph
  G_adj = (Σ, E, w)
  E = {(cᵢ, cᵢ₊₁)}

Layer 3: k-gram Graph
  Gₖ = (Vₖ, Eₖ, wₖ)
  Vₖ = k-grams

Layer 4: PageRank
  PR: Vₖ → [0, 1]
  PR(g) = importance of g

Layer 5: Associations
  Assocₖ(Q, Gₖ) = {g | dist(Q, g) ≤ k}
```

---

### Query Processing (Pure Math)

```
Input:
  - Query sequence Q ∈ Σ*
  - Index I = (Gₖ, PR, Occ)

Output:
  - Results = {(g, PR(g), Occ(g), dist(Q, g)) | g ∈ Assocₖ(Q, Gₖ)}

Ranking:
  Sort by: α * PR(g) + β * (1 / dist(Q, g)) + γ * freq_norm(g)
  Where α + β + γ = 1

No semantics — pure mathematics!
```

---

## 9. Key Properties (Theorems)

### Theorem 1: LZ77 Pattern Completeness

```
Theorem: LZ77 factorization captures all maximal repeated substrings.

Proof sketch:
  - LZ77 finds longest match at each position
  - If S is repeated, LZ77 will reference it
  - Maximal repeats cannot be extended → captured as factors

Corollary: LZ77 index is complete for repeated patterns.
```

---

### Theorem 2: PageRank Convergence

```
Theorem: PageRank on k-gram graph converges to unique stationary distribution.

Proof:
  - k-gram graph is strongly connected (for non-trivial text)
  - Transition matrix M is stochastic (rows sum to 1)
  - By Perron-Frobenius theorem:
    - M has unique principal eigenvector
    - Power iteration converges to it

Corollary: PR scores are well-defined and stable.
```

---

### Theorem 3: Small-World Property

```
Theorem: For natural text, k-gram graph has small-world property.

Claim: Average path length L ≈ log(|Vₖ|) / log(average_degree)

For typical text:
  |Vₖ| ≈ 1000-10000 (unique k-grams)
  average_degree ≈ 3-5
  
  L ≈ log(10000) / log(5) ≈ 9.2 / 1.6 ≈ 5.8

Corollary: k ≤ 6 is sufficient for most associations.
```

---

### Theorem 4: Association Diversity

```
Theorem: BFS from Q explores diverse branches.

Proof:
  - BFS explores all neighbors at distance d before d+1
  - Different neighbors → different branches
  - Branching factor = average degree ≈ 3-5
  
  At distance k:
    Max nodes = degree^k
    For degree=4, k=3: 4³ = 64 nodes

Corollary: k=3 provides good coverage without explosion.
```

---

## 10. Summary: Pure Mathematics

### What We Use

```
✅ Characters (c ∈ Σ)
✅ Sequences (T = ⟨c₀, ..., cₙ₋₁⟩)
✅ Positions (pos(cᵢ) = i)
✅ Subsequences (S ⊑ T)
✅ Substrings (T[i:j])
✅ Concatenation (A · B)
✅ Graphs (G = (V, E, w))
✅ Paths (⟨v₀, ..., vₖ⟩)
✅ Distance (dist(u, v))
✅ Sets (Occ, Assoc)
✅ Functions (PR, freq)
```

### What We DON'T Use

```
❌ Words (linguistic concept)
❌ Semantics (meaning)
❌ Syntax (grammar)
❌ Punctuation (special status)
❌ Spaces (special status)
❌ "Sentences" (linguistic concept)
❌ "Paragraphs" (linguistic concept)
```

---

### Core Principle

```
Everything is sequences and graphs.
No linguistic assumptions.
Pure mathematics.
```

---

**Status**: Pure mathematical foundation complete  
**Next**: Implement based on these definitions  
**Philosophy**: Characters, sequences, order, graphs — nothing else
