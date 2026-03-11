# Mathematical Model

Purpose: Formal mathematical foundation for TraceFlux algorithms.

NOTE: Consolidated from research/01-foundations/ (2026-03-11)

---

## Goal

Express all algorithms in pure mathematics using:
- Set theory
- Graph theory
- Information theory

---

## Fundamental Definitions

### Text as Sequence

Definition 1 (Text Sequence):

A text T is a finite sequence of characters:
  T = <c_0, c_1, c_2, ..., c_{n-1}>

Where:
  - c_i in Sigma (alphabet, e.g., Unicode)
  - n = |T| (length of T)
  - pos(c_i) = i (position of character c_i)

Example:

T = "hello"
T = <'h', 'e', 'l', 'l', 'o'>
|T| = 5
pos('h') = 0, pos('e') = 1, ..., pos('o') = 4

---

## Substring and Subsequence

Definition 2 (Substring):

A substring of T from position i to j (inclusive):
  T[i:j] = <c_i, c_{i+1}, ..., c_j>

Where 0 <= i <= j < n

Definition 3 (Subsequence):

A subsequence S of T:
  S = <c_{i_1}, c_{i_2}, ..., c_{i_k}>

Where 0 <= i_1 < i_2 < ... < i_k < n

Key Difference:
- Substring: contiguous (sliding window)
- Subsequence: not necessarily contiguous (can skip characters)

---

## Punctuation Set

Definition 4 (Punctuation Set):

Let P subset Sigma be the set of punctuation characters.

P = {c in Sigma | c is punctuation}

Examples:
  P includes: , . ! ? ; : " ' ( ) [ ] { } ...
  P excludes: a-z, A-Z, 0-9, Unicode letters

Complement:
  Let R = Sigma \ P be the set of readable characters.

---

## N-gram Mathematical Model

### Definition

Definition 5 (N-gram):

The set of n-grams of text T:
  G_n(T) = {T[i:i+n] | 0 <= i <= |T| - n}

Cardinality:
  |G_n(T)| = |T| - n + 1

Example:

T = "hello", n = 2

G_2(T) = {"he", "el", "ll", "lo"}
|G_2(T)| = 5 - 2 + 1 = 4

---

## N-gram Frequency

Definition 6 (N-gram Frequency):

For a corpus C = {T_1, T_2, ..., T_m}:

freq(g, C) = sum |{i | G_n(T_j)[i] = g}|
              j=1 to m

Normalized frequency:
  freq_norm(g, C) = freq(g, C) / |C|

---

## Punctuation Segmentation Model

### Definition

Definition 7 (Punctuation Segmentation):

Given text T and punctuation set P:

A segmentation S(T, P) is a sequence of segments:
  S(T, P) = [s_1, s_2, ..., s_k]

Where each segment s_i = (content_i, pre_i, post_i):
  - content_i in R* (readable characters)
  - pre_i in P union {START}
  - post_i in P union {END}

And:
  T = pre_1 + content_1 + post_1 + pre_2 + content_2 + ... + post_k

Example:

T = "Hello, world!"
P = {',', '!', '.', '?'}

S(T, P) = [
  ("Hello", START, ','),
  (" world", ',', '!')
]

---

## Type Identifier

Definition 8 (Segment Type):

The type of segment s = (content, pre, post):
  type(s) = hash(pre, post)

Where hash: (P union {START}) x (P union {END}) -> N

This groups segments by punctuation context.

---

## PageRank Model

### Definition

Definition 9 (Co-occurrence Graph):

Given corpus C and pattern set G:

Co-occurrence graph G = (V, E):
  - V = G (patterns as nodes)
  - E = {(g_i, g_j) | g_i and g_j co-occur in same document}
  - w(g_i, g_j) = frequency of co-occurrence

Definition 10 (PageRank):

For pattern g in V:

PR(g) = (1 - d) / N + d * sum(PR(h) / out_degree(h))
                               h in In(g)

Where:
  - d = damping factor (0.85)
  - N = |V| (total patterns)
  - In(g) = patterns linking to g

---

## Combined Scoring Model

### Definition

Definition 11 (Pattern Score):

For pattern p in corpus C:

score(p) = alpha * freq_norm(p) + beta * PR(p) + gamma * pos_weight(p)

Where:
  - alpha + beta + gamma = 1 (weights sum to 1)
  - freq_norm(p) in [0, 1] (normalized frequency)
  - PR(p) in [0, 1] (PageRank score)
  - pos_weight(p) in [0, 1] (position weight)

### Position Weight

pos_weight(p) =
  1.0  if p appears at start of text
  0.8  if p appears at end of text
  0.5  otherwise

---

## See Also

- [Proofs and Properties](./mathematical-proofs.md) - Formal proofs
- [Information Theory](./mathematical-proofs.md#information-theory) - Entropy and applications
- [Text Segmentation](./text-segmentation.md) - Punctuation segmentation
- [N-gram Analysis](./ngram-analysis.md) - Pattern extraction
- [Frequency Ranking](./frequency-ranking.md) - Scoring and weighting

---

Last Updated: 2026-03-11
Source Files: 2026-03-06_mathematical-formalization*.md
