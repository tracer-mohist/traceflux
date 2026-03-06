# tests/test_associations.py
"""Tests for Associative Search."""

import pytest
from traceflux.associations import (
    AssociativeSearch,
    Association,
    AssociationResult,
    find_associations,
)
from traceflux.graph import CooccurrenceGraph


class TestAssociativeSearchBasic:
    """Basic associative search tests."""

    def test_empty_graph(self):
        """Search on empty graph returns no results."""
        graph = CooccurrenceGraph()
        search = AssociativeSearch(graph)
        result = search.find_associations("query")

        assert result.associations == []
        assert result.total_found == 0

    def test_nonexistent_query(self):
        """Query that doesn't exist returns no results."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("a", "b")

        search = AssociativeSearch(graph)
        result = search.find_associations("nonexistent")

        assert result.associations == []

    def test_simple_association(self):
        """Find direct associations."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("query", "assoc1")
        graph.add_cooccurrence("query", "assoc2")

        search = AssociativeSearch(graph)
        result = search.find_associations("query")

        assert result.total_found == 2
        patterns = [a.pattern for a in result.associations]
        assert "assoc1" in patterns
        assert "assoc2" in patterns


class TestAssociationDegrees:
    """Test degree of separation tracking."""

    def test_degree_1(self):
        """Direct neighbors are degree 1."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("a", "b")
        graph.add_cooccurrence("a", "c")

        search = AssociativeSearch(graph)
        result = search.find_associations("a")

        assert all(a.degree == 1 for a in result.associations)

    def test_degree_2(self):
        """Neighbors of neighbors are degree 2."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("a", "b")
        graph.add_cooccurrence("b", "c")

        search = AssociativeSearch(graph)
        result = search.find_associations("a")

        # b is degree 1, c is degree 2
        assoc_dict = {a.pattern: a.degree for a in result.associations}
        assert assoc_dict.get("b") == 1
        assert assoc_dict.get("c") == 2

    def test_max_degree_limit(self):
        """Respects max_degree parameter."""
        graph = CooccurrenceGraph()
        # Create chain: a-b-c-d-e
        for i in range(4):
            graph.add_cooccurrence(chr(ord("a") + i), chr(ord("a") + i + 1))

        search = AssociativeSearch(graph)
        result = search.find_associations("a", max_degree=2)

        # Should only find b (degree 1) and c (degree 2)
        assert all(a.degree <= 2 for a in result.associations)
        assert "d" not in [a.pattern for a in result.associations]


