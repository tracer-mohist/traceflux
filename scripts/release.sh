#!/bin/bash
# release.sh - Create a new release for traceflux
#
# Philosophy: Simple, Practical, Elegant
# - Only updates pyproject.toml (single source of truth)
# - Runs tests (must pass)
# - Creates commit and tag
# - No version sync needed (runtime reading)
#
# Usage: ./scripts/release.sh <version>
# Example: ./scripts/release.sh 1.0.1

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }

# Show help
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    echo "Usage: $0 <version>"
    echo ""
    echo "Create a new release for traceflux."
    echo ""
    echo "Arguments:"
    echo "  version    Semantic version (MAJOR.MINOR.PATCH)"
    echo ""
    echo "Examples:"
    echo "  $0 1.0.1         # Patch release"
    echo "  $0 1.1.0         # Minor release"
    echo "  $0 2.0.0         # Major release"
    echo "  $0 1.0.1-beta    # Pre-release"
    echo ""
    echo "What it does:"
    echo "  1. Updates pyproject.toml (single source of truth)"
    echo "  2. Runs tests (must pass)"
    echo "  3. Creates git commit and tag"
    echo ""
    echo "Next steps:"
    echo "  git push origin main --tags"
    echo "  CI/CD will create GitHub Release"
    exit 0
fi

if [[ $# -ne 1 ]]; then
    print_error "Usage: $0 <version>"
    print_info "Example: $0 1.0.1"
    print_info "Run '$0 --help' for more information"
    exit 1
fi

VERSION=$1

# Validate SemVer
if ! [[ $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9]+)?$ ]]; then
    print_error "Invalid version format: $VERSION"
    print_info "Expected: MAJOR.MINOR.PATCH (e.g., 1.0.1)"
    exit 1
fi

print_info "Creating release v$VERSION"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
cd "$PROJECT_ROOT"

# Update pyproject.toml (single source of truth)
print_info "Updating pyproject.toml..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/^version = \".*\"/version = \"$VERSION\"/" pyproject.toml
else
    sed -i "s/^version = \".*\"/version = \"$VERSION\"/" pyproject.toml
fi
print_success "pyproject.toml updated"

# Run tests
print_info "Running tests..."
if command -v pytest &> /dev/null; then
    if pytest -q; then
        print_success "Tests passed"
    else
        print_error "Tests failed"
        exit 1
    fi
else
    print_info "pytest not found, skipping tests"
fi

# Commit and tag
print_info "Creating commit and tag..."
git add pyproject.toml
git commit -m "Release v$VERSION" || print_info "No changes to commit"
git tag -a "v$VERSION" -m "Release v$VERSION"

print_success "Release v$VERSION prepared"
echo ""
print_info "Next steps:"
echo "  1. Review: git show"
echo "  2. Push: git push origin main --tags"
echo "  3. CI/CD will create GitHub Release"
