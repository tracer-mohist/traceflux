# Research: Punctuation-Based Sequence Segmentation

DATE: 2026-03-06
STATUS: Algorithm Design & Analysis
TOPIC: Segment text by punctuation, extract sequential features

---

## Proposed Algorithm (User's Idea)

### Step 1: Punctuation-Based Segmentation

INPUT: Text sequence

IMPORTANT-NOTE: Space is NOT punctuation -- it's part of readable text.

REASON: In English (and many languages), spaces are required for words/phrases:
- "Hello world" -> One segment (not "Hello" + "world")
- "The quick brown fox" -> One segment (not 4 separate words)

PROCESS:
1. Identify punctuation marks (, . ! ? ; : " ' () [] {} ...)
   - EXCLUDES: Space (' '), tab ('\t'), newline ('\n')
   - Spaces are part of readable content
2. Split text into readable segments
3. For each segment, record:
   - Content: The readable text (may include spaces)
   - Pre-punctuation: Punctuation before segment (or START)
   - Post-punctuation: Punctuation after segment (or END)

EXAMPLE:
```text
Text: "Hello, world! How are you?"

Segments:
  1. Content: "Hello"
     Pre: START, Post: ","
     Type: hash("S,")

  2. Content: "world"
     Pre: ",", Post: "!"
     Type: hash(",!")

  3. Content: "How are you"
     Pre: "!", Post: "?"
     Type: hash("!?")
```

TYPE-IDENTIFIER:
- (pre_punct, post_punct) -> 2-char string -> hash
- Example: hash(",!") = some integer

BENEFIT: Groups segments by punctuation context.

---

## Analysis: Is This Useful?

### Advantages

1. NATURAL-BOUNDARIES
   - Punctuation marks natural pauses/boundaries
   - More meaningful than fixed-size windows
   - Language-independent (all languages have punctuation)

2. CONTEXT-PRESERVATION
   - Pre/post punctuation captures sentence structure
   - "Hello," vs "Hello!" have different types
   - Preserves tone/strength of statement

3. EFFICIENT-GROUPING
   - Hash of (pre, post) is O(1) to compute
   - Segments with same type can be grouped
   - Enables pattern matching across documents

### Limitations

1. PUNCTUATION-VARIABILITY
   - Some text has no punctuation (code, logs)
   - Different languages use different punctuation
   - Informal text may lack punctuation

2. SEGMENT-LENGTH-VARIATION
   - "Hi!" (2 chars) vs "This is a very long sentence," (35 chars)
   - Hard to compare segments of vastly different lengths

3. NESTED-PUNCTUATION
   - "He said, \"Hello, world!\""
   - Which punctuation counts? Outer or inner?

---

## Step 2: Sequential Feature Extraction

PROBLEM: How to represent the content of each segment for matching?

### Option A: (Character, Position) Pairs

```text
Segment: "Hello"

Representation:
[('H', 0), ('e', 1), ('l', 2), ('l', 3), ('o', 4)]

Pros:
- Exact position information
- Easy to compare same-length segments

Cons:
- Different lengths can't be directly compared
- "Hello" (5 chars) vs "Hi" (2 chars) -> incompatible
- Position 2 in "Hello" ('l') != Position 2 in "Hi" (out of bounds)

Verdict:  Not suitable for variable-length segments
```

### Option B: (Character, Next Character) Pairs

```text
Segment: "Hello"

Representation:
[('H', 'e'), ('e', 'l'), ('l', 'l'), ('l', 'o'), ('o', END)]

As hash: hash("He") + hash("el") + hash("ll") + hash("lo") + hash("oEND")

Pros:
- Captures character transitions (bigrams)
- Order-sensitive (He != eH)
- Variable-length segments can be compared via set overlap

Cons:
- Loses absolute position information
- "Hello" and "lleHo" have same pairs (different order)
- Need to preserve pair order for exact matching

Verdict:  Partial -- good for similarity, not exact match
```

### Option C: N-grams (Sliding Window)

```text
Segment: "Hello"

2-grams: ["He", "el", "ll", "lo"]
3-grams: ["Hel", "ell", "llo"]
4-grams: ["Hell", "ello"]

As index:
{
  "He": [segment_1],
  "el": [segment_1],
  "ll": [segment_1],
  "lo": [segment_1],
  "Hel": [segment_1],
  ...
}

Pros:
- Captures local patterns
- Variable-length segments comparable via shared n-grams
- Standard technique (well-understood)
- Efficient indexing (inverted index)

Cons:
- Explosion of n-grams for long segments
- Need to choose n (2? 3? 4?)
- Still doesn't capture global structure

Verdict:  Recommended for character-level matching
```

### Option D: Prefix Tree (Trie)

```text
Segment: "Hello"

Trie:
    (root)
      |
      H
      |
      e
      |
      l
      |
      l
      |
      o
      |
    (END)

Pros:
- Compact representation
- Fast prefix matching
- Good for autocomplete

Cons:
- Can't match middle substrings ("ell" requires traversing from root)
- Need suffix tree for middle matching
- Overkill for single segment

Verdict:  Not suitable for general substring matching
```
