# Supplement: Space is Readable Text

**Date**: 2026-03-06  
**Type**: Clarification / Correction  
**Related**: `2026-03-06_punctuation-segmentation.md`

---

## Key Clarification

**Space is NOT punctuation** — it's part of readable text.

---

## Why This Matters

### English Example

```
Text: "Hello world, how are you?"

❌ Wrong (space as punctuation):
  Segments: ["Hello", "world", "how", "are", "you"]
  Lost: Word relationships, phrases

✅ Correct (space as readable):
  Segments: ["Hello world", "how are you"]
  Preserved: Natural phrases
```

### Phrase Preservation

```
Text: "The quick brown fox jumps over the lazy dog."

✅ Correct segmentation:
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

```
, . ! ? ; : " ' () [] {} ... — – – ( ) [ ] { } < > « » „ " ' …
```

### NOT Punctuation (Part of Content)

```
' ' (space)
'\t' (tab)
'\n' (newline)
'\r' (carriage return)
```

**Rationale**:
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
    if char in '…†‡•‰⁄⁊⁏⁐⁑⁓⁔⁕⁖⁗⁘⁙⁚⁛⁜⁝⁞':
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

```
"Hello world, how are you?"
→ ["Hello world", " how are you"]
Spaces preserve word boundaries.
```

### Chinese

```
"你好，世界！最近怎么样？"
→ ["你好", "世界", "最近怎么样"]
Chinese doesn't use spaces, but punctuation still works.
```

### Mixed

```
"Hello 世界，how are you 你好吗？"
→ ["Hello 世界", "how are you 你好吗"]
Spaces in English part are preserved.
```

### Code / Technical Text

```
"def hello_world(): return None"
→ ["def hello_world(): return None"] (no punctuation)
Spaces are part of the code content.
```

---

## Benefits of Treating Space as Readable

### 1. Phrase Preservation

```
"quick brown fox" → One segment
Preserves: Adjective order, noun phrase

vs.

"quick", "brown", "fox" → Three segments
Lost: Relationship between words
```

### 2. N-gram Quality

```
Segment: "quick brown fox"

3-grams: ["qui", "uic", "ick", ..., "own", "wn ", "n f", " fo", "fox"]

Includes: "wn " (word boundary), " fo" (cross-word)
These capture phrase-level patterns.

vs.

Segments: "quick", "brown", "fox"

3-grams: ["qui", "uic", "ick"], ["bro", "row", "own"], ["fox"]

Lost: Cross-word patterns
```

### 3. Search Relevance

```
User searches: "brown fox"

With space as readable:
  Segment: "quick brown fox jumps"
  Match: "brown fox" (exact phrase)

Without space (split on space):
  Segment: "brown"
  Segment: "fox"
  Match: Separate words, lose phrase context
```

---

## Edge Cases

### Multiple Spaces

```
Text: "Hello   world" (3 spaces)

Treatment: Spaces are content
Segment: "Hello   world"

Optional: Normalize whitespace
Segment: "Hello world" (single space)
```

### Leading/Trailing Spaces

```
Text: "  Hello world  , how are you?"

Option 1: Preserve spaces
Segment: "  Hello world  " (pre: START, post: ",")
Segment: " how are you" (pre: ",", post: "?")

Option 2: Strip (recommended)
Segment: "Hello world" (pre: START, post: ",")
Segment: "how are you" (pre: ",", post: "?")
```

### Punctuation Without Space

```
Text: "Hello,world" (no space after comma)

Segment: "Hello" (pre: START, post: ",")
Segment: "world" (pre: ",", post: END)

This is correct — comma is still a boundary.
```

### Abbreviations

```
Text: "Dr. Smith arrived."

Option 1: Split on all periods
Segment: "Dr" (post: ".")
Segment: " Smith arrived" (post: ".")

Option 2: Handle abbreviations (advanced)
Segment: "Dr. Smith arrived" (post: ".")

Recommendation: Start with Option 1 (simple),
add abbreviation handling later if needed.
```

---

## Revised Algorithm

```python
def extract_segments(text, doc_id):
    """
    Extract segments based on punctuation boundaries.
    
    Space is NOT punctuation — it's part of readable content.
    """
    segments = []
    start = 0
    
    for i, char in enumerate(text):
        if is_punctuation(char):  # Space returns False
            # Extract content from start to current position
            content = text[start:i].strip()  # Strip leading/trailing spaces
            
            if content:  # Skip empty segments
                pre_punct = text[start-1] if start > 0 else None
                post_punct = char
                
                segment = Segment(
                    content=content,  # Internal spaces preserved
                    pre_punct=pre_punct,
                    post_punct=post_punct,
                    doc_id=doc_id,
                    start_pos=start,
                    end_pos=i
                )
                segments.append(segment)
            
            start = i + 1
    
    # Handle last segment (after last punctuation)
    if start < len(text):
        content = text[start:].strip()
        if content:
            segment = Segment(
                content=content,
                pre_punct=text[start-1] if start > 0 else None,
                post_punct=None,  # END
                doc_id=doc_id,
                start_pos=start,
                end_pos=len(text)
            )
            segments.append(segment)
    
    return segments
```

---

## Summary

| Character Type | Treatment | Example |
|----------------|-----------|---------|
| **Letters/Digits** | Readable content | "Hello" |
| **Space** | Readable content | "Hello world" (one segment) |
| **Tab/Newline** | Readable content (or normalize) | "Hello\tworld" |
| **Punctuation** | Split point | "Hello," → ["Hello"] |

**Key Principle**: Space is part of readable text, not a boundary.

---

**Status**: Clarification complete  
**Action**: Update implementation to treat space as readable content
