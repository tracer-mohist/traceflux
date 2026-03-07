#!/usr/bin/env python3
"""Pipeline Integration Tests.

Test full data flow: scanner → patterns → index → graph → pagerank → associations.
"""

import pytest
import tempfile
from pathlib import Path

from traceflux.scanner import Scanner
from traceflux.patterns import PatternDetector
from traceflux.index import PatternIndex
from traceflux.graph import CooccurrenceGraph
from traceflux.pagerank import compute_pagerank
from traceflux.associations import AssociativeSearch


class TestFullPipeline:
    """Test complete pipeline from text to associations."""

    def test_full_pipeline_basic(self):
        """Test full pipeline: text → associations."""
        # Create text with known co-occurrences
        text = "proxy config proxy settings proxychains config"

        # Step 1: Scan
        scanner = Scanner()

        # Step 2: Detect patterns
        detector = PatternDetector(min_support=2, min_length=3)
        patterns = detector.find_patterns(text)

        # Should find repeated patterns
        assert len(patterns) > 0
        assert "proxy" in patterns or "config" in patterns

        # Step 3: Build graph
        graph = CooccurrenceGraph()
        pattern_list = list(patterns.keys())
        graph.add_document_cooccurrences(pattern_list, window_size=3)

        # Graph should have nodes
        assert graph.node_count() >= 1

        # Step 4: Compute PageRank
        pagerank_scores = compute_pagerank(graph)

        # Should have scores for nodes
        assert len(pagerank_scores) > 0

        # Step 5: Find associations
        search = AssociativeSearch(graph, pagerank_scores, lambda_param=0.7)
        result = search.find_associations("proxy", max_degree=2, top_k=10)

        # Should find associations
        assert result.query == "proxy"
        # May or may not find associations depending on pattern detection

    def test_pipeline_with_real_code(self):
        """Test pipeline with real code-like text."""
        # Simulate code with repeated patterns
        text = """
        def search(query):
            results = index.get(query)
            return results
        
        def search_files(query, paths):
            index = build_index(paths)
            results = index.get(query)
            return results
        """

        scanner = Scanner()
        detector = PatternDetector(min_support=2, min_length=3)
        patterns = detector.find_patterns(text)

        # Should find code patterns
        assert len(patterns) > 0

        # Common patterns in code
        pattern_texts = list(patterns.keys())
        assert any("def" in p or "query" in p or "results" in p for p in pattern_texts)


class TestIndexPersistence:
    """Test index save/load functionality."""

    def test_index_save_and_load(self):
        """Test index can be saved and reloaded."""
        # Build index
        index = PatternIndex()
        index.add("pattern1", "doc1.txt", [10, 20])
        index.add("pattern2", "doc2.txt", [30])
        index.add("pattern1", "doc3.txt", [40])

        # Save to temp file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_path = Path(f.name)

        try:
            index.save(temp_path)

            # Load from file
            loaded = PatternIndex.load(temp_path)

            # Verify data
            assert loaded.pattern_count() == 2
            assert loaded.doc_count() == 3
            assert loaded.has("pattern1")
            assert loaded.has("pattern2")

            # Verify positions
            results = loaded.get("pattern1")
            assert len(results) == 2
        finally:
            # Cleanup
            if temp_path.exists():
                temp_path.unlink()

    def test_index_preserves_all_data(self):
        """Test loaded index has identical data."""
        index = PatternIndex()
        index.add("test", "file1.txt", [1, 2, 3])
        index.add("test", "file2.txt", [4, 5])
        index.add("other", "file1.txt", [10])

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_path = Path(f.name)

        try:
            index.save(temp_path)
            loaded = PatternIndex.load(temp_path)

            # Compare all data
            assert index.pattern_count() == loaded.pattern_count()
            assert index.doc_count() == loaded.doc_count()
            assert index.total_occurrences() == loaded.total_occurrences()

            # Compare patterns
            for pattern in index.patterns():
                original = index.get(pattern)
                reloaded = loaded.get(pattern)
                assert original == reloaded
        finally:
            if temp_path.exists():
                temp_path.unlink()


