# Six Degrees Implementation

Purpose: Code examples for multi-hop associations.

NOTE: Companion to six-degrees.md (2026-03-11)

---

## Co-occurrence Graph Construction

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
                graph[word1][word2] += 1
                graph[word2][word1] += 1
    
    return graph
```

---

## Multi-Degree Association Search

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
                strength = weight / degree
                associations.append((neighbor, degree + 1, new_path, strength))
                queue.append((neighbor, degree + 1, new_path))
    
    return sorted(associations, key=lambda x: -x[3])
```

---

## Noise Filtering

```python
def filter_by_strength(associations, min_strength=0.1):
    """Filter associations by strength threshold."""
    return [
        (word, degree, path, strength)
        for word, degree, path, strength in associations
        if strength >= min_strength
    ]

def filter_by_consistency(associations, min_paths=2):
    """Filter associations requiring multiple paths."""
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

Last Updated: 2026-03-11
