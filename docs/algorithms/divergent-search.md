# Divergent Search

**Purpose**: Show diverse associations instead of predictive autocomplete.

**NOTE**: Consolidated from research/01-foundations/ (2026-03-11)

---

## Core Insight

**Predictive autocomplete is wrong** — we cannot predict the future. Users input keywords, but we cannot determine what they actually want. Showing only the most frequent results leads to flattening and errors.

---

## The Problem with Predictive Autocomplete

### Traditional Assumption

```text
Assumption: There is a "most likely" completion

User types: "proxy"
System predicts: "proxy configuration" (most frequent)
Shows: ["proxy configuration", "proxy settings", "proxy server"]

Problem: Assumes we know what user wants!
```

### Why This Is Wrong

**Problem 1: We Cannot Predict Intent**

```text
User types: "proxy"

Possible intents:
  A: "proxy configuration" (want to configure)
  B: "proxy git" (want git proxy info)
  C: "proxy SSH tunnel" (want SSH tunneling)
  D: "proxy authentication" (want auth info)
  E: "proxy firewall rules" (want firewall config)

We don't know which! Predicting "A" assumes too much.
```

**Problem 2: High Frequency ≠ Relevant**

```text
"proxy configuration" appears 1000 times (high freq)
"proxy SSH tunnel" appears 50 times (low freq)

But: User wants SSH tunnel info!
Showing only high-freq = wrong result
```

**Problem 3: Flattening Effect**

```text
All users see same top-N completions:
  ["proxy configuration", "proxy settings", "proxy server"]

Result: Everyone follows same path
Diverse intents → Same results

This is "flattening" — diversity lost!
```

**Problem 4: Not How Humans Think**

```text
Human thinking is DIVERGENT, not CONVERGENT:

When human thinks "proxy", mind associates:
  - configuration
  - git
  - SSH
  - authentication
  - firewall
  - settings
  - tunnel
  - ... (many branches)

NOT just: "configuration" (most frequent)

Predictive autocomplete is convergent (narrows down)
Human thinking is divergent (expands out)
```

---

## Better Approach: Divergent Association Display

### Core Principle

```text
Don't predict "most likely" — show "possibility space"!

User types: "proxy"

Show diverse associations:
  ├── configuration (freq: high)
  ├── git (freq: medium)
  ├── SSH (freq: medium)
  ├── authentication (freq: low)
  ├── firewall (freq: low)
  ├── settings (freq: high)
  └── tunnel (freq: medium)

User chooses their own path!
```

### Benefits

```text
1. Respects user intent
   - User chooses, not system

2. Preserves diversity
   - Multiple paths visible
   - Rare but relevant options shown

3. Matches human cognition
   - Divergent thinking supported
   - Associations, not predictions

4. Reduces errors
   - No wrong predictions
   - User always in control
```

---

## Implementation

### Association Graph

```text
Build a graph of associations:
  - Nodes: patterns/concepts
  - Edges: co-occurrence relationships
  - Weight: frequency of co-occurrence

Example:
  "proxy" —(1000)—> "configuration"
  "proxy" —(500)—> "git"
  "proxy" —(300)—> "SSH"
  "proxy" —(100)—> "authentication"
  "proxy" —(50)—> "firewall"
```

### Divergent Query Algorithm

```python
def divergent_search(query, graph, top_k=10, diversity=0.5):
    """
    Get diverse associations for query.
    
    Args:
        query: User's input
        graph: Association graph {node: {neighbor: weight}}
        top_k: Number of results
        diversity: 0.0 = pure frequency, 1.0 = pure diversity
    
    Returns: List of (association, score) tuples
    """
    # Get direct neighbors
    neighbors = graph.get(query, {})
    
    if not neighbors:
        return []
    
    # Score by frequency
    freq_scores = {
        node: weight / max(neighbors.values())
        for node, weight in neighbors.items()
    }
    
    # Score by diversity (dissimilarity to already-selected)
    selected = []
    diversity_scores = {}
    
    for node in neighbors:
        if not selected:
            diversity_scores[node] = 1.0
        else:
            # How different is this from already-selected?
            avg_sim = sum(
                ngram_similarity(node, s)
                for s in selected
            ) / len(selected)
            diversity_scores[node] = 1.0 - avg_sim
    
    # Combine scores
    final_scores = {
        node: (1 - diversity) * freq_scores[node] + 
              diversity * diversity_scores[node]
        for node in neighbors
    }
    
    # Sort and return top-k
    results = sorted(final_scores.items(), key=lambda x: -x[1])[:top_k]
    
    return results
```

### Example Output

```text
Query: "proxy"

Divergent results (diversity=0.5):
  1. configuration (score: 0.85, freq: high)
  2. git (score: 0.72, freq: medium)
  3. SSH (score: 0.68, freq: medium)
  4. settings (score: 0.65, freq: high)
  5. authentication (score: 0.55, freq: low)
  6. firewall (score: 0.48, freq: low)
  7. tunnel (score: 0.45, freq: medium)
  8. rules (score: 0.42, freq: low)
  9. server (score: 0.40, freq: high)
  10. port (score: 0.38, freq: medium)

Note: Mix of high-freq and low-freq, diverse topics!
```

---

## Six Degrees Integration

### Multi-Hop Associations

```text
Direct associations (1-hop):
  "proxy" → "configuration", "git", "SSH"

2-hop associations:
  "proxy" → "git" → "push", "commit", "branch"
  "proxy" → "SSH" → "tunnel", "key", "authentication"

3-hop associations:
  "proxy" → "SSH" → "tunnel" → "port forwarding"

Show associations at multiple distances!
```

### Distance Weighting

```text
Score decay by distance:
  score(node, distance) = base_score / distance

1-hop: full score
2-hop: 50% score
3-hop: 33% score

This ensures distant associations are visible but not dominant.
```

---

## UI Design

### Visual Layout

```text
User types: "proxy"

Associations (radial layout):

              git
            /     \
    configuration — proxy — SSH
            \     /
          settings

Click any node to expand further!
```

### Interaction

```text
1. User types keyword
2. System shows diverse associations (radial or list)
3. User clicks an association
4. System expands from that node (more associations)
5. User navigates their own path

System never predicts — always shows possibilities!
```

---

## Comparison: Predictive vs Divergent

| Aspect | Predictive | Divergent |
|--------|------------|-----------|
| Goal | Guess intent | Show possibilities |
| Results | Top-N frequent | Diverse associations |
| User role | Passive (accepts prediction) | Active (chooses path) |
| Error mode | Wrong prediction | Overwhelming options |
| Cognition | Convergent | Divergent |
| Diversity | Low (flattening) | High (exploration) |

---

## Related

- [Autocomplete](./autocomplete.md) - Traditional LZW autocomplete
- [Six Degrees](../associations/six-degrees.md) - Multi-hop associations
- [Frequency Ranking](../core/frequency-ranking.md) - Scoring associations

---

**Last Updated**: 2026-03-11  
**Source Files**: `2026-03-06_divergent-associations*.md`
