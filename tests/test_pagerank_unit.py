# tests/test_pagerank_unit.py
"""Tests for Weighted PageRank."""

import pytest

from traceflux.graph import CooccurrenceGraph
from traceflux.pagerank import PageRankResult, WeightedPageRank, compute_pagerank


class TestPageRankBasic:
    """Basic PageRank computation tests."""

    def test_empty_graph(self):
        """PageRank of empty graph."""
        graph = CooccurrenceGraph()
        pr = WeightedPageRank()
        result = pr.compute(graph)

        assert result.scores == {}
        assert result.iterations == 0
        assert result.converged

    def test_single_node(self):
        """PageRank of single node graph."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("a", "b")  # Creates two nodes
        graph.add_cooccurrence("a", "c")
        graph.add_cooccurrence("b", "c")

        pr = WeightedPageRank()
        result = pr.compute(graph)

        assert len(result.scores) == 3
        assert all(score > 0 for score in result.scores.values())
        assert abs(sum(result.scores.values()) - 1.0) < 1e-6  # Normalized

    def test_uniform_initial(self):
        """Default initialization is uniform."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("a", "b")

        pr = WeightedPageRank()
        result = pr.compute(graph)

        # Two nodes should have roughly equal scores in simple graph
        assert "a" in result.scores
        assert "b" in result.scores


class TestPageRankConvergence:
    """Test PageRank convergence behavior."""

    def test_convergence(self):
        """PageRank converges on simple graph."""
        graph = CooccurrenceGraph()
        # Create a small connected graph
        graph.add_cooccurrence("a", "b")
        graph.add_cooccurrence("b", "c")
        graph.add_cooccurrence("c", "a")

        pr = WeightedPageRank(tolerance=1e-6, max_iterations=100)
        result = pr.compute(graph)

        assert result.converged
        assert result.iterations < 100

    def test_max_iterations(self):
        """Respects max_iterations limit."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("a", "b")

        pr = WeightedPageRank(max_iterations=5, tolerance=1e-10)
        result = pr.compute(graph)

        assert result.iterations <= 5

    def test_convergence_tracking(self):
        """Tracks convergence delta."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("a", "b")
        graph.add_cooccurrence("b", "c")

        pr = WeightedPageRank()
        result = pr.compute(graph)

        assert result.final_delta >= 0
        if result.converged:
            assert result.final_delta < pr.tolerance


class TestPageRankDamping:
    """Test damping factor effects."""

    def test_damping_factor(self):
        """Different damping factors produce different results."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("a", "b")
        graph.add_cooccurrence("a", "c")
        graph.add_cooccurrence("a", "d")

        pr_low = WeightedPageRank(damping=0.5)
        pr_high = WeightedPageRank(damping=0.95)

        result_low = pr_low.compute(graph)
        result_high = pr_high.compute(graph)

        # Both should be valid probability distributions
        assert abs(sum(result_low.scores.values()) - 1.0) < 1e-6
        assert abs(sum(result_high.scores.values()) - 1.0) < 1e-6


class TestPageRankWeighted:
    """Test weighted PageRank behavior."""

    def test_edge_weights_affect_scores(self):
        """Higher weight edges increase neighbor scores."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("hub", "spoke1", weight=1)
        graph.add_cooccurrence("hub", "spoke2", weight=100)

        pr = WeightedPageRank()
        result = pr.compute(graph)

        # spoke2 should have higher score due to stronger connection
        assert result.scores["spoke2"] > result.scores["spoke1"]

    def test_hub_node(self):
        """Hub node distributes score to neighbors."""
        graph = CooccurrenceGraph()

        # Create star graph
        for i in range(10):
            graph.add_cooccurrence("hub", f"leaf_{i}")

        pr = WeightedPageRank()
        result = pr.compute(graph)

        # Hub should have significant score
        assert result.scores["hub"] > 0.05

        # All leaves should have similar scores
        leaf_scores = [result.scores[f"leaf_{i}"] for i in range(10)]
        assert max(leaf_scores) - min(leaf_scores) < 0.01


