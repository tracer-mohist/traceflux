# Mathematical Proofs

Purpose: Formal proofs and properties for TraceFlux algorithms.

NOTE: Companion to mathematical-model.md (2026-03-11)

---

## Proofs and Properties

### Property 1: N-gram Completeness

Theorem: For any text T and any substring s of T, there exists n such that s in G_n(T).

Proof: Let n = |s|. By definition of substring, s = T[i:i+n] for some i. Therefore s in G_n(T). QED

### Property 2: Frequency Monotonicity

Theorem: For patterns p1, p2 where p1 is a substring of p2: freq(p1, C) >= freq(p2, C).

Proof: Every occurrence of p2 contains an occurrence of p1. Therefore freq(p2) <= freq(p1). QED

### Property 3: PageRank Convergence

Theorem: PageRank iteration converges to a unique stationary distribution for any strongly connected graph.

Proof: Standard PageRank convergence proof applies. The co-occurrence graph is strongly connected if all patterns co-occur transitively. QED

---

## Information Theory

### Entropy

Definition 12 (Pattern Entropy):

For pattern distribution P over corpus C:

H(P) = -sum p_i * log2(p_i)

Where p_i = freq(pattern_i) / sum freq(pattern_j)

Low entropy = concentrated distribution (few dominant patterns)
High entropy = uniform distribution (many equal patterns)

### Application

Use entropy to:
  1. Measure corpus diversity
  2. Detect topic shifts (entropy changes)
  3. Optimize n-gram size (minimize entropy)

---

## Detailed Derivations

### N-gram Cardinality

For text T of length n:

|G_n(T)| = n - n + 1

Example:
  T = "hello" (length 5)
  G_2(T) = {"he", "el", "ll", "lo"}
  |G_2(T)| = 5 - 2 + 1 = 4

### PageRank Iteration

Initial:
  PR_0(g) = 1 / N for all g

Iteration k+1:
  PR_{k+1}(g) = (1 - d) / N + d * sum(PR_k(h) / out_degree(h))
                                          h in In(g)

Convergence:
  lim_{k->infinity} PR_k(g) = PR*(g)

Where PR* is the stationary distribution.

---

Last Updated: 2026-03-11
Source Files: 2026-03-06_mathematical-formalization*.md
