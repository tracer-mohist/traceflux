# Research: Mathematical Formalization

DATE: 2026-03-06
STATUS: Mathematical Model Design
TOPIC: Unified mathematical framework for all algorithms

---

## Goal: Unified Mathematical Framework

Express all algorithms in pure mathematics:
- N-gram
- Punctuation Namespace Index (PNI)
- LZ77 pattern detection
- PageRank
- Six Degrees of Separation

LANGUAGE: Set theory, Graph theory, Information theory

---

## 1. Fundamental Definitions

### Text as Sequence

DEFINITION-1-(TEXT-SEQUENCE):
```text
A text T is a finite sequence of characters:
  T = ⟨c_0, c_1, c_2, ..., c_n_-_1⟩

Where:
  - cᵢ IN SIGMA (alphabet, e.g., Unicode)
  - n = |T| (length of T)
  - pos(cᵢ) = i (position of character cᵢ)
```

EXAMPLE:
```text
T = "hello"
T = ⟨'h', 'e', 'l', 'l', 'o'⟩
|T| = 5
pos('h') = 0, pos('e') = 1, ..., pos('o') = 4
```

---

### Subsequence and Substring

DEFINITION-2-(SUBSTRING):
```text
A substring of T from position i to j (inclusive):
  T[i:j] = ⟨cᵢ, cᵢ_+_1, ..., cⱼ⟩

Where 0 <= i <= j < n
```

DEFINITION-3-(SUBSEQUENCE):
```text
A subsequence S of T:
  S = ⟨cᵢ_1, cᵢ_2, ..., cᵢ_k⟩

Where 0 <= i_1 < i_2 < ... < i_k < n
```

KEY-DIFFERENCE:
> - Substring: contiguous ()
> - Subsequence: not necessarily contiguous ()

---

### Punctuation Set

DEFINITION-4-(PUNCTUATION-SET):
```text
Let P SUBSET SIGMA be the set of punctuation characters.

P = {c IN SIGMA | c is punctuation}

Examples:
  P includes: , . ! ? ; : " ' ( ) [ ] { } space tab newline ...
  P excludes: a-z, A-Z, 0-9, Unicode letters
```

COMPLEMENT:
```text
Let R = SIGMA \ P be the set of readable characters.
```

---

## 2. N-gram Mathematical Model

### Definition

DEFINITION-5-(N-GRAM):
```text
The set of n-grams of text T:
  G_n(T) = {T[i:i+n] | 0 <= i <= |T| - n}

Cardinality:
  |G_n(T)| = |T| - n + 1
```

EXAMPLE:
```text
T = "hello", n = 2

G_2(T) = {"he", "el", "ll", "lo"}
|G_2(T)| = 5 - 2 + 1 = 4
```

---

### N-gram Index

DEFINITION-6-(N-GRAM-INVERTED-INDEX):
```text
For a corpus C = {T_1, T_2, ..., Tₘ}:

I_n: G_n(C) -> 𝒫(D x ℕ)

Where:
  - G_n(C) = ⋃ᵢ G_n(Tᵢ) (all n-grams in corpus)
  - D = {1, 2, ..., m} (document IDs)
  - 𝒫 is power set
  - I_n(g) = {(d, pos) | g appears at pos in Tₔ}
```

EXAMPLE:
```text
C = {T_1="hello", T_2="hallo"}

I_2("ll") = {(1, 2), (2, 2)}  // "ll" at position 2 in both docs
I_2("he") = {(1, 0)}          // "he" only in T_1
I_2("ha") = {(2, 0)}          // "ha" only in T_2
```

---

### N-gram Similarity

DEFINITION-7-(JACCARD-SIMILARITY-ON-N-GRAMS):
```text
For texts T_1, T_2:

sim_n(T_1, T_2) = |G_n(T_1) INTERSECT G_n(T_2)| / |G_n(T_1) UNION G_n(T_2)|

Properties:
  - 0 <= sim_n(T_1, T_2) <= 1
  - sim_n(T_1, T_2) = 1 iff G_n(T_1) = G_n(T_2)
  - sim_n(T_1, T_2) = 0 iff G_n(T_1) INTERSECT G_n(T_2) = ∅
```

EXAMPLE:
```text
T_1 = "hello", T_2 = "hallo", n = 2

G_2(T_1) = {"he", "el", "ll", "lo"}
G_2(T_2) = {"ha", "al", "ll", "lo"}

G_2(T_1) INTERSECT G_2(T_2) = {"ll", "lo"}  (size 2)
G_2(T_1) UNION G_2(T_2) = {"he", "el", "ll", "lo", "ha", "al"}  (size 6)

sim_2(T_1, T_2) = 2/6 = 1/3 ≈ 0.33
```

---

## 3. Punctuation Namespace Index (PNI) Mathematical Model

### Punctuation Segmentation

DEFINITION-8-(PUNCTUATION-POSITIONS):
```text
For text T, the set of punctuation positions:
  PPos(T) = {i | T[i] IN P, 0 <= i < |T|}

Ordered: PPos(T) = {p_0, p_1, ..., p_k_-_1} where p_0 < p_1 < ... < p_k_-_1
```

DEFINITION-9-(SEGMENTS):
```text
Segments of T (split by punctuation):
  Seg(T) = {T[pᵢ_+_1:pᵢ_+_1] | 0 <= i < k-1}

Where:
  - p_-_1 = -1 (before start)
  - p_k = |T| (after end)
  - Each segment sⱼ = T[pⱼ_-_1+1 : pⱼ]
```

EXAMPLE:
```text
T = "hello, world!"
P = {',', '!', ...}

PPos(T) = {5, 12}  // ',' at 5, '!' at 12

Seg(T) = {
  s_0 = T[0:5] = "hello",
  s_1 = T[6:12] = " world"
}
```

---
