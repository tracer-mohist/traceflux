# Research: Character-Level Sequence Analysis

**Date**: 2026-03-06  
**Status**: Foundational Research  
**Topic**: Pure mathematical approach based on character sequences, not "words"

---

## Core Problem

### What is a "Word"?

**Problem**: We cannot reliably define "word" across languages:

| Language | Word Boundary | Challenge |
|----------|---------------|-----------|
| English | Space | Relatively clear |
| Chinese | No space | Requires segmentation (ambiguous) |
| Japanese | Mixed scripts | Complex boundaries |
| Arabic | Cursive | Connected characters |
| Thai | No space | Requires dictionary |

**Conclusion**: "Word" is a **linguistic abstraction**, not a fundamental unit.

### What CAN We Rely On?

**Answer**: Computer encoding — characters as integers.

```
Text: "Hello 世界"

UTF-8 Encoding:
H    e    l    l    o       世    界
0x48 0x65 0x6C 0x6C 0x6F 0x20 0xE4 0xB8 0x96 0xE7 0x95 0x8C

Position: 0    1    2    3    4    5    6    7    8    9    10   11
```

**Key Insight**: Characters at positions form a **sequence** — this is universal, language-independent.

---

## Mathematical Foundations

### 1. Set Theory — Ordered Sets

**Definition**: A set with a binary relation ≤ that is:
- Reflexive: a ≤ a
- Antisymmetric: if a ≤ b and b ≤ a, then a = b
- Transitive: if a ≤ b and b ≤ c, then a ≤ c

**Application to Text**:

```
Document as Ordered Set:
D = {(char, position) | char ∈ Unicode, position ∈ ℕ}

Example: "Hello"
D = {('H', 0), ('e', 1), ('l', 2), ('l', 3), ('o', 4)}

Order Relation:
('H', 0) < ('e', 1) < ('l', 2) < ('l', 3) < ('o', 4)
```

**Key Property**: Position defines order, independent of character meaning.

### 2. Sequence Theory

**Definition**: A sequence is an ordered list of elements.

```
Text as Sequence:
S = [c₀, c₁, c₂, ..., cₙ]

Where:
- cᵢ ∈ Unicode (character at position i)
- i ∈ {0, 1, 2, ..., n} (position)
```

**Subsequence**:
```
S' is subsequence of S if:
S' = [cᵢ₁, cᵢ₂, ..., cᵢₖ] where i₁ < i₂ < ... < iₖ

Example:
S = "Hello World"
S' = "HloWrd" (subsequence, positions 0,2,4,6,8,9)
```

### 3. String Metrics (Distance Measures)

| Metric | Definition | Use Case |
|--------|------------|----------|
| **Hamming Distance** | Positions where characters differ | Fixed-length strings |
| **Levenshtein Distance** | Min edits (insert/delete/substitute) | Spell checking |
| **Jaccard Similarity** | |A ∩ B| / |A ∪ B| | Set overlap |
| **Longest Common Subsequence** | Length of longest shared subsequence | Sequence similarity |

### 4. Information Theory — Sequence Entropy

**Shannon Entropy**:
```
H(X) = -Σ p(xᵢ) log₂ p(xᵢ)

For text:
- xᵢ = character at position i
- p(xᵢ) = probability of character xᵢ
```

**Application**: Measure sequence complexity, predictability.

### 5. Formal Language Theory

**Regular Languages**:
- Defined by regular expressions
- Recognized by finite automata
- Pattern matching foundation

**Application**:
```
Pattern: "proxy"
Regex: p-r-o-x-y
Automaton: State machine that accepts this sequence
```

---

## Proposed Approach: Pure Sequence Analysis

### Level 0: Character Sequences (Foundation)

```
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

```
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

```
Pattern P₁ = "pro" at positions [10, 245, 892]
Pattern P₂ = "xy" at positions [13, 248, 895]

Co-occurrence:
P₁ and P₂ appear within window W=5:
- Position 10 and 13: distance=3 ✓
- Position 245 and 248: distance=3 ✓
- Position 892 and 895: distance=3 ✓

Association: P₁ ↔ P₂ (strength = 3 co-occurrences)
```

### Level 3: User Query Matching (Application)

```
User Input: "proxy"

Step 1: Convert to sequence
Query = [(p,0), (r,1), (o,2), (x,3), (y,4)]

Step 2: Find exact matches in document
Matches: positions [10, 245, 892]

Step 3: Find fuzzy matches (edit distance ≤ 2)
Fuzzy: "proxies" [567], "proxying" [789]

Step 4: Find co-occurring patterns
Co-occurring: "config" [15, 250], "git" [8, 243]

Output: All matches with positions and distances
```

