# Punctuation Context Tree Implementation

Purpose: Code examples for PCT algorithm.

NOTE: Companion to punctuation-context-tree.md (2026-03-11)

---

## Punctuation Hierarchy

```python
PUNCTUATION_LEVELS = {
    0: {'.', '!', '?'},      # Sentence level
    1: {',', ';', ':'},       # Clause level
    2: {'"', "'", '(', ')'},  # Phrase level
    3: {'-', '—', '–'},       # Break level
}
```

---

## Recursive Segmentation

```python
def build_punctuation_tree(text, level=0, pre='START', post='END'):
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

    punct_set = PUNCTUATION_LEVELS.get(level, set())

    if not punct_set or level > 3:
        return node

    split_positions = [
        i for i, char in enumerate(text)
        if char in punct_set
    ]

    if not split_positions:
        return node

    segments = split_by_positions(text, split_positions)

    for i, segment in enumerate(segments):
        child_pre = post if i == 0 else split_positions[i-1]
        child_post = split_positions[i] if i < len(split_positions) else post

        child_node = build_punctuation_tree(
            segment, level + 1, child_pre, child_post
        )
        node['children'].append(child_node)

    return node
```

---

## Tree Traversal

```python
def dfs_traverse(node, callback):
    """Process nodes depth-first."""
    callback(node)
    for child in node['children']:
        dfs_traverse(child, callback)

def bfs_traverse(root, callback):
    """Process nodes level-by-level."""
    queue = [root]
    while queue:
        node = queue.pop(0)
        callback(node)
        queue.extend(node['children'])
```

---

## Pattern Matching

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

Last Updated: 2026-03-11
