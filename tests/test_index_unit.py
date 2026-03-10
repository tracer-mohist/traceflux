# tests/test_index_unit.py
"""Tests for Pattern Index."""

import json
from pathlib import Path

import pytest

from traceflux.index import PatternIndex


class TestPatternIndexBasic:
    """Basic index operations tests."""

    def setup_method(self):
        """Set up test fixtures."""
        self.index = PatternIndex()

    def test_empty_index(self):
        """Empty index has no patterns."""
        assert self.index.pattern_count() == 0
        assert self.index.doc_count() == 0
        assert self.index.patterns() == []

    def test_add_pattern(self):
        """Add pattern to index."""
        self.index.add("hello", "doc1.txt", [10, 20])

        assert self.index.has("hello")
        assert self.index.pattern_count() == 1

    def test_add_multiple_occurrences(self):
        """Add multiple occurrences of same pattern."""
        self.index.add("hello", "doc1.txt", [10])
        self.index.add("hello", "doc1.txt", [20])

        results = self.index.get("hello")
        assert len(results) == 1
        assert results[0][0] == "doc1.txt"
        assert results[0][1] == [10, 20]

    def test_add_multiple_documents(self):
        """Add pattern to multiple documents."""
        self.index.add("hello", "doc1.txt", [10])
        self.index.add("hello", "doc2.txt", [20])

        results = self.index.get("hello")
        assert len(results) == 2

        doc_ids = [r[0] for r in results]
        assert "doc1.txt" in doc_ids
        assert "doc2.txt" in doc_ids

    def test_get_nonexistent_pattern(self):
        """Get pattern that doesn't exist."""
        results = self.index.get("nonexistent")
        assert results == []

    def test_has_pattern(self):
        """Check pattern existence."""
        self.index.add("hello", "doc1.txt", [10])

        assert self.index.has("hello")
        assert not self.index.has("world")


class TestPatternIndexPositions:
    """Test position tracking in index."""

    def setup_method(self):
        """Set up test fixtures."""
        self.index = PatternIndex()

    def test_positions_sorted(self):
        """Positions are stored in sorted order."""
        self.index.add("test", "doc1.txt", [50, 10, 30])

        results = self.index.get("test")
        positions = results[0][1]
        assert positions == [10, 30, 50]

    def test_positions_across_documents(self):
        """Positions tracked separately per document."""
        self.index.add("test", "doc1.txt", [10, 20])
        self.index.add("test", "doc2.txt", [30, 40])

        results = self.index.get("test")

        doc1_result = next(r for r in results if r[0] == "doc1.txt")
        doc2_result = next(r for r in results if r[0] == "doc2.txt")

        assert doc1_result[1] == [10, 20]
        assert doc2_result[1] == [30, 40]


class TestPatternIndexStats:
    """Test index statistics."""

    def setup_method(self):
        """Set up test fixtures."""
        self.index = PatternIndex()

    def test_doc_count(self):
        """Count unique documents."""
        self.index.add("hello", "doc1.txt", [10])
        self.index.add("hello", "doc2.txt", [20])
        self.index.add("world", "doc1.txt", [30])

        assert self.index.doc_count() == 2

    def test_pattern_count(self):
        """Count unique patterns."""
        self.index.add("hello", "doc1.txt", [10])
        self.index.add("world", "doc1.txt", [20])
        self.index.add("test", "doc1.txt", [30])

        assert self.index.pattern_count() == 3

    def test_total_occurrences(self):
        """Count total occurrences."""
        self.index.add("hello", "doc1.txt", [10, 20])
        self.index.add("world", "doc1.txt", [30])

        assert self.index.total_occurrences() == 3

    def test_stats(self):
        """Get comprehensive statistics."""
        self.index.add("hello", "doc1.txt", [10, 20])
        self.index.add("world", "doc2.txt", [30])

        stats = self.index.stats()

        assert stats["pattern_count"] == 2
        assert stats["doc_count"] == 2
        assert stats["total_occurrences"] == 3
        assert stats["avg_occurrences_per_pattern"] == 1.5


class TestPatternIndexPersistence:
    """Test index save/load functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.index = PatternIndex()
        self.test_dir = Path("/tmp/traceflux_test")
        self.test_dir.mkdir(exist_ok=True)

    def teardown_method(self):
        """Clean up test files."""
        test_file = self.test_dir / "test_index.json"
        if test_file.exists():
            test_file.unlink()

    def test_save_and_load(self):
        """Save index and reload it."""
        self.index.add("hello", "doc1.txt", [10, 20])
        self.index.add("world", "doc2.txt", [30])

        test_file = self.test_dir / "test_index.json"
        self.index.save(test_file)

        # Load into new index
        loaded = PatternIndex.load(test_file)

        assert loaded.pattern_count() == 2
        assert loaded.doc_count() == 2
        assert loaded.has("hello")
        assert loaded.has("world")

    def test_save_creates_directory(self):
        """Save creates parent directories if needed."""
        nested_dir = self.test_dir / "nested" / "path"
        test_file = nested_dir / "test_index.json"

        self.index.add("test", "doc1.txt", [10])
        self.index.save(test_file)

        assert test_file.exists()

    def test_load_preserves_data(self):
        """Loaded index has same data as original."""
        self.index.add("pattern1", "doc1.txt", [1, 2, 3])
        self.index.add("pattern2", "doc2.txt", [4, 5])
        self.index.add("pattern3", "doc3.txt", [6])

        test_file = self.test_dir / "test_index.json"
        self.index.save(test_file)

        loaded = PatternIndex.load(test_file)

        # Check all patterns
        for pattern in ["pattern1", "pattern2", "pattern3"]:
            assert loaded.has(pattern)
            original = self.index.get(pattern)
            reloaded = loaded.get(pattern)
            assert original == reloaded


class TestPatternIndexClear:
    """Test index clear operation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.index = PatternIndex()

    def test_clear(self):
        """Clear removes all data."""
        self.index.add("hello", "doc1.txt", [10])
        self.index.add("world", "doc2.txt", [20])

        self.index.clear()

        assert self.index.pattern_count() == 0
        assert self.index.doc_count() == 0
        assert not self.index.has("hello")
        assert not self.index.has("world")


class TestPatternIndexEdgeCases:
    """Test edge cases."""

    def setup_method(self):
        """Set up test fixtures."""
        self.index = PatternIndex()

    def test_add_empty_positions(self):
        """Add with empty positions list."""
        self.index.add("test", "doc1.txt", [])

        assert not self.index.has("test")
        assert self.index.pattern_count() == 0

    def test_unicode_patterns(self):
        """Handle Unicode patterns."""
        self.index.add("你好", "doc1.txt", [10])
        self.index.add("café", "doc2.txt", [20])

        assert self.index.has("你好")
        assert self.index.has("café")

    def test_special_characters_in_doc_id(self):
        """Handle special characters in document IDs."""
        self.index.add("test", "path/to/doc.txt", [10])
        self.index.add("test", "file with spaces.txt", [20])

        assert self.index.doc_count() == 2

    def test_large_number_of_occurrences(self):
        """Handle many occurrences."""
        positions = list(range(0, 1000, 10))
        self.index.add("frequent", "doc1.txt", positions)

        results = self.index.get("frequent")
        assert len(results[0][1]) == 100
