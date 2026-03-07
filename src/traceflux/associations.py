# src/traceflux/associations.py
"""Associative Search - Discover related patterns through graph traversal.

This module implements associative search: finding patterns related to a query
by traversing a co-occurrence graph. Unlike keyword search (find what you know),
associative search helps you **discover what you don't know to search for**.

## Philosophy

**Divergent discovery, not predictive completion.**

- Search engines show you what matches your query
- Associative search shows you what's **related** to your query
- Goal: Expand understanding, not narrow results

**Show possibilities, not predictions.**

We don't predict what you want. We show you what exists, ranked by
importance and relevance. You decide what's valuable.

## How It Works

### Multi-Hop Associations

**1-hop (Direct)**: Patterns that co-occur with query
```
query: "proxy"
1-hop: "config", "http", "proxychains", "socks5"
```

**2-hop (Friends of friends)**: Patterns connected through 1-hop
```
query: "proxy"
1-hop: "proxychains"
2-hop: "tor", "anonymity", "privacy"
```

**3-hop (Distant relations)**: More abstract connections
```
query: "proxy"
1-hop: "proxychains"
2-hop: "tor"
3-hop: "encryption", "security", "surveillance"
```

### Scoring

Associations are scored by combining:
1. **PageRank** (importance): How central is this pattern?
2. **Distance** (relevance): How close to the query?

Formula: `score = lambda * pagerank + (1 - lambda) * (1 / degree)`

- `lambda=0.7` (default): 70% PageRank, 30% distance
- Higher lambda: More weight to global importance
- Lower lambda: More weight to proximity

## Algorithm: BFS Traversal

We use Breadth-First Search (BFS) because:
1. **Guarantees shortest paths**: First time we see a node = closest degree
2. **Level-by-level**: Explores 1-hop, then 2-hop, then 3-hop
3. **Efficient**: O(V + E) where V=nodes, E=edges

## Use Cases

### Code Exploration
```python
associations = find_associations("PageRank", src/)
# 1-hop: "pagerank.py", "graph.py"
# 2-hop: "CooccurrenceGraph", "adjacency_list"
# 3-hop: "convergence", "tolerance"
```

### Documentation Navigation
```python
associations = find_associations("proxy", docs/)
# 1-hop: "proxychains", "HTTP_PROXY"
# 2-hop: "configuration", "environment variables"
# 3-hop: "security", "authentication"
```

## Example

```python
from traceflux import CooccurrenceGraph
from traceflux.pagerank import compute_pagerank
from traceflux.associations import AssociativeSearch

# Build graph and compute PageRank
graph = CooccurrenceGraph()
graph.add_document_cooccurrences(["proxy", "config", "http"], window_size=5)
pagerank_scores = compute_pagerank(graph)

# Find associations
search = AssociativeSearch(graph, pagerank_scores, lambda_param=0.7)
result = search.find_associations("proxy", max_degree=2, top_k=10)

for assoc in result.associations:
    print(f"{assoc.pattern}: degree={assoc.degree}, score={assoc.score:.3f}")
```

## Parameters

- **max_degree** (default: 3): How far to traverse (1=direct, 2=friends-of-friends, 3=distant)
- **lambda_param** (default: 0.7): Balance PageRank vs distance (0.7 = 70% PageRank)
- **top_k** (default: 20): Number of results to return
- **min_score** (default: 0.0): Minimum score threshold for filtering
"""

from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from .graph import CooccurrenceGraph


@dataclass
class Association:
    """An associated pattern with metadata.

    Represents a single association found during graph traversal.

    Attributes:
        pattern: The associated pattern text
        degree: Distance from query (1=direct, 2=friend-of-friend, 3=distant)
        score: Combined score (PageRank + inverse distance)
        path: Path from query to this pattern (e.g., ["proxy", "config", "settings"])
        pagerank: Original PageRank score (importance in graph)

    Example:
        >>> assoc = Association(
        ...     pattern="proxychains",
        ...     degree=1,
        ...     score=0.308,
        ...     path=["proxy", "proxychains"],
        ...     pagerank=0.052
        ... )
        >>> print(f"{assoc.pattern}: degree={assoc.degree}, score={assoc.score:.3f}")
        proxychains: degree=1, score=0.308
    """

    pattern: str
    degree: int  # Distance from query (1, 2, 3, ...)
    score: float  # Combined score (PageRank + distance)
    path: List[str] = field(default_factory=list)  # Path from query
    pagerank: float = 0.0  # Original PageRank score


