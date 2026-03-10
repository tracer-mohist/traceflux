# tests/test_graph_unit.py
"""Tests for Co-occurrence Graph."""

import pytest

from traceflux.graph import CooccurrenceGraph, GraphStats


class TestCooccurrenceGraphBasic:
    """Basic graph operations tests."""

    def setup_method(self):
        """Set up test fixtures."""
        self.graph = CooccurrenceGraph()

    def test_empty_graph(self):
        """Empty graph has no nodes or edges."""
        assert self.graph.node_count() == 0
        assert self.graph.edge_count() == 0
        assert self.graph.nodes() == []
        assert self.graph.edges() == []

    def test_add_cooccurrence(self):
        """Add single co-occurrence edge."""
        self.graph.add_cooccurrence("proxy", "config")

        assert self.graph.has_node("proxy")
        assert self.graph.has_node("config")
        assert self.graph.has_edge("proxy", "config")
        assert self.graph.has_edge("config", "proxy")

    def test_add_cooccurrence_weight(self):
        """Add co-occurrence with weight."""
        self.graph.add_cooccurrence("proxy", "config", weight=5)

        assert self.graph.get_weight("proxy", "config") == 5
        assert self.graph.get_weight("config", "proxy") == 5

    def test_add_cooccurrence_accumulate(self):
        """Multiple additions accumulate weight."""
        self.graph.add_cooccurrence("proxy", "config", weight=2)
        self.graph.add_cooccurrence("proxy", "config", weight=3)

        assert self.graph.get_weight("proxy", "config") == 5

    def test_no_self_loops(self):
        """Self-loops are not added."""
        self.graph.add_cooccurrence("proxy", "proxy")

        assert not self.graph.has_edge("proxy", "proxy")
        assert self.graph.edge_count() == 0


class TestCooccurrenceGraphDocument:
    """Test document co-occurrence processing."""

    def setup_method(self):
        """Set up test fixtures."""
        self.graph = CooccurrenceGraph()

    def test_add_document_cooccurrences(self):
        """Add co-occurrences from pattern sequence."""
        patterns = ["proxy", "config", "settings"]
        self.graph.add_document_cooccurrences(patterns)

        # Adjacent pairs should be connected
        assert self.graph.has_edge("proxy", "config")
        assert self.graph.has_edge("config", "settings")

    def test_add_document_window_size(self):
        """Window size affects co-occurrence."""
        patterns = ["a", "b", "c", "d"]

        # Default window (2): connects adjacent and next-to-adjacent
        self.graph.add_document_cooccurrences(patterns, window_size=2)

        assert self.graph.has_edge("a", "b")  # adjacent
        assert self.graph.has_edge("a", "c")  # within window
        assert not self.graph.has_edge("a", "d")  # outside window

    def test_add_document_single_pattern(self):
        """Single pattern produces no co-occurrences."""
        patterns = ["single"]
        self.graph.add_document_cooccurrences(patterns)

        assert self.graph.edge_count() == 0

    def test_add_document_empty(self):
        """Empty pattern list produces no co-occurrences."""
        self.graph.add_document_cooccurrences([])

        assert self.graph.edge_count() == 0


class TestCooccurrenceGraphNeighbors:
    """Test neighbor queries."""

    def setup_method(self):
        """Set up test fixtures."""
        self.graph = CooccurrenceGraph()
        # Create a small graph
        self.graph.add_cooccurrence("a", "b")
        self.graph.add_cooccurrence("a", "c")
        self.graph.add_cooccurrence("a", "d")
        self.graph.add_cooccurrence("b", "c")

    def test_neighbors(self):
        """Get neighbors of a node."""
        neighbors = self.graph.neighbors("a")

        assert len(neighbors) == 3
        assert "b" in neighbors
        assert "c" in neighbors
        assert "d" in neighbors

    def test_neighbors_nonexistent(self):
        """Get neighbors of non-existent node."""
        neighbors = self.graph.neighbors("z")

        assert neighbors == []

    def test_degree(self):
        """Get degree of a node."""
        assert self.graph.degree("a") == 3
        assert self.graph.degree("b") == 2
        assert self.graph.degree("d") == 1

    def test_weighted_degree(self):
        """Get weighted degree."""
        self.graph.add_cooccurrence("a", "b", weight=5)

        # a has edges to b (weight 6), c (weight 1), d (weight 1)
        assert self.graph.weighted_degree("a") == 8


class TestCooccurrenceGraphEdges:
    """Test edge operations."""

    def setup_method(self):
        """Set up test fixtures."""
        self.graph = CooccurrenceGraph()

    def test_edges_undirected(self):
        """Edges appear once in undirected graph."""
        self.graph.add_cooccurrence("a", "b")
        self.graph.add_cooccurrence("b", "a")  # Same edge

        edges = self.graph.edges()

        # Should appear only once
        assert len(edges) == 1
        assert ("a", "b", 2) in edges or ("b", "a", 2) in edges

    def test_edges_with_weights(self):
        """Edges include weights."""
        self.graph.add_cooccurrence("a", "b", weight=5)

        edges = self.graph.edges()

        assert len(edges) == 1
        edge = edges[0]
        assert edge[2] == 5  # weight


