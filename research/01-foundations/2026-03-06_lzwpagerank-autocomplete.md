# Research: Dictionary-Based Compression + Autocomplete for Search

DATE: 2026-03-06
STATUS: Advanced Algorithm Analysis
TOPIC: LZW dictionary + PageRank, Autocomplete for relation analysis

---

## 1. Dictionary-Based Compression (LZW/LZ78)

### User's Question

> ", PageRank  n-gram"
>
> (A famous compression algorithm generates a dictionary. Is this dictionary + PageRank better than n-gram indexing?)

---

### Algorithm Identification

THE-ALGORITHM: LZW-(LEMPEL-ZIV-WELCH) or LZ78

AWARDS:
- LZW: IEEE Computer Society Golden Jubilee Award
- Used in: GIF, Unix compress, early ZIP

---

### How LZW Works

```text
LZW builds a dictionary dynamically:

Input: "hello hello world hello"

Step-by-step:
  1. Read "h" -> not in dict, add "h" (code 0)
  2. Read "he" -> not in dict, add "he" (code 1)
  3. Read "hel" -> not in dict, add "hel" (code 2)
  4. Read "hell" -> not in dict, add "hell" (code 3)
  5. Read "hello" -> not in dict, add "hello" (code 4)
  6. Read "hello " -> not in dict, add "hello " (code 5)
  7. Read " " (space) -> in dict (code 6)
  8. Read "he" -> in dict! Output code 1
  9. Read "ll" -> continue...

Output: [codes for compressed data]
Dictionary: {
  0: "h",
  1: "he",
  2: "hel",
  3: "hell",
  4: "hello",
  5: "hello ",
  6: " ",
  ...
}
```

---

### LZW vs LZ77

| Aspect | LZ77 | LZW/LZ78 |
|--------|------|----------|
| DICTIONARY | Implicit (sliding window) | Explicit (grows dynamically) |
| REFERENCE | (offset, length) | Dictionary code |
| PATTERN-DISCOVERY | Local (window-limited) | Global (entire text) |
| INDEX-OUTPUT | Positions | Dictionary + codes |
| BEST-FOR | Local redundancy | Global patterns |

---

### LZW Dictionary as Index

KEY-INSIGHT: LZW dictionary = Natural pattern index!

```text
LZW Dictionary for corpus:
  {
    0: "proxy",
    1: "proxy ",
    2: "proxy c",
    3: "proxy co",
    4: "proxy con",
    5: "proxy conf",
    6: "proxy confi",
    7: "proxy config",
    8: "config",
    9: "configuration",
    10: "settings",
    ...
  }

Each entry has:
  - Code (unique ID)
  - Pattern (string)
  - Frequency (how many times used)
  - Positions (where used)
```

---

### LZW Dictionary + PageRank

PROPOSAL: Build co-occurrence graph on LZW dictionary entries!

```text
Step 1: Run LZW on corpus
  Output: Dictionary D = {code -> pattern}

Step 2: Extract co-occurrences
  For each document:
    Sequence of codes: [4, 5, 8, 10, ...]
    Adjacent codes co-occur: (4,5), (5,8), (8,10), ...

Step 3: Build graph
  Nodes: Dictionary codes (patterns)
  Edges: Co-occurrence in code sequence
  Weights: Co-occurrence frequency

Step 4: Run PageRank
  Rank patterns by graph importance
```

---

### Example: LZW + PageRank

```text
Corpus:
  Doc 1: "proxy configuration proxy settings"
  Doc 2: "proxy settings proxy config"
  Doc 3: "proxy configuration"

LZW Dictionary (simplified):
  0: "proxy"
  1: "proxy "
  2: "proxy configuration"
  3: " settings"
  4: " config"

Code sequences:
  Doc 1: [2, 3, 0, 1, 3]  (proxy config + settings + proxy + settings)
  Doc 2: [0, 1, 3, 0, 1, 4]
  Doc 3: [2]

Co-occurrence graph:
  0 ↔ 1: 3 times
  1 ↔ 3: 2 times
  1 ↔ 4: 1 time
  2 ↔ 3: 1 time

PageRank:
  Pattern 0 ("proxy"): 0.30
  Pattern 1 ("proxy "): 0.25
  Pattern 2 ("proxy configuration"): 0.20
  Pattern 3 (" settings"): 0.15
  Pattern 4 (" config"): 0.10

Index:
  "proxy" -> code 0, rank 0.30, positions [...]
  "proxy configuration" -> code 2, rank 0.20, positions [...]
```

---

### LZW+PageRank vs N-gram

| Metric | N-gram Index | LZW+PageRank | Winner |
|--------|--------------|--------------|--------|
| PATTERN-TYPE | Fixed size | Variable (natural) | LZW  |
| INDEX-SIZE | O(|C|xmax_n) | O(|Dictionary|) | LZW  |
| PATTERN-DISCOVERY | Sliding window | Dictionary growth | LZW  |
| FREQUENCY | Per n-gram | Per dictionary entry | Tie |
| RANKING | None (or post-hoc) | Built-in PageRank | LZW  |
| QUERY-SPEED | O(1) lookup | O(1) code lookup | Tie |
| CONTEXT | Lost | Preserved in codes | LZW  |
| COMPRESSION | None | Built-in | LZW  |

CONCLUSION: LZW+PageRank is superior to N-gram for indexing!

---

### Advantages of LZW+PageRank

```text
1. Natural Patterns
   - Dictionary entries grow organically
   - Not artificially cut to fixed size
   - "proxy configuration" is one entry (not fragmented)

2. Built-in Compression
   - Index is compressed representation
   - Smaller than raw text
   - Faster to search

3. PageRank Integration
   - Patterns ranked by importance
   - High-rank patterns prioritized
   - Low-rank patterns filtered (noise)

4. Hierarchical Structure
   - "proxy" -> "proxy " -> "proxy c" -> ... -> "proxy configuration"
   - Prefix relationships captured
   - Efficient prefix queries
```

---
