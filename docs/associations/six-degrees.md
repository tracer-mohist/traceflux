# Six Degrees

**Purpose**: Multi-hop association discovery using co-occurrence graphs.

**NOTE**: Consolidated from research/02-associations/ (2026-03-11)

---

## Core Concept

**Six Degrees of Separation** applied to text associations: any two concepts are connected within 6 hops through co-occurrence relationships.

---

## Co-occurrence Graph Construction

### Algorithm

```python
from collections import defaultdict

def build_cooccurrence_graph(documents, window_size=5):
    """
    Build co-occurrence graph from documents.

    Args:
        documents: List of text documents
        window_size: Words within this distance are connected

    Returns: Graph as adjacency dict {node: {neighbor: weight}}
    """
    graph = defaultdict(lambda: defaultdict(int))

    for doc in documents:
        words = tokenize(doc)
        for i, word1 in enumerate(words):
            for j in range(i + 1, min(i + window_size, len(words))):
                word2 = words[j]
                # Add edge (undirected)
                graph[word1][word2] += 1
                graph[word2][word1] += 1

    return graph
```

### Example

```text
Documents:
  ["proxy configuration for git",
   "git SSH authentication",
   "proxy settings firewall rules"]

Co-occurrence graph (window=5):
  proxy → configuration (2), git (1), settings (1)
  configuration → proxy (2), git (1), for (1)
  git → proxy (1), configuration (1), SSH (1), authentication (1)
  SSH → git (1), authentication (1)
  ...
```

---

## Multi-Degree Association Search

### Algorithm

```python
from collections import deque

def find_associations(graph, start_word, max_degrees=3):
    """
    Find words connected within max_degrees steps.

    Returns: List of (word, degree, path, strength) tuples
    """
    visited = {start_word}
    queue = deque([(start_word, 0, [start_word])])
    associations = []

    while queue:
        word, degree, path = queue.popleft()

        if degree >= max_degrees:
            continue

        for neighbor, weight in graph[word].items():
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = path + [neighbor]
                # Strength = product of edge weights / degree
                strength = weight / degree
                associations.append((neighbor, degree + 1, new_path, strength))
                queue.append((neighbor, degree + 1, new_path))

    # Sort by strength
    return sorted(associations, key=lambda x: -x[3])
```

### Example Output

```text
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
```

---

## Path Visualization

### Text Output

```text
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
```

### Graph Visualization

```text
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
```

---

## Noise Filtering

### Problem: Multi-Hop Noise

```text
As degree increases, associations become weaker:

1st degree: Strong, direct relationship
2nd degree: Moderate, indirect relationship
3rd degree: Weak, possibly noise
4th+ degree: Very weak, likely noise

Need to filter noise while preserving valid long-range associations!
```

### Solution: Strength Threshold

```python
def filter_by_strength(associations, min_strength=0.1):
    """Filter associations by strength threshold."""
    return [
        (word, degree, path, strength)
        for word, degree, path, strength in associations
        if strength >= min_strength
    ]
```

### Solution: Path Consistency

```python
def filter_by_consistency(associations, min_paths=2):
    """
    Filter associations requiring multiple paths.

    Valid association must have >= min_paths independent paths.
    """
    path_count = defaultdict(int)
    path_details = defaultdict(list)

    for word, degree, path, strength in associations:
        path_count[word] += 1
        path_details[word].append((path, strength))

    return [
        (word, min_degree, path_details[word][0], max_strength)
        for word, paths in path_details.items()
        if len(paths) >= min_paths
        for min_degree, _, _, max_strength in [
            (min(p[1] for p in paths), None, None, max(p[3] for p in paths))
        ]
    ]
```

---

## Applications

### 1. Divergent Search

```text
User searches: "proxy"

Show associations at multiple degrees:
  1st: configuration, git, settings
  2nd: SSH, security, firewall
  3rd: authentication, key, rules

User explores their own path!
```

### 2. Topic Discovery

```text
Analyze document corpus:
  - Build co-occurrence graph
  - Find central nodes (high degree)
  - Discover topic clusters

Result: Automatic topic modeling!
```

### 3. Analogy Detection

```text
Find analogous relationships:

"proxy is to git as SSH is to ?"

Search paths:
  proxy → git
  SSH → ?

Answer: key (both are authentication methods)
```

### 4. Knowledge Graph Construction

```text
Build knowledge graph from text:
  - Nodes: concepts
  - Edges: co-occurrence relationships
  - Weights: association strength

Query: Multi-hop traversal
```

---

## Performance

### Graph Size

```text
For 1000 documents (10K words each):
  - Unique words: ~50K
  - Edges: ~500K (window=5)
  - Memory: ~100MB

Optimization:
  - Frequency threshold (keep words with freq >= 2)
  - Sparse representation (adjacency dict)
  - Incremental updates
```

### Query Speed

```text
BFS traversal (max_degrees=3):
  - Time: O(V + E) where V=visited nodes, E=edges
  - Typical: 10-100ms for 50K nodes

Optimization:
  - Pre-compute common queries
  - Cache results
  - Limit max_degrees (3-4 is usually enough)
```

---

## Related

- [Divergent Search](../algorithms/divergent-search.md) - Application of multi-hop associations
- [Frequency Ranking](../core/frequency-ranking.md) - Edge weighting
- [Multi-Hop Noise](../theory/multi-hop-noise.md) - Noise analysis

---

**Last Updated**: 2026-03-11
**Source Files**: `2026-03-06_six-degrees*.md`
