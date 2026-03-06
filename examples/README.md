# traceflux Examples

Practical usage examples for real-world scenarios.

Each example is a self-contained script or command sequence.

---

## Quick Examples

### 1. Find Related Terms

```bash
# What's related to "proxy" in my codebase?
traceflux associations "proxy" src/ --hops 2
```

### 2. Explore with Pipes

```bash
# Get top 5 related terms, then search for each
traceflux associations "pattern" src/ --json | \
  jq -r '.associations[:5][].term' | \
  while read term; do
    echo "=== Searching for: $term ==="
    traceflux search "$term" src/ --limit 3
  done
```

### 3. Discover API Endpoints

```bash
# Find all API-related patterns
traceflux associations "api" src/ --json | \
  jq -r '.associations[].term' | \
  grep -E "(route|endpoint|handler|url)"
```

### 4. Explore Configuration

```bash
# What configuration options exist?
traceflux associations "config" src/ --hops 2 --explain
```

---

## Example Scripts

### explore.sh — Iterative Exploration

Explore a codebase by following associations:

```bash
#!/bin/bash
# Usage: ./explore.sh <start_term> <path>

TERM=$1
PATH=$2

echo "Starting exploration from: $TERM"
echo "=============================="

for i in {1..3}; do
    echo ""
    echo "=== Hop $i ==="
    
    # Get top association
    NEXT=$(traceflux associations "$TERM" $PATH --json | \
             jq -r '.associations[0].term')
    
    echo "Discovered: $NEXT"
    
    # Search for it
    traceflux search "$NEXT" $PATH --limit 5
    
    # Move to next term
    TERM=$NEXT
done
```

**Usage:**
```bash
./explore.sh "proxy" src/
```

---

### find-related.sh — Find Related Files

Find files related to a concept:

```bash
#!/bin/bash
# Usage: ./find-related.sh <term> <path>

TERM=$1
PATH=$2

# Get associations
ASSOCS=$(traceflux associations "$TERM" $PATH --json | \
           jq -r '.associations[:10][].term')

# Search for each association
for assoc in $ASSOCS; do
    FILES=$(traceflux search "$assoc" $PATH --json | \
              jq -r '.results[].file' | sort -u)
    
    if [ -n "$FILES" ]; then
        echo "=== $assoc ==="
        echo "$FILES"
        echo ""
    fi
done
```

**Usage:**
```bash
./find-related.sh "PageRank" src/
```

---

### code-explorer.sh — Code Discovery Workflow

Complete code exploration workflow:

```bash
#!/bin/bash
# Usage: ./code-explorer.sh <concept> <codebase_path>

CONCEPT=$1
CODEBASE=$2

echo "🔍 Exploring: $CONCEPT in $CODEBASE"
echo ""

# Step 1: Search for the concept
echo "📍 Step 1: Searching for '$CONCEPT'..."
traceflux search "$CONCEPT" $CODEBASE --limit 5
echo ""

# Step 2: Find related terms
echo "🔗 Step 2: Finding related terms..."
traceflux associations "$CONCEPT" $CODEBASE --hops 2 --limit 10
echo ""

# Step 3: List common patterns
echo "📊 Step 3: Common patterns in codebase..."
traceflux patterns $CODEBASE --min-length 5 --limit 20
echo ""

echo "✅ Exploration complete!"
echo "💡 Tip: Use --json for programmatic access"
```

**Usage:**
```bash
./code-explorer.sh "database" src/
```

---

### doc-navigator.sh — Documentation Navigation

Navigate documentation by associations:

```bash
#!/bin/bash
# Usage: ./doc-navigator.sh <topic> <docs_path>

TOPIC=$1
DOCS=$2

echo "📚 Navigating documentation: $TOPIC"
echo ""

# Find related topics
RELATED=$(traceflux associations "$TOPIC" $DOCS --json)

echo "Related topics:"
echo "$RELATED" | jq -r '.associations[] | "  • \(.term) (strength: \(.strength))"'

# Show which files contain related topics
echo ""
echo "Files covering related topics:"
echo "$RELATED" | jq -r '.associations[:5][].term' | while read term; do
    FILES=$(traceflux search "$term" $DOCS --json | \
              jq -r '.results[].file' | head -3)
    if [ -n "$FILES" ]; then
        echo "  $term:"
        echo "$FILES" | sed 's/^/    /'
    fi
done
```

**Usage:**
```bash
./doc-navigator.sh "authentication" docs/
```

---

## Use Cases

### 1. Onboarding to a New Codebase

```bash
# Start with a known concept
./code-explorer.sh "main" src/

# Follow associations to understand architecture
./explore.sh "main" src/
```

### 2. Finding Configuration Options

```bash
# What config options exist?
traceflux associations "config" src/ --hops 2

# Which files contain them?
./find-related.sh "config" src/
```

### 3. API Discovery

```bash
# Find all API-related code
traceflux associations "api" src/ --json | \
  jq -r '.associations[].term' | \
  xargs -I {} traceflux search {} src/ --limit 3
```

### 4. Research Note Navigation

```bash
# Connect concepts in research notes
./doc-navigator.sh "nilpotent" notes/
```

---

## Tips

### Combine with Standard Tools

```bash
# Count occurrences per file
traceflux search "pattern" src/ --json | \
  jq '.results | map({file, count: .positions | length})'

# Find unique files
traceflux search "pattern" src/ --json | \
  jq -r '.results[].file' | sort -u

# Pipe to grep for refinement
traceflux associations "proxy" src/ | \
  grep -E "(chain|tunnel|socks)"
```

### Use JSON for Automation

```bash
# Extract just the terms
traceflux associations "pattern" src/ --json | \
  jq -r '.associations[].term'

# Filter by strength
traceflux associations "pattern" src/ --json | \
  jq '.associations[] | select(.strength > 0.5)'

# Build a list for batch processing
traceflux associations "pattern" src/ --json | \
  jq -r '.associations[:10][].term' > terms.txt
```

### Combine Multiple Searches

```bash
# Search for multiple terms at once
for term in "proxy" "config" "settings"; do
    echo "=== $term ==="
    traceflux search "$term" src/ --limit 3
done
```

---

## Contributing Examples

Have a useful pattern? Share it!

1. Create a script in `examples/`
2. Add usage instructions
3. Document the use case
4. Submit a pull request

---

**Remember**: traceflux is for **discovery**, not just search.

Let the associations guide you.
