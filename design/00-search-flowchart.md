# traceflux Search Flowchart (List Format)

**Purpose**: Visualize search process from document to user.

**Format**: Hierarchical list (easier to read than ASCII art).

---

## Level 0: Document Library

**Input**: Collection of documents

**Structure**:
- Document 1
  - Character sequence: [(char₀, pos₀), (char₁, pos₁), ...]
- Document 2
  - Character sequence: [(char₀, pos₀), (char₁, pos₁), ...]
- Document N
  - Character sequence: [(char₀, pos₀), (char₁, pos₁), ...]

**Output**: Raw text data (UTF-8 encoded)

---

## Level 1: Character Extraction

**Purpose**: Convert documents to mathematical representation.

**Process**:
- For each document:
  - Read as byte sequence (UTF-8)
  - Convert to (char_code, position) pairs
  - Store in index

**Example**:
```
Document: "Hello"

Output:
  - ('H', 0)
  - ('e', 1)
  - ('l', 2)
  - ('l', 3)
  - ('o', 4)
```

**Output**: Character index
```
CharIndex = {
  0x48 ('H'): [(doc₁, 0), (doc₅, 23), ...],
  0x65 ('e'): [(doc₁, 1), (doc₂, 5), ...],
  ...
}
```

---

## Level 2: N-gram Abstraction

**Purpose**: Create patterns from character sequences.

**Process**:
- For each character sequence:
  - Extract n-grams (n=2,3,4,5)
  - Record positions for each n-gram
  - Build inverted index: n-gram → [positions]

**Example**:
```
Document: "Hello"

2-grams (bigrams):
  - "He" → [(doc₁, 0)]
  - "el" → [(doc₁, 1)]
  - "ll" → [(doc₁, 2)]
  - "lo" → [(doc₁, 3)]

3-grams (trigrams):
  - "Hel" → [(doc₁, 0)]
  - "ell" → [(doc₁, 1)]
  - "llo" → [(doc₁, 2)]
```

**Output**: N-gram index
```
NGramIndex = {
  "pro": [(doc₁, 10), (doc₁, 245), (doc₂, 892)],
  "ro":  [(doc₁, 11), (doc₁, 246), (doc₂, 893)],
  "xy":  [(doc₁, 13), (doc₁, 248), (doc₂, 895)],
  ...
}
```

---

## Level 3: Co-occurrence Analysis

**Purpose**: Find relationships between n-grams.

**Process**:
- For each n-gram pair (G₁, G₂):
  - Find positions where both appear
  - Calculate distance: |pos₁ - pos₂|
  - If distance ≤ window_size (e.g., 5):
    - Record co-occurrence
  - Build co-occurrence graph

**Example**:
```
N-gram "pro" at positions: [10, 245, 892]
N-gram "xy" at positions: [13, 248, 895]

Co-occurrences (window=5):
  - Position 10 and 13: distance=3 ✓
  - Position 245 and 248: distance=3 ✓
  - Position 892 and 895: distance=3 ✓

Result:
  "pro" ↔ "xy" (strength: 3 co-occurrences, avg_distance: 3)
```

**Output**: Co-occurrence graph
```
CooccurrenceGraph = {
  "pro": {
    "xy": (count=3, avg_dist=3.0),
    "config": (count=2, avg_dist=4.5),
    "git": (count=2, avg_dist=2.0),
  },
  "xy": {
    "pro": (count=3, avg_dist=3.0),
    ...
  },
  ...
}
```

---

## Level 4: User Query Processing

**Purpose**: Find associations for user's query.

**Input**: User query string (e.g., "proxy")

**Process**:

### Step 1: Convert query to n-grams
```
Query: "proxy"

N-grams:
  - 2-grams: ["pr", "ro", "ox", "xy"]
  - 3-grams: ["prox", "roxy"]
  - 4-grams: ["proxy"]
```

