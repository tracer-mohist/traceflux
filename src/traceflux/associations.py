# src/traceflux/associations.py
"""Associative Search - Find related patterns using graph traversal.

Uses BFS (Breadth-First Search) to discover patterns related to a query.
Supports multi-hop associations with path tracking.

Philosophy: Divergent discovery, not predictive completion.
Show possibilities, not predictions.
"""

from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from .graph import CooccurrenceGraph


@dataclass
class Association:
    """An associated pattern with metadata."""

    pattern: str
    degree: int  # Distance from query (1, 2, 3, ...)
    score: float  # Combined score (PageRank + distance)
    path: List[str] = field(default_factory=list)  # Path from query
    pagerank: float = 0.0  # Original PageRank score


@dataclass
class AssociationResult:
    """Result of associative search."""

    query: str
    associations: List[Association]
    total_found: int
    max_degree: int


class AssociativeSearch:
    """Find patterns associated with a query.

    Uses BFS traversal on co-occurrence graph to discover
    related patterns at multiple degrees of separation.

    Example:
        >>> search = AssociativeSearch(graph, pagerank_scores)
        >>> result = search.find_associations("proxy", max_degree=3, top_k=20)
        >>> for assoc in result.associations:
        ...     print(f"{assoc.pattern} (degree {assoc.degree}): {assoc.score:.4f}")
    """

    def __init__(
        self,
        graph: CooccurrenceGraph,
        pagerank_scores: Optional[Dict[str, float]] = None,
        lambda_param: float = 0.7
    ):
        """Initialize associative search.

        Args:
            graph: Co-occurrence graph
            pagerank_scores: Pre-computed PageRank scores
            lambda_param: Balance between PageRank and distance (0-1)
                         Higher = more weight to PageRank
        """
        self.graph = graph
        self.pagerank_scores = pagerank_scores or {}
        self.lambda_param = lambda_param

    def find_associations(
        self,
        query: str,
        max_degree: int = 3,
        top_k: int = 20,
        min_score: float = 0.0
    ) -> AssociationResult:
        """Find patterns associated with query.

        Uses BFS to traverse graph up to max_degree hops.

        Args:
            query: Query pattern
            max_degree: Maximum degrees of separation
            top_k: Maximum associations to return
            min_score: Minimum score threshold

        Returns:
            AssociationResult with ranked associations
        """
        if not self.graph.has_node(query):
            return AssociationResult(
                query=query,
                associations=[],
                total_found=0,
                max_degree=0
            )

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
                            pagerank=self.pagerank_scores.get(neighbor, 0.0)
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
            max_degree=max(assoc.degree for assoc in top_associations) if top_associations else 0
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
        combined = (self.lambda_param * pr_score +
                   (1 - self.lambda_param) * distance_score)

        return combined

    def find_multi_query_associations(
        self,
        queries: List[str],
        max_degree: int = 3,
        top_k: int = 20
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
        sorted_assocs = sorted(
            all_associations.values(),
            key=lambda a: -a.score
        )[:top_k]

        return AssociationResult(
            query=", ".join(queries),
            associations=sorted_assocs,
            total_found=len(all_associations),
            max_degree=max(a.degree for a in sorted_assocs) if sorted_assocs else 0
        )

    def get_association_paths(
        self,
        query: str,
        target: str,
        max_degree: int = 5
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
    top_k: int = 20
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

    return [
        (assoc.pattern, assoc.degree, assoc.score)
        for assoc in result.associations
    ]
