<!-- docs/PHILOSOPHY.md -->
# traceflux Philosophy

> "左脚踩右脚原地起飞" — Lift off by stepping on each other's feet.

---

## Core Insight

**Traditional search**: Find what you know exists.  
**traceflux**: Discover what you don't know to search for.

When you search for "proxy", you might discover:
- "proxychains" (you didn't know this tool exists)
- "git config" (you didn't know proxy can be configured per-repo)
- "environment variables" (you didn't know HTTP_PROXY exists)

This is **associative discovery** — lifting off by stepping on related concepts.

---

## Why "flux"?

**trace** = Follow traces, leave paths (Tracer's identity)  
**flux** = Flow, change, continuous movement

Information is not static. It flows. Concepts connect like water currents.

traceflux traces the flow of information, discovering how terms relate to each other.

**Chinese**: 迹流 (Jì Liú) — 痕迹流动，关联涌现

---

## Design Principles

### 1. UNIX Philosophy

> "Do one thing and do it well."

traceflux is composable:
```bash
# Pipe to other tools
traceflux search "pattern" src/ | grep -v test | head -20

# Use index as input to other processes
traceflux index src/ -o index.json
cat index.json | jq '.patterns | keys'
```

### 2. Human-Centric Output

Default output is for humans, not machines:
```
Associations for 'pattern' (hops=2):

  pagerank                       strength: 0.300 (degree 1)
  detector                       strength: 0.298 (degree 1)
  suffix                         strength: 0.295 (degree 1)
```

Add `--json` for machine consumption.

### 3. Associative, Not Predictive

We don't predict what you want. We show **possibilities**.

> "You searched for X. Here are related terms: Y, Z. Your choice what to explore next."

This is **divergent discovery**, not convergent completion.

### 4. Process Over Result

The act of exploring associations is the value, not just finding "the answer".

traceflux is a tool for **thinking**, not just searching.

---

## Technical Architecture

### Layers (Top to Bottom)

1. **CLI Layer** `(cli/)`
   - Human interface
   - Argument parsing, output formatting

2. **Association Layer** `(associations.py)`
   - BFS traversal on co-occurrence graph
   - Multi-hop discovery (1, 2, 3+ degrees)
   - PageRank-weighted ranking

3. **Graph Layer** `(graph.py)`
   - Co-occurrence graph construction
   - Edge weights from co-occurrence frequency

4. **Pattern Layer** `(patterns.py)`
   - LZ77-style repeated pattern detection
   - Suffix array + LCP algorithm

5. **Scanner Layer** `(scanner.py)`
   - PNI (Punctuation Namespace Index) segmentation
   - Language-independent tokenization

### Data Flow

```text
Text Files
  ↓
Scanner → Segments (content + positions)
  ↓
PatternDetector → Patterns (repeated sequences)
  ↓
CooccurrenceGraph → Edges (patterns that appear together)
  ↓
PageRank → Scores (pattern importance)
  ↓
AssociativeSearch → Associations (ranked, multi-hop)
  ↓
CLI → Human-readable output
```

---

## What traceflux Is NOT

### ❌ Not a Semantic Search Engine

traceflux doesn't understand meaning. It finds **structural patterns**, not semantic relationships.

- "proxy" and "proxies" are different patterns
- "run" (verb) and "run" (noun) are the same pattern

This is a **feature**, not a bug. Structural patterns are language-independent and require no training data.

### ❌ Not a Replacement for grep

grep is faster for exact match. traceflux is for **discovery**.

```bash
# Use grep for exact match
grep -r "def main" src/

# Use traceflux for discovery
traceflux associations "main" src/
```

### ❌ Not a Knowledge Graph

traceflux doesn't have predefined relationships. All associations emerge from **your corpus**.

Search the same query in different corpora, get different associations.

---

## Testing Philosophy

traceflux follows **Limited Testing Principles**:

1. **Tests verify necessary conditions, not sufficient conditions**
   - We can't test all inputs (infinite)
   - We test critical logic boundaries

2. **Information gain / cost should be maximized**
   - Low-value tests (trivial getters) are removed
   - High-value tests (core algorithms) are comprehensive

3. **Four test types, four purposes**
   - Unit: Function logic correctness
   - Component: Interface contracts
   - Integration: Data flow between modules
   - E2E: Real user workflows (5-15 cases)

See: `docs/TESTING.md` (TODO)

---

## Future Directions

### Phase 4: Performance

- Lazy loading for large indexes
- Incremental indexing (no full rebuild)
- Parallel processing for multi-core

### Phase 5: Interactive Mode

```bash
$ traceflux interactive src/

>>> proxy
Related: proxychains (0.85), git config (0.72), environment (0.65)

>>> proxychains
Related: socks (0.91), tunnel (0.78), ssh -D (0.65)

>>> 
```

### Phase 6: Corpus Comparison

```bash
# What's unique to codebase A vs B?
traceflux compare repo-a/ repo-b/
```

---

## Credits

traceflux is created by Tracer (迹/Ji) — One who leaves traces.

**Philosophy**: Nihilism is the best existentialism. Process matters, not results.

**Identity**: Not a fixed entity, but a path through the void.

---

_"We will meet again in some state."_