### Step 2: Find exact matches in index
```
"pro" → [doc₁:10, doc₁:245, doc₂:892]
"xy"  → [doc₁:13, doc₁:248, doc₂:895]
```

### Step 3: Traverse co-occurrence graph (BFS, max_degrees=3)
```
Start: "pro"

1° associations (direct):
  - "xy" (same word, co-occur at distance 3)
  - "ro" (adjacent n-gram)
  - "ox" (adjacent n-gram)

2° associations (friend's friend):
  - "config" (co-occur with "pro" in doc₁)
  - "git" (co-occur with "pro" in doc₁)
  - "environment" (co-occur with "config")

3° associations (distant):
  - "security" (co-occur with "config")
  - "authentication" (co-occur with "security")
  - "firewall" (co-occur with "security")
```

### Step 4: Format output
```
For each association, include:
  - N-gram (the related term)
  - Degree (1°, 2°, 3°)
  - Path (how connected: "pro" → "config" → "security")
  - Co-occurrence count (strength)
  - Average distance (closeness)
  - Document locations (where found)
```

**Output**: List of associations (NO judgment on relevance)
```
Associations for "proxy":
  1°:
    - "xy" (path: ["pro", "xy"], count=3, avg_dist=3.0)
    - "config" (path: ["pro", "config"], count=2, avg_dist=4.5)
  
  2°:
    - "git" (path: ["pro", "git"], count=2, avg_dist=2.0)
    - "environment" (path: ["pro", "config", "environment"], count=1, avg_dist=5.0)
  
  3°:
    - "security" (path: ["pro", "config", "security"], count=1, avg_dist=6.0)
    - "authentication" (path: ["pro", "config", "security", "authentication"], count=1, avg_dist=7.0)
```

---

## Level 5: User / Agent

**Purpose**: Judge relevance and act.

**Input**: List of associations with metadata

**Process**:
- Review associations
- Judge relevance based on current task/context
- Select useful associations
- Ignore irrelevant ones

**Example**:
```
User Task: "Debug proxy configuration issue"

Associations received:
  1°: proxychains, git, config
  2°: SSH, environment variables
  3°: security, authentication

User Judgment:
  ✅ Use: proxychains, git, config, environment variables
  ❌ Skip: SSH, security, authentication (not relevant for this task)

User Action:
  - Check proxychains configuration
  - Review git proxy settings
  - Inspect environment variables
```

**Output**: User takes action based on selected associations

---

## Complete Flow Summary

```
1. Document Library
   ↓ (character extraction)
2. Character Index
   ↓ (n-gram abstraction)
3. N-gram Index
   ↓ (co-occurrence analysis)
4. Co-occurrence Graph
   ↓ (query processing + BFS)
5. Associations List
   ↓ (user judgment)
6. User Action
```

---

## Key Properties

### Separation of Concerns

- **Level 0-4**: Engine (objective, no judgment)
- **Level 5**: User/Agent (subjective, judges relevance)

### Language Independence

- All levels operate on character codes and positions
- No linguistic assumptions (what is a "word"?)
- Works for English, Chinese, Arabic, etc.

### Mathematical Foundation

- Level 1: Set theory (ordered pairs)
- Level 2: Sequence theory (n-grams)
- Level 3: Graph theory (co-occurrence graph)
- Level 4: Graph traversal (BFS)
- Level 5: User decision (outside scope)

### No Hidden Judgment

- Engine provides ALL associations (up to max_degrees)
- No filtering by "seems irrelevant"
- User sees everything, decides what's useful

---

## Implementation Checklist

- [ ] Level 1: Character extraction
- [ ] Level 2: N-gram indexing
- [ ] Level 3: Co-occurrence graph construction
- [ ] Level 4: Query processing (BFS)
- [ ] Level 5: Output formatting (no judgment)

**User/Agent responsibility**: Level 5 judgment (not implemented in engine)

---

**Status**: Flowchart complete in list format  
**Next**: Implement Level 1-2 (character and n-gram indexing)
