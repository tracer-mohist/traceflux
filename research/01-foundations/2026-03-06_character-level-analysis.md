# Research: Character-Level Sequence Analysis

DATE: 2026-03-06
STATUS: Foundational Research
TOPIC: Pure mathematical approach based on character sequences, not "words"

---

## Core Problem

### What is a "Word"?

PROBLEM: We cannot reliably define "word" across languages:

| Language | Word Boundary | Challenge |
|----------|---------------|-----------|
| English | Space | Relatively clear |
| Chinese | No space | Requires segmentation (ambiguous) |
| Japanese | Mixed scripts | Complex boundaries |
| Arabic | Cursive | Connected characters |
| Thai | No space | Requires dictionary |

CONCLUSION: "Word" is a LINGUISTIC-ABSTRACTION, not a fundamental unit.

### What CAN We Rely On?

ANSWER: Computer encoding -- characters as integers.

```text
Text: "Hello 世界"

UTF-8 Encoding:
H    e    l    l    o       世    界
0x48 0x65 0x6C 0x6C 0x6F 0x20 0xE4 0xB8 0x96 0xE7 0x95 0x8C

Position: 0    1    2    3    4    5    6    7    8    9    10   11
```

KEY-INSIGHT: Characters at positions form a SEQUENCE -- this is universal, language-independent.

---

## Mathematical Foundations

### 1. Set Theory -- Ordered Sets

DEFINITION: A set with a binary relation <= that is:
- Reflexive: a <= a
- Antisymmetric: if a <= b and b <= a, then a = b
- Transitive: if a <= b and b <= c, then a <= c

APPLICATION-TO-TEXT:

```text
Document as Ordered Set:
D = {(char, position) | char IN Unicode, position IN ℕ}

Example: "Hello"
D = {('H', 0), ('e', 1), ('l', 2), ('l', 3), ('o', 4)}

Order Relation:
('H', 0) < ('e', 1) < ('l', 2) < ('l', 3) < ('o', 4)
```

KEY-PROPERTY: Position defines order, independent of character meaning.

### 2. Sequence Theory

DEFINITION: A sequence is an ordered list of elements.

```text
Text as Sequence:
S = [c_0, c_1, c_2, ..., c_n]

Where:
- cᵢ IN Unicode (character at position i)
- i IN {0, 1, 2, ..., n} (position)
```

SUBSEQUENCE:
```text
S' is subsequence of S if:
S' = [cᵢ_1, cᵢ_2, ..., cᵢ_k] where i_1 < i_2 < ... < i_k

Example:
S = "Hello World"
S' = "HloWrd" (subsequence, positions 0,2,4,6,8,9)
```

### 3. String Metrics (Distance Measures)

| Metric | Definition | Use Case |
|--------|------------|----------|
| HAMMING-DISTANCE | Positions where characters differ | Fixed-length strings |
| LEVENSHTEIN-DISTANCE | Min edits (insert/delete/substitute) | Spell checking |
| JACCARD-SIMILARITY | |A INTERSECT B| / |A UNION B| | Set overlap |
| LONGEST-COMMON-SUBSEQUENCE | Length of longest shared subsequence | Sequence similarity |

### 4. Information Theory -- Sequence Entropy

SHANNON-ENTROPY:
```text
H(X) = -SIGMA p(xᵢ) log_2 p(xᵢ)

For text:
- xᵢ = character at position i
- p(xᵢ) = probability of character xᵢ
```

APPLICATION: Measure sequence complexity, predictability.

### 5. Formal Language Theory

REGULAR-LANGUAGES:
- Defined by regular expressions
- Recognized by finite automata
- Pattern matching foundation

APPLICATION:
```text
Pattern: "proxy"
Regex: p-r-o-x-y
Automaton: State machine that accepts this sequence
```

---

## Proposed Approach: Pure Sequence Analysis

### Level 0: Character Sequences (Foundation)

