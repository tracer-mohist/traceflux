# src/traceflux/scanner.py
"""PNI (Punctuation Namespace Index) One-Pass Scanner.

Segment text by punctuation boundaries, extracting character sequences
with their positions. Language-independent - operates on character codes.
"""

from dataclasses import dataclass
from typing import Iterator


@dataclass
class Segment:
    """A segment of text with punctuation context.

    Attributes:
        pre_punct: Punctuation characters before content (may be empty)
        content: Alphanumeric content sequence
        post_punct: Punctuation characters after content (may be empty)
        start_pos: Start position in original text
        end_pos: End position in original text
    """

    pre_punct: str
    content: str
    post_punct: str
    start_pos: int
    end_pos: int

    def __len__(self) -> int:
        """Total length including punctuation."""
        return len(self.pre_punct) + len(self.content) + len(self.post_punct)

    @property
    def content_start(self) -> int:
        """Position where content starts (after pre_punct)."""
        return self.start_pos + len(self.pre_punct)

    @property
    def content_end(self) -> int:
        """Position where content ends (before post_punct)."""
        return self.end_pos - len(self.post_punct)


class Scanner:
    """One-pass text scanner using PNI segmentation.

    Scans text left-to-right, segmenting by punctuation boundaries.
    Operates on character codes - language independent.

    Example:
        >>> scanner = Scanner()
        >>> text = "Hello, world! How are you?"
        >>> segments = list(scanner.scan(text))
        >>> len(segments)
        4
        >>> segments[0].content
        'Hello'
        >>> segments[0].post_punct
        ', '
    """

    def __init__(self, min_content_len: int = 1):
        """Initialize scanner.

        Args:
            min_content_len: Minimum content length to emit segment.
                            Segments with shorter content are merged
                            with adjacent punctuation.
        """
        self.min_content_len = min_content_len

    @staticmethod
    def is_alphanumeric(char: str) -> bool:
        """Check if character is alphanumeric.

        Uses Unicode categorization - works for all languages.

        Args:
            char: Single character

        Returns:
            True if character is letter or digit
        """
        return char.isalnum()

    @staticmethod
    def is_punctuation(char: str) -> bool:
        """Check if character is punctuation.

        Includes spaces, symbols, control characters.

        Args:
            char: Single character

        Returns:
            True if character is not alphanumeric
        """
        return not char.isalnum()

    def scan(self, text: str) -> Iterator[Segment]:
        """Scan text and yield segments.

        One-pass O(n) algorithm:
        1. Iterate through characters left-to-right
        2. Group consecutive alphanumerics as content
        3. Group consecutive non-alphanumerics as punctuation
        4. Emit segments with position tracking

        Args:
            text: Input text to scan

        Yields:
            Segment objects with content and positions
        """
        if not text:
            return

        pos = 0
        length = len(text)

        while pos < length:
            # Collect pre-punctuation
            pre_start = pos
            while pos < length and self.is_punctuation(text[pos]):
                pos += 1
            pre_punct = text[pre_start:pos]

            # Collect content
            content_start = pos
            while pos < length and self.is_alphanumeric(text[pos]):
                pos += 1
            content = text[content_start:pos]

            # Collect post-punctuation
            post_start = pos
            while pos < length and self.is_punctuation(text[pos]):
                pos += 1
            post_punct = text[post_start:pos]

            # Emit segment if content meets minimum length
            if len(content) >= self.min_content_len:
                yield Segment(
                    pre_punct=pre_punct,
                    content=content,
                    post_punct=post_punct,
                    start_pos=pre_start,
                    end_pos=pos,
                )
            elif pre_punct or post_punct:
                # Content too short, emit as punctuation-only segment
                # This preserves position information
                if pre_punct or post_punct:
                    yield Segment(
                        pre_punct=pre_punct,
                        content="",
                        post_punct=post_punct,
                        start_pos=pre_start,
                        end_pos=pos,
                    )

    def scan_to_list(self, text: str) -> list[Segment]:
        """Scan text and return list of segments.

        Convenience method for when you need all segments at once.

        Args:
            text: Input text to scan

        Returns:
            List of Segment objects
        """
        return list(self.scan(text))

    def extract_content(self, text: str) -> list[str]:
        """Extract only content sequences (no punctuation).

        Utility method for simple use cases.

        Args:
            text: Input text to scan

        Returns:
            List of content strings
        """
        return [seg.content for seg in self.scan(text) if seg.content]

    def extract_positions(self, text: str) -> list[tuple[str, int]]:
        """Extract content sequences with their start positions.

        Args:
            text: Input text to scan

        Returns:
            List of (content, start_position) tuples
        """
        return [(seg.content, seg.content_start) for seg in self.scan(text) if seg.content]
