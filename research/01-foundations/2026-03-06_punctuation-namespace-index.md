# Research: Punctuation Namespace Index (PNI)

DATE: 2026-03-06
STATUS: Algorithm Clarification
TOPIC: Character pairs as namespaces/scopes, one-pass indexing

---

## Core Clarification (User's Correction)

### Previous Misunderstanding

I previously thought:
- Build tree recursively
- Multiple passes for analysis
- Complex hierarchy

### Correct Understanding

ACTUAL-ALGORITHM:
1. ONE-PASS-SEQUENTIAL-READ -- Single scan, build index on-the-fly
2. SPACE-+-ESCAPE-CHARS-=-PUNCTUATION -- Used for segmentation
3. NO-SEMANTIC-ANALYSIS-NEEDED -- Pure mechanical segmentation
4. CHARACTER-PAIRS-AS-NAMESPACES -- (pre, post) defines scope
5. DYNAMIC-SUBSET-RELATIONS -- Based on actual text content

---

## Algorithm: One-Pass Segmentation

### Input -> Output

```text
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

```text
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

```text
Character pair (pre, post) acts like:
  - Namespace identifier
  - Scope marker
  - Similar to `"` quotes or `()` parentheses

Example:
  ("S", "?") -> Namespace A
  ("?", "!") -> Namespace B
  ("!", ".") -> Namespace C
```

### Subset Relations (Dynamic)

```text
Based on text content, some pairs are subsets of others:

Text 1: "Hello, world! How are you?"
  Pairs: (S, ","), (",", "!"), ("!", "?"), ("?", END)

  Hierarchy:
    (S, END) -- Root namespace
      +-- (S, ",") -- Sub-namespace
      +-- (",", "!") -- Sub-namespace
      +-- ("!", "?") -- Sub-namespace

Text 2: "She said, \"Hello, world!\""
  Pairs: (S, ","), (",", "\""), ("\"", "!"), ("!", "\""), ("\"", END)

  Hierarchy:
    (S, END) -- Root
      +-- (S, ",") -- Statement level
      +-- (",", "\"") -- Quote start
          +-- ("\"", "!") -- Quoted content
              +-- ("!", "\"") -- Quote end
                  +-- ("\"", END) -- After quote
```

KEY: Subset relations emerge from text structure, not predefined.

---

## One-Pass Index Construction

### Algorithm

```python
def build_index(text, doc_id):
    """
    One-pass sequential scan to build punctuation namespace index.

    Returns:
        List of (type_hash, content) tuples
        Index mapping type_hash -> [positions]
    """
    index = []  # List of (type_hash, content)
    inverted_index = defaultdict(list)  # type_hash -> [positions]

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

```text
Input: "hello??world"

i=0: 'h' -> current_segment=['h']
i=1: 'e' -> current_segment=['h','e']
i=2: 'l' -> current_segment=['h','e','l']
i=3: 'l' -> current_segment=['h','e','l','l']
i=4: 'o' -> current_segment=['h','e','l','l','o']
i=5: '?' -> PUNCTUATION!
  - End segment: content="hello"
  - Find next non-punct: i=7 ('w')
  - post_punct = '?' (first ? of ??)
  - type_hash = hash(('S', '?'))
  - Add: (hash(('S','?')), "hello", 0, 5)
  - Reset: current_segment=[], pre_punct='?', position=7
i=7: 'w' -> current_segment=['w']
i=8: 'o' -> current_segment=['w','o']
i=9: 'r' -> current_segment=['w','o','r']
i=10: 'l' -> current_segment=['w','o','r','l']
i=11: 'd' -> current_segment=['w','o','r','l','d']
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
