# Punctuation Context Tree

**Purpose**: Build hierarchical tree structure from punctuation context.

**NOTE**: Consolidated from research/01-foundations/ (2026-03-11)

---

## Core Insight

**Why record pre/post punctuation?**

1. **Filter noise** — Most random sequences don't have valid punctuation context
2. **Create tree structure** — Punctuation hashes form nested levels
3. **Recursive nature** — Analysis is sequential, but structure is hierarchical

**Key Metaphor**:
```text
Analysis: Sequential (left-to-right reading)
Structure: Tree (nested by punctuation context)

Like: Reading a book (sequential) → Understanding chapters/sections (hierarchical)
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

Problem: No hierarchy — all segments are siblings.
```

### Desired Approach (Tree Structure)

```text
Text: "Hello, world! How are you? I'm fine."

Structure (tree):
  Root (START → END)
  └── Sentence 1: "Hello, world!"
      ├── "Hello" (START → ",")
      └── "world" ("," → "!")
  └── Sentence 2: "How are you?"
      └── "How are you" ("!" → "?")
  └── Sentence 3: "I'm fine."
      └── "I'm fine" ("?" → ".")

Better: Captures flow and nesting.
```

---

## Punctuation Context Tree (PCT)

### Level 0: Root Node

```text
Root:
  type_hash: hash((START, END))
  children: [Level 1 nodes]
  content: Full text
```

### Level 1: Top-Level Segments

Segments separated by sentence-ending punctuation (`. ! ?`):

```text
Text: "Hello, world! How are you? I'm fine."

Level 1 nodes:
  Node 1: "Hello, world" (pre: START, post: "!")
  Node 2: "How are you" (pre: "!", post: "?")
  Node 3: "I'm fine" (pre: "?", post: ".")
```

### Level 2: Sub-Segments

Within each Level 1 node, split by weaker punctuation (`, ; :`):

```text
Node 1: "Hello, world" (START → "!")
  ├── "Hello" (START → ",")
  └── "world" ("," → "!")
```

### Type Hash

```text
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
```

---

## Tree Construction Algorithm

### Step 1: Define Punctuation Hierarchy

```python
PUNCTUATION_LEVELS = {
    0: {'.', '!', '?'},      # Sentence level
    1: {',', ';', ':'},       # Clause level
    2: {'"', "'", '(', ')'},  # Phrase level
    3: {'-', '—', '–'},       # Break level
}
```

### Step 2: Recursive Segmentation

```python
def build_punctuation_tree(text, level=0, pre=START, post=END):
    """
    Build Punctuation Context Tree recursively.

    Args:
        text: Text to segment
        level: Current punctuation level (0 = sentence)
        pre: Pre-punctuation (or START)
        post: Post-punctuation (or END)

    Returns: Tree node
    """
    node = {
        'content': text,
        'pre': pre,
        'post': post,
        'type_hash': hash((pre, post)),
        'level': level,
        'children': []
    }

    # Get punctuation for this level
    punct_set = PUNCTUATION_LEVELS.get(level, set())

    if not punct_set or level > 3:
        # Leaf node
        return node

    # Find split points
    split_positions = []
    for i, char in enumerate(text):
        if char in punct_set:
            split_positions.append(i)

    if not split_positions:
        # No splits at this level
        return node

    # Split and recurse
    segments = split_by_positions(text, split_positions)

    for i, segment in enumerate(segments):
        child_pre = post if i == 0 else split_positions[i-1]
        child_post = split_positions[i] if i < len(split_positions) else post

        child_node = build_punctuation_tree(
            segment,
            level + 1,
            child_pre,
            child_post
        )
        node['children'].append(child_node)

    return node
```

### Step 3: Example Output

```text
Input: "Hello, world! How are you? I'm fine."

Tree:
  Root (START → END, level=0)
  ├── Node 1 (START → "!", level=0)
  │   ├── "Hello" (START → ",", level=1)
  │   └── "world" ("," → "!", level=1)
  ├── Node 2 ("!" → "?", level=0)
  │   └── "How are you" ("!" → "?", level=1)
  └── Node 3 ("?" → ".", level=0)
      └── "I'm fine" ("?" → ".", level=1)
```

---

## Applications

### 1. Noise Filtering

```text
Random text: "asdf jkl; qwerty"

PCT analysis:
  - No valid sentence structure
  - No hierarchical punctuation
  - Low tree depth

Conclusion: Likely noise, skip analysis.
```

### 2. Structure Comparison

```text
Compare two texts by their PCT:

Text A: "Hello, world! How are you?"
Text B: "Hi there! What's up?"

PCT similarity:
  - Same tree depth: YES (2 levels)
  - Same punctuation pattern: YES (!, ?)
  - Similar structure: HIGH

Use case: Detect similar writing styles
```

### 3. Context-Aware Search

```text
Search: "world"

With PCT:
  - Found in: "Hello, world!"
  - Context: ("," → "!")
  - Siblings: "Hello"
  - Parent: Sentence 1

Without PCT:
  - Found: "world"
  - No context

PCT provides rich context for ranking!
```

### 4. Hierarchical Summarization

```text
PCT allows summarization at multiple levels:

Level 0 (Root): Full text summary
Level 1 (Sentences): Key sentences
Level 2 (Clauses): Key phrases

User can zoom in/out!
```

---

## Tree Traversal

### Depth-First (Detailed Analysis)

```python
def dfs_traverse(node, callback):
    """Process nodes depth-first."""
    callback(node)
    for child in node['children']:
        dfs_traverse(child, callback)
```

### Breadth-First (Level-by-Level)

```python
def bfs_traverse(root, callback):
    """Process nodes level-by-level."""
    queue = [root]
    while queue:
        node = queue.pop(0)
        callback(node)
        queue.extend(node['children'])
```

### Pattern Matching

```python
def find_pattern(node, target_type_hash):
    """Find all nodes with matching type hash."""
    matches = []

    if node['type_hash'] == target_type_hash:
        matches.append(node)

    for child in node['children']:
        matches.extend(find_pattern(child, target_type_hash))

    return matches
```

---

## Performance

### Tree Depth

```text
Typical depths:
  - Simple sentence: 2-3 levels
  - Complex paragraph: 4-5 levels
  - Full document: 6-8 levels

Max depth: Limited by punctuation hierarchy (4 levels defined)
```

### Memory Usage

```text
Tree size ≈ 2-3x original text size

Optimization:
  - Store only type_hash, not full punctuation strings
  - Share common subtrees
  - Lazy construction (build on-demand)
```

---

## Related

- [Text Segmentation](../core/text-segmentation.md) - Basic segmentation
- [N-gram Analysis](../core/ngram-analysis.md) - Pattern extraction within segments
- [Mathematical Model](../core/mathematical-model.md) - Formal definitions

---

**Last Updated**: 2026-03-11
**Source Files**: `2026-03-06_punctuation-context-tree*.md`, `2026-03-06_punctuation-namespace-index*.md`
