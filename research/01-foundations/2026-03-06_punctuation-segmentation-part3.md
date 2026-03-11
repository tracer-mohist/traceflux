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
```text

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

RECOMMENDATION: Combine both approaches:
- Use punctuation segmentation for **coarse grouping**
- Use character-level n-grams for **fine matching**

---

## Key Insights

### 1. Punctuation Provides Natural Boundaries

Segments between punctuation are more meaningful than fixed windows:
- "Hello, world!" -> ["Hello", "world"] (natural)
- Fixed window: ["Hello, w", "orld!"] (arbitrary)

### 2. Type Hashing Enables Fast Grouping

```
Type hash: hash(pre_punct + post_punct)

Segments with same type:
  - "Hello," and "Hi," (both end with comma)
  - "Really?" and "Sure?" (both end with question)

Enables: Group by sentence type (statement, question, exclamation)
```text

### 3. N-grams Capture Local Patterns

```
"Hello" -> 2-grams: ["He", "el", "ll", "lo"]

Matching:
  - "Hello" matches "Hello" (4/4 n-grams)
  - "Hello" matches "Hallo" (3/4 n-grams: "al", "ll", "lo")
  - "Hello" matches "World" (0/4 n-grams)
```text

### 4. Structural Features Enable Fuzzy Matching

```
"Hello" vs "Hallo":
  - Same length:
  - Same first/last:  (H, o)
  - Same char set:  (e vs a)
  - Same pattern:  (FIRST_CAP)

Similarity: 3/4 = 0.75
```text

---

## Next Steps

1. **Implement segment extraction** -- Punctuation-based splitting
2. **Implement n-gram indexing** -- For each segment
3. **Implement structural features** -- Length, first/last, etc.
4. **Test on multilingual corpus** -- Verify punctuation handling
5. **Compare with pure character-level** -- Measure effectiveness

---

STATUS: Algorithm analyzed, hybrid approach proposed
NEXT: Implement and test segmentation + n-gram indexing
PHILOSOPHY: Combine natural boundaries (punctuation) with character-level matching (n-grams)