```text
Document: "Hello 世界"

Representation:
[(0x48, 0), (0x65, 1), (0x6C, 2), (0x6C, 3), (0x6F, 4),
 (0x20, 5), (0xE4, 6), (0xB8, 7), (0x96, 8), ...]

Operations:
- Subsequence extraction
- Pattern matching (regex)
- Position-based queries
```

### Level 1: N-gram Sequences (Abstracted)

```text
Document: "Hello"

Character 2-grams (bigrams):
"He", "el", "ll", "lo"
Positions: [(0,1), (1,2), (2,3), (3,4)]

Character 3-grams (trigrams):
"Hel", "ell", "llo"
Positions: [(0,1,2), (1,2,3), (2,3,4)]

Key: N-grams are still character-based, no linguistic "word" concept.
```

### Level 2: Co-occurrence Patterns (Relational)

```text
Pattern P_1 = "pro" at positions [10, 245, 892]
Pattern P_2 = "xy" at positions [13, 248, 895]

Co-occurrence:
P_1 and P_2 appear within window W=5:
- Position 10 and 13: distance=3
- Position 245 and 248: distance=3
- Position 892 and 895: distance=3

Association: P_1 ↔ P_2 (strength = 3 co-occurrences)
```

### Level 3: User Query Matching (Application)

```text
User Input: "proxy"

Step 1: Convert to sequence
Query = [(p,0), (r,1), (o,2), (x,3), (y,4)]

Step 2: Find exact matches in document
Matches: positions [10, 245, 892]

Step 3: Find fuzzy matches (edit distance <= 2)
Fuzzy: "proxies" [567], "proxying" [789]

Step 4: Find co-occurring patterns
Co-occurring: "config" [15, 250], "git" [8, 243]

Output: All matches with positions and distances
```

---

## Flowchart: Character-Level Search

```text
+-------------------------------------------------------------+
|                    DOCUMENT LIBRARY                          |
|  [Doc_1, Doc_2, Doc_3, ..., Doc_n]                              |
|  Each Doc = Sequence of (character, position) pairs         |
+-------------------------------------------------------------+
                            |
                            v
+-------------------------------------------------------------+
|              LEVEL 0: CHARACTER EXTRACTION                   |
|                                                              |
|  For each document:                                          |
|    1. Read as byte sequence (UTF-8)                         |
|    2. Convert to (char_code, position) pairs                |
|    3. Store in index                                        |
|                                                              |
|  Output: [(0x48,0), (0x65,1), (0x6C,2), ...]               |
+-------------------------------------------------------------+
                            |
                            v
+-------------------------------------------------------------+
|              LEVEL 1: N-GRAM ABSTRACTION                     |
|                                                              |
|  For each character sequence:                                |
|    1. Extract n-grams (n=2,3,4,5)                           |
|    2. Record positions for each n-gram                      |
|    3. Build inverted index: n-gram -> [positions]            |
|                                                              |
|  Output:                                                     |
|    "pro" -> [(doc_1, [10,245]), (doc_2, [892])]               |
|    "ro"  -> [(doc_1, [11,246]), (doc_2, [893])]               |
|    "o"   -> [(doc_1, [12,247]), (doc_2, [894])]               |
+-------------------------------------------------------------+
                            |
                            v
+-------------------------------------------------------------+
|           LEVEL 2: CO-OCCURRENCE ANALYSIS                    |
|                                                              |
|  For each n-gram pair (G_1, G_2):                             |
|    1. Find positions where both appear                      |
|    2. Calculate distance: |pos_1 - pos_2|                     |
|    3. If distance <= window_size:                            |
|         Record co-occurrence                                |
|    4. Build co-occurrence graph:                            |
|         G_1 --(distance, count)--> G_2                        |
|                                                              |
|  Output: Graph where:                                        |
|    Nodes = n-grams                                          |
|    Edges = Co-occurrences (weighted by count, distance)     |
+-------------------------------------------------------------+
                            |
                            v
