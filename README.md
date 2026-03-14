# traceflux

Associative text search engine.

---

## What It Does

You search for "proxy". You find it. But you miss "proxychains", "HTTP_PROXY", "git config http.proxy".

traceflux discovers related concepts you do not know to search for.

```bash
traceflux associations "proxy" src/ --hops 2

# Output:
#   proxychains              strength: 0.85
#   HTTP_PROXY               strength: 0.72
#   git config               strength: 0.65
```

---

## Quick Start

### Install

```bash
pipx install git+https://github.com/tracer-mohist/traceflux.git
```

### Use

```bash
# Find associations
traceflux associations "PageRank" src/

# Search patterns
traceflux search "def " src/ --limit 10

# List patterns
traceflux patterns src/ --min-length 8 --limit 20
```

### JSON Output

```bash
traceflux associations "proxy" src/ --json | jq '.associations[]'
```

---

## Documentation

- Getting Started (docs/GETTING_STARTED.md) - 5-minute setup
- Usage Guide (docs/USAGE.md) - Commands and options
- Architecture (docs/ARCHITECTURE.md) - How it works
- Use Cases (docs/USE-CASES.md) - Real-world examples
- Philosophy (docs/PHILOSOPHY.md) - Design principles
- Contributing (CONTRIBUTING.md) - How to contribute
- Testing (TESTING.md) - Run and write tests

---

## For Contributors

```bash
git clone https://github.com/tracer-mohist/traceflux.git
cd traceflux
pipx install pdm
pdm install --dev
pytest
```

REFERENCE: CONTRIBUTING.md for full guide.

---

Created: 2026-03-06
Last Updated: 2026-03-10

## Workflow Automation

This project uses workflow-as-list for process automation.

NOTE: For `.workflow.list` files, use `workflow --help` or execute:
  workflow check/run/exec <workflow-name>

Quick start:
  workflow list              # List available workflows
  workflow check <name>      # Validate workflow
  workflow run <name>        # Start execution
