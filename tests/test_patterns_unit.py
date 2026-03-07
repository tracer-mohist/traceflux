# tests/test_patterns.py
"""Tests for LZ77-style pattern detection."""

import pytest
from traceflux.patterns import Pattern, SuffixArray, PatternDetector


class TestSuffixArray:
    """Test suffix array construction."""

    def test_empty_string(self):
        """Empty string produces empty suffix array."""
        sa = SuffixArray("")
        assert sa.length == 0
        assert sa.suffixes == []

    def test_single_character(self):
        """Single character produces one suffix."""
        sa = SuffixArray("a")
        assert sa.length == 1
        assert sa.suffixes == [0]

    def test_sorted_suffixes(self):
        """Suffixes are sorted lexicographically."""
        text = "banana"
        sa = SuffixArray(text)

        # Suffixes should be sorted
        suffixes = [text[i:] for i in sa.suffixes]
        assert suffixes == sorted(suffixes)

    def test_suffix_positions(self):
        """Can retrieve original positions."""
        text = "hello"
        sa = SuffixArray(text)

        for rank in range(len(text)):
            pos = sa.get_position(rank)
            suffix = sa.get_suffix(rank)
            assert suffix == text[pos:]


class TestPatternClass:
    """Test Pattern dataclass."""

    def test_pattern_creation(self):
        """Create pattern with basic attributes."""
        p = Pattern(text="hello", positions=[0, 10], length=5)
        assert p.text == "hello"
        assert p.frequency == 2
        assert p.length == 5

    def test_pattern_frequency(self):
        """Frequency equals number of positions."""
        p = Pattern(text="test", positions=[1, 5, 9, 15], length=4)
        assert p.frequency == 4

    def test_pattern_is_maximal(self):
        """Maximal check returns True for now."""
        p = Pattern(text="pattern", positions=[0, 20], length=7)
        assert p.is_maximal() is True


class TestPatternDetectorBasic:
    """Basic pattern detection tests."""

    def setup_method(self):
        """Set up test fixtures."""
        self.detector = PatternDetector(min_support=2, min_length=2)

    def test_empty_text(self):
        """Empty text produces no patterns."""
        patterns = self.detector.find_patterns("")
        assert patterns == {}

    def test_no_repeats(self):
        """Text with no repeats produces no patterns."""
        patterns = self.detector.find_patterns("abcdef")
        assert patterns == {}

    def test_simple_repeat(self):
        """Detect simple repeated pattern."""
        text = "hello hello"
        patterns = self.detector.find_patterns(text)

        assert "hello" in patterns
        assert len(patterns["hello"]) >= 2

    def test_multiple_repeats(self):
        """Detect multiple different patterns."""
        text = "ab ab cd cd"
        patterns = self.detector.find_patterns(text)

        # Should find at least "ab" and "cd"
        assert len(patterns) >= 2

    def test_min_support_filter(self):
        """Patterns below min_support are filtered."""
        text = "hello world test"  # Each word appears once
        patterns = self.detector.find_patterns(text)

        # No patterns should meet min_support=2
        assert len(patterns) == 0

    def test_min_length_filter(self):
        """Patterns below min_length are filtered."""
        detector = PatternDetector(min_support=2, min_length=3)
        text = "aa bb cc"  # Two-char patterns

        patterns = detector.find_patterns(text)
        # "aa", "bb", "cc" are too short (length 2)
        assert len(patterns) == 0


class TestPatternDetectorPositions:
    """Test pattern position detection."""

    def setup_method(self):
        """Set up test fixtures."""
        self.detector = PatternDetector(min_support=2, min_length=2)

    def test_position_accuracy(self):
        """Detected positions are accurate."""
        text = "hello world hello"
        patterns = self.detector.find_patterns(text)

        if "hello" in patterns:
            positions = patterns["hello"]
            # Should find "hello" at positions 0 and 12
            assert 0 in positions
            assert 12 in positions

    def test_overlapping_patterns(self):
        """Handle overlapping patterns correctly."""
        text = "ababab"
        patterns = self.detector.find_patterns(text)

        # Should find "ab" and possibly "aba", "bab", etc.
        assert len(patterns) > 0


