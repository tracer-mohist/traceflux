# Research: Six Degrees Research Questions

DATE: 2026-03-06
STATUS: Research & Analysis (Research Questions)
PART: 3 of 3

---

## Research Questions

### 1. Optimal Degree Limit

QUESTION: What's the best max_degrees value?

HYPOTHESIS:
- 1st: Accurate but limited (no surprise)
- 2-3rd: Sweet spot (discoverable, not noisy)
- 4th+: Too noisy (weak associations)

EXPERIMENT: User testing with different degree limits.

### 2. Weighted vs Unweighted Paths

QUESTION: Should we prioritize high-frequency co-occurrences?

APPROACHES:
- Unweighted: All edges equal (BFS)
- Weighted: High co-occurrence = stronger edge (Dijkstra)
- Hybrid: BFS with weight-based ranking

TRADE-OFF:
- Unweighted: Finds all paths, may include weak associations
- Weighted: Stronger paths, may miss interesting connections

### 3. Hub Word Filtering

QUESTION: Should we filter out hub words (too generic)?

HUB WORDS: "system", "data", "process", "use" (connect everything)

APPROACHES:
- Remove stop words + domain-specific hubs
- Downweight high-degree nodes
- Keep but mark as "bridge words"

### 4. Domain Boundaries

QUESTION: Should we limit associations within domains?

EXAMPLE:
- "proxy" (networking) -> "authentication" (security) (Cross-domain, useful)
- "proxy" (networking) -> "recipe" (cooking) (Too distant, noise)

APPROACH:
- Topic modeling to detect domain boundaries
- User feedback to validate cross-domain associations

---

## Connections to Prompt Engineering

### Consensus Terminology

This research uses established terms:
- Small-World Network (Watts & Strogatz, 1998)
- Weak Ties (Granovetter, 1973)
- Triadic Closure (Simmel, 1908)
- Betweenness Centrality (Freeman, 1977)

WHY: Activates existing knowledge clusters, reduces ambiguity.

### Vocabulary Disambiguation

| Term | Framework | Definition |
|------|-----------|------------|
| Degree | Graph Theory | Number of edges in path |
| Co-occurrence | Corpus Linguistics | Words appearing in same context |
| Clustering | Network Science | Tendency for nodes to form groups |

### Annotation Style

```markdown
NOTE: This algorithm uses BFS (Breadth-First Search) for unweighted graphs.

REFERENCE: See Watts & Strogatz (1998) for small-world network model.

TIP: Start with max_degrees=3, adjust based on user feedback.
```

---

## Next Steps

### Immediate (Phase 2A Enhancement)

1. Implement basic co-occurrence graph
2. Add 2-degree association extraction
3. Test on workspace docs (memory/, docs/)

### Short-term (Phase 3)

1. Implement weighted paths (Dijkstra)
2. Add hub word filtering
3. User testing for optimal degree limit

### Long-term (Phase 4+)

1. Topic modeling for domain boundaries
2. Dynamic path visualization
3. Integration with prompt engineering framework

---

## Key Insights

### 1. Mathematical Basis

Six degrees is not magic -- it's logarithmic scaling:

```math
L = log(N) / log(k)
```

For typical text corpora, L = 3-4 degrees.

### 2. Weak Ties are Key

Direct co-occurrences (strong ties) are obvious.
Indirect associations (weak ties) enable discovery.

### 3. Hub Words Bridge Topics

Generic words ("system", "process") connect domains.
Filter carefully -- they're useful but can dominate.

### 4. Flywheel Effect

> 左脚踩右脚 (左脚踩右脚 -- stepping on your own foot to rise)

The flywheel effect is small-world networks in action:
- Each association leads to new associations
- 3-4 steps can reach distant concepts
- Exponential knowledge expansion

---

## References

1. Milgram, S. (1967) -- "The Small World Problem"
2. Watts, D. & Strogatz, S. (1998) -- "Collective dynamics of small-world networks"
3. Granovetter, M. (1973) -- "The Strength of Weak Ties"
4. Newman, M. (2010) -- "Networks: An Introduction"

---

STATUS: Research complete, ready for implementation design
NEXT: Design Phase 3 algorithm with multi-degree associations
PHILOSOPHY: Mathematical foundation for associative discovery
