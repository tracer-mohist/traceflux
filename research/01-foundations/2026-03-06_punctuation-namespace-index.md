# Research: Punctuation Namespace Index (PNI)

**Date**: 2026-03-06  
**Status**: Algorithm Clarification  
**Topic**: Character pairs as namespaces/scopes, one-pass indexing

---

## Core Clarification (User's Correction)

### Previous Misunderstanding

I previously thought:
- Build tree recursively
- Multiple passes for analysis
- Complex hierarchy

### Correct Understanding

**Actual Algorithm**:
1. **One-pass sequential read** — Single scan, build index on-the-fly
2. **Space + escape chars = punctuation** — Used for segmentation
3. **No semantic analysis needed** — Pure mechanical segmentation
4. **Character pairs as namespaces** — (pre, post) defines scope
5. **Dynamic subset relations** — Based on actual text content

---

## Algorithm: One-Pass Segmentation

### Input → Output

```
Input: "hello??world"

Scan left-to-right:
  Position 0-4: "hello" (readable)
  Position 5-6: "??" (punctuation sequence)
  Position 7-11: "world" (readable)

Output:
  [("S", "?"), "hello"]
  [("?", "!"), "world"]  # Assuming "!" or END follows

Note: "??" is the boundary, not part of content.
```

---

### Example 2

```
Input: "hi mine?? world!"

Scan:
  "hi mine" (readable, includes space)
  "??" (punctuation sequence)
  " world" (readable, includes leading space)
  "!" (punctuation)

Output:
  [("S", "?"), "hi mine"]
  [("?", "!"), " world"]

Note: 
  - Segment 1: pre="S" (START), post="?" (first ? of ??)
  - Segment 2: pre="?" (last ? of ??), post="!"
```

---

## Character Pair as Namespace

### Key Insight

```
Character pair (pre, post) acts like:
  - Namespace identifier
  - Scope marker
  - Similar to `"` quotes or `()` parentheses

Example:
  ("S", "?") → Namespace A
  ("?", "!") → Namespace B
  ("!", ".") → Namespace C
```

### Subset Relations (Dynamic)

```
Based on text content, some pairs are subsets of others:

Text 1: "Hello, world! How are you?"
  Pairs: (S, ","), (",", "!"), ("!", "?"), ("?", END)
  
  Hierarchy:
    (S, END) — Root namespace
      ├── (S, ",") — Sub-namespace
      ├── (",", "!") — Sub-namespace
      └── ("!", "?") — Sub-namespace

Text 2: "She said, \"Hello, world!\""
  Pairs: (S, ","), (",", "\""), ("\"", "!"), ("!", "\""), ("\"", END)
  
  Hierarchy:
    (S, END) — Root
      ├── (S, ",") — Statement level
      └── (",", "\"") — Quote start
          └── ("\"", "!") — Quoted content
              └── ("!", "\"") — Quote end
                  └── ("\"", END) — After quote
```

**Key**: Subset relations emerge from text structure, not predefined.

---

## One-Pass Index Construction

### Algorithm

```python
def build_index(text, doc_id):
    """
    One-pass sequential scan to build punctuation namespace index.
    
    Returns:
        List of (type_hash, content) tuples
        Index mapping type_hash → [positions]
    """
    index = []  # List of (type_hash, content)
    inverted_index = defaultdict(list)  # type_hash → [positions]
    
    # State
    current_segment = []
    pre_punct = 'S'  # START
    position = 0
    
    i = 0
    while i < len(text):
        char = text[i]
        
        if is_punctuation(char):  # Space, escape chars included
            # End current segment
            if current_segment:
                content = ''.join(current_segment)
                # Find next non-punctuation char for post_punct
                j = i
                while j < len(text) and is_punctuation(text[j]):
                    j += 1
                post_punct = text[j] if j < len(text) else 'E'  # END
                
                type_hash = hash((pre_punct, post_punct))
                entry = (type_hash, content, position, i)
                index.append(entry)
                inverted_index[type_hash].append(entry)
                
                current_segment = []
                position = j
                pre_punct = post_punct
                i = j
            else:
                # Consecutive punctuation
                i += 1
        else:
            # Readable character
            current_segment.append(char)
            i += 1
    
    # Handle last segment
    if current_segment:
        content = ''.join(current_segment)
        post_punct = 'E'  # END
        type_hash = hash((pre_punct, post_punct))
        entry = (type_hash, content, position, len(text))
        index.append(entry)
        inverted_index[type_hash].append(entry)
    
    return index, inverted_index
