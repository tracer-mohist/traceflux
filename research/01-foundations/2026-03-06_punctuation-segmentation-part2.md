### Option E: Suffix Tree / Suffix Array

```text
Segment: "Hello"

Suffix Tree:
(root)
  +- "Hello$"
  +- "ello$"
  +- "llo$"
  +- "lo$"
  +- "o$"

Pros:
- Can match any substring in O(m) time
- Captures all possible substrings
- Efficient for repeated queries

Cons:
- Complex to implement
- High memory overhead
- Overkill for short segments

Verdict:  Good for long segments, overkill for short ones
```

### Option F: Structural Features (Abstract)

```text
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

Verdict:  Recommended as supplementary features
```

---

## Proposed Hybrid Approach

### Multi-Level Representation

```text
For each segment:

Level 1: Type (Punctuation Context)
  - hash(pre_punct + post_punct)
  - Example: hash(",!") = 12345

Level 2: N-gram Index (Local Patterns)
  - 2-grams: ["He", "el", "ll", "lo"]
  - 3-grams: ["Hel", "ell", "llo"]
  - Stored as: ngram -> segment_ids

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

```text
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

```text
Segment S = (content, pre_punct, post_punct)

Where:
  content IN SIGMA* (string over Unicode alphabet)
  pre_punct IN P UNION {START} (punctuation or start)
  post_punct IN P UNION {END} (punctuation or end)

Type(S) = hash(pre_punct + post_punct)

NGrams(S, n) = {S[i:i+n] | 0 <= i <= len(S) - n}

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

```text
Similarity(S1, S2) =
  α * ngram_overlap(S1, S2) +
  β * structural_similarity(S1, S2) +
  γ * type_match(S1, S2)

Where:
  ngram_overlap = |NGrams(S1) INTERSECT NGrams(S2)| / |NGrams(S1) UNION NGrams(S2)|
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
    'by_type': Dict[int, List[Segment]],  # type_hash -> segments
    'by_ngram': Dict[str, List[Segment]],  # ngram -> segments
    'by_length': Dict[int, List[Segment]],  # length -> segments
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
    ngrams: Dict[int, Set[str]]  # n -> set of n-grams
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
