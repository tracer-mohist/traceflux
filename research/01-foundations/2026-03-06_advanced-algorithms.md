# Research: Advanced Compression & Search Algorithms

DATE: 2026-03-06
STATUS: Algorithm Inspiration
TOPIC: LZMA, PageRank, BWT -- Inspiration for traceflux

---

## User's Hint

N-GRAM-MAY-NOT-BE-THE-BEST-STRATEGY.

REFERENCES:
1. 7Z-COMPRESSION-ALGORITHM -- Award-winning algorithm
2. GOOGLE'S-SEARCH-ALGORITHM -- Famous search technique

Let me recall and analyze these.

---

## 1. LZMA (Lempel-Ziv-Markov Algorithm)

### Background

USED-IN: 7z file format (7-Zip)

AWARDS:
- LZ77 (basis): IEEE Computer Society Golden Jubilee Award
- LZW: Various awards for data compression

KEY-IDEA: DICTIONARY-BASED-COMPRESSION-WITH-SLIDING-WINDOW

---

### Core Algorithm (LZ77/LZMA)

```text
Instead of storing repeated data, store references:

Text: "hello hello world hello"

Naive storage:
  "hello hello world hello" (24 chars)

LZ77 compression:
  "hello" (5 chars)
  + <copy from 6 chars ago, length 5>  -> "hello"
  + " world" (6 chars)
  + <copy from 17 chars ago, length 5> -> "hello"

Result: "hello" + (offset=6, len=5) + " world" + (offset=17, len=5)
        Much smaller!
```

### Sliding Window + Dictionary

```text
Position: 0    5    10   15   20
Text:     h e l l o   h e l l o   w o r l d   h e l l o
          |         |              |
          +---------+              |
          Already seen             |
                                   +-------------+
                                   Match found! (offset=17, len=5)

Algorithm:
  1. Maintain sliding window of recent text
  2. For each position, find longest match in window
  3. Output: (offset, length) or literal char
```

### Application to traceflux

```text
Instead of n-grams, use LZ-style references:

Text: "proxy configuration proxy settings"

Index:
  "proxy " (literal, pos 0)
  "configuration" (literal, pos 6)
  " " (literal, pos 19)
  <match: offset=20, length=6>  -> "proxy "
  "settings" (literal, pos 26)

Benefit:
  - Captures repeated patterns automatically
  - No fixed n-gram size
  - Variable-length patterns
  - Space-efficient
```

### Key Insight for Search

```text
LZ77 finds: "This sequence appeared before at position X"

For search:
  - "proxy" appears at [0, 20, 100, 250]
  - "proxy config" appears at [0, 100] (longer pattern)
  - "proxy settings" appears at [20, 250] (longer pattern)

Instead of fixed n-grams, find **maximal repeated sequences**.
```

---

## 2. PageRank (Google's Algorithm)

### Background

CREATED-BY: Larry Page & Sergey Brin (1996)

PURPOSE: Rank web pages by importance

KEY-IDEA: LINK-STRUCTURE-AS-IMPORTANCE-SIGNAL

---

### Core Algorithm

```text
Web as graph:
  Page A -> Page B (A links to B)

PageRank:
  - A page is important if important pages link to it
  - Recursive definition

Formula:
  PR(A) = (1-d)/N + d * SIGMA(PR(Ti)/C(Ti))

  Where:
    PR(A) = PageRank of page A
    d = damping factor (0.85)
    N = total pages
    Ti = pages linking to A
    C(Ti) = number of outbound links from Ti
```

### Intuition

```text
Page A has many inbound links -> Important
Page B has few inbound links -> Less important

But: One link from important page > many links from unimportant pages
```

### Application to traceflux

```text
Text segments as "pages":
  Segment A: "proxy configuration"
  Segment B: "proxy settings"
  Segment C: "git proxy"

Co-occurrence as "links":
  If A and B appear in same document -> A ↔ B (linked)

Segment "PageRank":
  - Segment appearing with many others -> Important (hub)
  - Segment appearing with important segments -> Important

Example:
  "proxy" appears with: config, settings, git, SSH, firewall...
  -> High "rank" (central concept)

  "authentication" appears with: security, proxy, firewall...
  -> Also high "rank"

  "xyz123" appears alone
  -> Low "rank" (likely noise)
```

### Key Insight for Search

```text
Not all segments are equal:
  - Some are "hubs" (appear with many others)
  - Some are "authorities" (linked by hubs)
  - Some are isolated (noise?)

Rank segments by "importance" in co-occurrence graph.
```

---

## 3. Burrows-Wheeler Transform (BWT)

### Background

CREATED-BY: Michael Burrows & David Wheeler (1994)

USED-IN: bzip2, gzip, modern compressors

KEY-IDEA: REORDER-TEXT-TO-GROUP-SIMILAR-CONTEXTS

---

### Core Algorithm

```text
Original: "banana"

All rotations:
  banana
  ananab
  nanaba
  anaban
  nabana
  abanan

Sort rotations:
  abanan
  anaban
  ananab
  banana  <- Original
  nabana
  nanaba

Take last column: "nnbaaa"

BWT("banana") = "nnbaaa"

Why? Similar contexts are grouped:
  "n" follows "a" multiple times -> grouped together
```
