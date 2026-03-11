# Architecture

Purpose: How traceflux works internally.

REFERENCE: docs/PHILOSOPHY.md (design principles)
REFERENCE: docs/USAGE.md (usage guide)

---

## Overview

traceflux finds related concepts you do not know to search for.

It works by:
1. Finding repeated patterns in text
2. Building a co-occurrence graph
3. Scoring importance with PageRank
4. Traversing associations with BFS

---

## Pipeline

```bash
Text Files
    |
    v
Scanner (PNI segmentation)
    |
    v
PatternDetector (LZ77-style repeats)
    |
    v
CooccurrenceGraph (patterns together)
    |
    v
PageRank (importance scoring)
    |
    v
AssociativeSearch (BFS traversal)
    |
    v
Results
```

---

## Components

### Scanner

Segments text by punctuation (language-independent).

Preserves semantic units:
- IP addresses: 127.0.0.1 (not 127, 0, 0, 1)
- Version numbers: 1.0.0 (not 1, 0, 0)
- Identifiers: my_function (not my, function)

### PatternDetector

Finds repeated patterns using suffix arrays.

Complexity: O(n log n)

Algorithm: LZ77-style repeat detection.

### CooccurrenceGraph

Builds graph of patterns that appear together.

Window size: Configurable (default: 10 tokens)

Edge weight: Co-occurrence frequency.

### PageRank

Scores pattern importance.

Weighted by:
- Co-occurrence strength
- Graph connectivity

Output: Rank score for each pattern.

### AssociativeSearch

Traverses graph with BFS.

Supports:
- 1-hop: Direct co-occurrences
- 2-hop: Friends of friends
- 3-hop: Extended associations

Explains paths: Shows how terms are connected.

---

## Design Decisions

### No Tokenization

Why: Language independence.

Trade-off: Patterns may be fragments.

Mitigation: Tune min-length parameter.

### No Dictionary

Why: Works out-of-box, no training.

Trade-off: Need to tune parameters.

Mitigation: Document best practices.

### No ML/Embeddings

Why: Lightweight, fast, transparent.

Trade-off: No semantic understanding.

Mitigation: Pattern-based association (not meaning).

---

## Performance

### Complexity

- Scanning: O(n)
- Pattern detection: O(n log n)
- Graph building: O(m^2) where m = number of patterns
- PageRank: O(m * iterations)
- Association search: O(m) for BFS

### Typical Performance

Small codebase (100 files): Under 1 second

Medium codebase (1000 files): 5-10 seconds

Large codebase (10000 files): 30-60 seconds

---

## Related Documents

- docs/PHILOSOPHY.md -- Design principles
- docs/USAGE.md -- Usage guide
- docs/TESTING-PHILOSOPHY.md -- Testing approach

---

Last Updated: 2026-03-10
