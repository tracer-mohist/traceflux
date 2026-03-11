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

```text
"hello world" -> "hello" and "world" are separate (space is punct)
"hello??world" -> "hello" and "world" are separate (?? is punct sequence)
"hi\\nthere" -> "hi" and "there" are separate (\n is punct)
"<div>content</div>" -> "<", ">", "</", ">" are punct, "content" is readable
```

---

## Namespace Subset Relations

### Dynamic Hierarchy

```text
Based on text, character pairs form subset relations:

Text: "She said, \"Hello, world!\""

Segments:
  1. ("S", ","), "She said"
  2. (",", "\""), "" (empty, between comma and quote)
  3: ("\"", "!"), "Hello, world"
  4: ("!", "\""), "" (empty, between ! and quote)
  5: ("\"", "E"), "" (empty, after closing quote)

Namespace Tree:
  (S, E) -- Root
    +-- (S, ",") -- "She said"
        +-- (",", "\"") -- (empty, quote start)
            +-- ("\"", "!") -- "Hello, world" (quoted content)
                +-- ("!", "\"") -- (empty, quote end)
                    +-- ("\"", E) -- (empty, after quote)
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

```text
Input: {"name": "John", "age": 30}

Segments:
  ("S", ":"), "" (empty, before first colon)
  (":", ","), " \"John\"" (after colon, before comma)
  (",", ":"), " \"age\"" (after comma, before colon)
  (":", "}"), " 30" (after colon, before brace)

Namespace Tree:
  (S, }) -- Root (object)
    +-- (S, :) -- Key before colon
    +-- (:, ,) -- Value after colon
    +-- ...

Benefit:
  - Removes redundant chars ({, }, ", etc.)
  - Indexes content by context (key vs value)
  - Easy to query: find all values (after ":")
```

### HTML

```text
Input: <div class="main">Hello World</div>

Segments:
  ("S", ">"), "div class=\"main\"" (tag content)
  (">", "<"), "Hello World" (element content)
  ("<", "E"), "/div" (closing tag)

Namespace Tree:
  (S, E) -- Root
    +-- (S, >) -- Tag definition
    +-- (>, <) -- Element content
    +-- (<, E) -- Closing tag

Benefit:
  - Separates tag definition from content
  - Easy to query: find all element content (between ">" and "<")
  - Removes redundant chars (<, >, /, etc.)
```

### Escape Sequences

```text
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

```text
Raw text: {"name": "John", "age": 30}
Indexable content: "John", "30" (values)
                  "name", "age" (keys)

Removed: {, }, ", :, , (structural chars)
```

### 2. Context Preservation

```text
(":", ",") -> "John" (value, between colon and comma)
("S", ":") -> "name" (key, between START and colon)

Same content, different context -> Different namespace
```

### 3. Format Agnostic

```text
JSON: {"name": "John"}
HTML: <name>John</name>
YAML: name: John

All produce similar namespaces:
  - Key/label: (S, :) or (S, >)
  - Value/content: (:, ,) or (>, <)
```
