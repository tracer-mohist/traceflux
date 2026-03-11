# traceflux Search Flowchart (List Format)

PURPOSE: Visualize search process from document to user.

FORMAT: Hierarchical list (easier to read than ASCII art).

---

## Level 0: Document Library

INPUT: Collection of documents

STRUCTURE:
- Document N: Character sequence [(char0, pos0), (char1, pos1), ...]

OUTPUT: Raw text data (UTF-8 encoded)

---

## Level 1: Character Extraction

PURPOSE: Convert documents to mathematical representation.

PROCESS:
- For each document: Read as UTF-8 byte sequence, convert to (char_code, position) pairs, store in index

EXAMPLE:
```text
Document: "Hello" -> [('H', 0), ('e', 1), ('l', 2), ('l', 3), ('o', 4)]
```

OUTPUT: Character index
```text
CharIndex = { 0x48 ('H'): [(doc1, 0), (doc5, 23), ...], 0x65 ('e'): [(doc1, 1), (doc2, 5), ...] }
```

---

## Level 2: N-gram Abstraction

PURPOSE: Create patterns from character sequences.

PROCESS:
- Extract n-grams (n=2,3,4,5), record positions, build inverted index: n-gram -> [positions]

EXAMPLE:
```text
Document: "Hello"
2-grams: "He"->[(doc1,0)], "el"->[(doc1,1)], "ll"->[(doc1,2)], "lo"->[(doc1,3)]
3-grams: "Hel"->[(doc1,0)], "ell"->[(doc1,1)], "llo"->[(doc1,2)]
```

OUTPUT: N-gram index
```text
NGramIndex = { "pro": [(doc1,10), (doc1,245), (doc2,892)], "ro": [(doc1,11), ...], "xy": [(doc1,13), ...] }
```

---

## Level 3: Co-occurrence Analysis

PURPOSE: Find relationships between n-grams.

PROCESS:
- For each n-gram pair (G1, G2): Find positions where both appear, calculate distance |pos1-pos2|, if distance <= window_size (e.g., 5) record co-occurrence, build co-occurrence graph

EXAMPLE:
```text
N-gram "pro" at [10, 245, 892], "xy" at [13, 248, 895]
Co-occurrences (window=5): 10-13 dist=3 [OK], 245-248 dist=3 [OK], 892-895 dist=3 [OK]
Result: "pro" <-> "xy" (strength: 3 co-occurrences, avg_distance: 3)
```

OUTPUT: Co-occurrence graph
```text
CooccurrenceGraph = { "pro": { "xy": (count=3, avg_dist=3.0), "config": (count=2, avg_dist=4.5) }, ... }
```

---

## Level 4: User Query Processing

PURPOSE: Find associations for user's query.

INPUT: User query string (e.g., "proxy")

PROCESS:

Step 1: Convert query to n-grams
```text
Query: "proxy" -> 2-grams: ["pr","ro","ox","xy"], 3-grams: ["prox","roxy"], 4-grams: ["proxy"]
```

Step 2: Find exact matches in index
```text
"pro" -> [doc1:10, doc1:245, doc2:892], "xy" -> [doc1:13, doc1:248, doc2:895]
```

Step 3: Traverse co-occurrence graph (BFS, max_degrees=3)
```text
Start: "pro"
1st: "xy" (same word), "ro"/"ox" (adjacent)
2nd: "config", "git", "environment" (co-occur with "pro")
3rd: "security", "authentication", "firewall" (distant)
```

Step 4: Format output
```text
For each: N-gram, Degree (1st/2nd/3rd), Path, Co-occurrence count, Avg distance, Document locations
```

OUTPUT: List of associations (NO judgment on relevance)
```text
Associations for "proxy":
  1st: "xy" (path:["pro","xy"], count=3, avg_dist=3.0), "config" (path:["pro","config"], count=2, avg_dist=4.5)
  2nd: "git" (path:["pro","git"], count=2, avg_dist=2.0), "environment" (path:["pro","config","environment"], count=1)
  3rd: "security" (path:["pro","config","security"], count=1), "authentication" (path:[...], count=1)
```

---

## Level 5: User / Agent

PURPOSE: Judge relevance and act.

INPUT: List of associations with metadata

PROCESS: Review associations, judge relevance based on context, select useful, ignore irrelevant

EXAMPLE:
```text
Task: "Debug proxy configuration issue"
Received: 1st: proxychains/git/config, 2nd: SSH/env vars, 3rd: security/auth
Judgment: [USE] proxychains/git/config/env, [SKIP] SSH/security/auth
Action: Check proxychains config, review git proxy settings, inspect env vars
```

OUTPUT: User takes action based on selected associations

---

## Complete Flow Summary

```text
1. Document Library -> 2. Character Index -> 3. N-gram Index -> 4. Co-occurrence Graph -> 5. Associations List -> 6. User Action
```

---

## Key Properties

Separation of Concerns:
- LEVEL 0-4: Engine (objective, no judgment)
- LEVEL 5: User/Agent (subjective, judges relevance)

Language Independence:
- All levels operate on character codes and positions
- No linguistic assumptions, works for English/Chinese/Arabic/etc.

Mathematical Foundation:
- Level 1: Set theory (ordered pairs)
- Level 2: Sequence theory (n-grams)
- Level 3: Graph theory (co-occurrence graph)
- Level 4: Graph traversal (BFS)
- Level 5: User decision (outside scope)

No Hidden Judgment:
- Engine provides ALL associations (up to max_degrees)
- User sees everything, decides what's useful

---

## Implementation Checklist

- [ ] Level 1: Character extraction
- [ ] Level 2: N-gram indexing
- [ ] Level 3: Co-occurrence graph construction
- [ ] Level 4: Query processing (BFS)
- [ ] Level 5: Output formatting (no judgment)

USER/AGENT RESPONSIBILITY: Level 5 judgment (not implemented in engine)

---

STATUS: Flowchart complete in list format
NEXT: Implement Level 1-2 (character and n-gram indexing)
