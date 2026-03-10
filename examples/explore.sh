#!/bin/bash
# examples/explore.sh
# explore.sh — Iterative Exploration
#
# Explore a codebase by following associations.
# Each hop discovers the most related term.
#
# Usage: ./explore.sh <start_term> <path> [hops]
#
# Example:
#   ./explore.sh "proxy" src/ 3
#   ./explore.sh "pattern" . 5

set -e

TERM=${1:-"main"}
PATH=${2:-"."}
HOPS=${3:-3}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRACEFLUX="${SCRIPT_DIR}/../.venv/bin/python -m traceflux.cli"

echo "🔍 Starting exploration from: $TERM"
echo "   Path: $PATH"
echo "   Hops: $HOPS"
echo "=============================="

for i in $(seq 1 $HOPS); do
    echo ""
    echo "=== Hop $i ==="
    
    # Get top association
    NEXT=$($TRACEFLUX associations "$TERM" $PATH --json 2>/dev/null | \
             jq -r '.associations[0].term // empty')
    
    if [ -z "$NEXT" ]; then
        echo "No more associations found."
        break
    fi
    
    echo "Discovered: $NEXT"
    
    # Search for it
    $TRACEFLUX search "$NEXT" $PATH --limit 3 2>/dev/null
    
    # Move to next term
    TERM=$NEXT
done

echo ""
echo "✅ Exploration complete!"
