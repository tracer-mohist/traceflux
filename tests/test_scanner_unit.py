# tests/test_scanner.py
"""Scanner Unit Tests.

Tests for PNI (Punctuation Namespace Index) scanner.

Core Logic Verified:
- PNI segmentation: content vs punctuation separation
- Position tracking: accurate start/end positions
- Multi-language support: space is punctuation (language-independent)
"""

import pytest
from traceflux.scanner import Scanner, Segment


class TestScannerBasic:
    """Basic scanner functionality tests."""

    def setup_method(self):
        """Set up test fixtures."""
        self.scanner = Scanner()

    def test_empty_text(self):
        # Scenario: User scans empty file or directory
        # Expected: No segments emitted (graceful handling)
        # If fails: Empty files cause crashes
        segments = list(self.scanner.scan(""))
        assert len(segments) == 0

    def test_single_word(self):
        # Scenario: Single word without punctuation (minimal input)
        # Expected: One segment with correct content and positions
        # If fails: Basic tokenization broken
        segments = list(self.scanner.scan("Hello"))
        assert len(segments) == 1
        assert segments[0].content == "Hello"
        assert segments[0].pre_punct == ""
        assert segments[0].post_punct == ""
        assert segments[0].start_pos == 0
        assert segments[0].end_pos == 5

    def test_word_with_trailing_punct(self):
        # Scenario: Word with trailing punctuation (e.g., "Hello,")
        # Expected: Content separated from punctuation
        # If fails: Pattern detection includes punctuation noise
        segments = list(self.scanner.scan("Hello,"))
        assert len(segments) == 1
        assert segments[0].content == "Hello"
        assert segments[0].post_punct == ","

    def test_word_with_surrounding_punct(self):
        # Scenario: Word surrounded by punctuation (e.g., "(Hello)")
        # Expected: Content extracted, punctuation preserved separately
        # If fails: Code patterns like "(x)" detected as "x" only
        segments = list(self.scanner.scan(",Hello!"))
        assert len(segments) == 1
        assert segments[0].content == "Hello"
        assert segments[0].pre_punct == ","
        assert segments[0].post_punct == "!"

    def test_multiple_words(self):
        # Scenario: Multiple space-separated words
        # Expected: Each word is separate segment (space is punctuation)
        # If fails: Multi-word patterns not detected correctly
        segments = list(self.scanner.scan("Hello world"))
        assert len(segments) == 2
        assert segments[0].content == "Hello"
        assert segments[1].content == "world"

    def test_sentence(self):
        # Scenario: Complete sentence with mixed punctuation
        # Expected: All content words separated, punctuation tracked
        # If fails: Natural language text parsed incorrectly
        text = "Hello, world! How are you?"
        segments = list(self.scanner.scan(text))

        assert len(segments) == 5
        assert segments[0].content == "Hello"
        assert segments[0].post_punct == ", "
        assert segments[1].content == "world"
        assert segments[1].post_punct == "! "
        assert segments[2].content == "How"
        assert segments[3].content == "are"
        assert segments[4].content == "you"
        assert segments[4].post_punct == "?"


class TestScannerPositions:
    """Position tracking tests."""

    def setup_method(self):
        """Set up test fixtures."""
        self.scanner = Scanner()

    def test_position_tracking(self):
        """Verify positions are correct."""
        text = "Hello, world!"
        segments = list(self.scanner.scan(text))

        assert segments[0].start_pos == 0
        assert segments[0].end_pos == 7  # "Hello, "
        assert segments[1].start_pos == 7
        assert segments[1].end_pos == 13  # "world!"

    def test_content_positions(self):
        """Verify content start/end positions."""
        text = "  Hello  "
        segments = list(self.scanner.scan(text))

        assert len(segments) == 1
        assert segments[0].content_start == 2  # After "  "
        assert segments[0].content_end == 7  # Before "  "
        assert segments[0].content == "Hello"

    def test_extract_positions(self):
        """Test extract_positions utility."""
        text = "Hello, world!"
        positions = self.scanner.extract_positions(text)

        assert len(positions) == 2
        assert positions[0] == ("Hello", 0)
        assert positions[1] == ("world", 7)


class TestScannerMultilang:
    """Multi-language support tests."""

    def setup_method(self):
        """Set up test fixtures."""
        self.scanner = Scanner()

    def test_chinese(self):
        """Chinese text (no spaces)."""
        text = "你好世界"
        segments = list(self.scanner.scan(text))

        assert len(segments) == 1
        assert segments[0].content == "你好世界"

    def test_mixed_chinese_english(self):
        """Mixed Chinese and English (space is punctuation)."""
        text = "Hello 世界"
        segments = list(self.scanner.scan(text))

        # Space separates content into 2 segments
        assert len(segments) == 2
        assert segments[0].content == "Hello"
        assert segments[1].content == "世界"

    def test_with_chinese_punctuation(self):
        """Chinese text with punctuation."""
        text = "你好，世界!"
        segments = list(self.scanner.scan(text))

        assert len(segments) == 2
        assert segments[0].content == "你好"
        assert segments[0].post_punct == "，"
        assert segments[1].content == "世界"
        assert segments[1].post_punct == "!"

    def test_arabic(self):
        """Arabic text (space is punctuation)."""
        text = "مرحبا بالعالم"
        segments = list(self.scanner.scan(text))

        # Space separates content into 2 segments
        assert len(segments) == 2
        assert segments[0].content == "مرحبا"
        assert segments[1].content == "بالعالم"

    def test_numbers(self):
        """Text with numbers."""
        text = "Version 3.14.2"
        segments = list(self.scanner.scan(text))

        # Numbers are alphanumeric, dots are punctuation
        assert len(segments) == 4
        assert segments[0].content == "Version"
        assert segments[1].content == "3"
        assert segments[2].content == "14"
        assert segments[3].content == "2"


class TestScannerUtilities:
    """Utility method tests."""

    def setup_method(self):
        """Set up test fixtures."""
        self.scanner = Scanner()

    def test_extract_content(self):
        """Test extract_content utility."""
        text = "Hello, world!"
        contents = self.scanner.extract_content(text)

        assert contents == ["Hello", "world"]

    def test_scan_to_list(self):
        """Test scan_to_list utility."""
        text = "Hello world"
        segments = self.scanner.scan_to_list(text)

        assert isinstance(segments, list)
        assert len(segments) == 2


class TestScannerEdgeCases:
    """Edge case tests."""

    def setup_method(self):
        """Set up test fixtures."""
        self.scanner = Scanner()

    def test_only_punctuation(self):
        """Text with only punctuation."""
        text = "!@#$%"
        segments = list(self.scanner.scan(text))

        # Should emit as punctuation-only segment
        assert len(segments) >= 1

    def test_whitespace_only(self):
        """Text with only whitespace."""
        text = "   \t\n  "
        segments = list(self.scanner.scan(text))

        # Whitespace is punctuation
        assert len(segments) >= 1

    def test_min_content_length(self):
        """Test minimum content length filter."""
        scanner = Scanner(min_content_len=3)
        text = "I am a"
        segments = list(scanner.scan(text))

        # "I" and "a" should be filtered out (too short)
        # "am" has length 2, also filtered with min_content_len=3
        contents = [seg.content for seg in segments if seg.content]
        assert len(contents) == 0  # All filtered out

    def test_unicode_emoji(self):
        """Text with emoji."""
        text = "Hello 😀 World"
        segments = list(self.scanner.scan(text))

        # Emoji is considered alphanumeric in Python
        assert any("Hello" in seg.content for seg in segments)
        assert any("World" in seg.content for seg in segments)