class TestCooccurrenceGraphStats:
    """Test graph statistics."""

    def setup_method(self):
        """Set up test fixtures."""
        self.graph = CooccurrenceGraph()

    def test_stats_empty(self):
        """Statistics of empty graph."""
        stats = self.graph.get_stats()

        assert stats.node_count == 0
        assert stats.edge_count == 0
        assert stats.avg_degree == 0.0
        assert stats.density == 0.0

    def test_stats_simple(self):
        """Statistics of simple graph."""
        self.graph.add_cooccurrence("a", "b")
        self.graph.add_cooccurrence("b", "c")
        self.graph.add_cooccurrence("c", "a")

        stats = self.graph.get_stats()

        assert stats.node_count == 3
        assert stats.edge_count == 3
        assert stats.avg_degree == 2.0  # Each node has 2 neighbors

    def test_stats_density(self):
        """Graph density calculation."""
        # Complete graph K4: 4 nodes, 6 edges
        nodes = ["a", "b", "c", "d"]
        for i, n1 in enumerate(nodes):
            for n2 in nodes[i + 1 :]:  # noqa: E203
                self.graph.add_cooccurrence(n1, n2)

        stats = self.graph.get_stats()

        assert stats.node_count == 4
        assert stats.edge_count == 6
        assert stats.density == 1.0  # Complete graph


class TestCooccurrenceGraphFiltering:
    """Test edge filtering."""

    def setup_method(self):
        """Set up test fixtures."""
        self.graph = CooccurrenceGraph()

    def test_remove_low_weight_edges(self):
        """Remove edges below threshold."""
        self.graph.add_cooccurrence("a", "b", weight=1)
        self.graph.add_cooccurrence("a", "c", weight=5)
        self.graph.add_cooccurrence("a", "d", weight=10)

        removed = self.graph.remove_low_weight_edges(min_weight=5)

        assert removed == 1  # One edge removed
        assert not self.graph.has_edge("a", "b")
        assert self.graph.has_edge("a", "c")
        assert self.graph.has_edge("a", "d")

    def test_remove_all_edges(self):
        """Remove all edges with high threshold."""
        self.graph.add_cooccurrence("a", "b", weight=1)

        self.graph.remove_low_weight_edges(min_weight=100)

        assert self.graph.edge_count() == 0


class TestCooccurrenceGraphPersistence:
    """Test graph export/import."""

    def setup_method(self):
        """Set up test fixtures."""
        self.graph = CooccurrenceGraph()

    def test_to_adjacency_dict(self):
        """Export to adjacency dictionary."""
        self.graph.add_cooccurrence("a", "b", weight=5)
        self.graph.add_cooccurrence("a", "c", weight=3)

        adj_dict = self.graph.to_adjacency_dict()

        assert "a" in adj_dict
        assert adj_dict["a"]["b"] == 5
        assert adj_dict["a"]["c"] == 3

    def test_from_adjacency_dict(self):
        """Import from adjacency dictionary."""
        adj_dict = {
            "a": {"b": 5, "c": 3},
            "b": {"a": 5},
            "c": {"a": 3},
        }

        graph = CooccurrenceGraph.from_adjacency_dict(adj_dict)

        assert graph.has_node("a")
        assert graph.has_node("b")
        assert graph.has_node("c")
        # Weight is doubled because graph is undirected (a->b and b->a both add)
        assert graph.get_weight("a", "b") == 10

    def test_roundtrip(self):
        """Export and import preserves graph."""
        self.graph.add_cooccurrence("a", "b", weight=5)
        self.graph.add_cooccurrence("a", "c", weight=3)
        self.graph.add_cooccurrence("b", "c", weight=2)

        adj_dict = self.graph.to_adjacency_dict()
        restored = CooccurrenceGraph.from_adjacency_dict(adj_dict)

        assert restored.node_count() == self.graph.node_count()
        assert restored.edge_count() == self.graph.edge_count()

        for node in self.graph.nodes():
            assert restored.degree(node) == self.graph.degree(node)


class TestCooccurrenceGraphEdgeCases:
    """Test edge cases."""

    def setup_method(self):
        """Set up test fixtures."""
        self.graph = CooccurrenceGraph()

    def test_unicode_nodes(self):
        """Handle Unicode pattern names."""
        self.graph.add_cooccurrence("你好", "世界")

        assert self.graph.has_node("你好")
        assert self.graph.has_edge("你好", "世界")

    def test_special_characters(self):
        """Handle special characters in patterns."""
        self.graph.add_cooccurrence("proxy-config", "settings_test")

        assert self.graph.has_edge("proxy-config", "settings_test")

    def test_many_edges(self):
        """Handle large number of edges."""
        # Create star graph with 100 leaves
        center = "center"
        for i in range(100):
            self.graph.add_cooccurrence(center, f"leaf_{i}")

        assert self.graph.node_count() == 101
        assert self.graph.edge_count() == 100
        assert self.graph.degree(center) == 100
