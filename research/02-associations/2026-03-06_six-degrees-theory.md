# Research: Six Degrees of Separation in Text Search

DATE: 2026-03-06
STATUS: Research & Analysis
TOPIC: Small-World Network Theory applied to text/keyword association

---

## Core Theory

### What is Six Degrees of Separation?

DEFINITION: Any two people on Earth are connected through at most 6 intermediate acquaintances.

ORIGIN:
- 1929: Frigyes Karinthy (Hungarian author) - short story "Chains"
- 1967: Stanley Milgram - small-world experiment
- 2011: Facebook study - average distance = 4.74

KEY INSIGHT: The world is a small-world network.

---

## Mathematical Foundation

### Small-World Network Properties

1. High Clustering -- Friends of friends tend to be friends (triadic closure)
2. Short Path Length -- Average distance between nodes is small (logarithmic)

### Average Path Length Formula

```math
L = log(N) / log(k)

Where:
- N = Total nodes
- k = Average degree (connections per node)
- L = Average path length
```

EXAMPLE CALCULATION:

```text
Social Network:
- N = 7 billion (world population)
- k = 1000 (average person knows ~1000 people)
- L = log(7,000,000,000) / log(1000)
- L = 22.8 / 3 = 7.6

-> ~6-8 degrees (matches empirical findings!)
```

---

## Why Does This Work?

### 1. Weak Ties Theory (Granovetter, 1973)

STRONG TIES: Close friends (high clustering, redundant connections)
WEAK TIES: Acquaintances (bridge different social circles)

KEY INSIGHT: Weak ties are the "shortcuts" that make the world small.

```text
You -> Close Friend -> Their Close Friend -> ... (long path, same cluster)
You -> Acquaintance -> Their Friend -> ... (short path, different cluster)
```

### 2. Hub Nodes

Some nodes have disproportionately high degree (connectors, influencers).

EXAMPLE:
- Most people: ~100-1000 connections
- Hub nodes: 10,000+ connections

EFFECT: Hubs dramatically reduce average path length.

### 3. Triadic Closure

If A knows B and B knows C, then A is likely to know C.

RESULT: High clustering coefficient, but hubs bridge clusters.

---

## Application to Text/Search Domain

### Mapping Concepts

| Social Network | Text/Search Domain |
|----------------|--------------------|
| Person (node) | Word / Token / Concept |
| Friendship (edge) | Co-occurrence (appear in same context) |
| Social circle | Topic cluster / Semantic field |
| Acquaintance | Weak co-occurrence (rare but exists) |
| Influencer/Hub | High-frequency connector words |
| 6 degrees | ~3-6 word associations |

### Text Network Properties

NODES: All unique words in corpus
EDGES: Two words connected if they co-occur within window (e.g., same paragraph)
WEIGHT: Co-occurrence frequency

EXPECTED PROPERTIES:
1. High Clustering -- Related words cluster together (topic coherence)
2. Short Paths -- Any two concepts connected via 3-6 intermediate words
3. Hub Words -- Common words bridge topics (e.g., "system", "data", "process")

---

## Calculation for Text Corpus

### Example: Technical Documentation

```text
Corpus Statistics:
- N = 10,000 unique words (vocabulary size)
- k = 20 (average word co-occurs with ~20 other words)

Average Path Length:
L = log(10,000) / log(20)
L = 9.2 / 3.0 = 3.1

-> ~3-4 degrees to connect any two words!
```

### Empirical Validation

TEST CASE: Connect "proxy" to "authentication"

```text
Path Found:
proxy (1st) -> git (2nd) -> config (3rd) -> security (4th) -> authentication

Actual Distance: 4 degrees
```

PREDICTION: Matches theoretical estimate (3-4 degrees for technical corpus).

---

## Implications for traceflux

### Current Design (Phase 2A)

1-Degree Association:

```text
Search: "proxy"
Extract: proxychains, git, config (direct co-occurrence)
```

LIMITATION: Only shows immediate neighbors, misses indirect discoveries.

### Enhanced Design (Phase 3+)

Multi-Degree Association:

```text
Search: "proxy"

1st (Direct):
  - proxychains (12 co-occurrences)
  - git (8 co-occurrences)
  - config (7 co-occurrences)

2nd (Friend's Friend):
  - SSH (via git)
  - environment variables (via config)
  - security (via config)

3rd (Distant Connection):
  - authentication (via security)
  - firewall (via security)
  - tunnel (via SSH)

Discovery: "proxy relates to authentication through 4-step path!"
```

---

CONTINUED IN: 2026-03-06_six-degrees-theory-algo.md
