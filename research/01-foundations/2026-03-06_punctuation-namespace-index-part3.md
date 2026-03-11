### 4. One-Pass Efficiency

```text
O(n) single scan
No recursion
No backtracking
Build index on-the-fly
```

---

## Comparison with Previous Approaches

| Aspect | Character-Level | Punctuation Tree | Punctuation Namespace |
|--------|----------------|------------------|----------------------|
| UNIT | Character/N-gram | Segment | Segment + Namespace |
| STRUCTURE | Flat/Graph | Recursive Tree | One-Pass Index |
| PUNCTUATION | Boundary | Hierarchy | Namespace Marker |
| SPACE | Content | Content | Separator |
| PASSES | 1-2 | Multiple | 1 |
| COMPLEXITY | O(n) | O(n log n) | O(n) |

---

## Implementation Notes

### Punctuation Set

```python
# Explicit punctuation set (includes space, escapes)
PUNCTUATION = set(' \t\n\r'  # Whitespace
                  ',.!?;:'   # Standard punctuation
                  '"\'`'     # Quotes
                  '()[]{}<>' # Brackets
                  '\\/|'     # Escapes/separators
                  '@#$%^&*_+-=~'  # Special chars
                  )
```

### One-Pass Scanner

```python
class PunctuationNamespaceIndex:
    def __init__(self):
        self.index = []  # List of (type_hash, content, start, end)
        self.inverted = defaultdict(list)  # type_hash -> [entries]

    def scan(self, text, doc_id):
        pre_punct = 'S'
        start = 0
        i = 0

        while i < len(text):
            if text[i] in PUNCTUATION:
                # End of segment
                if i > start:
                    content = text[start:i]
                    # Find next non-punct
                    j = i
                    while j < len(text) and text[j] in PUNCTUATION:
                        j += 1
                    post_punct = text[j] if j < len(text) else 'E'

                    type_hash = hash((pre_punct, post_punct))
                    entry = (type_hash, content, start, i, doc_id)
                    self.index.append(entry)
                    self.inverted[type_hash].append(entry)

                    start = j
                    pre_punct = post_punct
                    i = j
                else:
                    i += 1
            else:
                i += 1

        # Handle last segment
        if start < len(text):
            content = text[start:]
            type_hash = hash((pre_punct, 'E'))
            entry = (type_hash, content, start, len(text), doc_id)
            self.index.append(entry)
            self.inverted[type_hash].append(entry)
```

---

## Key Insights

### 1. Character Pairs as Namespaces

```text
(pre, post) is like a namespace identifier:
  - ("S", ":") -> Key namespace
  - (":", ",") -> Value namespace
  - (">", "<") -> Element content namespace
```

### 2. Dynamic Subset Relations

```text
Subset relations emerge from text, not predefined:
  - In JSON: (":", ",") SUBSET (S, "}")
  - In HTML: (">", "<") SUBSET (S, E)
  - Different text -> Different hierarchies
```

### 3. One-Pass Efficiency

```text
No recursion, no backtracking:
  - Read left-to-right
  - Segment on punctuation
  - Build index on-the-fly
  - O(n) time, O(n) space
```

### 4. Format Agnostic

```text
JSON, HTML, YAML, plain text:
  - Same algorithm
  - Different namespaces emerge
  - No format-specific parsing
```

---

## Next Steps

1. IMPLEMENT-ONE-PASS-SCANNER -- PunctuationNamespaceIndex class
2. TEST-ON-JSON/HTML -- Verify noise reduction
3. QUERY-BY-NAMESPACE -- Find segments by (pre, post) pair
4. VISUALIZE-NAMESPACE-TREE -- Show dynamic hierarchy

---

STATUS: Algorithm clarified, one-pass design complete
NEXT: Implement and test on real data (JSON, HTML, plain text)
PHILOSOPHY: One-pass scan, namespace indexing, format-agnostic