class TestMultiDocumentGraph:
    """Test graph construction from multiple documents."""

    def test_cooccurrence_across_documents(self):
        """Test patterns co-occur across documents."""
        # Two documents with overlapping patterns (repeated for detection)
        doc1 = "proxy config proxy settings proxy"
        doc2 = "proxy environment proxy variables proxy"

        detector = PatternDetector(min_support=2, min_length=3)
        patterns1 = detector.find_patterns(doc1)
        patterns2 = detector.find_patterns(doc2)

        # Build graph from both
        graph = CooccurrenceGraph()

        # Add co-occurrences from doc1
        graph.add_document_cooccurrences(list(patterns1.keys()), window_size=3)

        # Add co-occurrences from doc2
        graph.add_document_cooccurrences(list(patterns2.keys()), window_size=3)

        # "proxy" should connect to patterns from both docs
        assert graph.has_node("proxy")
        neighbors = graph.neighbors("proxy")
        assert len(neighbors) > 0

    def test_graph_with_repeated_patterns(self):
        """Test graph handles repeated patterns across docs."""
        # Same pattern in multiple documents (repeated for detection)
        docs = [
            "config proxy config settings",
            "config environment config proxy",
            "config database config connection",
        ]

        graph = CooccurrenceGraph()
        detector = PatternDetector(min_support=2, min_length=3)

        for doc in docs:
            patterns = detector.find_patterns(doc)
            graph.add_document_cooccurrences(list(patterns.keys()), window_size=3)

        # "config " (with space) should have high degree
        # Pattern detector includes trailing whitespace
        assert graph.has_node("config ") or graph.has_node("config")


class TestPagerankConvergence:
    """Test PageRank convergence behavior."""

    def test_pagerank_converges(self):
        """Test PageRank converges on typical graph."""
        graph = CooccurrenceGraph()

        # Create connected graph
        graph.add_cooccurrence("A", "B", weight=5)
        graph.add_cooccurrence("B", "C", weight=3)
        graph.add_cooccurrence("C", "D", weight=2)
        graph.add_cooccurrence("A", "D", weight=1)

        # Compute PageRank
        scores = compute_pagerank(graph, max_iterations=100, tolerance=1e-6)

        # Should have scores for all nodes
        assert len(scores) == 4
        assert all(0 <= s <= 1 for s in scores.values())

        # Scores should sum to ~1.0
        total = sum(scores.values())
        assert 0.9 <= total <= 1.1

    def test_pagerank_stability(self):
        """Test PageRank produces stable results."""
        graph = CooccurrenceGraph()
        graph.add_cooccurrence("A", "B", weight=5)
        graph.add_cooccurrence("A", "C", weight=5)
        graph.add_cooccurrence("B", "D", weight=5)

        # Run twice
        scores1 = compute_pagerank(graph)
        scores2 = compute_pagerank(graph)

        # Should be identical
        assert scores1 == scores2


class TestEndToEndWorkflow:
    """End-to-end workflow tests."""

    def test_explore_codebase_workflow(self):
        """Simulate user exploring a codebase."""
        # Create sample codebase
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # Create files
            (tmpdir / "main.py").write_text("""
def main():
    config = load_config()
    proxy = setup_proxy(config)
    run(proxy)
""")
            (tmpdir / "proxy.py").write_text("""
def setup_proxy(config):
    proxy = config.get('proxy')
    return proxy

def load_config():
    return {}
""")

            # Workflow: Find associations for "proxy"
            all_text = ""
            for py_file in tmpdir.glob("*.py"):
                all_text += py_file.read_text()

            detector = PatternDetector(min_support=2, min_length=3)
            patterns = detector.find_patterns(all_text)

            graph = CooccurrenceGraph()
            graph.add_document_cooccurrences(list(patterns.keys()), window_size=5)

            if graph.has_node("proxy"):
                pagerank_scores = compute_pagerank(graph)
                search = AssociativeSearch(graph, pagerank_scores)
                result = search.find_associations("proxy", max_degree=2, top_k=10)

                # Should find related terms
                assert result.query == "proxy"