---

## Flowchart: Character-Level Search

```
┌─────────────────────────────────────────────────────────────┐
│                    DOCUMENT LIBRARY                          │
│  [Doc₁, Doc₂, Doc₃, ..., Docₙ]                              │
│  Each Doc = Sequence of (character, position) pairs         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              LEVEL 0: CHARACTER EXTRACTION                   │
│                                                              │
│  For each document:                                          │
│    1. Read as byte sequence (UTF-8)                         │
│    2. Convert to (char_code, position) pairs                │
│    3. Store in index                                        │
│                                                              │
│  Output: [(0x48,0), (0x65,1), (0x6C,2), ...]               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              LEVEL 1: N-GRAM ABSTRACTION                     │
│                                                              │
│  For each character sequence:                                │
│    1. Extract n-grams (n=2,3,4,5)                           │
│    2. Record positions for each n-gram                      │
│    3. Build inverted index: n-gram → [positions]            │
│                                                              │
│  Output:                                                     │
│    "pro" → [(doc₁, [10,245]), (doc₂, [892])]               │
│    "ro"  → [(doc₁, [11,246]), (doc₂, [893])]               │
│    "o"   → [(doc₁, [12,247]), (doc₂, [894])]               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│           LEVEL 2: CO-OCCURRENCE ANALYSIS                    │
│                                                              │
│  For each n-gram pair (G₁, G₂):                             │
│    1. Find positions where both appear                      │
│    2. Calculate distance: |pos₁ - pos₂|                     │
│    3. If distance ≤ window_size:                            │
│         Record co-occurrence                                │
│    4. Build co-occurrence graph:                            │
│         G₁ --(distance, count)--> G₂                        │
│                                                              │
│  Output: Graph where:                                        │
│    Nodes = n-grams                                          │
│    Edges = Co-occurrences (weighted by count, distance)     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              LEVEL 3: USER QUERY PROCESSING                  │
│                                                              │
│  User Input: "proxy"                                        │
│                                                              │
│  Step 1: Convert to n-grams                                 │
│    "proxy" → ["pro", "ro", "ox", "xy", "prox", "roxy", ...]│
│                                                              │
│  Step 2: Find exact matches in index                        │
│    "pro" → [doc₁:10, doc₁:245, doc₂:892]                   │
│    "xy"  → [doc₁:13, doc₁:248, doc₂:895]                   │
│                                                              │
│  Step 3: Traverse co-occurrence graph (BFS, max_degrees=3)  │
│    "pro" → "xy" (direct, same word)                         │
│    "pro" → "config" (2°, co-occur in doc₁)                  │
│    "pro" → "git" (2°, co-occur in doc₁)                     │
│    "pro" → "security" (3°, via "config")                    │
│                                                              │
│  Step 4: Return all associations with:                      │
│    - Degree (1°, 2°, 3°)                                    │
│    - Path (how connected)                                   │
│    - Positions (where found)                                │
│    - Co-occurrence count (strength)                         │
│                                                              │
│  Output: List of associations (NO judgment on relevance)    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    USER / AGENT                              │
│                                                              │
│  Receives: All associations with metadata                   │
│  Judges: Which are relevant for current task               │
│  Acts: Uses selected associations                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Mathematical Concepts

### 1. Ordered Sets (Set Theory)

```
Text as Ordered Set:
T = {(c, p) | c ∈ Unicode, p ∈ ℕ, c appears at position p}

Order: (c₁, p₁) < (c₂, p₂) iff p₁ < p₂

Properties:
- Total order (any two positions comparable)
- Well-founded (no infinite descending chain)
- Discrete (positions are integers)
```

### 2. Subsequences (Sequence Theory)

```
Subsequence Relation:
S' ⊑ S iff S' can be obtained by deleting elements from S

Example:
S  = "Hello World"
S' = "HloWrd" (delete e,l,l,o,o,l)

Application: Fuzzy matching (user query as subsequence of document)
```

### 3. Graph Theory (Co-occurrence Network)

```
Co-occurrence Graph:
G = (V, E)

V = Set of n-grams
E = {(u, v) | u and v co-occur within window W}

Edge Weight:
w(u,v) = co-occurrence_count / distance

Path Finding:
BFS from query n-gram to find all associations within k degrees
```

### 4. Information Theory (Sequence Complexity)

```
Entropy of n-gram distribution:
H = -Σ p(gᵢ) log₂ p(gᵢ)

Where:
- gᵢ = n-gram
- p(gᵢ) = frequency of gᵢ / total n-grams

