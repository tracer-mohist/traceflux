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
        punct_type: Punctuation type identifier (pre[0:1], post[0:1])
    """

    pre_punct: str
    content: str
    post_punct: str
    start_pos: int
    end_pos: int
    punct_type: tuple = None

    def __post_init__(self):
        """Compute punct_type after initialization."""
        if self.punct_type is None:
            # Type is first char of pre and post (or empty)
            pre_char = self.pre_punct[0:1] if self.pre_punct else ""
            post_char = self.post_punct[0:1] if self.post_punct else ""
            self.punct_type = (pre_char, post_char)

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

    @property
    def type_key(self) -> str:
        """Get string key for punct_type (for dict indexing)."""
        return f"{self.punct_type[0]}|{self.punct_type[1]}"


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

    def __init__(self, min_content_len: int = 1, semantic_segmentation: bool = True):
        """Initialize scanner.

        Args:
            min_content_len: Minimum content length to emit segment.
            semantic_segmentation: If True, use context-aware segmentation
                                  (preserves IP addresses, identifiers, versions).
                                  If False, use simple alphanumeric segmentation.
        """
        self.min_content_len = min_content_len
        self.semantic_segmentation = semantic_segmentation

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

    def is_content_char(self, char: str, prev_char: str = None, next_char: str = None) -> bool:
        """Check if character should be part of content (semantic-aware).

        When semantic_segmentation is True:
        - Letters and digits are always content
        - Underscore (_) is content (identifiers: proxy_config)
        - Dot (.) is content between digits (IP: 127.0.0.1, version: v3.14.2)
        - Dot (.) between letters is punctuation (file.txt)

        Args:
            char: Current character
            prev_char: Previous character (for context)
            next_char: Next character (for context)

        Returns:
            True if character should be part of content
        """
        if not self.semantic_segmentation:
            return self.is_alphanumeric(char)

        # Letters and digits are always content
        if char.isalnum():
            return True

        # Underscore is content (for identifiers like proxy_config, HTTP_PROXY)
        if char == "_":
            return True

        # Dot is content between digits (IP addresses, version numbers)
        if char == ".":
            if prev_char and prev_char.isdigit():
                return True
            if next_char and next_char.isdigit():
                return True

        # Everything else is punctuation
        return False

    def scan(self, text: str) -> Iterator[Segment]:
        """Scan text and yield segments.

        One-pass O(n) algorithm:
        1. Iterate through characters left-to-right
        2. Group consecutive content chars (semantic-aware if enabled)
        3. Group consecutive non-content as punctuation
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
            while pos < length:
                prev_char = text[pos - 1] if pos > 0 else None
                next_char = text[pos + 1] if pos < length - 1 else None
                if not self.is_content_char(text[pos], prev_char, next_char):
                    pos += 1
                else:
                    break
            pre_punct = text[pre_start:pos]

            # Collect content (using semantic-aware rules)
            content_start = pos
            while pos < length:
                prev_char = text[pos - 1] if pos > 0 else None
                next_char = text[pos + 1] if pos < length - 1 else None
                if self.is_content_char(text[pos], prev_char, next_char):
                    pos += 1
                else:
                    break
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
