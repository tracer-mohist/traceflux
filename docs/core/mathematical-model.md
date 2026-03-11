# Mathematical Model

**Purpose**: Formal mathematical foundation for TraceFlux algorithms.

**NOTE**: Consolidated from research/01-foundations/ (2026-03-11)

---

## Goal

Express all algorithms in pure mathematics using:
- Set theory
- Graph theory
- Information theory

---

## Fundamental Definitions

### Text as Sequence

**Definition 1 (Text Sequence)**:

```text
A text T is a finite sequence of characters:
  T = ⟨c_0, c_1, c_2, ..., c_{n-1}⟩

Where:
  - c_i ∈ Σ (alphabet, e.g., Unicode)
  - n = |T| (length of T)
  - pos(c_i) = i (position of character c_i)
```

**Example**:

```text
T = "hello"
T = ⟨'h', 'e', 'l', 'l', 'o'⟩
|T| = 5
pos('h') = 0, pos('e') = 1, ..., pos('o') = 4
```

---

### Substring and Subsequence

**Definition 2 (Substring)**:

```text
A substring of T from position i to j (inclusive):
  T[i:j] = ⟨c_i, c_{i+1}, ..., c_j⟩

Where 0 ≤ i ≤ j < n
```

**Definition 3 (Subsequence)**:

```text
A subsequence S of T:
  S = ⟨c_{i_1}, c_{i_2}, ..., c_{i_k}⟩

Where 0 ≤ i_1 < i_2 < ... < i_k < n
```

**Key Difference**:
- Substring: contiguous (sliding window)
- Subsequence: not necessarily contiguous (can skip characters)

---

### Punctuation Set

**Definition 4 (Punctuation Set)**:

```text
Let P ⊂ Σ be the set of punctuation characters.

P = {c ∈ Σ | c is punctuation}

Examples:
  P includes: , . ! ? ; : " ' ( ) [ ] { } ...
  P excludes: a-z, A-Z, 0-9, Unicode letters

Complement:
  Let R = Σ \ P be the set of readable characters.
```

---

## N-gram Mathematical Model

### Definition

**Definition 5 (N-gram)**:

```text
The set of n-grams of text T:
  G_n(T) = {T[i:i+n] | 0 ≤ i ≤ |T| - n}

Cardinality:
  |G_n(T)| = |T| - n + 1
```

**Example**:

```text
T = "hello", n = 2

G_2(T) = {"he", "el", "ll", "lo"}
|G_2(T)| = 5 - 2 + 1 = 4
```

---

### N-gram Frequency

**Definition 6 (N-gram Frequency)**:

```text
For a corpus C = {T_1, T_2, ..., T_m}:

freq(g, C) = Σ |{i | G_n(T_j)[i] = g}|
              j=1 to m

Normalized frequency:
  freq_norm(g, C) = freq(g, C) / |C|
```

---

## Punctuation Segmentation Model

### Definition

**Definition 7 (Punctuation Segmentation)**:

```text
Given text T and punctuation set P:

A segmentation S(T, P) is a sequence of segments:
  S(T, P) = [s_1, s_2, ..., s_k]

Where each segment s_i = (content_i, pre_i, post_i):
  - content_i ∈ R* (readable characters)
  - pre_i ∈ P ∪ {START}
  - post_i ∈ P ∪ {END}

And:
  T = pre_1 + content_1 + post_1 + pre_2 + content_2 + ... + post_k
```

**Example**:

```text
T = "Hello, world!"
P = {',', '!', '.', '?'}

S(T, P) = [
  ("Hello", START, ','),
  (" world", ',', '!')
]
```

---

### Type Identifier

**Definition 8 (Segment Type)**:

```text
The type of segment s = (content, pre, post):
  type(s) = hash(pre, post)

Where hash: (P ∪ {START}) × (P ∪ {END}) → ℕ

This groups segments by punctuation context.
```

---

## PageRank Model

### Definition

**Definition 9 (Co-occurrence Graph)**:

```text
Given corpus C and pattern set G:

Co-occurrence graph G = (V, E):
  - V = G (patterns as nodes)
  - E = {(g_i, g_j) | g_i and g_j co-occur in same document}
  - w(g_i, g_j) = frequency of co-occurrence
```

**Definition 10 (PageRank)**:

```text
For pattern g ∈ V:

PR(g) = (1 - d) / N + d * Σ(PR(h) / out_degree(h))
                               h∈In(g)

Where:
  - d = damping factor (0.85)
  - N = |V| (total patterns)
  - In(g) = patterns linking to g
```

---

## Combined Scoring Model

### Definition

**Definition 11 (Pattern Score)**:

```text
For pattern p in corpus C:

score(p) = α * freq_norm(p) + β * PR(p) + γ * pos_weight(p)

Where:
  - α + β + γ = 1 (weights sum to 1)
  - freq_norm(p) ∈ [0, 1] (normalized frequency)
  - PR(p) ∈ [0, 1] (PageRank score)
  - pos_weight(p) ∈ [0, 1] (position weight)
```

### Position Weight

```text
pos_weight(p) =
  1.0  if p appears at start of text
  0.8  if p appears at end of text
  0.5  otherwise
```

---

## Information Theory

### Entropy

**Definition 12 (Pattern Entropy)**:

```text
For pattern distribution P over corpus C:

H(P) = -Σ p_i * log2(p_i)
        i

Where p_i = freq(pattern_i) / Σ freq(pattern_j)

Low entropy = concentrated distribution (few dominant patterns)
High entropy = uniform distribution (many equal patterns)
```

### Application

```text
Use entropy to:
  1. Measure corpus diversity
  2. Detect topic shifts (entropy changes)
  3. Optimize n-gram size (minimize entropy)
```

---

## Proofs and Properties

### Property 1: N-gram Completeness

**Theorem**: For any text T and any substring s of T, there exists n such that s ∈ G_n(T).

**Proof**: Let n = |s|. By definition of substring, s = T[i:i+n] for some i. Therefore s ∈ G_n(T). ∎

### Property 2: Frequency Monotonicity

**Theorem**: For patterns p1, p2 where p1 is a substring of p2: freq(p1, C) ≥ freq(p2, C).

**Proof**: Every occurrence of p2 contains an occurrence of p1. Therefore freq(p2) ≤ freq(p1). ∎

### Property 3: PageRank Convergence

**Theorem**: PageRank iteration converges to a unique stationary distribution for any strongly connected graph.

**Proof**: Standard PageRank convergence proof applies. The co-occurrence graph is strongly connected if all patterns co-occur transitively. ∎

---

## Related

- [Text Segmentation](./text-segmentation.md) - Punctuation segmentation
- [N-gram Analysis](./ngram-analysis.md) - Pattern extraction
- [Frequency Ranking](./frequency-ranking.md) - Scoring and weighting

---

**Last Updated**: 2026-03-11
**Source Files**: `2026-03-06_mathematical-formalization*.md`
