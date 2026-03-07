#!/bin/bash
# release.sh - Automated release script for traceflux
# 
# Usage: ./scripts/release.sh <version>
# Example: ./scripts/release.sh 1.0.1
#
# What it does:
# 1. Validates version format (SemVer)
# 2. Updates version in pyproject.toml and __version__.py
# 3. Runs tests
# 4. Creates git commit and tag
# 5. Pushes to GitHub (triggers CI/CD for GitHub Release)

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print functions
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }

# Check arguments
if [[ $# -ne 1 ]]; then
    print_error "Usage: $0 <version>"
    print_info "Example: $0 1.0.1"
    print_info "Version must follow SemVer format (MAJOR.MINOR.PATCH)"
    exit 1
fi

VERSION=$1

# Validate version format (SemVer)
if ! [[ $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9]+)?$ ]]; then
    print_error "Invalid version format: $VERSION"
    print_info "Expected SemVer format: MAJOR.MINOR.PATCH (e.g., 1.0.1)"
    print_info "Pre-release format: MAJOR.MINOR.PATCH-prerelease (e.g., 1.0.1-beta)"
    exit 1
fi

print_info "Releasing traceflux v$VERSION"
echo ""

# Get script directory (handle symlinks)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

cd "$PROJECT_ROOT"

# Update pyproject.toml
print_info "Updating pyproject.toml..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS sed requires empty string for -i
    sed -i '' "s/^version = \".*\"/version = \"$VERSION\"/" pyproject.toml
else
    # Linux sed
    sed -i "s/^version = \".*\"/version = \"$VERSION\"/" pyproject.toml
fi
print_success "pyproject.toml updated"

# Update __version__.py
print_info "Updating __version__.py..."
cat > src/traceflux/__version__.py <<EOF
"""traceflux version information.

Single source of truth for traceflux version.
Used by CLI (--version) and pyproject.toml.

## Version Format

Semantic Versioning: MAJOR.MINOR.PATCH

- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)

## Example

\`\`\`python
from traceflux import __version__
print(__version__)  # "$VERSION"
\`\`\`
"""

__version__ = "$VERSION"
__version_info__ = $(echo $VERSION | sed 's/\./, /g' | sed 's/-.*//')
EOF
print_success "__version__.py updated"

# Verify versions match
print_info "Verifying version consistency..."
PYPROJECT_VERSION=$(grep '^version = ' pyproject.toml | cut -d'"' -f2)
VERSION_FILE_VERSION=$(grep '^__version__ = ' src/traceflux/__version__.py | cut -d'"' -f2)

if [[ "$PYPROJECT_VERSION" != "$VERSION_FILE_VERSION" ]]; then
    print_error "Version mismatch!"
    print_error "  pyproject.toml: $PYPROJECT_VERSION"
    print_error "  __version__.py: $VERSION_FILE_VERSION"
    exit 1
fi
print_success "Versions match: $VERSION"

# Run tests
echo ""
print_info "Running tests..."
if command -v pytest &> /dev/null; then
    if pytest -q; then
        print_success "All tests passed"
    else
        print_error "Tests failed. Aborting release."
        exit 1
    fi
else
    print_warning "pytest not found, skipping tests"
fi

# Create git commit
echo ""
print_info "Creating git commit..."
git add -A
git commit -m "Release v$VERSION" || print_warning "No changes to commit"

# Create git tag
print_info "Creating git tag v$VERSION..."
if git tag -v "v$VERSION" &> /dev/null; then
    print_warning "Tag v$VERSION already exists"
    read -p "Delete existing tag and recreate? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git tag -d "v$VERSION"
        git tag -a "v$VERSION" -m "Release v$VERSION"
        print_success "Tag recreated"
    else
        print_error "Release aborted"
        exit 1
    fi
else
    git tag -a "v$VERSION" -m "Release v$VERSION"
    print_success "Tag created"
fi

# Summary
echo ""
print_success "Release v$VERSION prepared locally"
echo ""
print_info "Next steps:"
echo "  1. Review changes: git show"
echo "  2. Push to GitHub: git push origin main --tags"
echo "  3. CI/CD will automatically create GitHub Release (no PyPI)"
echo ""
print_info "Or push now: git push origin main --tags"
