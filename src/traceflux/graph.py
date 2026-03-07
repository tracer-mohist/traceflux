# src/traceflux/graph.py
"""Co-occurrence Graph - Build pattern relationship graph.

Constructs a graph where:
- Nodes: Patterns
- Edges: Co-occurrence relationships
- Weights: Co-occurrence frequency

Used for associative search and PageRank computation.
"""

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple


@dataclass
class GraphStats:
    """Statistics about the graph."""

    node_count: int
    edge_count: int
    avg_degree: float
    max_degree: int
    min_degree: int
    density: float


class CooccurrenceGraph:
    """Co-occurrence graph for pattern relationships.

    Undirected weighted graph where edges represent
    patterns appearing together in documents.

    Example:
        >>> graph = CooccurrenceGraph()
        >>> graph.add_cooccurrence("proxy", "config", weight=5)
        >>> graph.neighbors("proxy")
        ['config']
    """

    def __init__(self):
        """Initialize empty graph.

        Uses adjacency list representation:
        {node: {neighbor: weight}}
        """
        # Adjacency list: node -> {neighbor -> weight}
        self._adj: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self._edge_count: int = 0

    def add_cooccurrence(self, pattern1: str, pattern2: str, weight: int = 1) -> None:
        """Add or update co-occurrence edge.

        Graph is undirected, so edge is added in both directions.

        Args:
            pattern1: First pattern
            pattern2: Second pattern
            weight: Co-occurrence count to add
        """
        if pattern1 == pattern2:
            # Skip self-loops
            return

        # Add edge in both directions (undirected graph)
        if pattern2 not in self._adj[pattern1]:
            self._edge_count += 1

        self._adj[pattern1][pattern2] += weight
        self._adj[pattern2][pattern1] += weight

    def add_document_cooccurrences(self, patterns: List[str], window_size: int = 2) -> None:
        """Add co-occurrences from a document's pattern sequence.

        Patterns within window_size of each other are considered
        co-occurring.

        Args:
            patterns: Sequence of patterns from document
            window_size: Window for co-occurrence (default: adjacent pairs)
        """
        if len(patterns) < 2:
            return

        for i in range(len(patterns)):
            # Look ahead within window
            for j in range(i + 1, min(i + window_size + 1, len(patterns))):
                self.add_cooccurrence(patterns[i], patterns[j])

    def has_node(self, pattern: str) -> bool:
        """Check if pattern exists in graph.

        Args:
            pattern: Pattern to check

        Returns:
            True if pattern is a node in graph
        """
        return pattern in self._adj

    def has_edge(self, pattern1: str, pattern2: str) -> bool:
        """Check if edge exists between patterns.

        Args:
            pattern1: First pattern
            pattern2: Second pattern

        Returns:
            True if edge exists
        """
        return pattern2 in self._adj.get(pattern1, {})

    def get_weight(self, pattern1: str, pattern2: str) -> int:
        """Get weight of edge between patterns.

        Args:
            pattern1: First pattern
            pattern2: Second pattern

        Returns:
            Edge weight (0 if no edge)
        """
        return self._adj.get(pattern1, {}).get(pattern2, 0)

    def neighbors(self, pattern: str) -> List[str]:
        """Get neighboring patterns.

        Args:
            pattern: Pattern to get neighbors for

        Returns:
            List of neighboring patterns
        """
        return list(self._adj.get(pattern, {}).keys())

    def degree(self, pattern: str) -> int:
        """Get degree (number of neighbors) of pattern.

        Args:
            pattern: Pattern

        Returns:
            Number of neighbors
        """
        return len(self._adj.get(pattern, {}))

    def weighted_degree(self, pattern: str) -> int:
        """Get weighted degree (sum of edge weights).

        Args:
            pattern: Pattern

        Returns:
            Sum of edge weights
        """
        return sum(self._adj.get(pattern, {}).values())

    def nodes(self) -> List[str]:
        """Get all nodes in graph.

        Returns:
            List of all patterns
        """
        return list(self._adj.keys())

    def edges(self) -> List[Tuple[str, str, int]]:
        """Get all edges in graph.

        Returns:
            List of (node1, node2, weight) tuples
            Each edge appears once (not duplicated for undirected)
        """
        edges = []
        seen = set()

        for node1, neighbors in self._adj.items():
            for node2, weight in neighbors.items():
                # Avoid duplicates in undirected graph
                edge_key = tuple(sorted([node1, node2]))
                if edge_key not in seen:
                    edges.append((node1, node2, weight))
                    seen.add(edge_key)

        return edges

    def node_count(self) -> int:
        """Get number of nodes.

        Returns:
            Number of nodes
        """
        return len(self._adj)

    def edge_count(self) -> int:
        """Get number of edges.

        Returns:
            Number of unique edges
        """
        return self._edge_count

    def get_stats(self) -> GraphStats:
        """Get graph statistics.

        Returns:
            GraphStats object with metrics
        """
        n = self.node_count()
        m = self.edge_count()

        if n == 0:
            return GraphStats(
                node_count=0, edge_count=0, avg_degree=0.0, max_degree=0, min_degree=0, density=0.0
            )

        degrees = [self.degree(node) for node in self._adj.keys()]
        avg_degree = sum(degrees) / n
        max_degree = max(degrees) if degrees else 0
        min_degree = min(degrees) if degrees else 0

        # Density = actual edges / possible edges
        # For undirected graph: max edges = n * (n-1) / 2
        max_edges = n * (n - 1) / 2 if n > 1 else 1
        density = m / max_edges if max_edges > 0 else 0.0

        return GraphStats(
            node_count=n,
            edge_count=m,
            avg_degree=avg_degree,
            max_degree=max_degree,
            min_degree=min_degree,
            density=density,
        )

    def remove_low_weight_edges(self, min_weight: int) -> int:
        """Remove edges below weight threshold.

        Args:
            min_weight: Minimum weight to keep edge

        Returns:
            Number of edges removed
        """
        removed = 0

        for node1 in list(self._adj.keys()):
            for node2 in list(self._adj[node1].keys()):
                if self._adj[node1][node2] < min_weight:
                    del self._adj[node1][node2]
                    removed += 1

        # Clean up empty nodes
        self._adj = defaultdict(lambda: defaultdict(int), {k: v for k, v in self._adj.items() if v})

        # Update edge count
        self._edge_count = len(self.edges())

        return removed // 2  # Divide by 2 (undirected)

    def to_adjacency_dict(self) -> Dict[str, Dict[str, int]]:
        """Export graph as adjacency dictionary.

        Returns:
            Dict mapping nodes to {neighbor: weight}
        """
        return {node: dict(neighbors) for node, neighbors in self._adj.items()}

    @classmethod
    def from_adjacency_dict(cls, adj_dict: Dict[str, Dict[str, int]]) -> "CooccurrenceGraph":
        """Create graph from adjacency dictionary.

        Args:
            adj_dict: Dict mapping nodes to {neighbor: weight}

        Returns:
            CooccurrenceGraph instance
        """
        graph = cls()

        for node1, neighbors in adj_dict.items():
            for node2, weight in neighbors.items():
                graph.add_cooccurrence(node1, node2, weight)

        return graph
