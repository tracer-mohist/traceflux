### Right: Association Network

```text
User types: "proxy"

Display:

proxy (center)
  |
  +-- 1deg (direct):
  |     +-- configuration [rank: 0.3]
  |     +-- git [rank: 0.2]
  |     +-- SSH [rank: 0.15]
  |     +-- auth [rank: 0.12]
  |     +-- firewall [rank: 0.1]
  |
  +-- 2deg (via configuration):
  |     +-- settings
  |     +-- file
  |     +-- path
  |
  +-- 2deg (via git):
        +-- commit
        +-- push
        +-- tunnel

User CHOOSES which branch to explore!
```

### Interface Metaphor

```text
NOT: Search bar with dropdown (predictive)
BUT: Interactive graph / mind map (divergent)

OR: Faceted navigation
  "proxy" found!

  Related concepts:
    [configuration] [git] [SSH] [auth] [firewall]

  Click one to explore that branch.
```

---

## 5. Algorithm: Divergent Association Retrieval

### Input/Output

```text
Input:
  - Query q
  - Graph G = (V, E)
  - Max depth k (e.g., k=3)
  - Max results per level [n_1, n_2, n_3]

Output:
  - Set of associations with:
    - Pattern
    - Distance (1deg, 2deg, 3deg)
    - Importance (PageRank)
    - Branch (which path from q)
```

### Algorithm

```text
DivergentAssociations(q, G, k, [n_1, n_2, n_3]):
  results = []
  visited = {q}

  # BFS with diversity
  for depth in 1..k:
    candidates = []

    # Find all nodes at this depth
    for v in visited:
      for neighbor in neighbors(v):
        if neighbor not in visited:
          candidates.append(neighbor)

    # Select diverse subset (not just top by rank)
    selected = MaximalMarginalRelevance(
      candidates,
      k = n_depth,
      importance_weight = 0.7,
      diversity_weight = 0.3
    )

    for s in selected:
      results.append({
        pattern: s,
        distance: depth,
        rank: PageRank(s),
        branch: Path(q, s)
      })
      visited.add(s)

  return results
```

### Maximal Marginal Relevance (MMR)

```text
MMR selects diverse results:

selected = []
remaining = candidates

while len(selected) < k:
  best = argmax_{c in remaining} [
    λ * importance(c) - (1-λ) * max_{s in selected} similarity(c, s)
  ]
  selected.append(best)
  remaining.remove(best)

return selected

Intuition:
  - Pick important patterns
  - But avoid picking similar ones
  - Result: Diverse set covering different branches
```

---

## 6. Example: Divergent vs Convergent

### Convergent (Predictive Autocomplete) -- WRONG

```text
User: "proxy"

System (top 3 by frequency):
  1. "proxy configuration" (freq: 1000)
  2. "proxy settings" (freq: 800)
  3. "proxy server" (freq: 600)

Problem:
  - All from same branch (configuration-related)
  - User interested in "proxy SSH tunnel" sees nothing relevant
  - Flattening: all users see same 3 options
```

### Divergent (Association Display) -- CORRECT

```text
User: "proxy"

System (diverse associations):

1deg associations:
  - configuration [rank: 0.30, branch: config]
  - git [rank: 0.20, branch: git]
  - SSH [rank: 0.15, branch: SSH]
  - auth [rank: 0.12, branch: security]
  - firewall [rank: 0.10, branch: security]

2deg associations (via git):
  - tunnel [rank: 0.08, branch: git->SSH]
  - commit [rank: 0.05, branch: git]

2deg associations (via SSH):
  - key [rank: 0.07, branch: SSH]
  - tunnel [rank: 0.06, branch: SSH]

User sees: Multiple branches!
User interested in SSH tunnel:
  -> Clicks "SSH" branch
  -> Sees "tunnel" option
  -> Success!
```

---

## 7. Why This Matches Human Cognition

### Human Memory is Associative

```text
When human hears "proxy":
  Activates associated concepts in parallel:
    - configuration
    - git
    - SSH
    - auth
    - ...

NOT sequentially:
    - configuration (most likely)
    - (if not, try next)
    - ...

Divergent display matches this parallel activation!
```

### Human Thinking is Branching

```text
Human reasoning:
  "proxy" -> could mean configuration -> explore
  "proxy" -> could mean git -> explore
  "proxy" -> could mean SSH -> explore

Multiple hypotheses in parallel!

Predictive autocomplete forces single hypothesis.
Divergent display supports multiple hypotheses.
```
