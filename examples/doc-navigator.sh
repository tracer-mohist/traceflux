#!/bin/bash
# doc-navigator.sh — Documentation Navigation
#
# Navigate documentation by associations.
# Shows related topics and which files contain them.
#
# Usage: ./doc-navigator.sh <topic> <docs_path>
#
# Example:
#   ./doc-navigator.sh "authentication" docs/
#   ./doc-navigator.sh "proxy" .

set -e

TOPIC=${1:-"config"}
DOCS=${2:-"."}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRACEFLUX="${SCRIPT_DIR}/../.venv/bin/python -m traceflux.cli"

echo "📚 Navigating documentation: $TOPIC"
echo ""

# Find related topics
RELATED=$($TRACEFLUX associations "$TOPIC" $DOCS --json 2>/dev/null)

if [ -z "$RELATED" ] || [ "$RELATED" = "null" ]; then
    echo "No associations found for '$TOPIC'"
    exit 0
fi

echo "Related topics:"
echo "$RELATED" | jq -r '.associations[] | "  • \(.term) (strength: \(.strength))"'

# Show which files contain related topics
echo ""
echo "Files covering related topics:"
echo "$RELATED" | jq -r '.associations[:5][].term' | while read term; do
    FILES=$($TRACEFLUX search "$term" $DOCS --json 2>/dev/null | \
              jq -r '.results[].file' 2>/dev/null | head -3)
    if [ -n "$FILES" ]; then
        echo "  $term:"
        echo "$FILES" | sed 's/^/    /'
    fi
done

echo ""
echo "✅ Navigation complete!"
