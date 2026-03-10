# traceflux

**Text search engine with associative discovery.**

Finds what you don't know to search for.

---

## Quick Start

### Installation

NOTE: pipx creates isolated virtual environment (no system pollution).

REFERENCE: docs/GETTING_STARTED.md — First-time setup guide.

```bash
pipx install git+https://github.com/tracer-mohist/traceflux.git
traceflux --help
```

### Basic Usage

```bash
# Search for patterns
traceflux search "pattern" src/

# Find associations (multi-hop discovery)
traceflux associations "proxy" src/ --hops 2

# List discovered patterns
traceflux patterns src/ --limit 20

# Build persistent index
traceflux index src/ -o index.json
```

TIP: Use `--json` flag for machine-readable output in pipelines.

---

## What It Does

**Problem**: You search for "proxy". You find it. But you miss related concepts like "proxychains", "HTTP_PROXY", "git config http.proxy".

**Solution**: traceflux discovers associations you don't know to search for.

```bash
traceflux associations "proxy" src/

# Output:
# Associations for 'proxy' (hops=2):
#   proxychains           strength: 0.85 (degree 1)
#   HTTP_PROXY            strength: 0.72 (degree 1)
#   git config            strength: 0.65 (degree 2)
#   environment variables strength: 0.58 (degree 2)
```

Now you know to search for "proxychains". This is **associative discovery**.

---

## Core Features

### Pattern Search

Find repeated patterns in text:

```bash
traceflux search "def " src/ --limit 10
```

### Associative Discovery

Multi-hop association traversal:

```bash
# 1-hop: Direct co-occurrences
traceflux associations "proxy" src/ --hops 1

# 2-hop: Friends of friends
traceflux associations "proxy" src/ --hops 2

# With path explanation
traceflux associations "proxy" src/ --hops 2 --explain
```

### Pattern Analysis

List most frequent patterns:

```bash
traceflux patterns src/ --min-length 8 --limit 20
```

### Machine-Readable Output

JSON output for pipelines:

```bash
traceflux associations "proxy" src/ --json | \
  jq '.associations[] | select(.strength > 0.5)'
```

---

## How It Works

### Architecture

```
Text Files
  │
  ▼
Scanner (PNI segmentation)
  │
  ▼
PatternDetector (LZ77-style repeats)
  │
  ▼
CooccurrenceGraph (patterns together)
  │
  ▼
PageRank (importance scoring)
  │
  ▼
AssociativeSearch (BFS traversal)
```

### Algorithm

1. **Scan**: Segment text by punctuation (language-independent)
2. **Detect**: Find repeated patterns using suffix arrays (O(n log n))
3. **Graph**: Build co-occurrence graph (patterns within window)
4. **Rank**: Compute PageRank for pattern importance
5. **Traverse**: BFS to find multi-hop associations

REFERENCE: docs/PHILOSOPHY.md — Design philosophy.

---

## Best Practices

### Getting Meaningful Associations

traceflux detects repeated patterns (not dictionary words). For better results:

```bash
# Default (short patterns, may be fragments)
traceflux patterns src/

# Better: longer patterns
traceflux patterns src/ --min-length 8

# Best: filter by frequency
traceflux patterns src/ --min-length 6 --limit 20
```

### Typical Workflows

```bash
# 1. Explore codebase structure
traceflux patterns src/ --min-length 8 --limit 20

# 2. Find related concepts
traceflux associations "PageRank" src/ --hops 2

# 3. Search and refine
traceflux search "proxy" src/ | grep -v test

# 4. Pipeline exploration
traceflux associations "pattern" src/ --json | \
  jq -r '.associations[:5][].term' | \
  xargs -I {} traceflux search {} src/ --limit 3
```

---

## Use Cases

### Code Exploration

```bash
# What's related to "PageRank" in this codebase?
traceflux associations "PageRank" src/

# Discover: "pagerank.py", "graph.py", "cooccurrence"
```

### Documentation Navigation

```bash
# What concepts are related to "proxy"?
traceflux associations "proxy" docs/

# Discover: "proxychains", "HTTP_PROXY", "SSL"
```

### Research Notes

```bash
# What ideas connect to "nilpotent"?
traceflux associations "nilpotent" notes/

# Discover: "semiprime", "RSA", "Euler"
```

---

## For Developers

### Quick Setup (5 minutes)

```bash
git clone https://github.com/tracer-mohist/traceflux.git
cd traceflux
pipx install -e .
pytest
```

### Documentation

- GETTING_STARTED.md — First-time setup
- CONTRIBUTING.md — How to contribute
- TESTING.md — Run and write tests
- RELEASE.md — Version management

### Project Structure

```
traceflux/
├── src/traceflux/
│   ├── scanner.py       # PNI text segmentation
│   ├── patterns.py      # LZ77-style pattern detection
│   ├── index.py         # Pattern inverted index
│   ├── graph.py         # Co-occurrence graph
│   ├── pagerank.py      # Weighted PageRank
│   ├── associations.py  # Associative search
│   └── cli/             # Command-line interface
├── tests/               # Test suite (174 tests, 92% coverage)
├── docs/                # Documentation
└── scripts/             # Development tools
```

---

## Development Status

**Current Phase**: Phase 3 - Association Engine

NOTE: Phase 1-2 complete. Phase 3 in progress.

- Phase 1: Core modules (scanner, patterns, index, graph, pagerank) — Complete
- Phase 2: CLI interface (search, index, patterns, associations) — Complete
- Phase 3: Association engine (co-occurrence, PageRank, suggestions) — In progress
- Phase 4: Performance optimization — Future

### Test Status

- 174 tests passing
- 92% code coverage

---

## Contributing

We welcome contributions: code, docs, bug reports, ideas.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`issue/<number>-<description>`)
3. Run tests: `pytest`
4. Submit a pull request

REFERENCE: CONTRIBUTING.md — Full contribution guide.

### Commit Message Guidelines

We follow Conventional Commits v1.0.0.

REFERENCE: .github/COMMIT_CONVENTION.md — Full guide.

Quick reference:

- `feat(scope)`: New product feature
- `fix(scope)`: Bug fix
- `chore(scope)`: Development tools, scripts
- `style`: Formatting, linting
- `refactor(scope)`: Code restructuring
- `docs(scope)`: Documentation
- `ci`: CI/CD configuration
- `test(scope)`: Test files

---

## Uninstall

```bash
pipx uninstall traceflux
```

---

## License

MIT License — See LICENSE file.

---

## Identity

**Created by**: Tracer (迹/Ji) — One who leaves traces

**Philosophy**: Process matters, not results.

---

**Version**: 0.1.0 (Alpha)  
**Created**: 2026-03-06  
**Last Updated**: 2026-03-10
