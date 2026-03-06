#!/bin/bash
# pipe-search.sh — Search Piped Content
#
# Search content from stdin and show associations.
# Useful for analyzing git diffs, command output, etc.
#
# Usage: <command> | ./pipe-search.sh <query>
#
# Examples:
#   git diff HEAD~1 | ./pipe-search.sh "config"
#   cat file.txt | ./pipe-search.sh "pattern"
#   find . -name "*.md" | xargs cat | ./pipe-search.sh "proxy"

set -e

QUERY=${1:-"pattern"}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRACEFLUX="${SCRIPT_DIR}/../.venv/bin/python -m traceflux.cli"

echo "🔍 Searching piped content for: $QUERY"
echo ""

# Read from stdin and search
$TRACEFLUX search "$QUERY" --limit 10

echo ""
echo "🔗 Related terms:"
# Re-read from stdin won't work, so just show a tip
echo "💡 Tip: Save output to a file first for association analysis"
echo "   Example: cat file.txt | tee /tmp/content.txt | $0 query"
echo "   Then: $TRACEFLUX associations \"query\" /tmp/content.txt"
