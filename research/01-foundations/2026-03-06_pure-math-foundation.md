# Research: Pure Mathematical Foundation

DATE: 2026-03-06
STATUS: Foundational Formalization
TOPIC: Pure mathematics -- characters, sequences, order, no linguistic assumptions

---

## Core Principle

> ",,,."
>
> (Must be pure text characters, character sequences, sequence order, pure mathematical algorithms.)

NO-LINGUISTIC-ASSUMPTIONS:
-  No "words" (linguistic concept)
-  No "semantics" (meaning-based)
-  No "syntax" (grammar-based)
-  Only: characters, positions, sequences, sets, graphs

---

## 1. Fundamental Objects

### Character (Primitive)

DEFINITION-1-(ALPHABET):
```text
SIGMA = finite set of characters (Unicode code points)

c IN SIGMA is a character
Example: c = 0x48 ('H'), c = 0xE4B896 ('世')
```

NOTE: No distinction between "letter", "digit", "punctuation" -- all are just characters in SIGMA.

---

### Text Sequence

DEFINITION-2-(TEXT):
```text
A text T is a finite sequence of characters:

T = ⟨c_0, c_1, c_2, ..., c_n_-_1⟩

Where:
  - cᵢ IN SIGMA for all 0 <= i < n
  - n = |T| (length of T)
  - pos(cᵢ) = i (position of cᵢ in T)
```

MATHEMATICAL-OBJECT: T IN SIGMA* (Kleene star -- all finite sequences over SIGMA)

---

### Subsequence

DEFINITION-3-(SUBSEQUENCE):
```text
S is a subsequence of T iff:
  S = ⟨cᵢ_1, cᵢ_2, ..., cᵢ_k⟩

Where:
  - 0 <= i_1 < i_2 < ... < i_k < n
  - Each cᵢⱼ IN T

Notation: S ⊑ T
```

KEY-PROPERTY: Order is preserved (i_1 < i_2 < ... < i_k)

---

### Substring (Contiguous Subsequence)

DEFINITION-4-(SUBSTRING):
```text
S is a substring of T iff:
  S = ⟨cᵢ, cᵢ_+_1, ..., cᵢ_+_k_-_1⟩

Where:
  - 0 <= i < n
  - 0 <= k <= n - i

Notation: T[i:i+k]

Key: Indices are consecutive (contiguous)
```

---

## 2. Pure Sequence Operations

### Concatenation

DEFINITION-5-(CONCATENATION):
```text
For sequences A = ⟨a_0, ..., aₘ_-_1⟩ and B = ⟨b_0, ..., b_n_-_1⟩:

A . B = ⟨a_0, ..., aₘ_-_1, b_0, ..., b_n_-_1⟩

Properties:
  - Associative: (A . B) . C = A . (B . C)
  - Identity: A . ⟨⟩ = A (empty sequence)
  - Not commutative: A . B != B . A (order matters!)
```

---

### Prefix and Suffix

DEFINITION-6-(PREFIX):
```text
P is a prefix of T iff:
  T = P . S for some sequence S

Notation: P ⊑ₚᵣₑ T

Example:
  T = "hello"
  Prefixes: ⟨⟩, "h", "he", "hel", "hell", "hello"
```

DEFINITION-7-(SUFFIX):
```text
S is a suffix of T iff:
  T = P . S for some sequence P

Notation: S ⊑ₛᵤ𝒻 T

Example:
  T = "hello"
  Suffixes: ⟨⟩, "o", "lo", "llo", "ello", "hello"
```

---

### Reversal

DEFINITION-8-(REVERSAL):
```text
For T = ⟨c_0, c_1, ..., c_n_-_1⟩:

Tᴿ = ⟨c_n_-_1, c_n_-_2, ..., c_1, c_0⟩

Properties:
  - (Tᴿ)ᴿ = T
  - (A . B)ᴿ = Bᴿ . Aᴿ
```

---

## 3. Pattern Matching (Pure)

### Exact Match

DEFINITION-9-(EXACT-MATCH):
```text
Pattern P occurs in T at position i iff:
  T[i:i+|P|] = P

Occurrence set:
  Occ(P, T) = {i | T[i:i+|P|] = P}

Frequency:
  freq(P, T) = |Occ(P, T)|
```

EXAMPLE:
```text
T = "hello hello world"
P = "hello"

Occ(P, T) = {0, 6}
freq(P, T) = 2
```

---

### Longest Common Subsequence

DEFINITION-10-(LCS):
```text
For sequences A and B:

LCS(A, B) = longest S such that S ⊑ A and S ⊑ B

Computation: Dynamic programming
  dp[i][j] = length of LCS(A[0:i], B[0:j])

  dp[i][j] = dp[i-1][j-1] + 1              if A[i] = B[j]
           = max(dp[i-1][j], dp[i][j-1])   otherwise
```

USE: Sequence similarity (not semantic!)

---

### Longest Common Substring

DEFINITION-11-(LONGEST-COMMON-SUBSTRING):
```text
For sequences A and B:

LCSubstr(A, B) = longest S such that S ⊑ₛᵤᵦ A and S ⊑ₛᵤᵦ B

Computation: Suffix tree or dynamic programming
```

---
