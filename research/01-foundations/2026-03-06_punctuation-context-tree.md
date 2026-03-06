# Research: Punctuation Context Tree (PCT)

**Date**: 2026-03-06  
**Status**: Algorithm Design — Tree Structure  
**Topic**: Using pre/post punctuation hashes to build nested tree structure

---

## Core Insight (User's Key Point)

**Why record pre/post punctuation?**

1. **Filter noise** — Most random sequences don't have valid punctuation context
2. **Create tree structure** — Punctuation hashes form nested levels
3. **Recursive nature** — Analysis is sequential, but structure is hierarchical

**Key Metaphor**:
```
Analysis: Sequential (left-to-right reading)
Structure: Tree (nested by punctuation context)

Like: Reading a book (sequential) → Understanding chapters/sections (hierarchical)
```

---

## Problem: Flat Segmentation Loses Structure

### Current Approach (Flat List)

```
Text: "Hello, world! How are you? I'm fine."

Segments (flat):
  1. "Hello" (pre: START, post: ",")
  2. "world" (pre: ",", post: "!")
  3. "How are you" (pre: "!", post: "?")
  4. "I'm fine" (pre: "?", post: ".")

Problem: No hierarchy — all segments are siblings.
```

### Desired Approach (Tree Structure)

```
Text: "Hello, world! How are you? I'm fine."

Structure (tree):
  Root (START → END)
  ├── "Hello" (START → ",")
  │   └── "world" ("," → "!")
  │       └── "How are you" ("!" → "?")
  │           └── "I'm fine" ("?" → ".")
  └── (END)

Better: Captures flow and nesting.
```

---

## Proposed: Punctuation Context Tree (PCT)

### Level 0: Root Node

```
Root:
  type_hash: hash((START, END))
  children: [Level 1 nodes]
  content: Full text
```

### Level 1: Top-Level Segments

```
Segments separated by sentence-ending punctuation (. ! ?):

"Hello, world! How are you? I'm fine."

Level 1 nodes:
  Node 1: "Hello, world" (pre: START, post: "!")
  Node 2: "How are you" (pre: "!", post: "?")
  Node 3: "I'm fine" (pre: "?", post: ".")
```

### Level 2: Sub-Segments

```
Within each Level 1 node, split by comma/semicolon:

Node 1: "Hello, world"
  Child 1a: "Hello" (pre: START, post: ",")
  Child 1b: "world" (pre: ",", post: "!")

Node 2: "How are you"
  (no internal punctuation → leaf node)

Node 3: "I'm fine"
  (no internal punctuation → leaf node)
```

### Full Tree

```
Root (START → END)
│
├── Level 1: "Hello, world" (START → "!")
│   ├── Level 2: "Hello" (START → ",")
│   └── Level 2: "world" ("," → "!")
│
├── Level 1: "How are you" ("!" → "?")
│   └── (leaf — no internal punctuation)
│
└── Level 1: "I'm fine" ("?" → ".")
    └── (leaf — no internal punctuation)
```

---

## Type Hash as Tree Key

### Hash Hierarchy

```
Level 1 keys (sentence boundaries):
  hash((START, "!")) → Node 1
  hash(("!", "?")) → Node 2
  hash(("?", ".")) → Node 3

Level 2 keys (internal boundaries):
  hash((START, ",")) → Child 1a
  hash((",", "!")) → Child 1b
```

### Tree Traversal

```
To find segment with context (START → ","):
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

```
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
    # Base case: no internal punctuation → leaf node
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

### Example Construction

```
Input: "Hello, world! How are you?"

Level 0 (Root):
  build_punct_tree("Hello, world! How are you?", START, END, 0)
  
  Internal punctuation found: "!" (sentence boundary)
  
  Split: ["Hello, world", " How are you"]
  
  Recurse for each segment...

Level 1:
  Child 1: build_punct_tree("Hello, world", START, "!", 1)
    Internal punctuation: ","
    Split: ["Hello", " world"]
    Recurse...
  
  Child 2: build_punct_tree(" How are you", "!", "?", 1)
    No internal punctuation → Leaf node

Level 2:
  Grandchild 1a: build_punct_tree("Hello", START, ",", 2)
    No internal punctuation → Leaf node
  
  Grandchild 1b: build_punct_tree(" world", ",", "!", 2)
    No internal punctuation → Leaf node

Result:
  Root
  ├── "Hello, world" (START → "!")
  │   ├── "Hello" (START → ",")
  │   └── " world" ("," → "!")
  └── " How are you" ("!" → "?")
```

---

## Noise Filtering via Type Hash

### Problem: Random Text Has No Structure

