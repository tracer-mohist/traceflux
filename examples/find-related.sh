#!/bin/bash
# find-related.sh — Find Related Files
#
# Find files related to a concept via associations.
#
# Usage: ./find-related.sh <term> <path>
#
# Example:
#   ./find-related.sh "PageRank" src/
#   ./find-related.sh "proxy" .

set -e

TERM=${1:-"config"}
PATH=${2:-"."}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRACEFLUX="${SCRIPT_DIR}/../.venv/bin/python -m traceflux.cli"

echo "🔗 Finding files related to: $TERM"
echo ""

# Get associations
ASSOCS=$($TRACEFLUX associations "$TERM" $PATH --json 2>/dev/null | \
           jq -r '.associations[:10][].term // empty')

if [ -z "$ASSOCS" ]; then
    echo "No associations found for '$TERM'"
    exit 0
fi

# Search for each association
for assoc in $ASSOCS; do
    FILES=$($TRACEFLUX search "$assoc" $PATH --json 2>/dev/null | \
              jq -r '.results[].file' 2>/dev/null | sort -u)

    if [ -n "$FILES" ]; then
        echo "=== $assoc ==="
        echo "$FILES" | sed 's/^/  /'
        echo ""
    fi
done

echo "✅ Done!"
