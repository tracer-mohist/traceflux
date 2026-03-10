# Usage Guide

Purpose: Complete command reference for traceflux.

REFERENCE: README.md (quick start)
REFERENCE: docs/PHILOSOPHY.md (design principles)

---

## Commands

### search

Find text patterns in files.

```bash
traceflux search "pattern" <path> [options]
```

Options:
- --limit N: Limit results (default: 20)
- --json: JSON output
- --explain: Show association paths

Examples:

```bash
# Basic search
traceflux search "def " src/

# With limit
traceflux search "import " src/ --limit 5

# JSON output
traceflux search "proxy" src/ --json | jq '.results[]'
```

---

### associations

Find related concepts.

```bash
traceflux associations "<term>" <path> [options]
```

Options:
- --hops N: Association depth (1-3, default: 2)
- --limit N: Limit results (default: 20)
- --json: JSON output
- --explain: Show how associations are found

Examples:

```bash
# Find associations
traceflux associations "PageRank" src/

# Multi-hop
traceflux associations "proxy" src/ --hops 2

# With explanations
traceflux associations "pattern" src/ --explain

# JSON pipeline
traceflux associations "proxy" src/ --json | jq '.associations[:5]'
```

---

### patterns

List discovered patterns.

```bash
traceflux patterns <path> [options]
```

Options:
- --min-length N: Minimum pattern length (default: 3)
- --limit N: Limit results (default: 20)
- --json: JSON output

Examples:

```bash
# List patterns
traceflux patterns src/

# Longer patterns
traceflux patterns src/ --min-length 8

# Top 30 patterns
traceflux patterns src/ --limit 30
```

---

### index

Build persistent index.

```bash
traceflux index <path> -o <output.json>
```

Example:

```bash
traceflux index src/ -o index.json
```

---

## Output Formats

### Human-Readable (Default)

```
Associations for 'proxy' (hops=2):
  proxychains              strength: 0.85 (degree 1)
  HTTP_PROXY               strength: 0.72 (degree 1)
  git config               strength: 0.65 (degree 2)
```

### JSON (Machine-Readable)

```bash
traceflux associations "proxy" src/ --json
```

```json
{
  "associations": [
    {"term": "proxychains", "strength": 0.85, "degree": 1},
    {"term": "HTTP_PROXY", "strength": 0.72, "degree": 1}
  ]
}
```

### With Explanations

```bash
traceflux associations "proxy" src/ --explain
```

```
proxy -> pagerank -> rank
  proxy co-occurs with pagerank (strength: 0.90)
  pagerank co-occurs with rank (strength: 0.85)
```

---

## Best Practices

### Getting Better Associations

traceflux detects repeated patterns, not dictionary words.

For better results:

```bash
# Default (may find fragments)
traceflux patterns src/

# Better (longer patterns)
traceflux patterns src/ --min-length 8

# Best (filter by frequency)
traceflux patterns src/ --min-length 6 --limit 20
```

### Design Trade-offs

Tokenization: None (language-independent). Patterns may be fragments.

Dictionary: None (works out-of-box). Tune min-length for your corpus.

ML/Embeddings: None (lightweight). No semantic understanding.

Benefits: Works on any language, no training, fast.

---

## Typical Workflows

### Explore Codebase

```bash
# 1. List patterns
traceflux patterns src/ --min-length 8 --limit 20

# 2. Find associations
traceflux associations "PageRank" src/ --hops 2

# 3. Search and refine
traceflux search "proxy" src/ | grep -v test
```

### Pipeline Exploration

```bash
traceflux associations "pattern" src/ --json | \
  jq -r '.associations[:5][].term' | \
  xargs -I {} traceflux search {} src/ --limit 3
```

### UNIX Pipes

```bash
# Pipe from cat
cat file.py | traceflux search "def " -

# Pipe to grep
traceflux associations "proxy" src/ | grep HTTP

# Pipe to jq
traceflux associations "proxy" src/ --json | jq '.associations[]'
```

---

## Related Documents

- README.md — Quick start
- docs/PHILOSOPHY.md — Design principles
- docs/GETTING_STARTED.md — First-time setup

---

Last Updated: 2026-03-10
