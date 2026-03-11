### Example: Pure Association

```text
T = "hello hello world hello world"

G_2 (2-gram graph):
  "he" -> "el" -> "ll" -> "lo" -> "o " -> " w" -> "wo" -> "or" -> "rl" -> "ld"

Query: "he"
k = 3

Assoc_3("he", G_2):
  1deg: "el" (path: ["he", "el"])
  2deg: "ll" (path: ["he", "el", "ll"])
  3deg: "lo" (path: ["he", "el", "ll", "lo"])

Output:
  "he" -> "el" -> "ll" -> "lo"
  (3-step association path)
```

---

## 8. Unified Pure Mathematical Framework

### Text as Multi-Layer Sequence Structure

```text
Layer 0: Characters
  T = ⟨c_0, c_1, ..., c_n_-_1⟩
  cᵢ IN SIGMA

Layer 1: k-grams
  G_k(T) = {T[i:i+k] | 0 <= i <= n-k}

Layer 2: Adjacency Graph
  G_adj = (SIGMA, E, w)
  E = {(cᵢ, cᵢ_+_1)}

Layer 3: k-gram Graph
  G_k = (V_k, E_k, w_k)
  V_k = k-grams

Layer 4: PageRank
  PR: V_k -> [0, 1]
  PR(g) = importance of g

Layer 5: Associations
  Assoc_k(Q, G_k) = {g | dist(Q, g) <= k}
```

---

### Query Processing (Pure Math)

```text
Input:
  - Query sequence Q IN SIGMA*
  - Index I = (G_k, PR, Occ)

Output:
  - Results = {(g, PR(g), Occ(g), dist(Q, g)) | g IN Assoc_k(Q, G_k)}

Ranking:
  Sort by: α * PR(g) + β * (1 / dist(Q, g)) + γ * freq_norm(g)
  Where α + β + γ = 1

No semantics -- pure mathematics!
```

---

## 9. Key Properties (Theorems)

### Theorem 1: LZ77 Pattern Completeness

```text
Theorem: LZ77 factorization captures all maximal repeated substrings.

Proof sketch:
  - LZ77 finds longest match at each position
  - If S is repeated, LZ77 will reference it
  - Maximal repeats cannot be extended -> captured as factors

Corollary: LZ77 index is complete for repeated patterns.
```

---

### Theorem 2: PageRank Convergence

```text
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

```text
Theorem: For natural text, k-gram graph has small-world property.

Claim: Average path length L ≈ log(|V_k|) / log(average_degree)

For typical text:
  |V_k| ≈ 1000-10000 (unique k-grams)
  average_degree ≈ 3-5

  L ≈ log(10000) / log(5) ≈ 9.2 / 1.6 ≈ 5.8

Corollary: k <= 6 is sufficient for most associations.
```

---

### Theorem 4: Association Diversity

```text
Theorem: BFS from Q explores diverse branches.

Proof:
  - BFS explores all neighbors at distance d before d+1
  - Different neighbors -> different branches
  - Branching factor = average degree ≈ 3-5

  At distance k:
    Max nodes = degree^k
    For degree=4, k=3: 4^3 = 64 nodes

Corollary: k=3 provides good coverage without explosion.
```

---

## 10. Summary: Pure Mathematics

### What We Use

```text
 Characters (c IN SIGMA)
 Sequences (T = ⟨c_0, ..., c_n_-_1⟩)
 Positions (pos(cᵢ) = i)
 Subsequences (S ⊑ T)
 Substrings (T[i:j])
 Concatenation (A . B)
 Graphs (G = (V, E, w))
 Paths (⟨v_0, ..., v_k⟩)
 Distance (dist(u, v))
 Sets (Occ, Assoc)
 Functions (PR, freq)
```

### What We DON'T Use

```text
 Words (linguistic concept)
 Semantics (meaning)
 Syntax (grammar)
 Punctuation (special status)
 Spaces (special status)
 "Sentences" (linguistic concept)
 "Paragraphs" (linguistic concept)
```

---

### Core Principle

```text
Everything is sequences and graphs.
No linguistic assumptions.
Pure mathematics.
```

---

STATUS: Pure mathematical foundation complete
NEXT: Implement based on these definitions
PHILOSOPHY: Characters, sequences, order, graphs -- nothing else