Application:
- High entropy: Diverse vocabulary
- Low entropy: Repetitive text
- Anomaly detection: Unusual n-gram patterns
```

---

## Advantages of Character-Level Approach

### 1. Language Independence

```
English: "proxy" → [(p,0), (r,1), (o,2), (x,3), (y,4)]
Chinese: "代理" → [(0xE4,0), (0xB8,1), (0x96,2), (0xE7,3), (0x95,4), (0x8C,5)]
Arabic: "وكيل" → [(0xD9,0), (0x88,1), (0xD9,2), (0x83,3), (0xD9,4), (0x8A,4)]

Same representation: (char_code, position)
Same operations: subsequence, co-occurrence, graph traversal
```

### 2. No Linguistic Assumptions

```
No need to define:
- What is a "word"?
- Where are word boundaries?
- What is grammar?

Only need:
- Character encoding (UTF-8)
- Position (integer)
- Co-occurrence window (integer)
```

### 3. Purely Mathematical

```
Operations:
- Set operations (union, intersection)
- Sequence operations (subsequence, concatenation)
- Graph operations (BFS, path finding)
- Information theory (entropy, mutual information)

All language-independent, based on integers and relations.
```

### 4. Scalable Abstraction

```
Level 0: Characters (universal)
  ↓
Level 1: N-grams (abstracted patterns)
  ↓
Level 2: Co-occurrences (relations)
  ↓
Level 3: User queries (application)

Each level builds on previous, no linguistic assumptions.
```

---

## Implementation Considerations

### Data Structures

```python
# Character-level index
CharIndex = Dict[int, List[Tuple[doc_id, position]]]
# char_code → [(doc₁, pos₁), (doc₂, pos₂), ...]

# N-gram index
NGramIndex = Dict[str, List[Tuple[doc_id, position]]]
# ngram_string → [(doc₁, pos₁), (doc₂, pos₂), ...]

# Co-occurrence graph
CooccurrenceGraph = Dict[str, Dict[str, Tuple[int, float]]]
# ngram₁ → {ngram₂: (count, avg_distance)}
```

### Algorithms

```python
# Build n-gram index
def build_ngram_index(documents, n=3):
    index = defaultdict(list)
    for doc_id, doc in enumerate(documents):
        for i in range(len(doc) - n + 1):
            ngram = doc[i:i+n]
            index[ngram].append((doc_id, i))
    return index

# Find co-occurrences
def find_cooccurrences(index, window=5):
    graph = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    for ngram, positions in index.items():
        for doc_id, pos in positions:
            # Find n-grams within window
            for other_ngram, other_positions in index.items():
                for other_doc_id, other_pos in other_positions:
                    if doc_id == other_doc_id and abs(pos - other_pos) <= window:
                        graph[ngram][other_ngram][0] += 1
                        graph[ngram][other_ngram][1] += abs(pos - other_pos)
    return graph

# BFS for associations
def find_associations(graph, start_ngram, max_degrees=3):
    visited = {start_ngram}
    queue = deque([(start_ngram, 0, [start_ngram])])
    associations = []
    
    while queue:
        ngram, degree, path = queue.popleft()
        if degree >= max_degrees:
            continue
        for neighbor, (count, total_dist) in graph[ngram].items():
            if neighbor not in visited:
                visited.add(neighbor)
                avg_dist = total_dist / count
                associations.append((neighbor, degree + 1, path + [neighbor], count, avg_dist))
                queue.append((neighbor, degree + 1, path + [neighbor]))
    
    return associations
```

---

## Key Insights

### 1. Characters are Universal

All text, regardless of language, reduces to:
- Character codes (integers)
- Positions (integers)
- Order (mathematical relation)

### 2. "Word" is Optional

We don't need linguistic "words" — n-grams serve the same purpose:
- "proxy" = 5-gram
- "Hello" = 5-gram
- "代理" = 6 bytes (3-grams: "代", "理" in UTF-8)

### 3. Co-occurrence is Position-Based

Two patterns co-occur if their positions are close:
- No semantic understanding needed
- Pure integer comparison: |pos₁ - pos₂| ≤ window

### 4. Graph Traversal Finds Associations

BFS on co-occurrence graph:
- 1°: Direct neighbors (same word or adjacent n-grams)
- 2°: Neighbors of neighbors (co-occur in same context)
- 3°+: Distant associations (bridge concepts)

---

## Next Steps

1. **Implement Level 0-1** — Character and n-gram indexing
2. **Implement Level 2** — Co-occurrence graph construction
3. **Implement Level 3** — Query processing with BFS
4. **Test on multilingual corpus** — Verify language independence

---

**Status**: Foundational design complete, ready for implementation  
**Next**: Implement character-level indexing (no linguistic assumptions)  
**Philosophy**: Pure mathematics (sets, sequences, graphs) over linguistics
