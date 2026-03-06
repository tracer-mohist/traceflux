# src/traceflux/index.py
"""Pattern Index - Store and serialize pattern occurrences.

Maps patterns to their document locations and positions.
Supports persistence to disk for fast reloading.
"""

import json
from pathlib import Path
from typing import Optional


class PatternIndex:
    """Inverted index mapping patterns to document locations.

    Thread-safe for reads, not for writes (build once, read many).

    Example:
        >>> index = PatternIndex()
        >>> index.add("proxy", "doc1.txt", [10, 245])
        >>> index.add("proxy", "doc2.txt", [892])
        >>> index.get("proxy")
        [('doc1.txt', [10, 245]), ('doc2.txt', [892])]
    """

    def __init__(self):
        """Initialize empty index."""
        # Dict[pattern, Dict[doc_id, List[positions]]]
        self._index: dict[str, dict[str, list[int]]] = {}
        self._doc_count: int = 0
        self._pattern_count: int = 0

    def add(self, pattern: str, doc_id: str, positions: list[int]) -> None:
        """Add pattern occurrences to index.

        Args:
            pattern: The pattern string
            doc_id: Document identifier
            positions: List of start positions in document
        """
        if not positions:
            return

        if pattern not in self._index:
            self._index[pattern] = {}
            self._pattern_count += 1

        if doc_id not in self._index[pattern]:
            self._index[pattern][doc_id] = []

        self._index[pattern][doc_id].extend(positions)
        self._index[pattern][doc_id].sort()

    def get(self, pattern: str) -> list[tuple[str, list[int]]]:
        """Get all occurrences of a pattern.

        Args:
            pattern: Pattern to look up

        Returns:
            List of (doc_id, positions) tuples
        """
        if pattern not in self._index:
            return []

        return [(doc_id, list(positions)) for doc_id, positions in self._index[pattern].items()]

    def has(self, pattern: str) -> bool:
        """Check if pattern exists in index.

        Args:
            pattern: Pattern to check

        Returns:
            True if pattern exists
        """
        return pattern in self._index

    def patterns(self) -> list[str]:
        """Get all patterns in index.

        Returns:
            List of all patterns
        """
        return list(self._index.keys())

    def pattern_count(self) -> int:
        """Get number of unique patterns.

        Returns:
            Number of patterns
        """
        return self._pattern_count

    def doc_count(self) -> int:
        """Get number of documents.

        Returns:
            Number of unique documents
        """
        if not self._index:
            return 0

        docs = set()
        for pattern_docs in self._index.values():
            docs.update(pattern_docs.keys())
        return len(docs)

    def total_occurrences(self) -> int:
        """Get total number of pattern occurrences.

        Returns:
            Total occurrences across all patterns and documents
        """
        total = 0
        for pattern_docs in self._index.values():
            for positions in pattern_docs.values():
                total += len(positions)
        return total

    def save(self, path: str | Path) -> None:
        """Save index to disk.

        Uses JSON format for human readability.
        For large indexes, consider MessagePack or pickle.

        Args:
            path: Output file path
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "version": 1,
            "pattern_count": self._pattern_count,
            "doc_count": self.doc_count(),
            "total_occurrences": self.total_occurrences(),
            "index": self._index,
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, path: str | Path) -> "PatternIndex":
        """Load index from disk.

        Args:
            path: Input file path

        Returns:
            Loaded PatternIndex instance
        """
        path = Path(path)

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        index = cls()
        index._index = data["index"]
        index._pattern_count = data.get("pattern_count", len(data["index"]))

        return index

    def clear(self) -> None:
        """Clear all data from index."""
        self._index.clear()
        self._pattern_count = 0

    def stats(self) -> dict:
        """Get index statistics.

        Returns:
            Dict with statistics:
            - pattern_count: Number of unique patterns
            - doc_count: Number of documents
            - total_occurrences: Total pattern occurrences
            - avg_occurrences_per_pattern: Average occurrences per pattern
        """
        total = self.total_occurrences()
        patterns = self._pattern_count

        return {
            "pattern_count": patterns,
            "doc_count": self.doc_count(),
            "total_occurrences": total,
            "avg_occurrences_per_pattern": total / patterns if patterns > 0 else 0,
        }
