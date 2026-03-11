# Text Segmentation

**Purpose**: Split text into readable units while preserving meaning.

**NOTE**: Consolidated from research/01-foundations/ (2026-03-11)

---

## Core Principle

**Space is NOT punctuation** — it is part of readable text.

### Why This Matters

```text
Text: "Hello world, how are you?"

Wrong (space as punctuation):
  Segments: ["Hello", "world", "how", "are", "you"]
  Lost: Word relationships, phrases

Right (space as readable):
  Segments: ["Hello world", "how are you"]
  Preserved: Natural phrases
```

### Phrase Preservation Example

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

## Punctuation Definition

### Punctuation Marks (Split Points)

```
, . ! ? ; : " ' ( ) [ ] { } < > « » „ " ' ... — – -
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

## Segmentation Algorithm

### Step 1: Identify Punctuation

Scan text for punctuation marks (split points).

### Step 2: Split into Segments

Split text at punctuation, keeping spaces within segments.

### Step 3: Record Context

For each segment, record:
- **Content**: The readable text (may include spaces)
- **Pre-punctuation**: Punctuation before segment (or START)
- **Post-punctuation**: Punctuation after segment (or END)

### Example

```text
Text: "Hello, world! How are you?"

Segments:
  1. Content: "Hello"
     Pre: START, Post: ","
     Type: hash("S,")

  2. Content: " world"
     Pre: ",", Post: "!"
     Type: hash(",!")

  3. Content: " How are you"
     Pre: "!", Post: "?"
     Type: hash("!?")
```

### Type Identifier

- Format: `(pre_punct, post_punct)` → 2-char string → hash
- Example: `hash(",!")` = integer ID
- Benefit: Groups segments by punctuation context

---

## Advantages

### Natural Boundaries

- Punctuation marks natural pauses/boundaries
- More meaningful than fixed-size windows
- Language-independent (all languages have punctuation)

### Context Preservation

- Pre/post punctuation captures sentence structure
- "Hello," vs "Hello!" have different types
- Preserves tone/strength of statement

### Efficient Grouping

- Hash of (pre, post) is O(1) to compute
- Segments with same type can be grouped
- Enables pattern matching across documents

---

## Limitations

### Punctuation Variability

- Some text has no punctuation (code, logs)
- Different languages use different punctuation
- Informal text may misuse punctuation

### Mitigation Strategies

1. **Fallback to character-level**: When no punctuation, use n-gram analysis
2. **Language detection**: Adapt punctuation rules per language
3. **Normalization**: Standardize punctuation before segmentation

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
    import unicodedata
    category = unicodedata.category(char)
    
    # P categories are punctuation
    if category.startswith('P'):
        return True
    
    # Some symbols act as punctuation
    if char in '...†‡-‰⁄⁊⁏⁐⁑⁓⁔⁕⁖⁗⁘⁙⁚⁛⁜⁝⁞':
        return True
    
    # Explicitly exclude whitespace
    if char in ' \t\n\r':
        return False
    
    return False
```

### Segmentation Function

```python
def segment_text(text):
    """
    Segment text by punctuation.
    
    Returns: List of (content, pre_punct, post_punct) tuples
    """
    segments = []
    current_segment = ""
    pre_punct = "START"
    
    for i, char in enumerate(text):
        if is_punctuation(char):
            if current_segment:
                segments.append((current_segment, pre_punct, char))
                current_segment = ""
            pre_punct = char
        else:
            current_segment += char
    
    # Handle final segment
    if current_segment:
        segments.append((current_segment, pre_punct, "END"))
    
    return segments
```

---

## Related

- [N-gram Analysis](./ngram-analysis.md) - Pattern extraction within segments
- [Punctuation Context Tree](../algorithms/punctuation-context-tree.md) - Advanced context modeling
- [Frequency Ranking](./frequency-ranking.md) - Weighting segments by importance

---

**Last Updated**: 2026-03-11  
**Source Files**: `2026-03-06_space-is-readable*.md`, `2026-03-06_punctuation-segmentation*.md`
