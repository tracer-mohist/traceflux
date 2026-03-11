# Research: Punctuation Context Tree (PCT)

DATE: 2026-03-06
STATUS: Algorithm Design -- Tree Structure
TOPIC: Using pre/post punctuation hashes to build nested tree structure

---

## Core Insight (User's Key Point)

WHY-RECORD-PRE/POST-PUNCTUATION?

1. FILTER-NOISE -- Most random sequences don't have valid punctuation context
2. CREATE-TREE-STRUCTURE -- Punctuation hashes form nested levels
3. RECURSIVE-NATURE -- Analysis is sequential, but structure is hierarchical

KEY-METAPHOR:
```text
Analysis: Sequential (left-to-right reading)
Structure: Tree (nested by punctuation context)

Like: Reading a book (sequential) -> Understanding chapters/sections (hierarchical)
```

---

## Problem: Flat Segmentation Loses Structure

### Current Approach (Flat List)

```text
Text: "Hello, world! How are you? I'm fine."

Segments (flat):
  1. "Hello" (pre: START, post: ",")
  2. "world" (pre: ",", post: "!")
  3. "How are you" (pre: "!", post: "?")
  4. "I'm fine" (pre: "?", post: ".")

Problem: No hierarchy -- all segments are siblings.
```

### Desired Approach (Tree Structure)

```text
Text: "Hello, world! How are you? I'm fine."

Structure (tree):
  Root (START -> END)
  +-- "Hello" (START -> ",")
  |   +-- "world" ("," -> "!")
  |       +-- "How are you" ("!" -> "?")
  |           +-- "I'm fine" ("?" -> ".")
  +-- (END)

Better: Captures flow and nesting.
```

---

## Proposed: Punctuation Context Tree (PCT)

### Level 0: Root Node

```text
Root:
  type_hash: hash((START, END))
  children: [Level 1 nodes]
  content: Full text
```

### Level 1: Top-Level Segments

```text
Segments separated by sentence-ending punctuation (. ! ?):

"Hello, world! How are you? I'm fine."

Level 1 nodes:
  Node 1: "Hello, world" (pre: START, post: "!")
  Node 2: "How are you" (pre: "!", post: "?")
  Node 3: "I'm fine" (pre: "?", post: ".")
```

### Level 2: Sub-Segments

```text
Within each Level 1 node, split by comma/semicolon:

Node 1: "Hello, world"
  Child 1a: "Hello" (pre: START, post: ",")
  Child 1b: "world" (pre: ",", post: "!")

Node 2: "How are you"
  (no internal punctuation -> leaf node)

Node 3: "I'm fine"
  (no internal punctuation -> leaf node)
```

### Full Tree

```text
Root (START -> END)
|
+-- Level 1: "Hello, world" (START -> "!")
|   +-- Level 2: "Hello" (START -> ",")
|   +-- Level 2: "world" ("," -> "!")
|
+-- Level 1: "How are you" ("!" -> "?")
|   +-- (leaf -- no internal punctuation)
|
+-- Level 1: "I'm fine" ("?" -> ".")
    +-- (leaf -- no internal punctuation)
```

---

## Type Hash as Tree Key

### Hash Hierarchy

```text
Level 1 keys (sentence boundaries):
  hash((START, "!")) -> Node 1
  hash(("!", "?")) -> Node 2
  hash(("?", ".")) -> Node 3

Level 2 keys (internal boundaries):
  hash((START, ",")) -> Child 1a
  hash((",", "!")) -> Child 1b
```

### Tree Traversal

```text
To find segment with context (START -> ","):
  1. Compute hash((START, ","))
  2. Search tree level-by-level
  3. Match: Level 2, Child 1a

To find all segments with post-punct ",":
  1. Traverse tree
  2. Filter: node.type_hash.post == ","
  3. Results: Child 1a
```

---

## Recursive Structure

### Definition

```text
PCT Node:
  type_hash: hash((pre_punct, post_punct))
  content: str (text between punctuation)
  children: List[PCT Node] (sub-segments)
  parent: PCT Node (or None for root)
  level: int (depth in tree)
```

### Recursive Construction

```python
def build_punct_tree(text, pre_punct=None, post_punct=None, level=0):
    """
    Recursively build Punctuation Context Tree.

    Args:
        text: Text segment to parse
        pre_punct: Punctuation before this segment
        post_punct: Punctuation after this segment
        level: Current depth (0 = root)

    Returns:
        PCTNode with children (sub-segments)
    """
    # Base case: no internal punctuation -> leaf node
    internal_punct = find_internal_punctuation(text)
    if not internal_punct:
        return PCTNode(
            type_hash=hash((pre_punct, post_punct)),
            content=text,
            children=[],
            level=level
        )

    # Recursive case: split by internal punctuation
    segments = split_by_punctuation(text, internal_punct)

    children = []
    prev_punct = pre_punct
    for i, seg_content in enumerate(segments):
        # Determine post-punct for this segment
        if i < len(segments) - 1:
            seg_post_punct = internal_punct
        else:
            seg_post_punct = post_punct

        # Recursively build child
        child = build_punct_tree(
            seg_content,
            pre_punct=prev_punct,
            post_punct=seg_post_punct,
            level=level + 1
        )
        children.append(child)
        prev_punct = seg_post_punct

    return PCTNode(
        type_hash=hash((pre_punct, post_punct)),
        content=text,
        children=children,
        level=level
    )
```
