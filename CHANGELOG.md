# Changelog

All notable changes to traceflux will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Automated release script (`scripts/release.sh`)
- Git hooks for pre-commit code quality checks
- GitHub Actions CI/CD pipeline
- Pull request template

### Changed
- Updated `pyproject.toml` with code quality tool configurations

### Fixed
- (None yet)

---

## [1.0.0] - 2026-03-07

### Added
- Core search functionality
- Associative keyword extraction
- PageRank-based suggestion engine
- UNIX pipe support (stdin/stdout)
- Comprehensive test suite (174+ tests)
- Documentation (README, PHILOSOPHY, examples)

### Changed
- (Initial release)

### Fixed
- (Initial release)

---

## Version Numbering

**Format**: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes (incompatible API modifications)
- **MINOR**: New features (backward-compatible functionality)
- **PATCH**: Bug fixes (backward-compatible issue resolution)

**Pre-release**: `MAJOR.MINOR.PATCH-prerelease` (e.g., `1.0.1-beta`)

---

## Release Process

1. Run `./scripts/release.sh <version>`
2. Review changes: `git show`
3. Push: `git push origin main --tags`
4. CI/CD automatically:
   - Runs tests on multiple Python versions
   - Performs linting and code quality checks
   - Builds distribution packages
   - Creates GitHub Release
   - Publishes to PyPI

---

## Links

- [GitHub Releases](https://github.com/tracer-mohist/traceflux/releases)
- [PyPI Package](https://pypi.org/project/traceflux/)
- [Contributing Guide](CONTRIBUTING.md)
