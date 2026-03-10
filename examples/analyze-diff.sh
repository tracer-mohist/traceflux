#!/bin/bash
# examples/analyze-diff.sh
# analyze-diff.sh — Analyze Git Diff
#
# Analyze what concepts changed in a git diff.
# Shows patterns and associations in the changed code.
#
# Usage: ./analyze-diff.sh [git diff options]
#
# Examples:
#   ./analyze-diff.sh HEAD~1
#   ./analyze-diff.sh main..feature
#   ./analyze-diff.sh  # Uses HEAD~1 by default

set -e

DIFF_ARGS=${*:-"HEAD~1"}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRACEFLUX="${SCRIPT_DIR}/../.venv/bin/python -m traceflux.cli"

# Save diff to temp file (need to reuse for multiple analyses)
TEMP_FILE=$(mktemp)
trap "rm -f $TEMP_FILE" EXIT

# Get the diff
git diff $DIFF_ARGS > "$TEMP_FILE"

if [ ! -s "$TEMP_FILE" ]; then
    echo "No changes in diff: $DIFF_ARGS"
    exit 0
fi

echo "📊 Analyzing git diff: $DIFF_ARGS"
echo "   Lines changed: $(wc -l < "$TEMP_FILE")"
echo ""

# Find patterns in the diff
echo "🔍 Patterns in changes:"
$TRACEFLUX patterns "$TEMP_FILE" --min-length 4 --limit 15 2>/dev/null
echo ""

# Search for common code concepts
for term in "def " "class " "import " "return " "if " "for "; do
    COUNT=$($TRACEFLUX search "$term" "$TEMP_FILE" 2>/dev/null | grep -c "occurrence" || true)
    if [ "$COUNT" -gt 0 ]; then
        echo "  $term: $COUNT occurrence(s)"
    fi
done
echo ""

echo "✅ Analysis complete!"
echo "💡 Full diff saved to: $TEMP_FILE (will be deleted on exit)"
