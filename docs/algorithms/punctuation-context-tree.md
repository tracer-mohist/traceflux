# Punctuation Context Tree

Purpose: Build hierarchical tree structure from punctuation context.

NOTE: Consolidated from research/01-foundations/ (2026-03-11)

---

## Core Insight

Why record pre/post punctuation?

1. Filter noise - Most random sequences don't have valid punctuation context
2. Create tree structure - Punctuation hashes form nested levels
3. Recursive nature - Analysis is sequential, but structure is hierarchical

Key Metaphor:

Analysis: Sequential (left-to-right reading)
Structure: Tree (nested by punctuation context)

Like: Reading a book (sequential) -> Understanding chapters/sections (hierarchical)

---

## Problem: Flat Segmentation Loses Structure

### Current Approach (Flat List)

Text: "Hello, world! How are you? I'm fine."

Segments (flat):
  1. "Hello" (pre: START, post: ",")
  2. "world" (pre: ",", post: "!")
  3. "How are you" (pre: "!", post: "?")
  4. "I'm fine" (pre: "?", post: ".")

Problem: No hierarchy - all segments are siblings.

### Desired Approach (Tree Structure)

Text: "Hello, world! How are you? I'm fine."

Structure (tree):
  Root (START -> END)
  +-- Sentence 1: "Hello, world!"
  |   +-- "Hello" (START -> ",")
  |   +-- "world" ("," -> "!")
  +-- Sentence 2: "How are you?"
  |   +-- "How are you" ("!" -> "?")
  +-- Sentence 3: "I'm fine."
      +-- "I'm fine" ("?" -> ".")

Better: Captures flow and nesting.

---

## Punctuation Context Tree (PCT)

### Level 0: Root Node

Root:
  type_hash: hash((START, END))
  children: [Level 1 nodes]
  content: Full text

### Level 1: Top-Level Segments

Segments separated by sentence-ending punctuation (. ! ?):

Text: "Hello, world! How are you? I'm fine."

Level 1 nodes:
  Node 1: "Hello, world" (pre: START, post: "!")
  Node 2: "How are you" (pre: "!", post: "?")
  Node 3: "I'm fine" (pre: "?", post: ".")

### Level 2: Sub-Segments

Within each Level 1 node, split by weaker punctuation (, ; :):

Node 1: "Hello, world" (START -> "!")
  +-- "Hello" (START -> ",")
  +-- "world" ("," -> "!")

### Type Identifier

type_hash = hash((pre_punct, post_punct))

Example:
  hash((START, ",")) = 101
  hash((",", "!")) = 205
  hash(("!", "?")) = 312
  hash(("?", ".")) = 418

This allows:
  - Fast grouping of similar contexts
  - Pattern matching across documents
  - Noise filtering (invalid hashes)

---

## Implementation Reference

See: [punctuation-context-tree-impl.md](./punctuation-context-tree-impl.md)

- Punctuation hierarchy definition
- Recursive segmentation algorithm
- Tree traversal methods
- Pattern matching

---

## Applications

### 1. Noise Filtering

Random text: "asdf jkl; qwerty"

PCT analysis:
  - No valid sentence structure
  - No hierarchical punctuation
  - Low tree depth

Conclusion: Likely noise, skip analysis.

### 2. Structure Comparison

Compare two texts by their PCT:

Text A: "Hello, world! How are you?"
Text B: "Hi there! What's up?"

PCT similarity:
  - Same tree depth: YES (2 levels)
  - Same punctuation pattern: YES (!, ?)
  - Similar structure: HIGH

Use case: Detect similar writing styles

### 3. Context-Aware Search

Search: "world"

With PCT:
  - Found in: "Hello, world!"
  - Context: ("," -> "!")
  - Siblings: "Hello"
  - Parent: Sentence 1

Without PCT:
  - Found: "world"
  - No context

PCT provides rich context for ranking!

### 4. Hierarchical Summarization

PCT allows summarization at multiple levels:

Level 0 (Root): Full text summary
Level 1 (Sentences): Key sentences
Level 2 (Clauses): Key phrases

User can zoom in/out!

---

## Performance

### Tree Depth

Typical depths:
  - Simple sentence: 2-3 levels
  - Complex paragraph: 4-5 levels
  - Full document: 6-8 levels

Max depth: Limited by punctuation hierarchy (4 levels defined)

### Memory Usage

Tree size ~= 2-3x original text size

Optimization:
  - Store only type_hash, not full punctuation strings
  - Share common subtrees
  - Lazy construction (build on-demand)

---

## Related

- [Text Segmentation](../core/text-segmentation.md) - Basic segmentation
- [N-gram Analysis](../core/ngram-analysis.md) - Pattern extraction within segments
- [Mathematical Model](../core/mathematical-model.md) - Formal definitions
- [Implementation](./punctuation-context-tree-impl.md) - Code examples

---

Last Updated: 2026-03-11
Source Files: 2026-03-06_punctuation-context-tree*.md, 2026-03-06_punctuation-namespace-index*.md
