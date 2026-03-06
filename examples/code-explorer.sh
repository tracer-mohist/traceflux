#!/bin/bash
# code-explorer.sh — Code Discovery Workflow
#
# Complete code exploration workflow:
# 1. Search for the concept
# 2. Find related terms
# 3. List common patterns
#
# Usage: ./code-explorer.sh <concept> <codebase_path>
#
# Example:
#   ./code-explorer.sh "database" src/
#   ./code-explorer.sh "authentication" .

set -e

CONCEPT=${1:-"main"}
CODEBASE=${2:-"."}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRACEFLUX="${SCRIPT_DIR}/../.venv/bin/python -m traceflux.cli"

echo "🔍 Exploring: $CONCEPT in $CODEBASE"
echo ""

# Step 1: Search for the concept
echo "📍 Step 1: Searching for '$CONCEPT'..."
$TRACEFLUX search "$CONCEPT" $CODEBASE --limit 5 2>/dev/null
echo ""

# Step 2: Find related terms
echo "🔗 Step 2: Finding related terms..."
$TRACEFLUX associations "$CONCEPT" $CODEBASE --hops 2 --limit 10 2>/dev/null
echo ""

# Step 3: List common patterns
echo "📊 Step 3: Common patterns in codebase..."
$TRACEFLUX patterns $CODEBASE --min-length 5 --limit 20 2>/dev/null
echo ""

echo "✅ Exploration complete!"
echo "💡 Tip: Use --json for programmatic access"
