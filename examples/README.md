# traceflux Examples

Practical usage examples for real-world scenarios.

traceflux works like `grep` or `rg`:
- Search files/directories directly
- OPTION: read from stdin (pipe input)
- Output can be piped to other tools

---

## Quick Examples

### 1. Search Files Directly

```bash
# What's related to "proxy" in my codebase?
traceflux associations "proxy" src/ --hops 2

# Search for a pattern
traceflux search "def " src/ --limit 10
```

### 2. Pipe Input to traceflux

```bash
# Search content from stdin
cat file.txt | traceflux search "pattern"

# Combine multiple files
find . -name "*.py" | xargs cat | traceflux associations "proxy"

# Filter then analyze
git diff HEAD~1 | traceflux patterns
```

### 3. Pipe traceflux Output to Other Tools

```bash
# Filter results with grep
traceflux search "pattern" src/ | grep -v test

# Extract specific fields with jq
traceflux associations "pattern" src/ --json | \
  jq -r '.associations[].term'

# Count and sort
traceflux patterns src/ --json | jq '.patterns | length'
```

### 4. Combined Pipeline

```bash
# Get top 5 related terms, then search for each
traceflux associations "pattern" src/ --json | \
  jq -r '.associations[:5][].term' | \
  while read term; do
    echo "=== Searching for: $term ==="
    traceflux search "$term" src/ --limit 3
  done
```

---

## Example Scripts

### explore.sh -- Iterative Exploration

Explore a codebase by following associations:

```bash
#!/bin/bash
TERM=$1; PATH=$2
for i in {1..3}; do
    NEXT=$(traceflux associations "$TERM" $PATH --json | jq -r '.associations[0].term')
    echo "=== Hop $i: $NEXT ==="
    traceflux search "$NEXT" $PATH --limit 5
    TERM=$NEXT
done
```

USAGE: `./explore.sh "proxy" src/`

---

### find-related.sh -- Find Related Files

Find files related to a concept:

```bash
#!/bin/bash
TERM=$1; PATH=$2
for assoc in $(traceflux associations "$TERM" $PATH --json | jq -r '.associations[:10][].term'); do
    FILES=$(traceflux search "$assoc" $PATH --json | jq -r '.results[].file' | sort -u)
    [ -n "$FILES" ] && echo "=== $assoc ===" && echo "$FILES"
done
```

USAGE: `./find-related.sh "PageRank" src/`

---

### code-explorer.sh -- Code Discovery Workflow

Complete code exploration workflow:

```bash
#!/bin/bash
CONCEPT=$1; CODEBASE=$2
echo "Exploring: $CONCEPT in $CODEBASE"
echo "Step 1: Searching..." && traceflux search "$CONCEPT" $CODEBASE --limit 5
echo "Step 2: Related terms..." && traceflux associations "$CONCEPT" $CODEBASE --hops 2 --limit 10
echo "Step 3: Patterns..." && traceflux patterns $CODEBASE --min-length 5 --limit 20
```

USAGE: `./code-explorer.sh "database" src/`

---

### doc-navigator.sh -- Documentation Navigation

Navigate documentation by associations:

```bash
#!/bin/bash
TOPIC=$1; DOCS=$2
RELATED=$(traceflux associations "$TOPIC" $DOCS --json)
echo "Related topics:"
echo "$RELATED" | jq -r '.associations[] | "  - \(.term) (strength: \(.strength))"'
```

USAGE: `./doc-navigator.sh "authentication" docs/`

---

## Use Cases

ONBOARDING: `./code-explorer.sh "main" src/` then `./explore.sh "main" src/`

CONFIG DISCOVERY: `traceflux associations "config" src/ --hops 2` then `./find-related.sh "config" src/`

API DISCOVERY: `traceflux associations "api" src/ --json | jq -r '.associations[].term' | xargs -I {} traceflux search {} src/ --limit 3`

RESEARCH NOTES: `./doc-navigator.sh "nilpotent" notes/`

---

## Tips

MEANINGFUL RESULTS: Use `traceflux patterns src/ --min-length 8` for longer patterns, `--min-length 6 --limit 20` to filter by frequency. See `../README.md` for trade-offs.

COMBINE WITH TOOLS:
- Count: `traceflux search "pattern" src/ --json | jq '.results | map({file, count: .positions | length})'`
- Unique files: `traceflux search "pattern" src/ --json | jq -r '.results[].file' | sort -u`
- Refine: `traceflux associations "proxy" src/ | grep -E "(chain|tunnel|socks)"`

JSON AUTOMATION:
- Extract terms: `traceflux associations "pattern" src/ --json | jq -r '.associations[].term'`
- Filter by strength: `jq '.associations[] | select(.strength > 0.5)'`
- Batch list: `jq -r '.associations[:10][].term' > terms.txt`

MULTIPLE SEARCHES: `for term in "proxy" "config"; do traceflux search "$term" src/ --limit 3; done`

---

## Contributing Examples

Have a useful pattern? Share it!

1. Create a script in `examples/`
2. Add usage instructions
3. Document the use case
4. Submit a pull request

---

REMEMBER: traceflux is for discovery, not just search.

Let the associations guide you.