```
Random: "xkjf832jdksl"
No punctuation → No tree structure → Likely noise

Structured: "Hello, world!"
Has punctuation → Has tree structure → Likely meaningful
```

### Filtering Strategy

```python
def is_meaningful(text, min_tree_depth=1, min_segments=2):
    """
    Check if text has meaningful structure.
    
    Criteria:
    1. Has punctuation (can build tree)
    2. Tree depth >= min_tree_depth
    3. Number of segments >= min_segments
    """
    tree = build_punct_tree(text)
    
    # Check tree depth
    if tree.max_depth() < min_tree_depth:
        return False
    
    # Check segment count
    if tree.count_segments() < min_segments:
        return False
    
    # Check type hash diversity
    unique_hashes = len(set(node.type_hash for node in tree.all_nodes()))
    if unique_hashes < 2:  # All same punctuation? Suspicious
        return False
    
    return True

# Examples
is_meaningful("xkjf832jdksl") → False (no punctuation)
is_meaningful("Hello") → False (no internal structure)
is_meaningful("Hello, world!") → True (has structure)
is_meaningful("Hello, world! How are you?") → True (rich structure)
```

### Why This Works

1. **Random text** rarely has valid punctuation patterns
2. **Structured text** has nested punctuation (sentences → clauses → phrases)
3. **Type hash diversity** indicates varied punctuation (natural language trait)

---

## Tree Properties

### Structural Metrics

```
For each tree:
  - Depth: Max nesting level
  - Branching factor: Average children per node
  - Leaf count: Number of terminal segments
  - Type hash diversity: Number of unique (pre, post) pairs
```

### Example Metrics

```
Text 1: "Hello, world!"
  Tree:
    Root
    ├── "Hello" (START → ",")
    └── " world" ("," → "!")
  
  Metrics:
    Depth: 2
    Branching: 2 (root has 2 children)
    Leaves: 2
    Type diversity: 2 (hash(START,",") ≠ hash(",", "!"))

Text 2: "xkjf832jdksl"
  Tree:
    Root
    └── "xkjf832jdksl" (START → END)
  
  Metrics:
    Depth: 1
    Branching: 0 (no children)
    Leaves: 1
    Type diversity: 1 (only hash(START, END))

Verdict: Text 1 is structured, Text 2 is likely noise.
```

---

## Comparison: List vs Tree

| Aspect | Flat List | Punctuation Context Tree |
|--------|-----------|--------------------------|
| **Structure** | Linear sequence | Hierarchical nesting |
| **Analysis** | Sequential | Recursive |
| **Noise filtering** | Hard (no structure to check) | Easy (check tree depth) |
| **Query** | Scan all segments | Navigate by type hash |
| **Context** | Lost (siblings only) | Preserved (parent-child) |
| **Efficiency** | O(n) scan | O(log n) tree navigation |

---

## Implementation Details

### PCT Node Class

```python
@dataclass
class PCTNode:
    type_hash: int  # hash((pre_punct, post_punct))
    pre_punct: Optional[str]
    post_punct: Optional[str]
    content: str
    children: List['PCTNode']
    level: int
    doc_id: Optional[int] = None
    start_pos: Optional[int] = None
    end_pos: Optional[int] = None
    
    def is_leaf(self) -> bool:
        return len(self.children) == 0
    
    def max_depth(self) -> int:
        if self.is_leaf():
            return self.level
        return max(child.max_depth() for child in self.children)
    
    def count_segments(self) -> int:
        if self.is_leaf():
            return 1
        return sum(child.count_segments() for child in self.children)
    
    def all_nodes(self) -> List['PCTNode']:
        """Get all nodes in subtree (including self)."""
        result = [self]
        for child in self.children:
            result.extend(child.all_nodes())
        return result
    
    def find_by_type_hash(self, target_hash: int) -> List['PCTNode']:
        """Find all nodes with matching type hash."""
        result = []
        for node in self.all_nodes():
            if node.type_hash == target_hash:
                result.append(node)
        return result
```

### Building the Tree

