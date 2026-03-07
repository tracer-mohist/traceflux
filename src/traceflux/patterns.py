# src/traceflux/patterns.py
"""LZ77-style Pattern Detection.

Find maximal repeated patterns in text sequences using suffix arrays.
Operates on character sequences - language independent.

Algorithm: Suffix Array + LCP (Longest Common Prefix)
Complexity: O(n log n) for construction, O(n) for pattern extraction
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Pattern:
    """A repeated pattern with occurrence information.

    Attributes:
        text: The pattern text
        positions: List of start positions in source text
        length: Length of the pattern
    """

    text: str
    positions: List[int]
    length: int

    @property
    def frequency(self) -> int:
        """Number of occurrences."""
        return len(self.positions)

    def is_maximal(self) -> bool:
        """Check if pattern is maximal (cannot be extended).

        A pattern is maximal if extending it by one character
        in any direction reduces its frequency.

        Note: This is a simplified check. Full maximality requires
        context analysis.
        """
        # For now, consider all detected patterns as potentially maximal
        # Full implementation would check left/right extensions
        return self.frequency >= 2


class SuffixArray:
    """Suffix array construction and utilities.

    Builds sorted suffix array for efficient pattern matching.
    Uses Python's built-in sort (Timsort) for simplicity.

    For production use with large texts, consider:
    - SA-IS algorithm (O(n) linear time)
    - DC3 algorithm (O(n) linear time)
    """

    def __init__(self, text: str):
        """Build suffix array for text.

        Args:
            text: Input text
        """
        self.text = text
        self.length = len(text)
        # Suffix array: indices sorted by suffix
        self.suffixes: List[int] = sorted(
            range(self.length),
            key=lambda i: text[i:]
        )

    def get_suffix(self, rank: int) -> str:
        """Get suffix at given rank.

        Args:
            rank: Position in suffix array

        Returns:
            Suffix string
        """
        start = self.suffixes[rank]
        return self.text[start:]

    def get_position(self, rank: int) -> int:
        """Get original position for suffix at rank.

        Args:
            rank: Position in suffix array

        Returns:
            Original position in text
        """
        return self.suffixes[rank]


class PatternDetector:
    """Detect repeated patterns in text.

    Uses suffix array + LCP to find maximal repeats.

    Example:
        >>> detector = PatternDetector(min_support=2)
        >>> patterns = detector.find_patterns("hello hello world")
        >>> "hello" in patterns
        True
    """

    def __init__(self, min_support: int = 2, min_length: int = 2, case_insensitive: bool = False):
        """Initialize pattern detector.

        Args:
            min_support: Minimum occurrences to consider a pattern
            min_length: Minimum pattern length to detect
            case_insensitive: If True, treat "Hello" and "hello" as same pattern
        """
        self.min_support = min_support
        self.min_length = min_length
        self.case_insensitive = case_insensitive

    def _compute_lcp(self, text: str, suffix_array: SuffixArray) -> List[int]:
        """Compute LCP (Longest Common Prefix) array.

        LCP[i] = length of common prefix between suffix[i] and suffix[i-1]

        Uses Kasai's algorithm: O(n) time

        Args:
            text: Original text
            suffix_array: SuffixArray instance

        Returns:
            LCP array (length = len(text))
        """
        n = len(text)
        if n == 0:
            return []

        # Rank array: rank[i] = position of suffix starting at i
        rank = [0] * n
        for i, pos in enumerate(suffix_array.suffixes):
            rank[pos] = i

        lcp = [0] * n
        h = 0  # Current LCP length

        for i in range(n):
            if rank[i] > 0:
                # Get previous suffix in sorted order
                j = suffix_array.suffixes[rank[i] - 1]

                # Extend match while characters match
                while (i + h < n and j + h < n and
                       text[i + h] == text[j + h]):
                    h += 1

                lcp[rank[i]] = h

                # Decrease h for next iteration (Kasai's insight)
                if h > 0:
                    h -= 1

        return lcp

    def _find_repeats_with_lcp(
        self,
        text: str,
        suffix_array: SuffixArray,
        lcp: List[int]
    ) -> Dict[str, List[int]]:
        """Find repeated patterns using LCP array.

        Groups suffixes with common prefixes and collects positions.

        Args:
            text: Original text
            suffix_array: SuffixArray instance
            lcp: LCP array

        Returns:
            Dict mapping patterns to their positions
        """
        patterns: Dict[str, List[int]] = {}
        n = len(text)

        if n == 0:
            return patterns

        # Scan LCP array to find repeated patterns
        i = 1
        while i < n:
            if lcp[i] >= self.min_length:
                # Found a repeated pattern - collect the group
                group_start = i - 1
                group_end = i

                # Extend group while LCP values are high enough
                while group_end < n and lcp[group_end] >= self.min_length:
                    group_end += 1

                # The pattern length is the minimum LCP in this group
                # This ensures we capture the longest common prefix
                pattern_len = min(lcp[j] for j in range(i, group_end))

                if pattern_len >= self.min_length:
                    # Get pattern from first suffix in group
                    pos = suffix_array.get_position(group_start)
                    pattern_text = text[pos:pos + pattern_len]

                    # Collect all positions in the group
                    positions = []
                    for j in range(group_start, group_end):
                        positions.append(suffix_array.get_position(j))

                    # Store pattern
                    if pattern_text not in patterns:
                        patterns[pattern_text] = []
                    patterns[pattern_text].extend(positions)

                i = group_end
            else:
                i += 1

        return patterns

    def find_patterns(self, text: str) -> Dict[str, List[int]]:
        """Find repeated patterns in text.

        Algorithm:
        1. Build suffix array (O(n log n))
        2. Compute LCP array using Kasai's algorithm (O(n))
        3. Scan LCP to find repeated patterns (O(n))

        Args:
            text: Input text

        Returns:
            Dict mapping patterns to their positions
        """
        if len(text) < self.min_length * self.min_support:
            return {}

        # For case-insensitive matching, work with lowercase text
        # but preserve original positions
        if self.case_insensitive:
            text_normalized = text.lower()
        else:
            text_normalized = text

        # Build suffix array on normalized text
        suffix_array = SuffixArray(text_normalized)

        # Compute LCP array
        lcp = self._compute_lcp(text_normalized, suffix_array)

        # Find repeated patterns in normalized text
        patterns = self._find_repeats_with_lcp(text_normalized, suffix_array, lcp)

        # Filter by minimum support
        filtered = {
            pattern: positions
            for pattern, positions in patterns.items()
            if len(positions) >= self.min_support
        }

        return filtered

    def find_patterns_with_metadata(
        self,
        text: str
    ) -> List[Pattern]:
        """Find patterns and return as Pattern objects.

        Args:
            text: Input text

        Returns:
            List of Pattern objects
        """
        pattern_dict = self.find_patterns(text)

        return [
            Pattern(
                text=pattern,
                positions=sorted(positions),
                length=len(pattern)
            )
            for pattern, positions in pattern_dict.items()
        ]

    def find_maximal_patterns(self, text: str) -> List[Pattern]:
        """Find only maximal repeated patterns.

        A pattern is maximal if it cannot be extended left or right
        without reducing its frequency.

        Args:
            text: Input text

        Returns:
            List of maximal Pattern objects
        """
        patterns = self.find_patterns_with_metadata(text)

        # Filter to keep only maximal patterns
        maximal = []
        for pattern in patterns:
            # Simple maximality check:
            # A pattern is maximal if no super-pattern has same frequency
            is_maximal = True

            # Check if any longer pattern contains this one with same frequency
            for other in patterns:
                if (len(other.text) > len(pattern.text) and
                    pattern.text in other.text and
                    other.frequency == pattern.frequency):
                    is_maximal = False
                    break

            if is_maximal:
                maximal.append(pattern)

        return maximal

    def get_pattern_stats(
        self,
        patterns: Dict[str, List[int]]
    ) -> Dict:
        """Get statistics about detected patterns.

        Args:
            patterns: Dict from find_patterns()

        Returns:
            Dict with statistics:
            - total_patterns: Number of unique patterns
            - total_occurrences: Total pattern occurrences
            - avg_length: Average pattern length
            - max_frequency: Highest frequency
            - min_frequency: Lowest frequency
        """
        if not patterns:
            return {
                "total_patterns": 0,
                "total_occurrences": 0,
                "avg_length": 0,
                "max_frequency": 0,
                "min_frequency": 0,
            }

        frequencies = [len(positions) for positions in patterns.values()]
        lengths = [len(pattern) for pattern in patterns.keys()]

        return {
            "total_patterns": len(patterns),
            "total_occurrences": sum(frequencies),
            "avg_length": sum(lengths) / len(lengths),
            "max_frequency": max(frequencies),
            "min_frequency": min(frequencies),
        }