@dataclass
class AssociationResult:
    """Result of associative search.

    Contains all associations found for a query, ranked by score.

    Attributes:
        query: Original query pattern
        associations: List of associations, sorted by score descending
        total_found: Total associations found (before top_k filtering)
        max_degree: Maximum degree reached in results

    Example:
        >>> result = search.find_associations("proxy", max_degree=2)
        >>> print(f"Query: {result.query}")
        Query: proxy
        >>> print(f"Found: {result.total_found} associations")
        Found: 15 associations
        >>> print(f"Max degree: {result.max_degree}")
        Max degree: 2
        >>> for assoc in result.associations[:5]:
        ...     print(f"  {assoc.pattern}: score={assoc.score:.3f}")
    """

    query: str
    associations: List[Association]
    total_found: int
    max_degree: int


class AssociativeSearch:
    """Find patterns associated with a query using BFS graph traversal.

    ## Purpose

    Discovers related patterns by traversing a co-occurrence graph.
    Unlike search (find what you know), this helps you **discover what you
    don't know to search for**.

    ## How It Works

    1. **Start at query node** in the co-occurrence graph
    2. **BFS traversal**: Explore neighbors level by level
    3. **Score each association**: Combine PageRank (importance) + distance (relevance)
    4. **Return ranked results**: Sorted by score, limited to top_k

    ## Scoring Formula

    ```
    score = lambda * pagerank + (1 - lambda) * (1 / degree)
    ```

    Where:
    - `pagerank`: Global importance of the pattern
    - `degree`: Distance from query (1=direct, 2=indirect, etc.)
    - `lambda`: Balance parameter (default: 0.7)

    **Why this formula?**
    - PageRank ensures important patterns rank higher
    - Inverse distance ensures closer patterns rank higher
    - Lambda balances the two (0.7 = 70% importance, 30% proximity)

    ## Example

    ```python
    from traceflux import CooccurrenceGraph
    from traceflux.pagerank import compute_pagerank
    from traceflux.associations import AssociativeSearch

    # Setup
    graph = CooccurrenceGraph()
    graph.add_document_cooccurrences(["proxy", "config", "http", "proxychains"], window_size=5)
    pagerank_scores = compute_pagerank(graph)

    # Find associations
    search = AssociativeSearch(graph, pagerank_scores, lambda_param=0.7)
    result = search.find_associations("proxy", max_degree=2, top_k=10)

    # Display results
    for assoc in result.associations:
        print(f"{assoc.pattern:20s} degree={assoc.degree} "
              f"score={assoc.score:.3f} path={' → '.join(assoc.path)}")
    ```

    ## Output

    ```
    config               degree=1 score=0.320 path=proxy → config
    http                 degree=1 score=0.311 path=proxy → http
    proxychains          degree=1 score=0.308 path=proxy → proxychains
    configuration        degree=2 score=0.289 path=proxy → config → configuration
    SSL                  degree=2 score=0.276 path=proxy → http → SSL
    ```

    ## Performance

    - **Time**: O(V + E) where V=nodes, E=edges (BFS complexity)
    - **Space**: O(V) for visited set and queue
    - **Typical**: <50ms for graphs with <1000 nodes
    """

    def __init__(
        self,
        graph: CooccurrenceGraph,
        pagerank_scores: Optional[Dict[str, float]] = None,
        lambda_param: float = 0.7,
    ):
        """Initialize associative search.

        Args:
            graph: Co-occurrence graph to traverse.
                Must contain nodes and edges representing pattern co-occurrences.

            pagerank_scores: Pre-computed PageRank scores for each pattern.
                Used to weight associations by importance.
                If None, uses uniform scores (all patterns equally important).
                Recommended: Always compute PageRank first for better results.

            lambda_param: Balance between PageRank and distance (default: 0.7).
                Formula: score = lambda * pagerank + (1 - lambda) * (1 / degree)

                - **0.9-1.0**: Almost entirely PageRank-based
                  - Use when: Graph has clear hubs, want global importance
                  - Risk: Distant but important patterns may rank higher than close ones

                - **0.7 (default)**: 70% PageRank, 30% distance
                  - Empirically good balance for most cases
                  - Recommended starting point

                - **0.5-0.6**: More weight to proximity
                  - Use when: Local context matters more than global importance
                  - Risk: May miss important but distant connections

                - **0.0-0.4**: Almost entirely distance-based
                  - Rarely useful
                  - Defeats purpose of combining PageRank

        Example:
            >>> search = AssociativeSearch(graph, pagerank_scores)
            >>> search.lambda_param
            0.7
            >>>
            >>> # Custom lambda for proximity-focused search
            >>> search_close = AssociativeSearch(graph, pagerank_scores, lambda_param=0.5)
        """
        self.graph = graph
        self.pagerank_scores = pagerank_scores or {}
        self.lambda_param = lambda_param

    def find_associations(
        self, query: str, max_degree: int = 3, top_k: int = 20, min_score: float = 0.0
    ) -> AssociationResult:
        """Find patterns associated with query using BFS traversal.

        ## Algorithm

        Uses Breadth-First Search (BFS) to explore the graph level by level:

        1. Start at query node (degree=0)
        2. Visit all neighbors (degree=1)
        3. Visit their neighbors (degree=2)
        4. Continue until max_degree reached
        5. Score and rank all discovered patterns
        6. Return top_k results

        ## Parameters

        Args:
            query: Pattern to find associations for.
                Must exist in the graph. If not found, returns empty result.

            max_degree: Maximum degrees of separation to explore (default: 3).
                - **1**: Direct co-occurrences only
                  - Best for: Finding immediate context
                  - Example: "proxy" → ["config", "http", "proxychains"]

                - **2**: Friends of friends (recommended)
                  - Best for: Exploring related concepts
                  - Example: "proxy" → "proxychains" → "tor"

                - **3**: Distant relations (default)
                  - Best for: Serendipitous discovery
                  - Example: "proxy" → "proxychains" → "tor" → "encryption"

                - **4+**: Very distant
                  - Generally too noisy
                  - Graph becomes highly connected

            top_k: Maximum number of associations to return (default: 20).
                Results are sorted by score (highest first).
                - **5-10**: Quick overview
                - **20**: Good for exploration (default)
                - **50+**: Comprehensive results

            min_score: Minimum score threshold for filtering (default: 0.0).
                Associations with score < min_score are excluded.
                - **0.0**: No filtering (return all)
                - **0.1-0.2**: Filter weak associations
                - **0.3+**: Only strong associations

        Returns:
            AssociationResult containing:
            - query: Original query pattern
            - associations: List of associations, sorted by score descending
            - total_found: Total associations found (before top_k filtering)
            - max_degree: Maximum degree reached in results

        ## Example

        ```python
        # Basic usage
        search = AssociativeSearch(graph, pagerank_scores)
        result = search.find_associations("proxy", max_degree=2)

        print(f"Found {result.total_found} associations")
        for assoc in result.associations[:10]:
            print(f"{assoc.pattern}: degree={assoc.degree}, score={assoc.score:.3f}")

        # With filtering
        result = search.find_associations(
            "proxy",
            max_degree=3,
            top_k=15,
            min_score=0.1  # Only associations with score >= 0.1
        )

        # With path explanation
        result = search.find_associations("proxy", max_degree=2)
        for assoc in result.associations[:5]:
            path_str = " → ".join(assoc.path)
            print(f"{assoc.pattern}: {path_str}")
        ```

        ## Edge Cases

        - **Query not in graph**: Returns empty result (total_found=0)
        - **Graph disconnected**: Only finds associations in query's component
        - **max_degree=0**: Returns empty (no traversal)
        - **top_k=0**: Returns empty list (but total_found still set)

        ## Performance

        - **Time**: O(V + E) where V=visited nodes, E=edges traversed
        - **Space**: O(V) for visited set and BFS queue
        - **Typical**: <50ms for graphs with <1000 nodes, max_degree=3
        """
        if not self.graph.has_node(query):
            return AssociationResult(query=query, associations=[], total_found=0, max_degree=0)

        # BFS traversal
        visited: Set[str] = {query}
        queue: deque = deque([(query, 0, [query])])  # (node, degree, path)
        associations: List[Association] = []

        while queue:
            current, degree, path = queue.popleft()

            # Skip if beyond max degree
            if degree >= max_degree:
                continue

            # Explore neighbors
            for neighbor in self.graph.neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    new_degree = degree + 1

                    # Calculate association score
                    score = self._calculate_score(neighbor, new_degree)

                    if score >= min_score:
                        assoc = Association(
                            pattern=neighbor,
                            degree=new_degree,
                            score=score,
                            path=new_path,
                            pagerank=self.pagerank_scores.get(neighbor, 0.0),
                        )
                        associations.append(assoc)

                    # Continue BFS
                    queue.append((neighbor, new_degree, new_path))

        # Sort by score descending
        associations.sort(key=lambda a: -a.score)

        # Return top-k
        top_associations = associations[:top_k]

        return AssociationResult(
            query=query,
            associations=top_associations,
            total_found=len(associations),
            max_degree=max(assoc.degree for assoc in top_associations) if top_associations else 0,
        )

    def _calculate_score(self, pattern: str, degree: int) -> float:
        """Calculate association score.

        Combines PageRank (importance) and inverse distance.

        Score = lambda * PageRank + (1 - lambda) * (1 / degree)

        Args:
            pattern: Pattern to score
            degree: Distance from query

        Returns:
            Combined score (0-1 range approximately)
        """
        # Get PageRank score (normalized)
        pr_score = self.pagerank_scores.get(pattern, 0.0)

        # Distance score (inverse)
        distance_score = 1.0 / degree if degree > 0 else 1.0

        # Combined score
        combined = self.lambda_param * pr_score + (1 - self.lambda_param) * distance_score

        return combined

    def find_multi_query_associations(
        self, queries: List[str], max_degree: int = 3, top_k: int = 20
    ) -> AssociationResult:
        """Find associations for multiple queries.

        Merges results from multiple query patterns.

        Args:
            queries: List of query patterns
            max_degree: Maximum degrees of separation
            top_k: Maximum associations to return

        Returns:
            Merged AssociationResult
        """
        all_associations: Dict[str, Association] = {}

        for query in queries:
            result = self.find_associations(query, max_degree, top_k=top_k * 2)

            for assoc in result.associations:
                if assoc.pattern in all_associations:
                    # Boost score if found from multiple queries
                    existing = all_associations[assoc.pattern]
                    existing.score += assoc.score * 0.5  # Diminishing returns
                else:
                    all_associations[assoc.pattern] = assoc

        # Sort and return top-k
        sorted_assocs = sorted(all_associations.values(), key=lambda a: -a.score)[:top_k]

        return AssociationResult(
            query=", ".join(queries),
            associations=sorted_assocs,
            total_found=len(all_associations),
            max_degree=max(a.degree for a in sorted_assocs) if sorted_assocs else 0,
        )

    def get_association_paths(
        self, query: str, target: str, max_degree: int = 5
    ) -> List[List[str]]:
        """Find all paths between query and target.

        Uses BFS to find paths up to max_degree hops.

        Args:
            query: Starting pattern
            target: Target pattern
            max_degree: Maximum path length

        Returns:
            List of paths (each path is a list of patterns)
        """
        if not self.graph.has_node(query) or not self.graph.has_node(target):
            return []

        if query == target:
            return [[query]]

        paths: List[List[str]] = []
        queue: deque = deque([(query, [query])])
        visited_in_path: Set[str] = {query}

        while queue:
            current, path = queue.popleft()

            if len(path) > max_degree + 1:
                continue

            for neighbor in self.graph.neighbors(current):
                if neighbor == target:
                    paths.append(path + [target])
                elif neighbor not in visited_in_path:
                    visited_in_path.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return paths


def find_associations(
    graph: CooccurrenceGraph,
    query: str,
    pagerank_scores: Optional[Dict[str, float]] = None,
    max_degree: int = 3,
    top_k: int = 20,
) -> List[Tuple[str, int, float]]:
    """Convenience function to find associations.

    Args:
        graph: Co-occurrence graph
        query: Query pattern
        pagerank_scores: Pre-computed PageRank scores
        max_degree: Maximum degrees of separation
        top_k: Maximum associations to return

    Returns:
        List of (pattern, degree, score) tuples
    """
    search = AssociativeSearch(graph, pagerank_scores)
    result = search.find_associations(query, max_degree, top_k)

    return [(assoc.pattern, assoc.degree, assoc.score) for assoc in result.associations]