```

### Example Execution

```
Input: "hello??world"

i=0: 'h' → current_segment=['h']
i=1: 'e' → current_segment=['h','e']
i=2: 'l' → current_segment=['h','e','l']
i=3: 'l' → current_segment=['h','e','l','l']
i=4: 'o' → current_segment=['h','e','l','l','o']
i=5: '?' → PUNCTUATION!
  - End segment: content="hello"
  - Find next non-punct: i=7 ('w')
  - post_punct = '?' (first ? of ??)
  - type_hash = hash(('S', '?'))
  - Add: (hash(('S','?')), "hello", 0, 5)
  - Reset: current_segment=[], pre_punct='?', position=7
i=7: 'w' → current_segment=['w']
i=8: 'o' → current_segment=['w','o']
i=9: 'r' → current_segment=['w','o','r']
i=10: 'l' → current_segment=['w','o','r','l']
i=11: 'd' → current_segment=['w','o','r','l','d']
i=12: END
  - End segment: content="world"
  - post_punct = 'E' (END)
  - type_hash = hash(('?', 'E'))
  - Add: (hash(('?','E')), "world", 7, 12)

Result:
  Index: [
    (hash(('S','?')), "hello", 0, 5),
    (hash(('?','E')), "world", 7, 12)
  ]
```

---

## Punctuation Definition (Revised)

### What Counts as Punctuation

```python
def is_punctuation(char):
    """
    Check if character is punctuation (separator).
    
    Includes:
    - Traditional punctuation: , . ! ? ; : " ' () [] {}
    - Whitespace: space, tab, newline
    - Escape characters: \, /, |
    - Special chars: @ # $ % ^ & * _ - + = < >
    
    Excludes:
    - Letters (a-z, A-Z, Unicode letters)
    - Digits (0-9)
    """
    # Letters and digits are NOT punctuation
    if char.isalnum():
        return False
    
    # Everything else is punctuation (separator)
    return True
```

### Examples

```
"hello world" → "hello" and "world" are separate (space is punct)
"hello??world" → "hello" and "world" are separate (?? is punct sequence)
"hi\\nthere" → "hi" and "there" are separate (\n is punct)
"<div>content</div>" → "<", ">", "</", ">" are punct, "content" is readable
```

---

## Namespace Subset Relations

### Dynamic Hierarchy

```
Based on text, character pairs form subset relations:

Text: "She said, \"Hello, world!\""

Segments:
  1. ("S", ","), "She said"
  2. (",", "\""), "" (empty, between comma and quote)
  3: ("\"", "!"), "Hello, world"
  4: ("!", "\""), "" (empty, between ! and quote)
  5: ("\"", "E"), "" (empty, after closing quote)

Namespace Tree:
  (S, E) — Root
    └── (S, ",") — "She said"
        └── (",", "\"") — (empty, quote start)
            └── ("\"", "!") — "Hello, world" (quoted content)
                └── ("!", "\"") — (empty, quote end)
                    └── ("\"", E) — (empty, after quote)
```

### Subset Detection

```python
def find_subset_relations(index):
    """
    Find which namespaces are subsets of others.
    
    A namespace (p1, p2) is a subset of (p0, p3) if:
    - Segments with (p1, p2) appear between segments with (p0, p3)
    - Based on position ordering
    """
    # Group by type_hash
    by_hash = defaultdict(list)
    for entry in index:
        by_hash[entry.type_hash].append(entry)
    
    # Find containment relations
    subsets = {}
    for hash1, entries1 in by_hash.items():
        for hash2, entries2 in by_hash.items():
            if hash1 == hash2:
                continue
            
            # Check if all entries1 are between entries2
            if is_subset(entries1, entries2):
                subsets[hash1] = hash2
    
    return subsets

def is_subset(inner, outer):
    """Check if inner segments are contained within outer segments."""
    for i_entry in inner:
        # Find outer segment that contains this inner segment
        found = False
        for o_entry in outer:
            if o_entry.start <= i_entry.start and i_entry.end <= o_entry.end:
                found = True
                break
        if not found:
            return False
    return True
