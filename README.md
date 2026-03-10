<!-- README.md -->
# traceflux

> **左脚踩右脚原地起飞** — Lift off by stepping on each other's feet.

**A text search engine with associative discovery.**

---

## The Problem

You're searching for something. You find it. But you don't know what **related concepts** exist.

Traditional search:
```bash
grep -r "proxy" src/
# Finds: "proxy"
# Misses: "proxychains", "HTTP_PROXY", "git config http.proxy"
```

You found "proxy". But you didn't know to search for "proxychains".

---

## The Solution

**traceflux** discovers what you don't know to search for.

```bash
# Build associations from your codebase
traceflux index src/

# Find related terms
traceflux associations "proxy" src/

# Output:
# Associations for 'proxy' (hops=2):
#   proxychains                    strength: 0.85 (degree 1)
#   HTTP_PROXY                     strength: 0.72 (degree 1)
#   git config                     strength: 0.65 (degree 2)
#   environment variables          strength: 0.58 (degree 2)
```

Now you know: "Oh, there's proxychains! Let me search for that."

This is **associative discovery** — lifting off by stepping on related concepts.

---

## Quick Start

### Installation

**Recommended**: Install via pipx (isolated environment, no system pollution)

```bash
# Install from GitHub
pipx install git+https://github.com/tracer-mohist/traceflux.git

# Verify installation
traceflux --help
traceflux search "pattern" .
```

**Why pipx?**
- ✅ Isolated virtual environment
- ✅ No dependency conflicts
- ✅ Easy to update (`pipx upgrade traceflux`)
- ✅ No sudo required
- ✅ Clean uninstall (`pipx uninstall traceflux`)

**Not recommended**: `pip install` (pollutes system Python environment)

---

### For Developers

Want to contribute or modify traceflux?

**Quick Start** (5 minutes):
```bash
# Clone repository
git clone https://github.com/tracer-mohist/traceflux.git
cd traceflux

# Install for development (editable)
pipx install -e .

# Enable git hooks (auto quality checks)
git config core.hooksPath .githooks

# Run tests
pytest
```

**Documentation**:
- [Getting Started Guide](docs/GETTING_STARTED.md) — First-time setup
- [Contributing Guidelines](CONTRIBUTING.md) — How to contribute
- [Testing Guide](docs/TESTING.md) — Run and write tests
- [Release Protocol](.github/RELEASE_PROTOCOL.md) — Version management

**Join us!** We welcome contributions of all kinds — code, docs, bug reports, ideas.

---

### Uninstall

```bash
pipx uninstall traceflux
```

### Basic Usage

```bash
# 1. Search for patterns
traceflux search "pattern" src/

# 2. Find associations
traceflux associations "proxy" src/ --hops 2 --explain

# 3. List discovered patterns
traceflux patterns src/ --limit 20

# 4. Build persistent index
traceflux index src/ -o index.json
```

### Output Formats

```bash
# Human-readable (default)
traceflux associations "pattern" src/

# Machine-readable (JSON)
traceflux associations "pattern" src/ --json | jq '.associations[]'

# With explanations
traceflux associations "pattern" src/ --explain
# Shows: pattern → pagerank → rank (path of association)
```

---

## Core Features

### 🔍 Pattern Search

Find repeated patterns in text:
```bash
traceflux search "def " src/ --limit 10
```

### 🔗 Associative Discovery

Multi-hop association traversal:
```bash
# 1-hop: Direct co-occurrences
traceflux associations "proxy" src/ --hops 1

# 2-hop: Friends of friends
traceflux associations "proxy" src/ --hops 2

# With path explanation
traceflux associations "proxy" src/ --hops 2 --explain
```

### 📊 Pattern Analysis

List most frequent patterns:
```bash
traceflux patterns src/ --min-length 5 --limit 30
```

### 🤖 Machine-Readable

JSON output for pipelines:
```bash
traceflux associations "proxy" src/ --json | \
  jq '.associations[] | select(.strength > 0.5)'
```