class TestAssociationScoring:
    """Test association scoring."""

    def test_score_with_pagerank(self):
        """PageRank affects association scores."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("query", "assoc1")
        graph.add_cooccurrence("query", "assoc2")

        pagerank = {
            "query": 0.3,
            "assoc1": 0.5,  # Higher PageRank
            "assoc2": 0.2,  # Lower PageRank
        }

        search = AssociativeSearch(graph, pagerank_scores=pagerank)
        result = search.find_associations("query")

        # assoc1 should have higher score due to higher PageRank
        scores = {a.pattern: a.score for a in result.associations}
        assert scores["assoc1"] > scores["assoc2"]

    def test_score_with_distance(self):
        """Closer associations have higher scores."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("query", "near")
        graph.add_cooccurrence("near", "far")

        search = AssociativeSearch(graph)
        result = search.find_associations("query")

        scores = {a.pattern: a.score for a in result.associations}
        assert scores["near"] > scores["far"]

    def test_lambda_parameter(self):
        """Lambda balances PageRank vs distance."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("query", "assoc1")
        graph.add_cooccurrence("query", "assoc2")

        pagerank = {
            "assoc1": 0.1,  # Low PageRank
            "assoc2": 0.9,  # High PageRank
        }

        # High lambda: PageRank dominates
        search_high = AssociativeSearch(graph, pagerank_scores=pagerank, lambda_param=0.9)
        result_high = search_high.find_associations("query")
        scores_high = {a.pattern: a.score for a in result_high.associations}

        # Low lambda: Distance dominates (both are degree 1, so similar)
        search_low = AssociativeSearch(graph, pagerank_scores=pagerank, lambda_param=0.1)
        result_low = search_low.find_associations("query")
        scores_low = {a.pattern: a.score for a in result_low.associations}

        # With high lambda, assoc2 should score much higher
        assert scores_high["assoc2"] > scores_high["assoc1"]


class TestAssociationPaths:
    """Test path tracking."""

    def test_path_tracking(self):
        """Associations include path from query."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("a", "b")
        graph.add_cooccurrence("b", "c")

        search = AssociativeSearch(graph)
        result = search.find_associations("a")

        assoc_c = next((a for a in result.associations if a.pattern == "c"), None)
        assert assoc_c is not None
        assert assoc_c.path == ["a", "b", "c"]

    def test_direct_path(self):
        """Direct associations have short paths."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("a", "b")

        search = AssociativeSearch(graph)
        result = search.find_associations("a")

        assoc_b = result.associations[0]
        assert assoc_b.path == ["a", "b"]


class TestMultiQuerySearch:
    """Test multi-query associations."""

    def test_merge_results(self):
        """Merge associations from multiple queries."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("q1", "shared")
        graph.add_cooccurrence("q2", "shared")
        graph.add_cooccurrence("q1", "only_q1")
        graph.add_cooccurrence("q2", "only_q2")

        search = AssociativeSearch(graph)
        result = search.find_multi_query_associations(["q1", "q2"])

        patterns = [a.pattern for a in result.associations]
        assert "shared" in patterns
        assert "only_q1" in patterns
        assert "only_q2" in patterns

    def test_boost_shared_associations(self):
        """Shared associations get score boost."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("q1", "shared")
        graph.add_cooccurrence("q2", "shared")
        graph.add_cooccurrence("q1", "unique")

        search = AssociativeSearch(graph)
        result = search.find_multi_query_associations(["q1", "q2"])

        # Shared should have higher score due to boost
        scores = {a.pattern: a.score for a in result.associations}
        assert scores["shared"] > scores["unique"]


class TestFindPaths:
    """Test path finding between nodes."""

    def test_find_path(self):
        """Find path between two nodes."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("a", "b")
        graph.add_cooccurrence("b", "c")
        graph.add_cooccurrence("c", "d")

        search = AssociativeSearch(graph)
        paths = search.get_association_paths("a", "d")

        assert len(paths) > 0
        assert paths[0] == ["a", "b", "c", "d"]

    def test_no_path(self):
        """Return empty list when no path exists."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("a", "b")
        graph.add_cooccurrence("c", "d")  # Disconnected

        search = AssociativeSearch(graph)
        paths = search.get_association_paths("a", "d")

        assert paths == []

    def test_same_node(self):
        """Path from node to itself."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("a", "b")

        search = AssociativeSearch(graph)
        paths = search.get_association_paths("a", "a")

        assert paths == [["a"]]


class TestConvenienceFunction:
    """Test find_associations convenience function."""

    def test_find_associations(self):
        """Convenience function works."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("query", "assoc1")
        graph.add_cooccurrence("query", "assoc2")

        results = find_associations(graph, "query")

        assert len(results) == 2
        patterns = [r[0] for r in results]
        assert "assoc1" in patterns
        assert "assoc2" in patterns


class TestAssociationEdgeCases:
    """Test edge cases."""

    def test_unicode_patterns(self):
        """Handle Unicode pattern names."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("查询", "关联 1")
        graph.add_cooccurrence("查询", "关联 2")

        search = AssociativeSearch(graph)
        result = search.find_associations("查询")

        assert len(result.associations) == 2

    def test_large_graph(self):
        """Handle large graphs efficiently."""
        graph = CooccurrenceGraph()

        # Create star graph with 100 leaves
        for i in range(100):
            graph.add_cooccurrence("center", f"leaf_{i}")

        search = AssociativeSearch(graph)
        result = search.find_associations("center", top_k=10)

        assert len(result.associations) == 10
        assert result.total_found == 100

    def test_cycle_handling(self):
        """Handle cycles in graph."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("a", "b")
        graph.add_cooccurrence("b", "c")
        graph.add_cooccurrence("c", "a")  # Creates cycle

        search = AssociativeSearch(graph)
        result = search.find_associations("a")

        # Should not infinite loop
        assert len(result.associations) == 2  # b and c
