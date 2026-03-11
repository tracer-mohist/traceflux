# Six Degrees

Purpose: Multi-hop association discovery using co-occurrence graphs.

NOTE: Consolidated from research/02-associations/ (2026-03-11)

---

## Core Concept

Six Degrees of Separation applied to text associations: any two concepts are connected within 6 hops through co-occurrence relationships.

---

## Co-occurrence Graph Construction

### Algorithm

Build graph from documents using sliding window:

Documents:
  ["proxy configuration for git",
   "git SSH authentication",
   "proxy settings firewall rules"]

Co-occurrence graph (window=5):
  proxy -> configuration (2), git (1), settings (1)
  configuration -> proxy (2), git (1), for (1)
  git -> proxy (1), configuration (1), SSH (1), authentication (1)
  SSH -> git (1), authentication (1)
  ...

### Implementation

See: [six-degrees-impl.md](./six-degrees-impl.md)

---

## Multi-Degree Association Search

### Algorithm

Find all words connected within max_degrees steps using BFS.

### Example Output

Search: "proxy"

Direct associations (1st degree):
  - configuration (weight: 2, path: ["proxy", "configuration"])
  - git (weight: 1, path: ["proxy", "git"])
  - settings (weight: 1, path: ["proxy", "settings"])

Indirect associations (2nd degree):
  - SSH (weight: 1, path: ["proxy", "git", "SSH"])
  - authentication (weight: 1, path: ["proxy", "git", "authentication"])
  - firewall (weight: 1, path: ["proxy", "settings", "firewall"])

3rd degree:
  - key (weight: 1, path: ["proxy", "git", "SSH", "key"])
  - rules (weight: 1, path: ["proxy", "settings", "firewall", "rules"])

---

## Path Visualization

### Text Output

Search: "proxy"

Direct associations (1st):
  - proxychains (12 co-occurrences)
  - git (8 co-occurrences)
  - config (7 co-occurrences)

Indirect associations (2-3rd):
  - SSH (2nd via git)
  - security (2nd via config)
  - authentication (3rd via security)
  - firewall (3rd via security)

### Graph Visualization

                    proxy
                   /  |  \
                  /   |   \
          proxychains  git  config
                        |     |
                       SSH  security
                        |     |
                       key  authentication
                              |
                           firewall

---

## Noise Filtering

### Problem: Multi-Hop Noise

As degree increases, associations become weaker:

1st degree: Strong, direct relationship
2nd degree: Moderate, indirect relationship
3rd degree: Weak, possibly noise
4th+ degree: Very weak, likely noise

Need to filter noise while preserving valid long-range associations!

### Solution: Strength Threshold

Filter associations by minimum strength threshold.

### Solution: Path Consistency

Valid association must have >= 2 independent paths.

See: [six-degrees-impl.md](./six-degrees-impl.md) for implementation.

---

## Applications

### 1. Divergent Search

User searches: "proxy"

Show associations at multiple degrees:
  1st: configuration, git, settings
  2nd: SSH, security, firewall
  3rd: authentication, key, rules

User explores their own path!

### 2. Topic Discovery

Analyze document corpus:
  - Build co-occurrence graph
  - Find central nodes (high degree)
  - Discover topic clusters

Result: Automatic topic modeling!

### 3. Analogy Detection

Find analogous relationships:

"proxy is to git as SSH is to ?"

Search paths:
  proxy -> git
  SSH -> ?

Answer: key (both are authentication methods)

### 4. Knowledge Graph Construction

Build knowledge graph from text:
  - Nodes: concepts
  - Edges: co-occurrence relationships
  - Weights: association strength

Query: Multi-hop traversal

---

## Performance

### Graph Size

For 1000 documents (10K words each):
  - Unique words: ~50K
  - Edges: ~500K (window=5)
  - Memory: ~100MB

Optimization:
  - Frequency threshold (keep words with freq >= 2)
  - Sparse representation (adjacency dict)
  - Incremental updates

### Query Speed

BFS traversal (max_degrees=3):
  - Time: O(V + E) where V=visited nodes, E=edges
  - Typical: 10-100ms for 50K nodes

Optimization:
  - Pre-compute common queries
  - Cache results
  - Limit max_degrees (3-4 is usually enough)

---

## Related

- [Divergent Search](../algorithms/divergent-search.md) - Application of multi-hop associations
- [Frequency Ranking](../core/frequency-ranking.md) - Edge weighting
- [Multi-Hop Noise](../theory/multi-hop-noise.md) - Noise analysis
- [Implementation](./six-degrees-impl.md) - Code examples

---

Last Updated: 2026-03-11
Source Files: 2026-03-06_six-degrees*.md
