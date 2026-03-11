# N-gram Implementations

Purpose: Code examples for n-gram operations.

NOTE: Companion to ngram-analysis.md (2026-03-11)

---

## N-gram Extraction

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

---

## N-gram Similarity

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

---

## N-gram Frequency Index

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

## Performance Optimization

### Frequency Threshold

```python
def filter_by_frequency(ngram_index, min_freq=2):
    """Remove n-grams below frequency threshold."""
    return {
        ng: freq for ng, freq in ngram_index.items()
        if freq >= min_freq
    }
```

### Hashing Trick

```python
def hash_ngram(ngram, num_buckets=10000):
    """Hash n-gram to fixed bucket."""
    return hash(ngram) % num_buckets
```

---

Last Updated: 2026-03-11