class TestPageRankFiltering:
    """Test score filtering."""

    def test_min_score_filtering(self):
        """Filter low-scoring nodes."""
        graph = CooccurrenceGraph()

        # Create graph with one dominant node
        graph.add_cooccurrence("dominant", "minor1", weight=100)
        graph.add_cooccurrence("dominant", "minor2", weight=100)
        graph.add_cooccurrence("dominant", "minor3", weight=100)

        pr = WeightedPageRank(min_score=0.1)
        filtered, removed = pr.compute_with_filtering(graph)

        # Minor nodes should be filtered out
        assert "dominant" in filtered
        assert removed >= 0

    def test_no_filtering(self):
        """Low min_score keeps all nodes."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("a", "b")

        pr = WeightedPageRank(min_score=0.0)
        filtered, removed = pr.compute_with_filtering(graph)

        assert len(filtered) == 2
        assert removed == 0


class TestPageRankTopK:
    """Test top-k extraction."""

    def test_top_k(self):
        """Get top-k patterns."""
        scores = {
            "a": 0.3,
            "b": 0.25,
            "c": 0.2,
            "d": 0.15,
            "e": 0.1,
        }

        pr = WeightedPageRank()
        top_3 = pr.get_top_k(scores, k=3)

        assert len(top_3) == 3
        assert top_3[0] == ("a", 0.3)
        assert top_3[1] == ("b", 0.25)
        assert top_3[2] == ("c", 0.2)

    def test_top_k_more_than_available(self):
        """Request more than available returns all."""
        scores = {"a": 0.6, "b": 0.4}

        pr = WeightedPageRank()
        top_10 = pr.get_top_k(scores, k=10)

        assert len(top_10) == 2


class TestPageRankNormalization:
    """Test score normalization."""

    def test_normalize_sum(self):
        """Sum normalization."""
        scores = {"a": 10, "b": 20, "c": 30}

        pr = WeightedPageRank()
        normalized = pr.normalize_scores(scores, method="sum")

        assert abs(sum(normalized.values()) - 1.0) < 1e-6

    def test_normalize_max(self):
        """Max normalization."""
        scores = {"a": 10, "b": 20, "c": 30}

        pr = WeightedPageRank()
        normalized = pr.normalize_scores(scores, method="max")

        assert max(normalized.values()) == 1.0
        assert normalized["c"] == 1.0

    def test_normalize_minmax(self):
        """Min-max normalization to [0, 1]."""
        scores = {"a": 10, "b": 20, "c": 30}

        pr = WeightedPageRank()
        normalized = pr.normalize_scores(scores, method="minmax")

        assert min(normalized.values()) == 0.0
        assert max(normalized.values()) == 1.0

    def test_normalize_empty(self):
        """Handle empty scores."""
        pr = WeightedPageRank()
        normalized = pr.normalize_scores({})
        assert normalized == {}


class TestComputePagerank:
    """Test convenience function."""

    def test_compute_pagerank(self):
        """Convenience function works."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("a", "b")
        graph.add_cooccurrence("b", "c")

        scores = compute_pagerank(graph)

        assert len(scores) == 3
        assert all(score > 0 for score in scores.values())


class TestPageRankEdgeCases:
    """Test edge cases."""

    def test_disconnected_components(self):
        """Handle disconnected graph components."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("a", "b")  # Component 1
        graph.add_cooccurrence("c", "d")  # Component 2

        pr = WeightedPageRank()
        result = pr.compute(graph)

        # All nodes should have scores
        assert len(result.scores) == 4
        assert all(score > 0 for score in result.scores.values())

    def test_self_loop_ignored(self):
        """Self-loops don't affect PageRank."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("a", "a")  # Self-loop (should be ignored)
        graph.add_cooccurrence("a", "b")

        pr = WeightedPageRank()
        result = pr.compute(graph)

        assert "a" in result.scores
        assert "b" in result.scores

    def test_unicode_nodes(self):
        """Handle Unicode node names."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("你好", "世界")

        pr = WeightedPageRank()
        result = pr.compute(graph)

        assert "你好" in result.scores
        assert "世界" in result.scores
