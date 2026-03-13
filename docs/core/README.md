# Core Concepts

Purpose: Foundational concepts for TraceFlux text analysis.

---

## Overview

TraceFlux uses a layered approach to text analysis:

1. Text Segmentation - Split text into readable units (not by spaces)
2. N-gram Analysis - Extract character patterns at multiple scales
3. Frequency Ranking - Weight patterns by occurrence and position
4. Mathematical Model - Formal foundation for scoring and ranking

---

## Quick Start

New to TraceFlux? Read in this order:

1. [Text Segmentation](./text-segmentation.md) - How we split text (spaces are readable!)
2. [N-gram Analysis](./ngram-analysis.md) - Pattern extraction at character level
3. [Frequency Ranking](./frequency-ranking.md) - LZW + PageRank for weighting
4. [Mathematical Model](./mathematical-model.md) - Formal definitions and proofs

Need implementation details? See [Algorithms](../algorithms/README.md)

---

## Key Principles

### Space is Readable

Spaces are NOT punctuation. They are part of readable content.

```text
Wrong: "Hello world" -> ["Hello", "world"]
Right: "Hello world" -> ["Hello world"]
```

Why? Preserves word relationships and phrases.

### Character-Level First

Start analysis at character level, not word level.

- Captures sub-word patterns (prefixes, suffixes, roots)
- Language-agnostic (works for Chinese, English, mixed)
- Better for autocomplete and fuzzy matching

### Frequency + Structure

Raw frequency is not enough. Use:

- LZW compression for pattern discovery
- PageRank for structural importance
- Position weighting (start/end of text matters)

---

## File Structure

```text
core/
├── README.md               # This file - overview and navigation
├── text-segmentation.md    # How to split text correctly
├── ngram-analysis.md       # N-gram extraction and usage
├── frequency-ranking.md    # LZW + PageRank weighting
└── mathematical-model.md   # Formal mathematical foundation
```

---

## Related

- [Algorithms](../algorithms/README.md) - Implementation details
- [Theory](../theory/README.md) - Theoretical background
- [Design](../design/README.md) - System architecture

---

NOTE: Consolidated from research/01-foundations/ (2026-03-11)
