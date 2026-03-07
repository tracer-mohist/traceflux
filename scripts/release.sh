#!/bin/bash
# scripts/release.sh - Create GitHub release for traceflux
#
# Usage: ./scripts/release.sh <version>
# Example: ./scripts/release.sh 1.0.0
#
# Requirements:
# - git
# - gh (GitHub CLI)
# - Proper authentication (gh auth login)

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${GREEN}ℹ $1${NC}"
}

log_warn() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

log_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check requirements
check_requirements() {
    if ! command -v git &> /dev/null; then
        log_error "git is required but not installed"
        exit 1
    fi
    
    if ! command -v gh &> /dev/null; then
        log_error "GitHub CLI (gh) is required but not installed"
        log_info "Install: https://cli.github.com/"
        exit 1
    fi
    
    if ! gh auth status &> /dev/null; then
        log_error "GitHub CLI is not authenticated"
        log_info "Run: gh auth login"
        exit 1
    fi
}

# Validate version format
validate_version() {
    local version=$1
    
    if [[ ! $version =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        log_error "Invalid version format: $version"
        log_info "Expected: MAJOR.MINOR.PATCH (e.g., 1.0.0)"
        exit 1
    fi
}

# Check if working directory is clean
check_clean_working_dir() {
    if [[ -n $(git status --porcelain) ]]; then
        log_error "Working directory is not clean"
        log_info "Commit or stash changes before releasing"
        exit 1
    fi
}

# Create release
create_release() {
    local version=$1
    local tag="v$version"
    
    log_info "Creating release v$version..."
    
    # Create annotated tag
    git tag -a "$tag" -m "Release $tag"
    
    # Push tag
    log_info "Pushing tag $tag to origin..."
    git push origin "$tag"
    
    # Create GitHub release
    log_info "Creating GitHub release..."
    gh release create "$tag" \
        --title "v$version" \
        --generate-notes \
        --notes-file RELEASE_NOTES.md \
        --verify-tag
    
    log_info "✅ Release $tag created successfully!"
}

# Main
main() {
    # Check arguments
    if [[ $# -ne 1 ]]; then
        log_error "Version required"
        echo "Usage: $0 <version>"
        echo "Example: $0 1.0.0"
        exit 1
    fi
    
    local version=$1
    
    # Pre-flight checks
    log_info "Running pre-flight checks..."
    check_requirements
    validate_version "$version"
    check_clean_working_dir
    
    # Confirm
    echo ""
    log_warn "This will create release v$version"
    echo ""
    echo "Changes since last release will be included in release notes."
    echo ""
    read -p "Continue? [y/N] " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_warn "Release cancelled"
        exit 0
    fi
    
    # Create release
    create_release "$version"
    
    # Post-release tasks
    echo ""
    log_info "Post-release tasks:"
    echo "1. Verify release on GitHub: https://github.com/tracer-mohist/traceflux/releases"
    echo "2. Test installation: pipx install git+https://github.com/tracer-mohist/traceflux.git@v$version"
    echo "3. Announce release (if applicable)"
    echo ""
}

# Run main
main "$@"
