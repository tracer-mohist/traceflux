# src/traceflux/patterns.py
"""LZ77-style Pattern Detection using Suffix Arrays.

Find maximal repeated patterns in text sequences efficiently.
This module implements pattern detection using suffix arrays and LCP
(Longest Common Prefix) arrays for O(n log n) pattern discovery.

## Algorithm Overview

1. **Build Suffix Array**: Sort all suffixes of the text
2. **Compute LCP Array**: Find longest common prefix between adjacent suffixes
3. **Extract Patterns**: Group suffixes with common prefixes, collect positions

## When to Use

Use pattern detection when you want to:
- Find repeated structures in code (function calls, imports)
- Discover common phrases in documents
- Identify recurring patterns without knowing them in advance

Use direct search (traceflux search) when you:
- Know what you're looking for
- Want to find a specific term
- Need case-insensitive matching

## Complexity

- Suffix Array construction: O(n log n)
- LCP Array computation: O(n) using Kasai's algorithm
- Pattern extraction: O(n)
- **Total**: O(n log n) where n = text length

## Example

```python
from traceflux.patterns import PatternDetector

# Find patterns that appear at least twice
detector = PatternDetector(min_support=2, min_length=3)
patterns = detector.find_patterns("hello world, hello universe")

# patterns = {"hello": [0, 13], "ello": [1, 14], ...}
```

## Language Independence

This module operates on character sequences, not words.
It works equally well on:
- English text
- Source code
- Binary data (as bytes)
- Any character sequence

No tokenization or language-specific processing.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Pattern:
    """A repeated pattern with occurrence information.

    Represents a pattern found in text with its positions.

    Attributes:
        text: The pattern text (exact substring)
        positions: List of start positions in source text
        length: Length of the pattern in characters

    Example:
        >>> pattern = Pattern(text="hello", positions=[0, 13], length=5)
        >>> pattern.frequency
        2
        >>> pattern.is_maximal()
        True
    """

    text: str
    positions: List[int]
    length: int

    @property
    def frequency(self) -> int:
        """Number of occurrences of this pattern.

        Returns:
            Count of times pattern appears in source text

        Example:
            >>> pattern = Pattern("test", [0, 10, 20], 4)
            >>> pattern.frequency
            3
        """
        return len(self.positions)

    def is_maximal(self) -> bool:
        """Check if pattern is maximal (cannot be extended).

        A pattern is maximal if extending it by one character
        in any direction would reduce its frequency.

        Example:
            In "hello world, hello universe":
            - "hello" is maximal (extending to "hello " appears 2 times,
              but "hello w" appears only 1 time)
            - "ello" is NOT maximal (can extend to "hello" with same frequency)

        Note:
            Current implementation uses simplified check:
            - Returns True if frequency >= min_support
            - Full implementation would check left/right extensions
            - This is sufficient for traceflux use cases

        Returns:
            True if pattern appears to be maximal
        """
        # Simplified maximality check
        # Full implementation would verify that extending the pattern
        # by one character (left or right) reduces frequency
        return self.frequency >= 2


class SuffixArray:
    """Suffix array for efficient pattern matching.

    A suffix array is a sorted array of all suffixes of a text.
    It enables fast pattern discovery and substring searches.

    ## Structure

    For text "banana":
    - Suffixes: ["banana", "anana", "nana", "ana", "na", "a"]
    - Sorted:   ["a", "ana", "anana", "banana", "na", "nana"]
    - Indices:  [5,    3,     1,       0,        4,    2   ]

    The suffixes array stores the starting indices [5, 3, 1, 0, 4, 2].

    ## Implementation

    Uses Python's built-in Timsort (O(n log n)) for simplicity.

    For large texts (>1MB), consider:
    - **SA-IS algorithm**: O(n) linear time, complex implementation
    - **DC3 algorithm**: O(n) linear time, good for very large texts

    For traceflux use cases (typical files <1MB), Timsort is sufficient.

    ## Example

    ```python
    sa = SuffixArray("banana")
    sa.suffixes  # [5, 3, 1, 0, 4, 2]
    sa.get_suffix(0)  # "a" (first sorted suffix)
    sa.get_position(0)  # 5 (starts at index 5 in original text)
    ```
    """

    def __init__(self, text: str):
        """Build suffix array for text.

        Args:
            text: Input text to build suffix array for

        Example:
            >>> sa = SuffixArray("banana")
            >>> sa.length
            6
            >>> len(sa.suffixes)
            6
        """
        self.text = text
        self.length = len(text)
        # Suffix array: indices sorted by suffix
        # suffixes[rank] = starting position of suffix at that rank
        self.suffixes: List[int] = sorted(range(self.length), key=lambda i: text[i:])

    def get_suffix(self, rank: int) -> str:
        """Get suffix string at given rank.

        Args:
            rank: Position in sorted suffix array (0 = first suffix)

        Returns:
            Suffix string starting at that rank

        Example:
            >>> sa = SuffixArray("banana")
            >>> sa.get_suffix(0)  # First sorted suffix
            'a'
            >>> sa.get_suffix(3)  # Fourth sorted suffix
            'banana'
        """
        start = self.suffixes[rank]
        return self.text[start:]

    def get_position(self, rank: int) -> int:
        """Get original text position for suffix at rank.

        Args:
            rank: Position in sorted suffix array

        Returns:
            Starting position in original text

        Example:
            >>> sa = SuffixArray("banana")
            >>> sa.get_position(0)  # "a" starts at index 5
            5
            >>> sa.get_position(3)  # "banana" starts at index 0
            0
        """
        return self.suffixes[rank]


class PatternDetector:
    """Detect repeated patterns in text using suffix arrays.

    Finds all patterns that appear at least min_support times.
    Uses suffix array + LCP (Longest Common Prefix) for efficient O(n log n)
    pattern discovery.

    ## How It Works

    1. Build suffix array for the text
    2. Compute LCP array (longest common prefix between adjacent suffixes)
    3. Group suffixes with common prefixes
    4. Extract patterns that meet min_support threshold

    ## Parameters

    - **min_support**: Minimum times a pattern must appear (default: 2)
      - Higher = fewer, more significant patterns
      - Lower = more patterns, including noise

    - **min_length**: Minimum pattern length (default: 2)
      - Filters out single characters
      - Typical: 2-5 characters

    - **case_insensitive**: Treat "Hello" and "hello" as same (default: False)
      - Useful for natural language
      - Keep False for source code (case matters)

    ## Example

    ```python
    from traceflux.patterns import PatternDetector

    # Find patterns appearing at least twice
    detector = PatternDetector(min_support=2, min_length=3)

    text = "hello world, hello universe, goodbye world"
    patterns = detector.find_patterns(text)

    # patterns = {
    #     "hello": [0, 13],
    #     " world": [5, 31],
    #     "ello": [1, 14],
    #     ...
    # }
    ```

    ## Use Cases

    **Source Code Analysis**:
    - Find repeated function calls
    - Identify common import patterns
    - Discover code clones

    **Document Analysis**:
    - Find repeated phrases
    - Identify common terminology
    - Discover writing patterns

    **Log Analysis**:
    - Find repeated error patterns
    - Identify common sequences
    - Discover anomalies
    """

    def __init__(self, min_support: int = 2, min_length: int = 2, case_insensitive: bool = False):
        """Initialize pattern detector.

        Args:
            min_support: Minimum occurrences to consider a pattern (default: 2)
                Higher values find only frequent patterns.
                Lower values find more patterns including rare ones.
            min_length: Minimum pattern length in characters (default: 2)
                Filters out single characters which are usually noise.
            case_insensitive: If True, normalize case before detection (default: False)
                Useful for natural language text.
                Keep False for source code where case matters.

        Example:
            >>> detector = PatternDetector(min_support=2, min_length=3)
            >>> detector.min_support
            2
            >>> detector.min_length
            3
        """
        self.min_support = min_support
        self.min_length = min_length
        self.case_insensitive = case_insensitive

    def _compute_lcp(self, text: str, suffix_array: SuffixArray) -> List[int]:
        """Compute LCP (Longest Common Prefix) array using Kasai's algorithm.

        The LCP array stores the length of the longest common prefix between
        each adjacent pair of suffixes in the sorted suffix array.

        ## LCP Array Structure

        For text "banana" with sorted suffixes:
        - Rank 0: "a" (index 5)
        - Rank 1: "ana" (index 3)
        - Rank 2: "anana" (index 1)
        - Rank 3: "banana" (index 0)
        - Rank 4: "na" (index 4)
        - Rank 5: "nana" (index 2)

        LCP array: [0, 1, 3, 0, 0, 2]
        - LCP[0] = 0 (no previous suffix)
        - LCP[1] = 1 ("a" and "ana" share "a")
        - LCP[2] = 3 ("ana" and "anana" share "ana")
        - LCP[3] = 0 ("anana" and "banana" share nothing)
        - LCP[4] = 0 ("banana" and "na" share nothing)
        - LCP[5] = 2 ("na" and "nana" share "na")

        ## Kasai's Algorithm

        Time complexity: O(n) - linear time
        Key insight: When moving from position i to i+1, the LCP can decrease
        by at most 1. This allows amortized O(n) computation.

        Args:
            text: Original text string
            suffix_array: Pre-computed SuffixArray instance

        Returns:
            LCP array where LCP[i] = length of common prefix between
            suffix at rank i and suffix at rank i-1.
            LCP[0] is always 0 (no previous suffix).

        Reference:
            Kasai, T., et al. (2001). "Linear-Time Longest-Common-Prefix
            Computation in Suffix Arrays and Its Applications."
        """
        n = len(text)
        if n == 0:
            return []

        # Rank array: rank[i] = position of suffix starting at position i
        # This is the inverse of the suffix array
        rank = [0] * n
        for i, pos in enumerate(suffix_array.suffixes):
            rank[pos] = i

        lcp = [0] * n
        h = 0  # Current LCP length (carried between iterations)

        # Process suffixes in original text order (not sorted order)
        for i in range(n):
            if rank[i] > 0:
                # Get previous suffix in sorted order
                j = suffix_array.suffixes[rank[i] - 1]

                # Extend match while characters match
                while i + h < n and j + h < n and text[i + h] == text[j + h]:
                    h += 1

                lcp[rank[i]] = h

                # Decrease h for next iteration (Kasai's key insight)
                # When moving to next position, LCP can decrease by at most 1
                if h > 0:
                    h -= 1

        return lcp

    def _find_repeats_with_lcp(
        self, text: str, suffix_array: SuffixArray, lcp: List[int]
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
                    pattern_text = text[pos : pos + pattern_len]  # noqa: E203

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

    def find_patterns_with_metadata(self, text: str) -> List[Pattern]:
        """Find patterns and return as Pattern objects.

        Args:
            text: Input text

        Returns:
            List of Pattern objects
        """
        pattern_dict = self.find_patterns(text)

        return [
            Pattern(text=pattern, positions=sorted(positions), length=len(pattern))
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
                if (
                    len(other.text) > len(pattern.text)
                    and pattern.text in other.text
                    and other.frequency == pattern.frequency
                ):
                    is_maximal = False
                    break

            if is_maximal:
                maximal.append(pattern)

        return maximal

    def get_pattern_stats(self, patterns: Dict[str, List[int]]) -> Dict:
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
