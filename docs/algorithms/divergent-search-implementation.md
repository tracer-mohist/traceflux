# Divergent Search Implementation

Purpose: Code examples for divergent search.

NOTE: Companion to divergent-search.md (2026-03-11)

---

## Divergent Query Algorithm

```python
def divergent_search(query, graph, top_k=10, diversity=0.5):
    """
    Get diverse associations for query.

    Args:
        query: User's input
        graph: Association graph {node: {neighbor: weight}}
        top_k: Number of results
        diversity: 0.0 = pure frequency, 1.0 = pure diversity

    Returns: List of (association, score) tuples
    """
    neighbors = graph.get(query, {})

    if not neighbors:
        return []

    # Score by frequency
    freq_scores = {
        node: weight / max(neighbors.values())
        for node, weight in neighbors.items()
    }

    # Score by diversity
    selected = []
    diversity_scores = {}

    for node in neighbors:
        if not selected:
            diversity_scores[node] = 1.0
        else:
            avg_sim = sum(
                ngram_similarity(node, s)
                for s in selected
            ) / len(selected)
            diversity_scores[node] = 1.0 - avg_sim

    # Combine scores
    final_scores = {
        node: (1 - diversity) * freq_scores[node] +
              diversity * diversity_scores[node]
        for node in neighbors
    }

    results = sorted(final_scores.items(), key=lambda x: -x[1])[:top_k]

    return results
```

---

## Multi-Hop Traversal

```python
from collections import deque

def find_associations(graph, start_word, max_degrees=3):
    """Find words connected within max_degrees steps."""
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
                strength = weight / degree
                associations.append((neighbor, degree + 1, new_path, strength))
                queue.append((neighbor, degree + 1, new_path))

    return sorted(associations, key=lambda x: -x[3])
```

---

Last Updated: 2026-03-11