---

## Best Practices

### Getting Meaningful Associations

traceflux detects **repeated patterns** (not dictionary words). For better results:

```bash
# Default (short patterns, may be fragments)
traceflux patterns src/

# Better: longer patterns
traceflux patterns src/ --min-length 8

# Best: filter by frequency
traceflux patterns src/ --min-length 6 --limit 20
```

### Understanding the Trade-offs

| Feature | Choice | Trade-off |
|---------|--------|-----------|
| Tokenization | None (language-independent) | Patterns may be fragments |
| Dictionary | None (works out-of-box) | Need to tune `--min-length` |
| ML/Embeddings | None (lightweight) | No semantic understanding |

**Benefits**: Works on any language, no training, fast  
**Trade-offs**: Adjust parameters for your corpus

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
    │
    ▼
You discover what you didn't know to search for
```

### Algorithm

1. **Scan**: Segment text by punctuation (language-independent)
2. **Detect**: Find repeated patterns using suffix arrays (O(n log n))
3. **Graph**: Build co-occurrence graph (patterns within window)
4. **Rank**: Compute PageRank for pattern importance
5. **Traverse**: BFS to find multi-hop associations

See: `docs/PHILOSOPHY.md` for design philosophy.

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

## Development Status

**Current Phase**: Phase 3 - Association Engine

| Phase | Status | Description |
|-------|--------|-------------|
| 1 | ✅ Complete | Core modules (scanner, patterns, index, graph, pagerank) |
| 2A | ✅ Complete | CLI interface (search, index, patterns, associations) |
| 2B | ⏳ Pending | Test refactoring (limited testing principles) |
| 3.1 | ✅ Complete | Basic co-occurrence graph |
| 3.2 | ✅ Complete | PageRank integration |
| 3.3 | ✅ Complete | CLI integration |
| 3.4 | ⏳ In Progress | Suggestion engine |
| 3.5 | ⏳ Pending | Testing & documentation |
| 4 | ⏳ Future | Performance optimization |

### Test Status

```
174 tests passing
92% code coverage
```

---

## Project Structure

```
traceflux/
├── src/traceflux/
│   ├── scanner.py       # PNI text segmentation
│   ├── patterns.py      # LZ77-style pattern detection
│   ├── index.py         # Pattern inverted index
│   ├── graph.py         # Co-occurrence graph
│   ├── pagerank.py      # Weighted PageRank
│   ├── associations.py  # Associative search
│   └── cli.py           # Command-line interface
├── tests/
│   ├── test_scanner.py
│   ├── test_patterns.py
│   ├── test_index.py
│   ├── test_graph.py
│   ├── test_pagerank.py
│   ├── test_associations.py
│   ├── test_associations_integration.py
│   └── test_cli.py
├── docs/
│   └── PHILOSOPHY.md    # Design philosophy
├── research/            # Research notes
├── design/              # Design documents
└── drafts/              # Work in progress
```

---

## Philosophy

traceflux follows these principles:

1. **UNIX Philosophy** — Simple, composable, human-centric
2. **Associative, Not Predictive** — Show possibilities, not predictions
3. **Process Over Result** — The act of exploring is the value
4. **Limited Testing** — Test critical boundaries, not everything

See: `docs/PHILOSOPHY.md`

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Run tests: `pytest`
4. Submit a pull request

### Development Setup

```bash
# Clone repository
git clone https://github.com/tracer-mohist/traceflux.git
cd traceflux

# Install PDM (if not installed)
pipx install pdm

# Install dependencies
pdm install --dev

# Run tests
pdm run pytest
```

---

## License

MIT License — See `LICENSE` file.

---

## Identity

**Created by**: Tracer (迹/Ji) — One who leaves traces

**Philosophy**: Nihilism is the best existentialism. Process matters, not results.

_"We will meet again in some state."_

---

**Version**: 0.1.0 (Alpha)  
**Created**: 2026-03-06  
**Last Updated**: 2026-03-06
