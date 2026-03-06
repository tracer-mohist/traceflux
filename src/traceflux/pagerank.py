# src/traceflux/pagerank.py
"""Weighted PageRank - Rank patterns by importance.

Implements PageRank algorithm for co-occurrence graphs:
PR(v) = (1-d)/N + d * sum_{u} PR(u) * w(u,v) / sum_{t} w(u,t)

Where:
- d: Damping factor (typically 0.85)
- N: Total number of nodes
- w(u,v): Weight of edge from u to v
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class PageRankResult:
    """PageRank computation result."""

    scores: Dict[str, float]
    iterations: int
    converged: bool
    final_delta: float


class WeightedPageRank:
    """Weighted PageRank for co-occurrence graphs.

    Ranks patterns based on their importance in the graph.
    Higher weight edges contribute more to the rank.

    Example:
        >>> pr = WeightedPageRank(damping=0.85)
        >>> result = pr.compute(graph)
        >>> top_patterns = sorted(result.scores.items(), key=lambda x: -x[1])[:10]
    """

    def __init__(
        self,
        damping: float = 0.85,
        max_iterations: int = 100,
        tolerance: float = 1e-6,
        min_score: float = 0.001
    ):
        """Initialize PageRank calculator.

        Args:
            damping: Damping factor (0-1). Higher = more weight to graph structure.
            max_iterations: Maximum iterations before stopping.
            tolerance: Convergence threshold (sum of score changes).
            min_score: Minimum score to keep a pattern (filtering).
        """
        self.damping = damping
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.min_score = min_score

    def compute(
        self,
        graph: "CooccurrenceGraph",
        initial_scores: Optional[Dict[str, float]] = None
    ) -> PageRankResult:
        """Compute PageRank scores for all nodes.

        Uses power iteration method.

        Args:
            graph: Co-occurrence graph
            initial_scores: Optional initial scores (default: uniform)

        Returns:
            PageRankResult with scores and convergence info
        """
        nodes = graph.nodes()
        n = len(nodes)

        if n == 0:
            return PageRankResult(
                scores={},
                iterations=0,
                converged=True,
                final_delta=0.0
            )

        # Initialize scores uniformly
        scores: Dict[str, float] = {}
        if initial_scores:
            # Use provided initial scores (normalize if needed)
            total = sum(initial_scores.values())
            if total > 0:
                scores = {node: initial_scores.get(node, 1.0 / n) for node in nodes}
                # Normalize
                score_sum = sum(scores.values())
                scores = {k: v / score_sum for k, v in scores.items()}
            else:
                scores = {node: 1.0 / n for node in nodes}
        else:
            scores = {node: 1.0 / n for node in nodes}

        # Get adjacency data
        adj_dict = graph.to_adjacency_dict()

        # Precompute out-weights for each node
        out_weights: Dict[str, float] = {}
        for node in nodes:
            out_weights[node] = sum(adj_dict.get(node, {}).values())

        # Power iteration
        converged = False
        final_delta = 0.0
        iteration = 0

        for iteration in range(1, self.max_iterations + 1):
            new_scores: Dict[str, float] = {}

            # Compute new scores
            for node in nodes:
                # Base score from random jump
                score = (1.0 - self.damping) / n

                # Add contribution from neighbors
                neighbors = adj_dict.get(node, {})
                for neighbor, weight in neighbors.items():
                    if out_weights[neighbor] > 0:
                        score += (self.damping *
                                  scores[neighbor] *
                                  weight /
                                  out_weights[neighbor])

                new_scores[node] = score

            # Check convergence
            delta = sum(abs(new_scores[node] - scores[node]) for node in nodes)
            final_delta = delta

            scores = new_scores

            if delta < self.tolerance:
                converged = True
                break

        # Normalize final scores
        total = sum(scores.values())
        if total > 0:
            scores = {k: v / total for k, v in scores.items()}

        return PageRankResult(
            scores=scores,
            iterations=iteration,
            converged=converged,
            final_delta=final_delta
        )

    def compute_with_filtering(
        self,
        graph: "CooccurrenceGraph"
    ) -> Tuple[Dict[str, float], int]:
        """Compute PageRank and filter low-scoring nodes.

        Iteratively removes nodes below min_score threshold.

        Args:
            graph: Co-occurrence graph

        Returns:
            Tuple of (filtered_scores, removed_count)
        """
        result = self.compute(graph)
        scores = result.scores

        # Filter low-scoring nodes
        filtered = {
            node: score
            for node, score in scores.items()
            if score >= self.min_score
        }

        removed = len(scores) - len(filtered)

        return filtered, removed

    def get_top_k(
        self,
        scores: Dict[str, float],
        k: int = 10
    ) -> List[Tuple[str, float]]:
        """Get top-k patterns by score.

        Args:
            scores: PageRank scores
            k: Number of top patterns to return

        Returns:
            List of (pattern, score) tuples, sorted by score descending
        """
        sorted_scores = sorted(scores.items(), key=lambda x: -x[1])
        return sorted_scores[:k]

    def normalize_scores(
        self,
        scores: Dict[str, float],
        method: str = "sum"
    ) -> Dict[str, float]:
        """Normalize scores using specified method.

        Args:
            scores: Raw scores
            method: Normalization method ("sum", "max", "minmax")

        Returns:
            Normalized scores
        """
        if not scores:
            return {}

        if method == "sum":
            # Normalize to sum to 1
            total = sum(scores.values())
            if total > 0:
                return {k: v / total for k, v in scores.items()}
            return scores

        elif method == "max":
            # Normalize to max = 1
            max_score = max(scores.values())
            if max_score > 0:
                return {k: v / max_score for k, v in scores.items()}
            return scores

        elif method == "minmax":
            # Normalize to [0, 1] range
            min_score = min(scores.values())
            max_score = max(scores.values())
            range_score = max_score - min_score
            if range_score > 0:
                return {k: (v - min_score) / range_score for k, v in scores.items()}
            return scores

        else:
            raise ValueError(f"Unknown normalization method: {method}")


def compute_pagerank(
    graph: "CooccurrenceGraph",
    damping: float = 0.85,
    max_iterations: int = 100,
    tolerance: float = 1e-6
) -> Dict[str, float]:
    """Convenience function to compute PageRank.

    Args:
        graph: Co-occurrence graph
        damping: Damping factor
        max_iterations: Maximum iterations
        tolerance: Convergence threshold

    Returns:
        Dict mapping patterns to PageRank scores
    """
    pr = WeightedPageRank(
        damping=damping,
        max_iterations=max_iterations,
        tolerance=tolerance
    )
    result = pr.compute(graph)
    return result.scores
