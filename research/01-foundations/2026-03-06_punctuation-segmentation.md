# Research: Punctuation-Based Sequence Segmentation

**Date**: 2026-03-06  
**Status**: Algorithm Design & Analysis  
**Topic**: Segment text by punctuation, extract sequential features

---

## Proposed Algorithm (User's Idea)

### Step 1: Punctuation-Based Segmentation

**Input**: Text sequence

**Important Note**: Space is NOT punctuation — it's part of readable text.

**Reason**: In English (and many languages), spaces are required for words/phrases:
- "Hello world" → One segment (not "Hello" + "world")
- "The quick brown fox" → One segment (not 4 separate words)

**Process**:
1. Identify punctuation marks (, . ! ? ; : " ' () [] {} ...)
   - **Excludes**: Space (' '), tab ('\t'), newline ('\n')
   - Spaces are part of readable content
2. Split text into readable segments
3. For each segment, record:
   - Content: The readable text (may include spaces)
   - Pre-punctuation: Punctuation before segment (or START)
   - Post-punctuation: Punctuation after segment (or END)

**Example**:
```
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

**Type Identifier**:
- (pre_punct, post_punct) → 2-char string → hash
- Example: hash(",!") = some integer

**Benefit**: Groups segments by punctuation context.

---

## Analysis: Is This Useful?

### Advantages

1. **Natural Boundaries**
   - Punctuation marks natural pauses/boundaries
   - More meaningful than fixed-size windows
   - Language-independent (all languages have punctuation)

2. **Context Preservation**
   - Pre/post punctuation captures sentence structure
   - "Hello," vs "Hello!" have different types
   - Preserves tone/strength of statement

3. **Efficient Grouping**
   - Hash of (pre, post) is O(1) to compute
   - Segments with same type can be grouped
   - Enables pattern matching across documents

### Limitations

1. **Punctuation Variability**
   - Some text has no punctuation (code, logs)
   - Different languages use different punctuation
   - Informal text may lack punctuation

2. **Segment Length Variation**
   - "Hi!" (2 chars) vs "This is a very long sentence," (35 chars)
   - Hard to compare segments of vastly different lengths

3. **Nested Punctuation**
   - "He said, \"Hello, world!\""
   - Which punctuation counts? Outer or inner?

---

## Step 2: Sequential Feature Extraction

**Problem**: How to represent the content of each segment for matching?

### Option A: (Character, Position) Pairs

```
Segment: "Hello"

Representation:
[('H', 0), ('e', 1), ('l', 2), ('l', 3), ('o', 4)]

Pros:
- Exact position information
- Easy to compare same-length segments

Cons:
- Different lengths can't be directly compared
- "Hello" (5 chars) vs "Hi" (2 chars) → incompatible
- Position 2 in "Hello" ('l') ≠ Position 2 in "Hi" (out of bounds)

Verdict: ❌ Not suitable for variable-length segments
```

### Option B: (Character, Next Character) Pairs

```
Segment: "Hello"

Representation:
[('H', 'e'), ('e', 'l'), ('l', 'l'), ('l', 'o'), ('o', END)]

As hash: hash("He") + hash("el") + hash("ll") + hash("lo") + hash("oEND")

Pros:
- Captures character transitions (bigrams)
- Order-sensitive (He ≠ eH)
- Variable-length segments can be compared via set overlap

Cons:
- Loses absolute position information
- "Hello" and "lleHo" have same pairs (different order)
- Need to preserve pair order for exact matching

Verdict: ⚠️ Partial — good for similarity, not exact match
```

### Option C: N-grams (Sliding Window)

```
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

Verdict: ✅ Recommended for character-level matching
```

### Option D: Prefix Tree (Trie)

```
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

Verdict: ❌ Not suitable for general substring matching
```

### Option E: Suffix Tree / Suffix Array

```
Segment: "Hello"

Suffix Tree:
(root)
  ├─ "Hello$"
  ├─ "ello$"
  ├─ "llo$"
  ├─ "lo$"
  └─ "o$"

Pros:
- Can match any substring in O(m) time
- Captures all possible substrings
- Efficient for repeated queries

Cons:
- Complex to implement
- High memory overhead
- Overkill for short segments

Verdict: ⚠️ Good for long segments, overkill for short ones
```

### Option F: Structural Features (Abstract)

```
Segment: "Hello"

Features:
- Length: 5
- First char: 'H'
- Last char: 'o'
- Character set: {H, e, l, o} (size: 4)
- Has repeats: True (l appears twice)
- Capitalization pattern: [1,0,0,0,0] (first letter cap)
- Vowel ratio: 2/5 = 0.4
- Unique char ratio: 4/5 = 0.8

Pros:
- Fixed-length feature vector (easy to compare)
- Captures global properties
- Language-independent

Cons:
- Loses specific character information
- "Hello" and "Hallo" have same features
- Best used with other methods (not alone)

Verdict: ✅ Recommended as supplementary features
```

---

## Proposed Hybrid Approach

### Multi-Level Representation

```
For each segment:

Level 1: Type (Punctuation Context)
  - hash(pre_punct + post_punct)
  - Example: hash(",!") = 12345

Level 2: N-gram Index (Local Patterns)
  - 2-grams: ["He", "el", "ll", "lo"]
  - 3-grams: ["Hel", "ell", "llo"]
  - Stored as: ngram → segment_ids

Level 3: Structural Features (Global Properties)
  - Length: 5
  - First/last char: 'H'/'o'
  - Char set size: 4
  - Has repeats: True
  - Capitalization: FIRST_CAP

Level 4: Character Sequence (Exact Content)
  - Store original: "Hello"
  - For exact matching and display
```

### Query Processing

```
User Query: "Hello"

Step 1: Extract query features
  - Type: hash("S?") (assuming query has no context)
  - 2-grams: ["He", "el", "ll", "lo"]
  - 3-grams: ["Hel", "ell", "llo"]
  - Length: 5
  - First/last: 'H'/'o'

Step 2: Match at each level
  Level 1 (Type):
    - Optional (query may not have punctuation context)
  
  Level 2 (N-grams):
    - Find segments with matching 2-grams
    - Find segments with matching 3-grams
    - Score by overlap: Jaccard similarity
  
  Level 3 (Structure):
    - Filter by length (±20%)
    - Filter by first/last char (optional)
    - Filter by capitalization pattern
  
  Level 4 (Exact):
    - Check for exact match (if any)

Step 3: Rank results
  - Exact match: Score = 1.0
  - High n-gram overlap + same structure: Score = 0.8
  - Medium n-gram overlap + similar structure: Score = 0.5
  - Low overlap: Score = 0.2

Step 4: Return ranked segments
```

---

## Mathematical Formulation

### Segment Representation

```
Segment S = (content, pre_punct, post_punct)

Where:
  content ∈ Σ* (string over Unicode alphabet)
  pre_punct ∈ P ∪ {START} (punctuation or start)
  post_punct ∈ P ∪ {END} (punctuation or end)

Type(S) = hash(pre_punct + post_punct)

NGrams(S, n) = {S[i:i+n] | 0 ≤ i ≤ len(S) - n}

StructuralFeatures(S) = {
  length: len(S),
  first: S[0],
  last: S[-1],
  char_set: set(S),
  has_repeats: len(S) > len(set(S)),
  cap_pattern: capitalize_pattern(S)
}
```

### Similarity Measure

```
Similarity(S1, S2) = 
  α * ngram_overlap(S1, S2) +
  β * structural_similarity(S1, S2) +
  γ * type_match(S1, S2)

Where:
  ngram_overlap = |NGrams(S1) ∩ NGrams(S2)| / |NGrams(S1) ∪ NGrams(S2)|
  structural_similarity = (length_match + first_last_match + cap_match) / 3
  type_match = 1 if Type(S1) == Type(S2) else 0
  
  α + β + γ = 1 (weights, typically α=0.6, β=0.3, γ=0.1)
```

---

## Implementation Considerations

### Data Structures

```python
# Segment index
SegmentIndex = {
    'by_type': Dict[int, List[Segment]],  # type_hash → segments
    'by_ngram': Dict[str, List[Segment]],  # ngram → segments
    'by_length': Dict[int, List[Segment]],  # length → segments
}

# Segment representation
@dataclass
class Segment:
    content: str
    pre_punct: str  # or None for START
    post_punct: str  # or None for END
    doc_id: int
    start_pos: int
    end_pos: int
    
    # Cached features
    type_hash: int
    ngrams: Dict[int, Set[str]]  # n → set of n-grams
    features: StructuralFeatures
```

### Algorithms

```python
# Segment extraction
def extract_segments(text, doc_id):
    # Find all punctuation positions
    punct_positions = [(i, char) for i, char in enumerate(text) 
                       if is_punctuation(char)]
    
    segments = []
    prev_punct = (None, None)  # (position, char) for START
    
    for curr_pos, curr_punct in punct_positions:
        # Extract content between punctuation
        start = prev_punct[0] + 1 if prev_punct[0] is not None else 0
        end = curr_pos
        content = text[start:end].strip()
        
        if content:  # Skip empty segments
            segment = Segment(
                content=content,
                pre_punct=prev_punct[1],
                post_punct=curr_punct,
                doc_id=doc_id,
                start_pos=start,
                end_pos=end,
                type_hash=hash((prev_punct[1], curr_punct)),
                ngrams=extract_ngrams(content),
                features=extract_features(content)
            )
            segments.append(segment)
        
        prev_punct = (curr_pos, curr_punct)
    
    return segments

# N-gram extraction
def extract_ngrams(content, max_n=4):
    ngrams = {}
    for n in range(2, max_n + 1):
        ngrams[n] = {content[i:i+n] for i in range(len(content) - n + 1)}
    return ngrams

# Structural features
def extract_features(content):
    return {
        'length': len(content),
        'first': content[0] if content else None,
        'last': content[-1] if content else None,
        'char_set_size': len(set(content)),
        'has_repeats': len(content) > len(set(content)),
        'cap_pattern': get_cap_pattern(content)
    }
```

---

## Comparison with Character-Level Approach

| Aspect | Punctuation Segmentation | Pure Character-Level |
|--------|-------------------------|---------------------|
| **Unit** | Segment (between punctuation) | Character / N-gram |
| **Boundary** | Natural (punctuation) | Artificial (fixed window) |
| **Context** | Pre/post punctuation | Position-based |
| **Matching** | Segment-level + N-grams | N-gram only |
| **Language** | Requires punctuation | Works without punctuation |
| **Complexity** | O(n) segmentation + O(m) matching | O(n) indexing + O(m) matching |

**Recommendation**: Combine both approaches:
- Use punctuation segmentation for **coarse grouping**
- Use character-level n-grams for **fine matching**

---

## Key Insights

### 1. Punctuation Provides Natural Boundaries

Segments between punctuation are more meaningful than fixed windows:
- "Hello, world!" → ["Hello", "world"] (natural)
- Fixed window: ["Hello, w", "orld!"] (arbitrary)

### 2. Type Hashing Enables Fast Grouping

```
Type hash: hash(pre_punct + post_punct)

Segments with same type:
  - "Hello," and "Hi," (both end with comma)
  - "Really?" and "Sure?" (both end with question)

Enables: Group by sentence type (statement, question, exclamation)
```

### 3. N-grams Capture Local Patterns

```
"Hello" → 2-grams: ["He", "el", "ll", "lo"]

Matching:
  - "Hello" matches "Hello" (4/4 n-grams)
  - "Hello" matches "Hallo" (3/4 n-grams: "al", "ll", "lo")
  - "Hello" matches "World" (0/4 n-grams)
```

### 4. Structural Features Enable Fuzzy Matching

```
"Hello" vs "Hallo":
  - Same length: ✓
  - Same first/last: ✓ (H, o)
  - Same char set: ✗ (e vs a)
  - Same pattern: ✓ (FIRST_CAP)

Similarity: 3/4 = 0.75
```

---

## Next Steps

1. **Implement segment extraction** — Punctuation-based splitting
2. **Implement n-gram indexing** — For each segment
3. **Implement structural features** — Length, first/last, etc.
4. **Test on multilingual corpus** — Verify punctuation handling
5. **Compare with pure character-level** — Measure effectiveness

---

**Status**: Algorithm analyzed, hybrid approach proposed  
**Next**: Implement and test segmentation + n-gram indexing  
**Philosophy**: Combine natural boundaries (punctuation) with character-level matching (n-grams)
