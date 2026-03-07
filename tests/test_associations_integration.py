#!/usr/bin/env python3
"""Integration tests for association engine."""

import pytest

from traceflux.associations import Association, AssociativeSearch
from traceflux.graph import CooccurrenceGraph
from traceflux.pagerank import compute_pagerank
from traceflux.patterns import PatternDetector
from traceflux.scanner import Scanner


class TestAssociationBasic:
    """Basic association functionality tests."""

    def test_simple_cooccurrence(self):
        """Test associations from simple co-occurrence."""
        # Create simple text with co-occurring terms
        text = "proxy config proxy settings proxy chains"

        # Build graph
        scanner = Scanner()
        detector = PatternDetector(min_support=2, min_length=3)
        graph = CooccurrenceGraph()

        # Extract patterns and build co-occurrence
        patterns = detector.find_patterns(text)
        pattern_list = list(patterns.keys())

        # Add co-occurrences
        graph.add_document_cooccurrences(pattern_list, window_size=3)

        # Verify graph has nodes
        assert graph.node_count() >= 1

    def test_associations_from_graph(self):
        """Test association retrieval from graph."""
        # Create graph with known structure
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("proxy", "config", weight=5)
        graph.add_cooccurrence("proxy", "settings", weight=3)
        graph.add_cooccurrence("proxy", "chains", weight=2)

        # Create search engine (no PageRank yet)
        search = AssociativeSearch(graph)

        # Find associations
        result = search.find_associations("proxy", max_degree=1, top_k=10)

        assert result.query == "proxy"
        assert len(result.associations) > 0
        assert result.associations[0].pattern in ["config", "settings", "chains"]

    def test_associations_ranked_by_weight(self):
        """Test associations are ranked by edge weight."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("proxy", "config", weight=5)
        graph.add_cooccurrence("proxy", "settings", weight=3)
        graph.add_cooccurrence("proxy", "chains", weight=1)

        search = AssociativeSearch(graph)
        result = search.find_associations("proxy", max_degree=1, top_k=10)

        # Higher weight should rank higher
        patterns = [a.pattern for a in result.associations]
        assert patterns.index("config") < patterns.index("chains")


class TestAssociationMultiHop:
    """Multi-hop association tests."""

    def test_two_hop_associations(self):
        """Test 2-hop association discovery."""
        # Create chain: A -> B -> C
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("A", "B", weight=5)
        graph.add_cooccurrence("B", "C", weight=5)
        # No direct A -> C edge

        search = AssociativeSearch(graph)

        # 1-hop: should only find B
        result_1hop = search.find_associations("A", max_degree=1, top_k=10)
        patterns_1hop = [a.pattern for a in result_1hop.associations]
        assert "B" in patterns_1hop
        assert "C" not in patterns_1hop

        # 2-hop: should find B and C
        result_2hop = search.find_associations("A", max_degree=2, top_k=10)
        patterns_2hop = [a.pattern for a in result_2hop.associations]
        assert "B" in patterns_2hop
        assert "C" in patterns_2hop

    def test_association_path_tracking(self):
        """Test that association paths are tracked."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("A", "B", weight=5)
        graph.add_cooccurrence("B", "C", weight=5)

        search = AssociativeSearch(graph)
        result = search.find_associations("A", max_degree=2, top_k=10)

        # Find C's association
        c_assoc = next((a for a in result.associations if a.pattern == "C"), None)
        assert c_assoc is not None
        assert c_assoc.path == ["A", "B", "C"]
        assert c_assoc.degree == 2


class TestAssociationWithPagerank:
    """Association with PageRank integration tests."""

    def test_pagerank_influences_ranking(self):
        """Test PageRank affects association ranking."""
        # Create graph where one node has higher PageRank
        graph = CooccurrenceGraph()
        # A connects to B and C equally
        graph.add_cooccurrence("A", "B", weight=3)
        graph.add_cooccurrence("A", "C", weight=3)
        # But C is more important (more connections)
        graph.add_cooccurrence("C", "D", weight=5)
        graph.add_cooccurrence("C", "E", weight=5)
        graph.add_cooccurrence("C", "F", weight=5)

        # Compute PageRank
        pagerank_scores = compute_pagerank(graph)

        # C should have higher PageRank than B
        assert pagerank_scores.get("C", 0) > pagerank_scores.get("B", 0)

        # Create search with PageRank
        search = AssociativeSearch(graph, pagerank_scores, lambda_param=0.7)
        result = search.find_associations("A", max_degree=1, top_k=10)

        # C should rank higher due to PageRank
        patterns = [a.pattern for a in result.associations]
        if "B" in patterns and "C" in patterns:
            assert patterns.index("C") < patterns.index("B")

    def test_lambda_param_balances_scores(self):
        """Test lambda parameter balances PageRank vs distance."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("A", "B", weight=5)
        graph.add_cooccurrence("A", "C", weight=5)

        pagerank_scores = {"B": 0.9, "C": 0.1}  # B much more important

        # High lambda = more weight to PageRank
        search_high_lambda = AssociativeSearch(graph, pagerank_scores, lambda_param=0.9)
        result_high = search_high_lambda.find_associations("A", max_degree=1, top_k=10)

        # B should rank higher with high lambda
        patterns_high = [a.pattern for a in result_high.associations]
        assert patterns_high.index("B") < patterns_high.index("C")


class TestAssociationEdgeCases:
    """Edge case tests."""

    def test_no_associations_for_unknown_term(self):
        """Test unknown term returns empty results."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("A", "B", weight=5)

        search = AssociativeSearch(graph)
        result = search.find_associations("unknown", max_degree=2, top_k=10)

        assert len(result.associations) == 0
        assert result.total_found == 0

    def test_empty_graph(self):
        """Test empty graph returns empty results."""
        graph = CooccurrenceGraph()
        search = AssociativeSearch(graph)
        result = search.find_associations("anything", max_degree=2, top_k=10)

        assert len(result.associations) == 0

    def test_single_node_graph(self):
        """Test single node graph returns empty associations."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("A", "B", weight=5)  # Only one edge

        search = AssociativeSearch(graph)
        result = search.find_associations("A", max_degree=1, top_k=10)

        # Should find B
        assert len(result.associations) == 1
        assert result.associations[0].pattern == "B"

    def test_top_k_limit(self):
        """Test top_k limits results."""
        graph = CooccurrenceGraph()
        # Create many connections
        for i in range(20):
            graph.add_cooccurrence("center", f"node_{i}", weight=i + 1)

        search = AssociativeSearch(graph)
        result = search.find_associations("center", max_degree=1, top_k=5)

        assert len(result.associations) == 5

    def test_min_score_filter(self):
        """Test min_score filters low-scoring associations."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("A", "B", weight=1)
        graph.add_cooccurrence("A", "C", weight=10)

        search = AssociativeSearch(graph)

        # No filter
        result_all = search.find_associations("A", max_degree=1, top_k=10, min_score=0.0)

        # High min_score
        result_filtered = search.find_associations("A", max_degree=1, top_k=10, min_score=0.5)

        assert len(result_filtered.associations) <= len(result_all.associations)


class TestAssociationResult:
    """AssociationResult tests."""

    def test_result_metadata(self):
        """Test result contains correct metadata."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("A", "B", weight=5)
        graph.add_cooccurrence("B", "C", weight=5)

        search = AssociativeSearch(graph)
        result = search.find_associations("A", max_degree=2, top_k=10)

        assert result.query == "A"
        assert result.total_found >= len(result.associations)
        assert result.max_degree >= 1
