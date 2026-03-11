# Supplement: Space is Readable Text

DATE: 2026-03-06
TYPE: Clarification / Correction
RELATED: `2026-03-06_punctuation-segmentation.md`

---

## Key Clarification

SPACE-IS-NOT-PUNCTUATION -- it's part of readable text.

---

## Why This Matters

### English Example

```text
Text: "Hello world, how are you?"

 Wrong (space as punctuation):
  Segments: ["Hello", "world", "how", "are", "you"]
  Lost: Word relationships, phrases

 Correct (space as readable):
  Segments: ["Hello world", "how are you"]
  Preserved: Natural phrases
```

### Phrase Preservation

```text
Text: "The quick brown fox jumps over the lazy dog."

 Correct segmentation:
  Segment: "The quick brown fox jumps over the lazy dog"
  Pre: START, Post: "."

  This preserves:
  - Complete sentence
  - Word order
  - Phrase structure ("quick brown fox", "lazy dog")
```

---

## Punctuation Definition (Revised)

### Punctuation Marks (Split Points)

```text
, . ! ? ; : " ' () [] {} ... -- - - ( ) [ ] { } < > « » „ " ' ...
```

### NOT Punctuation (Part of Content)

```text
' ' (space)
'\t' (tab)
'\n' (newline)
'\r' (carriage return)
```

RATIONALE:
- Spaces separate words but are part of readable content
- Removing spaces destroys word boundaries in English
- Tabs/newlines are formatting, not semantic boundaries

---

## Implementation

### Punctuation Detection

```python
def is_punctuation(char):
    """
    Check if character is a punctuation mark (split point).

    Returns True for: , . ! ? ; : " ' () [] {} etc.
    Returns False for: space, tab, newline, letters, digits, etc.
    """
    # Unicode punctuation categories
    import unicodedata
    category = unicodedata.category(char)

    # P categories are punctuation
    # But exclude space-like characters
    if category.startswith('P'):
        return True

    # Some symbols act as punctuation
    if char in '...†‡-‰⁄⁊⁏⁐⁑⁓⁔⁕⁖⁗⁘⁙⁚⁛⁜⁝⁞':
        return True

    # Explicitly exclude whitespace
    if char in ' \t\n\r':
        return False

    return False

# Alternative: Use regex
import re
PUNCTUATION_PATTERN = re.compile(r'[^\w\s]')  # Not word, not space

def is_punctuation(char):
    return bool(PUNCTUATION_PATTERN.match(char)) and char not in ' \t\n\r'
```

### Segmentation Example

```python
text = "Hello world, how are you? I'm fine!"

segments = extract_segments(text)

# Result:
[
    Segment(
        content="Hello world",  # Includes space
        pre_punct=None,  # START
        post_punct=",",
        type_hash=hash((None, ","))
    ),
    Segment(
        content=" how are you",  # Includes leading space
        pre_punct=",",
        post_punct="?",
        type_hash=hash((",", "?"))
    ),
    Segment(
        content=" I'm fine",  # Includes leading space
        pre_punct="?",
        post_punct="!",
        type_hash=hash(("?", "!"))
    )
]

# Optional: Strip leading/trailing spaces from content
# (but spaces within content are preserved)
Segment(content="Hello world", ...)  # Not "Hello world"
```

---

## Multilingual Considerations

### English

```text
"Hello world, how are you?"
-> ["Hello world", " how are you"]
Spaces preserve word boundaries.
```

### Chinese

```text
"你好,世界!最近怎么样?"
-> ["你好", "世界", "最近怎么样"]
Chinese doesn't use spaces, but punctuation still works.
```

### Mixed

```text
"Hello 世界,how are you 你好吗?"
-> ["Hello 世界", "how are you 你好吗"]
Spaces in English part are preserved.
```

### Code / Technical Text

```text
"def hello_world(): return None"
-> ["def hello_world(): return None"] (no punctuation)
Spaces are part of the code content.
```

---

## Benefits of Treating Space as Readable

### 1. Phrase Preservation

```text
"quick brown fox" -> One segment
Preserves: Adjective order, noun phrase

vs.

"quick", "brown", "fox" -> Three segments
Lost: Relationship between words
```

### 2. N-gram Quality

```text
Segment: "quick brown fox"

3-grams: ["qui", "uic", "ick", ..., "own", "wn ", "n f", " fo", "fox"]

Includes: "wn " (word boundary), " fo" (cross-word)
These capture phrase-level patterns.

vs.

Segments: "quick", "brown", "fox"

3-grams: ["qui", "uic", "ick"], ["bro", "row", "own"], ["fox"]

Lost: Cross-word patterns
```
