## Query Examples

### Find Segments by Punctuation Context

```python
tree = build_punct_tree("Hello, world! How are you? I'm fine.")

# Find all segments ending with comma
target_hash = hash((None, ","))  # START -> ","
matches = tree.find_by_type_hash(target_hash)
# Result: ["Hello"]

# Find all segments starting with "!"
target_hash = hash(("!", "?"))  # "!" -> "?"
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
richness("xkjf832jdksl") -> 0.0 (no structure)
richness("Hello") -> low (shallow)
richness("Hello, world!") -> medium
richness("Hello, world! How are you? I'm fine.") -> high
```

---

## Key Insights

### 1. Tree Structure Captures Hierarchy

```text
Flat: ["Hello", "world", "How are you", "I'm fine"]
Tree: Shows which segments are related (siblings under same parent)
```

### 2. Type Hash Enables Fast Filtering

```text
hash((pre, post)) acts as tree key:
  - Navigate directly to matching nodes
  - Filter by punctuation pattern
  - Group segments by context type
```

### 3. Depth Indicates Meaningfulness

```text
Depth 1: Single segment (likely noise or very short)
Depth 2-3: Some structure (likely meaningful)
Depth 4+: Rich structure (likely well-formed text)
```

### 4. Recursive Analysis, Hierarchical Storage

```text
Analysis: Left-to-right scan (sequential)
Storage: Tree structure (hierarchical)

Benefit: Best of both worlds
  - Sequential: Easy to parse
  - Hierarchical: Easy to navigate
```

---

## Next Steps

1. IMPLEMENT-PCT-CONSTRUCTION -- Recursive tree building
2. TEST-NOISE-FILTERING -- Verify depth/diversity thresholds
3. OPTIMIZE-TYPE-HASH-LOOKUP -- Index by hash for O(1) access
4. COMPARE-WITH-FLAT-APPROACH -- Measure filtering accuracy

---

STATUS: Tree structure design complete
NEXT: Implement PCT construction algorithm
PHILOSOPHY: Sequential analysis -> Hierarchical storage -> Efficient filtering
