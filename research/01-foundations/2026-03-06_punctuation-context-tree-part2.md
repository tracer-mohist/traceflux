### Example Construction

```text
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
    No internal punctuation -> Leaf node

Level 2:
  Grandchild 1a: build_punct_tree("Hello", START, ",", 2)
    No internal punctuation -> Leaf node

  Grandchild 1b: build_punct_tree(" world", ",", "!", 2)
    No internal punctuation -> Leaf node

Result:
  Root
  +-- "Hello, world" (START -> "!")
  |   +-- "Hello" (START -> ",")
  |   +-- " world" ("," -> "!")
  +-- " How are you" ("!" -> "?")
```

---

## Noise Filtering via Type Hash

### Problem: Random Text Has No Structure

```text
Random: "xkjf832jdksl"
No punctuation -> No tree structure -> Likely noise

Structured: "Hello, world!"
Has punctuation -> Has tree structure -> Likely meaningful
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
is_meaningful("xkjf832jdksl") -> False (no punctuation)
is_meaningful("Hello") -> False (no internal structure)
is_meaningful("Hello, world!") -> True (has structure)
is_meaningful("Hello, world! How are you?") -> True (rich structure)
```

### Why This Works

1. RANDOM-TEXT rarely has valid punctuation patterns
2. STRUCTURED-TEXT has nested punctuation (sentences -> clauses -> phrases)
3. TYPE-HASH-DIVERSITY indicates varied punctuation (natural language trait)

---

## Tree Properties

### Structural Metrics

```text
For each tree:
  - Depth: Max nesting level
  - Branching factor: Average children per node
  - Leaf count: Number of terminal segments
  - Type hash diversity: Number of unique (pre, post) pairs
```

### Example Metrics

```text
Text 1: "Hello, world!"
  Tree:
    Root
    +-- "Hello" (START -> ",")
    +-- " world" ("," -> "!")

  Metrics:
    Depth: 2
    Branching: 2 (root has 2 children)
    Leaves: 2
    Type diversity: 2 (hash(START,",") != hash(",", "!"))

Text 2: "xkjf832jdksl"
  Tree:
    Root
    +-- "xkjf832jdksl" (START -> END)

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
| STRUCTURE | Linear sequence | Hierarchical nesting |
| ANALYSIS | Sequential | Recursive |
| NOISE-FILTERING | Hard (no structure to check) | Easy (check tree depth) |
| QUERY | Scan all segments | Navigate by type hash |
| CONTEXT | Lost (siblings only) | Preserved (parent-child) |
| EFFICIENCY | O(n) scan | O(log n) tree navigation |

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

        # Base case: no punctuation at this level -> leaf
        if not positions:
            # Try next level (deeper punctuation)
            if level < len(PUNCT_HIERARCHY) - 1:
                return _build(text, pre, post, level + 1, start)
            else:
                # No more levels -> leaf node
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