```python
def build_punct_tree(text: str, doc_id: int = None) -> PCTNode:
    """
    Build Punctuation Context Tree from text.
    
    Punctuation hierarchy (split order):
      Level 1: . ! ? (sentence boundaries)
      Level 2: ; : (clause boundaries)
      Level 3: , (phrase boundaries)
      Level 4: " ' () [] {} (quoted/parenthetical)
    """
    # Define punctuation hierarchy
    PUNCT_HIERARCHY = [
        '.!?',      # Level 1: sentence
        ';:',       # Level 2: clause
        ',',        # Level 3: phrase
        '"\'()[]{}', # Level 4: quoted/parenthetical
    ]
    
    def _build(text: str, pre: str, post: str, level: int, start: int) -> PCTNode:
        # Find punctuation at current level
        punct_chars = PUNCT_HIERARCHY[min(level, len(PUNCT_HIERARCHY)-1)]
        
        # Find all positions of current-level punctuation
        positions = [(i, c) for i, c in enumerate(text) if c in punct_chars]
        
        # Base case: no punctuation at this level → leaf
        if not positions:
            # Try next level (deeper punctuation)
            if level < len(PUNCT_HIERARCHY) - 1:
                return _build(text, pre, post, level + 1, start)
            else:
                # No more levels → leaf node
                return PCTNode(
                    type_hash=hash((pre, post)),
                    pre_punct=pre,
                    post_punct=post,
                    content=text,
                    children=[],
                    level=level,
                    doc_id=doc_id,
                    start_pos=start,
                    end_pos=start + len(text)
                )
        
        # Recursive case: split by punctuation
        children = []
        prev_pos = 0
        prev_punct = pre
        
        for pos, punct in positions:
            # Extract segment before this punctuation
            seg_text = text[prev_pos:pos]
            if seg_text.strip():  # Skip empty segments
                child = _build(
                    seg_text,
                    prev_punct,
                    punct,
                    level + 1,
                    start + prev_pos
                )
                children.append(child)
            
            prev_pos = pos + 1
            prev_punct = punct
        
        # Handle last segment (after last punctuation)
        if prev_pos < len(text):
            seg_text = text[prev_pos:]
            if seg_text.strip():
                child = _build(
                    seg_text,
                    prev_punct,
                    post,
                    level + 1,
                    start + prev_pos
                )
                children.append(child)
        
        return PCTNode(
            type_hash=hash((pre, post)),
            pre_punct=pre,
            post_punct=post,
            content=text,
            children=children,
            level=level,
            doc_id=doc_id,
            start_pos=start,
            end_pos=start + len(text)
        )
    
    return _build(text, None, None, 0, 0)
```

---

## Query Examples

### Find Segments by Punctuation Context

```python
tree = build_punct_tree("Hello, world! How are you? I'm fine.")

# Find all segments ending with comma
target_hash = hash((None, ","))  # START → ","
matches = tree.find_by_type_hash(target_hash)
# Result: ["Hello"]

# Find all segments starting with "!"
target_hash = hash(("!", "?"))  # "!" → "?"
matches = tree.find_by_type_hash(target_hash)
# Result: [" How are you"]
```

### Find Deeply Nested Segments

```python
# Find segments at level >= 2 (deep nesting)
deep_segments = [
    node for node in tree.all_nodes()
    if node.level >= 2
]
# Result: ["Hello", " world"] (Level 2 nodes)
```

### Check Structural Richness

```python
def structural_richness(tree: PCTNode) -> float:
    """
    Measure how structured/rich the text is.
    
    Score = (depth * branching * type_diversity) / length
    """
    depth = tree.max_depth()
    branching = len(tree.children)
    type_diversity = len(set(n.type_hash for n in tree.all_nodes()))
    length = len(tree.content)
    
    if length == 0:
        return 0.0
    
    return (depth * branching * type_diversity) / length

# Examples
richness("xkjf832jdksl") → 0.0 (no structure)
richness("Hello") → low (shallow)
richness("Hello, world!") → medium
richness("Hello, world! How are you? I'm fine.") → high
```

---

## Key Insights

### 1. Tree Structure Captures Hierarchy

```
Flat: ["Hello", "world", "How are you", "I'm fine"]
Tree: Shows which segments are related (siblings under same parent)
```

### 2. Type Hash Enables Fast Filtering

```
hash((pre, post)) acts as tree key:
  - Navigate directly to matching nodes
  - Filter by punctuation pattern
  - Group segments by context type
```

### 3. Depth Indicates Meaningfulness

```
Depth 1: Single segment (likely noise or very short)
Depth 2-3: Some structure (likely meaningful)
Depth 4+: Rich structure (likely well-formed text)
```

### 4. Recursive Analysis, Hierarchical Storage

```
Analysis: Left-to-right scan (sequential)
Storage: Tree structure (hierarchical)

Benefit: Best of both worlds
  - Sequential: Easy to parse
  - Hierarchical: Easy to navigate
```

---

## Next Steps

1. **Implement PCT construction** — Recursive tree building
2. **Test noise filtering** — Verify depth/diversity thresholds
3. **Optimize type hash lookup** — Index by hash for O(1) access
4. **Compare with flat approach** — Measure filtering accuracy

---

**Status**: Tree structure design complete  
**Next**: Implement PCT construction algorithm  
**Philosophy**: Sequential analysis → Hierarchical storage → Efficient filtering
