# Search vs Judgment

**Purpose**: Separation of concerns — search provides associations, user provides judgment.

**NOTE**: Consolidated from research/03-philosophy/ (2026-03-11)

---

## Core Insight

**TraceFlux is a text search engine, not a meaning judge.**

### Responsibility Separation

```text
TraceFlux: Provide associations (what's related)
User/Agent: Judge relevance (what's meaningful)
```

### Human Cognition Analogy

```text
Human Mind:
  - Brain: Generates associations
  - Will/Volition: Decides what to express

TraceFlux:
  - Engine: Extracts associations (multi-hop connections)
  - User/Agent: Judges relevance (selects useful ones)

> 浮想联翩 (mind wandering)
> 意志判断 (intentional expression)
```

---

## Design Principle

### What TraceFlux Should Do

1. **Extract** co-occurrences — Words appearing together
2. **Compute** degrees — 1 degree, 2 degree, 3 degree associations
3. **Show** paths — How terms are connected
4. **Present** options — Here are related terms

### What TraceFlux Should NOT Do

1. **Judge** intent — "Is this what user meant?"
2. **Filter** by meaning — "This seems irrelevant"
3. **Assume** purpose — "User probably wants..."
4. **Hide** "noise" — "This might be too distant"

---

## Human Cognition Model

### Two-Stage Process

```text
Stage 1: Association Generation (Unconscious)
  - Free floating ideas
  - Distant connections
  - Seemingly random jumps

Stage 2: Expression Selection (Conscious)
  - Will/volition judges
  - Selects appropriate ideas
  - Filters for context

> 浮想联翩 (mind wandering)
> 意志判断 (intentional expression)
```

**Key Insight**: Stage 1 is messy, creative, noisy. Stage 2 is focused, intentional, filtered.

**TraceFlux Role**: Be Stage 1 (association generator), not Stage 2 (meaning judge).

---

## Implementation Implications

### Correct Design

```python
def find_associations(graph, start_word, max_degrees=3):
    """
    Find all words within max_degrees.
    Returns: All associations with degree and path.
    No judgment about relevance or meaning.
    """
    # BFS to find all connections
    # Return everything found
    # Don't filter by "seems irrelevant"
```

### Correct Output Format

```text
Search: "proxy"

Associations (no judgment):
  1st degree: configuration, git, settings, proxychains
  2nd degree: SSH, security, firewall, tunnel
  3rd degree: authentication, key, rules, port

All shown — user decides what's relevant!
```

### Wrong Design (Don't Do This)

```python
def find_associations_WRONG(graph, start_word):
    """
    WRONG: Judge relevance inside search engine.
    """
    associations = bfs_search(graph, start_word)

    # DON'T: Filter by "seems irrelevant"
    associations = [a for a in associations if is_relevant(a)]

    # DON'T: Assume user intent
    if user_type == "developer":
        associations = filter_technical(associations)

    return associations  # Over-filtered!
```

---

## Why This Separation Matters

### 1. Respects User Autonomy

```text
User knows their intent, not the system.

System filters → User sees limited options → May miss what they need
System presents all → User chooses → Finds what they need
```

### 2. Enables Creative Discovery

```text
Distant associations (3rd degree) may seem irrelevant but:
  - Spark new ideas
  - Reveal hidden connections
  - Enable analogical thinking

Filtering kills creativity!
```

### 3. Reduces System Complexity

```text
Search engine: Simple, focused (extract associations)
User/Agent: Complex, contextual (judge relevance)

Separation of concerns = cleaner design
```

### 4. Avoids Bias

```text
System filtering = System bias

What system deems "irrelevant" may be exactly what user needs.
Don't impose system's judgment on user!
```

---

## Connection to Prompt Engineering

### Six Principles Alignment

```text
1. English ASCII — Compatibility
2. Simple English — Clarity
3. Lists over tables — Efficiency
4. No asterisk conflict — Stability
5. No negative sentences — Choice clarity
6. No emoji in content — Consistency

All principles serve: Make associations clear, let user judge.
```

### Design Mantra

```text
"Search provides options, user provides judgment."

Repeat this when designing features:
  - Should we filter this? NO — user judges.
  - Should we rank by relevance? NO — show all paths.
  - Should we hide "noise"? NO — noise is signal for someone.
```

---

## Implementation Checklist

### Do

- [ ] Extract all co-occurrences
- [ ] Compute multi-degree paths
- [ ] Show all associations with degree labels
- [ ] Provide path visualization
- [ ] Let user filter/sort/choose

### Don't

- [ ] Filter by "seems irrelevant"
- [ ] Assume user intent
- [ ] Hide distant associations
- [ ] Rank by "predicted relevance"
- [ ] Make judgment for user

---

## Related

- [Divergent Search](../algorithms/divergent-search.md) - Application of this principle
- [Multi-Hop Noise](./multi-hop-noise.md) - Understanding noise in associations
- [Six Degrees](../associations/six-degrees.md) - Multi-hop algorithm

---

**Last Updated**: 2026-03-11
**Source Files**: `2026-03-06_search-vs-judgment*.md`
