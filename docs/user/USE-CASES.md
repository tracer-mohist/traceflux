# Use Cases

Purpose: Real-world examples of using traceflux.

REFERENCE: docs/USAGE.md (command reference)

---

## Code Exploration

### Scenario

You join a new project. You see "PageRank" mentioned. You want to understand how it is implemented.

### Workflow

```bash
# 1. Find related concepts
traceflux associations "PageRank" src/ --hops 2

# Output:
#   pagerank.py              strength: 0.95
#   graph.py                 strength: 0.88
#   cooccurrence             strength: 0.75

# 2. Search in discovered files
traceflux search "class" src/pagerank.py

# 3. Explore further
traceflux associations "graph" src/ --hops 2
```text

### Result

You discover: pagerank.py, graph.py, cooccurrence.py -- the core modules.

---

## Documentation Navigation

### Scenario

You need to configure proxy settings. You find "proxy" mentioned. You want to know all related configurations.

### Workflow

```bash
# Find proxy-related concepts
traceflux associations "proxy" docs/ --hops 2

# Output:
#   proxychains              strength: 0.85
#   HTTP_PROXY               strength: 0.72
#   SSL                      strength: 0.65
#   git config               strength: 0.58

# Search for specific config
traceflux search "HTTP_PROXY" docs/
```text

### Result

You discover: proxychains config, environment variables, SSL settings, git proxy config.

---

## Research Notes

### Scenario

You have research notes about cryptography. You want to find connections between concepts.

### Workflow

```bash
# Find connections to "nilpotent"
traceflux associations "nilpotent" notes/ --hops 2

# Output:
#   semiprime                strength: 0.78
#   RSA                      strength: 0.72
#   Euler                    strength: 0.65

# Follow the chain
traceflux associations "RSA" notes/ --hops 2
```text

### Result

You discover unexpected connections between mathematical concepts and cryptographic algorithms.

---

## Log Analysis

### Scenario

You have error logs. You want to find related error patterns.

### Workflow

```bash
# Find patterns in logs
traceflux patterns logs/ --min-length 5 --limit 20

# Find associations with "timeout"
traceflux associations "timeout" logs/ --hops 2

# Output:
#   connection reset         strength: 0.82
#   retry failed             strength: 0.75
#   upstream error           strength: 0.68
```text

### Result

You discover: timeout is often accompanied by connection reset and retry failures.

---

## Learning a Language

### Scenario

You are learning a programming language. You want to find common patterns.

### Workflow

```bash
# Find common Python patterns
traceflux patterns src/ --min-length 8 --limit 30

# Output:
#   def test_                strength: 0.95
#   assertEqual              strength: 0.88
#   __init__                 strength: 0.85

# Find associations with "class"
traceflux associations "class" src/ --hops 1
```text

### Result

You discover: common testing patterns, class structure, method naming conventions.

---

## Related Documents

- docs/USAGE.md -- Command reference
- docs/GETTING_STARTED.md -- Quick start
- README.md -- Project overview

---

Last Updated: 2026-03-10
