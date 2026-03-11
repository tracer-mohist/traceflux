# Research: Six Degrees Algorithm Design

DATE: 2026-03-06
STATUS: Research & Analysis (Algorithm Design)
PART: 2 of 3

---

## Algorithm Design

### Co-occurrence Graph Construction

```python
from collections import defaultdict
import networkx as nx

# Build co-occurrence graph
def build_cooccurrence_graph(documents, window_size=5):
    """
    documents: List of text documents
    window_size: Co-occurrence window (words within this distance are connected)
    """
    graph = nx.Graph()
    cooccurrence_count = defaultdict(int)

    for doc in documents:
        words = tokenize(doc)
        for i, word1 in enumerate(words):
            for j in range(i+1, min(i+window_size, len(words))):
                word2 = words[j]
                # Add edge (undirected)
                graph.add_edge(word1, word2)
                cooccurrence_count[(word1, word2)] += 1

    # Add edge weights
    for edge in graph.edges():
        graph.edges[edge]['weight'] = cooccurrence_count[edge]

    return graph
```

### Multi-Degree Association Search

```python
def find_associations(graph, start_word, max_degrees=3):
    """
    Find words connected within max_degrees steps.
    Returns: List of (word, degree, path) tuples
    """
    from collections import deque

    visited = {start_word}
    queue = deque([(start_word, 0, [start_word])])  # (word, degree, path)
    associations = []

    while queue:
        word, degree, path = queue.popleft()

        if degree >= max_degrees:
            continue

        for neighbor in graph.neighbors(word):
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = path + [neighbor]
                associations.append((neighbor, degree + 1, new_path))
                queue.append((neighbor, degree + 1, new_path))

    return associations

# Example usage
associations = find_associations(graph, "proxy", max_degrees=3)
# [
#   ("git", 1, ["proxy", "git"]),
#   ("config", 1, ["proxy", "config"]),
#   ("SSH", 2, ["proxy", "git", "SSH"]),
#   ("security", 2, ["proxy", "config", "security"]),
#   ("authentication", 3, ["proxy", "config", "security", "authentication"]),
#   ...
# ]
```

### Path Visualization

```text
Output Format:

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

Discovery paths:
  proxy -> git -> SSH -> tunnel
  proxy -> config -> security -> authentication
  proxy -> config -> security -> firewall
```

---

CONTINUED IN: 2026-03-06_six-degrees-theory-research.md