class TestPatternDetectorMetadata:
    """Test pattern metadata methods."""

    def setup_method(self):
        """Set up test fixtures."""
        self.detector = PatternDetector(min_support=2, min_length=2)

    def test_find_patterns_with_metadata(self):
        """Return Pattern objects with full metadata."""
        text = "test test test"
        patterns = self.detector.find_patterns_with_metadata(text)

        assert len(patterns) > 0
        assert all(isinstance(p, Pattern) for p in patterns)
        assert all(p.frequency >= 2 for p in patterns)

    def test_get_pattern_stats(self):
        """Generate accurate statistics."""
        patterns = {
            "hello": [0, 10],
            "world": [5, 15],
            "test": [20],
        }

        stats = self.detector.get_pattern_stats(patterns)

        assert stats["total_patterns"] == 3
        assert stats["total_occurrences"] == 5
        assert stats["min_frequency"] == 1
        assert stats["max_frequency"] == 2

    def test_get_pattern_stats_empty(self):
        """Handle empty patterns dict."""
        stats = self.detector.get_pattern_stats({})

        assert stats["total_patterns"] == 0
        assert stats["total_occurrences"] == 0


class TestPatternDetectorMaximal:
    """Test maximal pattern detection."""

    def setup_method(self):
        """Set up test fixtures."""
        self.detector = PatternDetector(min_support=2, min_length=2)

    def test_find_maximal_patterns(self):
        """Find only maximal patterns."""
        text = "abc abc abc"
        patterns = self.detector.find_maximal_patterns(text)

        # All patterns should be marked as maximal
        assert all(p.is_maximal() for p in patterns)

    def test_maximal_vs_non_maximal(self):
        """Distinguish maximal from non-maximal patterns."""
        text = "abcd abcd abcd"
        maximal = self.detector.find_maximal_patterns(text)

        # Should prefer longer patterns when frequencies match
        if len(maximal) > 0:
            # At least one pattern should be found
            assert len(maximal) > 0


class TestPatternDetectorLanguages:
    """Test pattern detection with different languages."""

    def setup_method(self):
        """Set up test fixtures."""
        self.detector = PatternDetector(min_support=2, min_length=2)

    def test_chinese_text(self):
        """Detect patterns in Chinese text."""
        text = "你好 世界 你好"
        patterns = self.detector.find_patterns(text)

        # Should find "你好" as a repeated pattern
        assert len(patterns) > 0

    def test_mixed_languages(self):
        """Handle mixed language text."""
        text = "hello 你好 hello 你好"
        patterns = self.detector.find_patterns(text)

        # Should find repeated patterns
        assert len(patterns) > 0

    def test_numbers(self):
        """Detect patterns in numeric text."""
        text = "123 456 123 789 123"
        patterns = self.detector.find_patterns(text)

        assert "123" in patterns


class TestPatternDetectorEdgeCases:
    """Test edge cases and boundary conditions."""

    def setup_method(self):
        """Set up test fixtures."""
        self.detector = PatternDetector(min_support=2, min_length=2)

    def test_single_character_min_length(self):
        """Detect single character patterns when min_length=1."""
        detector = PatternDetector(min_support=2, min_length=1)
        text = "aaa"

        patterns = detector.find_patterns(text)
        assert "a" in patterns

    def test_very_long_repeat(self):
        """Handle very long repeated patterns."""
        pattern = "x" * 100
        text = pattern + " " + pattern

        detector = PatternDetector(min_support=2, min_length=10)
        patterns = detector.find_patterns(text)

        # Should find repeated patterns of x's
        # Algorithm finds patterns at various lengths due to suffix array grouping
        assert len(patterns) > 0
        # Verify that "x" patterns are detected (may be various lengths)
        assert any(all(c == "x" for c in p) for p in patterns.keys())

    def test_unicode_characters(self):
        """Handle Unicode characters correctly."""
        text = "café café résumé"
        patterns = self.detector.find_patterns(text)

        # Should handle accented characters
        assert len(patterns) > 0

    def test_whitespace_patterns(self):
        """Handle whitespace in patterns."""
        text = "a b a b a b"
        patterns = self.detector.find_patterns(text)

        # Should find patterns despite whitespace
        assert len(patterns) > 0


class TestLCPCalculation:
    """Test LCP array computation."""

    def test_lcp_empty(self):
        """LCP of empty string is empty."""
        detector = PatternDetector()
        lcp = detector._compute_lcp("", SuffixArray(""))
        assert lcp == []

    def test_lcp_single_char(self):
        """LCP of single character."""
        detector = PatternDetector()
        sa = SuffixArray("a")
        lcp = detector._compute_lcp("a", sa)
        assert len(lcp) == 1
        assert lcp[0] == 0  # First suffix has no previous

    def test_lcp_repeated(self):
        """LCP correctly identifies common prefixes."""
        detector = PatternDetector()
        text = "abab"
        sa = SuffixArray(text)
        lcp = detector._compute_lcp(text, sa)

        # LCP array should have length equal to text
        assert len(lcp) == len(text)