```

---

## Benefits for Specific Formats

### JSON

```
Input: {"name": "John", "age": 30}

Segments:
  ("S", ":"), "" (empty, before first colon)
  (":", ","), " \"John\"" (after colon, before comma)
  (",", ":"), " \"age\"" (after comma, before colon)
  (":", "}"), " 30" (after colon, before brace)

Namespace Tree:
  (S, }) — Root (object)
    ├── (S, :) — Key before colon
    ├── (:, ,) — Value after colon
    └── ...

Benefit:
  - Removes redundant chars ({, }, ", etc.)
  - Indexes content by context (key vs value)
  - Easy to query: find all values (after ":")
```

### HTML

```
Input: <div class="main">Hello World</div>

Segments:
  ("S", ">"), "div class=\"main\"" (tag content)
  (">", "<"), "Hello World" (element content)
  ("<", "E"), "/div" (closing tag)

Namespace Tree:
  (S, E) — Root
    ├── (S, >) — Tag definition
    ├── (>, <) — Element content
    └── (<, E) — Closing tag

Benefit:
  - Separates tag definition from content
  - Easy to query: find all element content (between ">" and "<")
  - Removes redundant chars (<, >, /, etc.)
```

### Escape Sequences

```
Input: "line1\\nline2\\nline3"

Segments:
  ("S", "\\n"), "line1"
  ("\\n", "\\n"), "line2"
  ("\\n", "E"), "line3"

Benefit:
  - Natural line segmentation
  - No need to handle \\n specially
  - Consistent with other punctuation
```

---

## Key Advantages

### 1. Noise Reduction

```
Raw text: {"name": "John", "age": 30}
Indexable content: "John", "30" (values)
                  "name", "age" (keys)

Removed: {, }, ", :, , (structural chars)
```

### 2. Context Preservation

```
(":", ",") → "John" (value, between colon and comma)
("S", ":") → "name" (key, between START and colon)

Same content, different context → Different namespace
```

### 3. Format Agnostic

```
JSON: {"name": "John"}
HTML: <name>John</name>
YAML: name: John

All produce similar namespaces:
  - Key/label: (S, :) or (S, >)
  - Value/content: (:, ,) or (>, <)
```

### 4. One-Pass Efficiency

```
O(n) single scan
No recursion
No backtracking
Build index on-the-fly
```

---

## Comparison with Previous Approaches

| Aspect | Character-Level | Punctuation Tree | Punctuation Namespace |
|--------|----------------|------------------|----------------------|
| **Unit** | Character/N-gram | Segment | Segment + Namespace |
| **Structure** | Flat/Graph | Recursive Tree | One-Pass Index |
| **Punctuation** | Boundary | Hierarchy | Namespace Marker |
| **Space** | Content | Content | Separator |
| **Passes** | 1-2 | Multiple | 1 |
| **Complexity** | O(n) | O(n log n) | O(n) |

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
        self.inverted = defaultdict(list)  # type_hash → [entries]
    
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

```
(pre, post) is like a namespace identifier:
  - ("S", ":") → Key namespace
  - (":", ",") → Value namespace
  - (">", "<") → Element content namespace
```

### 2. Dynamic Subset Relations

```
Subset relations emerge from text, not predefined:
  - In JSON: (":", ",") ⊂ (S, "}")
  - In HTML: (">", "<") ⊂ (S, E)
  - Different text → Different hierarchies
```

### 3. One-Pass Efficiency

```
No recursion, no backtracking:
  - Read left-to-right
  - Segment on punctuation
  - Build index on-the-fly
  - O(n) time, O(n) space
```

### 4. Format Agnostic

```
JSON, HTML, YAML, plain text:
  - Same algorithm
  - Different namespaces emerge
  - No format-specific parsing
```

---

## Next Steps

1. **Implement one-pass scanner** — PunctuationNamespaceIndex class
2. **Test on JSON/HTML** — Verify noise reduction
3. **Query by namespace** — Find segments by (pre, post) pair
4. **Visualize namespace tree** — Show dynamic hierarchy

---

**Status**: Algorithm clarified, one-pass design complete  
**Next**: Implement and test on real data (JSON, HTML, plain text)  
**Philosophy**: One-pass scan, namespace indexing, format-agnostic
