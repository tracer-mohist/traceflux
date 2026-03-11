### 3. Search Relevance

```text
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

```text
Text: "Hello   world" (3 spaces)

Treatment: Spaces are content
Segment: "Hello   world"

Optional: Normalize whitespace
Segment: "Hello world" (single space)
```

### Leading/Trailing Spaces

```text
Text: "  Hello world  , how are you?"

Option 1: Preserve spaces
Segment: "  Hello world  " (pre: START, post: ",")
Segment: " how are you" (pre: ",", post: "?")

Option 2: Strip (recommended)
Segment: "Hello world" (pre: START, post: ",")
Segment: "how are you" (pre: ",", post: "?")
```

### Punctuation Without Space

```text
Text: "Hello,world" (no space after comma)

Segment: "Hello" (pre: START, post: ",")
Segment: "world" (pre: ",", post: END)

This is correct -- comma is still a boundary.
```

### Abbreviations

```text
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

    Space is NOT punctuation -- it's part of readable content.
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
| LETTERS/DIGITS | Readable content | "Hello" |
| SPACE | Readable content | "Hello world" (one segment) |
| TAB/NEWLINE | Readable content (or normalize) | "Hello\tworld" |
| PUNCTUATION | Split point | "Hello," -> ["Hello"] |

KEY-PRINCIPLE: Space is part of readable text, not a boundary.

---

STATUS: Clarification complete
ACTION: Update implementation to treat space as readable content
