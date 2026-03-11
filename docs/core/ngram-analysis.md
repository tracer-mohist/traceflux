# N-gram Analysis

**Purpose**: Extract character patterns at multiple scales.

**NOTE**: Consolidated from research/01-foundations/ (2026-03-11)

---

## What is N-gram?

N-gram is a contiguous sequence of n characters from a text.

### Example: "hello"

```text
1-gram (unigram) - single characters:
  ["h", "e", "l", "l", "o"]

2-gram (bigram) - 2 consecutive characters:
  ["he", "el", "ll", "lo"]

3-gram (trigram) - 3 consecutive characters:
  ["hel", "ell", "llo"]

4-gram - 4 consecutive characters:
  ["hell", "ello"]

5-gram - 5 consecutive characters:
  ["hello"]
```

### Sliding Window

```text
Text:  h  e  l  l  o
        +--+  <- 2-gram: "he"
           +--+  <- 2-gram: "el"
              +--+  <- 2-gram: "ll"
                 +--+  <- 2-gram: "lo"

Window size = 2, slides 1 character at a time
```

---

## Why N-gram?

### Fuzzy Matching

**Problem**: Exact match fails on typos.

```text
Text 1: "hello"
Text 2: "hallo"

Exact match: No match (completely different)

Human intuition: Very similar! Only 1 letter different.
```

**Solution**: N-gram similarity.

```text
"hello" 2-grams: ["he", "el", "ll", "lo"]
"hallo" 2-grams: ["ha", "al", "ll", "lo"]

Common 2-grams: ["ll", "lo"] (2/4 = 50% similar)

Conclusion: Partial match, 50% similarity
```

---

## Applications

### 1. Search Engine

```text
User search: "hello"
Document: "hallo world"

Traditional match: Not found ("hello" != "hallo")

N-gram match:
  Search 2-grams: ["he", "el", "ll", "lo"]
  Document 2-grams: ["ha", "al", "ll", "lo", "o ", " w", ...]
  Common: ["ll", "lo"]
  Similarity: 2/4 = 50%

  Result: Found similar content!
```

### 2. Autocomplete

```text
User types: "hel"

Find all 3-grams starting with "hel":
  "hel" + "lo" -> "hello"
  "hel" + "p" -> "help"
  "hel" + "met" -> "helmet"

Rank by frequency: "hello" > "help" > "helmet"
```

### 3. Language Detection

```text
English common 2-grams: ["th", "he", "in", "er", "an"]
German common 2-grams: ["er", "en", "ch", "de", "un"]
Chinese: Use character-level (not applicable)

Analyze text's n-gram distribution -> detect language
```

### 4. Text Compression

```text
Frequent n-grams can be replaced with shorter codes.

Example: "th" appears 1000 times
  Replace "th" with 1-byte code
  Save: 1000 * (2 - 1) = 1000 bytes

LZW compression uses this principle.
```

---

## N-gram Size Selection

### Small N (1-2)

**Pros**:
- Captures local patterns
- Good for typo tolerance
- Low memory usage

**Cons**:
- Many false positives
- Less semantic meaning

**Use case**: Fuzzy search, spell check

### Medium N (3-4)

**Pros**:
- Balance between specificity and generality
- Captures common patterns
- Good for autocomplete

**Cons**:
- More memory than small N

**Use case**: Autocomplete, search suggestions

### Large N (5+)

**Pros**:
- High specificity
- Captures phrases
- Low false positive rate

**Cons**:
- Sparse data (many n-grams appear once)
- High memory usage

**Use case**: Exact phrase matching, plagiarism detection

---

## Implementation

### N-gram Extraction

```python
def extract_ngrams(text, n):
    """
    Extract all n-grams from text.

    Args:
        text: Input string
        n: N-gram size

    Returns: List of n-grams
    """
    if len(text) < n:
        return [text] if text else []

    return [text[i:i+n] for i in range(len(text) - n + 1)]

# Example
text = "hello"
print(extract_ngrams(text, 2))  # ["he", "el", "ll", "lo"]
print(extract_ngrams(text, 3))  # ["hel", "ell", "llo"]
```

### N-gram Similarity

```python
def ngram_similarity(text1, text2, n=2):
    """
    Calculate n-gram similarity between two texts.

    Returns: Similarity score (0.0 to 1.0)
    """
    ngrams1 = set(extract_ngrams(text1, n))
    ngrams2 = set(extract_ngrams(text2, n))

    if not ngrams1 or not ngrams2:
        return 0.0

    intersection = ngrams1 & ngrams2
    union = ngrams1 | ngrams2

    return len(intersection) / len(union)

# Example
sim = ngram_similarity("hello", "hallo", n=2)
print(f"Similarity: {sim:.2f}")  # 0.50
```

### N-gram Frequency Index

```python
from collections import defaultdict

class NgramIndex:
    def __init__(self, n=2):
        self.n = n
        self.frequency = defaultdict(int)
        self.positions = defaultdict(list)

    def add_text(self, text, doc_id):
        """Add text to index."""
        for i, ngram in enumerate(extract_ngrams(text, self.n)):
            self.frequency[ngram] += 1
            self.positions[ngram].append((doc_id, i))

    def get_similar(self, query, top_k=10):
        """Get documents similar to query."""
        query_ngrams = set(extract_ngrams(query, self.n))

        scores = defaultdict(float)
        for ngram in query_ngrams:
            for doc_id, pos in self.positions[ngram]:
                scores[doc_id] += 1

        # Normalize by query length
        for doc_id in scores:
            scores[doc_id] /= len(query_ngrams)

        # Return top-k
        return sorted(scores.items(), key=lambda x: -x[1])[:top_k]
```

---

## Performance Considerations

### Memory Usage

```text
N-gram size | Memory (for 1M chars)
------------|----------------------
2-gram      | ~100K entries
3-gram      | ~500K entries
4-gram      | ~2M entries
5-gram      | ~10M entries

Rule: Larger N = exponentially more entries
```

### Optimization Strategies

1. **Frequency threshold**: Only store n-grams appearing >= 2 times
2. **Hashing**: Use hash functions instead of storing full strings
3. **Compression**: Use LZW or similar to compress n-gram index
4. **Lazy evaluation**: Compute n-grams on-demand, not upfront

---

## Related

- [Text Segmentation](./text-segmentation.md) - How to split text before n-gram analysis
- [Frequency Ranking](./frequency-ranking.md) - Weight n-grams by importance
- [Autocomplete](../algorithms/autocomplete.md) - Application of n-gram matching

---

**Last Updated**: 2026-03-11
**Source Files**: `2026-03-06_ngram-explained*.md`
