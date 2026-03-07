# Contributing to traceflux

**Thank you for your interest in contributing!**

This document provides guidelines and instructions for contributing to traceflux.

**First Time?** Start here:
- 🚀 [Getting Started Guide](docs/GETTING_STARTED.md) — 5-minute setup
- 📖 [Testing Guide](docs/TESTING.md) — How to run tests
- 📝 [Quick Reference](docs/QUICK_REF.md) — Common commands

**Related**:
- [Release Protocol](.github/RELEASE_PROTOCOL.md) — Version management and release process
- [CI/CD Pipeline](.github/workflows/ci.yml) — Automated testing and release
- [Release Guide](docs/RELEASE.md) — User-facing release documentation

---

## Quick Start

**Want to contribute?** Here's how to get started:

```bash
# 1. Fork the repository
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/traceflux.git
cd traceflux

# 3. Install for development
pipx install -e .

# 4. Create a branch (use issue/<number>-<description> format)
git checkout -b issue/42-your-feature-name

# 5. Make your changes, test, and commit (follow Conventional Commits)
# 6. Push and open a Pull Request (required - no direct pushes to main)
```

**Important**: We use **Pull Requests for all changes** - no direct pushes to `main`. See [Branch Protection & PR Workflow](.github/BRANCH_PROTECTION.md) for details.

---

## Commit Convention

We use **Conventional Commits** for standardized version management.

### Format

```
<type>: <description>

[optional body]

[optional footer]
```

### Types

| Type | Description | Version Impact |
|------|-------------|----------------|
| `feat:` | New feature | Minor (1.1.0) |
| `fix:` | Bug fix | Patch (1.0.1) |
| `docs:` | Documentation only | None |
| `style:` | Code style (formatting) | None |
| `refactor:` | Code refactoring | None |
| `test:` | Add or update tests | None |
| `chore:` | Maintenance tasks | None |

### Breaking Changes

Add `BREAKING CHANGE:` in the footer:

```
feat: remove deprecated API

BREAKING CHANGE: old_api() is removed, use new_api() instead
```

→ Triggers **Major** version bump (2.0.0)

### Examples

```bash
# Feature
git commit -m "feat: add multi-hop association search"

# Bug fix
git commit -m "fix: handle empty input gracefully"

# Documentation
git commit -m "docs: update installation guide"

# Refactor
git commit -m "refactor: simplify PageRank calculation"

# Breaking change
git commit -m "feat: redesign association API

BREAKING CHANGE: AssociationResult structure changed"
```

### Why Conventional Commits?

- ✅ **Automated versioning** - Commit type determines version bump
- ✅ **Clear changelog** - Automatically generated from commits
- ✅ **Standardized** - Industry-standard convention
- ✅ **Transparent** - Anyone can predict version changes

**Learn more**: [Conventional Commits Specification](https://www.conventionalcommits.org/)

---

## What We're Looking For

### High Priority Contributions

**Bug Reports**:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS

**Bug Fixes**:
- Fix the bug
- Add a test to prevent regression
- Update documentation if needed

**Documentation Improvements**:
- Fix typos or unclear explanations
- Add examples
- Improve installation guides
- Translate documentation

**Feature Requests**:
- Describe the use case
- Explain why it's valuable
- Provide examples of usage

### Medium Priority Contributions

**New Features**:
- Open an issue first to discuss
- Implement with tests
- Document the feature
- Update README if needed

**Performance Improvements**:
- Benchmark before/after
- Ensure no functionality breaks
- Document trade-offs

### Not Looking For

- ❌ Premature optimization (without benchmarks)
- ❌ Features that violate UNIX philosophy
- ❌ Breaking changes without strong justification
- ❌ Dependencies without security review

---

## Development Setup

### Requirements

- Python 3.10+
- pipx (`pip install pipx`)
- git

### Installation

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/traceflux.git
cd traceflux

# Install for development
pipx install -e .

# Verify installation
traceflux --version

# Run tests
cd tests
pytest -v
```

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=src/traceflux --cov-report=term-missing

# Specific test file
pytest tests/test_scanner_unit.py -v

# Specific test function
pytest tests/test_scanner_unit.py::test_scan_simple_text -v
```

### Code Quality Tools

**Install development dependencies**:
```bash
pip install -e ".[dev]"
pip install black flake8 isort mypy
```

**Format code**:
```bash
black src/ tests/
isort src/ tests/
```

**Check code quality**:
```bash
black --check src/ tests/
isort --check-only src/ tests/
flake8 --max-line-length=100 --ignore=E501,W503 src/ tests/
mypy src/ --ignore-missing-imports
```

### Git Hooks (Recommended)

**Enable pre-commit hooks**:
```bash
git config core.hooksPath .githooks
```

This automatically runs code quality checks before each commit:
- Python syntax validation
- Code formatting check (black)
- Import order check (isort)
- Linting (flake8)

---

## Pull Request Process

### Branch Naming

**Format**: `issue/<number>-<short-description>`

```bash
# Good
git checkout -b issue/42-multi-hop-search
git checkout -b issue/38-fix-empty-input

# Avoid
git checkout -b feature/new-stuff
git checkout -b my-branch
```

**Why**: Clear traceability to issues, easy to identify purpose.

### Before Submitting

1. **Update documentation** if behavior changes
2. **Add tests** for new features or bug fixes
3. **Run all tests** locally: `pytest`
4. **Check code quality**: `black --check`, `flake8`
5. **Update CHANGELOG.md** with your changes

### Submitting a PR

1. **Ensure branch is up to date**:
   ```bash
   git checkout main
   git pull origin main
   git checkout issue/42-your-feature
   git rebase main  # Or merge
   ```

2. **Make your changes and commit** (follow Conventional Commits):
   ```bash
   git add .
   git commit -m "feat: add multi-hop search"
   ```

3. **Push to your fork**:
   ```bash
   git push -u origin issue/42-your-feature
   ```

4. **Open a Pull Request** on GitHub:
   - Use the PR template
   - Title must follow Conventional Commits
   - Reference the issue: "Closes #42"

### Review Process

- All PRs require **manual review** before merging
- CI/CD must pass (tests, linting)
- At least one maintainer approval required
- Address review feedback promptly

### Merge Strategy

**Use "Create a merge commit"** (NOT squash or rebase):

- ✅ Preserves individual commit history
- ✅ Clear traceability to PR and issue
- ✅ Easier to revert if needed

**Avoid squash merge** unless PR has many small "fix typo" commits.

### After Approval

- Maintainer will merge the PR
- Delete your feature branch after merge

**Full details**: See [Branch Protection & PR Workflow](.github/BRANCH_PROTECTION.md)

---

## Code Style

### Python Style

- **Formatting**: Follow PEP 8
- **Type Hints**: Use type hints for all public APIs
- **Docstrings**: Google-style or NumPy-style
- **Line Length**: Max 100 characters
- **Imports**: Standard library first, then third-party

### Example

```python
"""Module docstring - one line summary.

Longer description if needed.
"""

from typing import List, Optional

from traceflux.output import OutputFormatter


def public_function(param: str, count: int = 1) -> List[str]:
    """Function docstring.
    
    Args:
        param: Description of param
        count: Description of count (default: 1)
    
    Returns:
        Description of return value
    
    Example:
        >>> public_function("test", 2)
        ['test', 'test']
    """
    # Implementation here
    pass
```

### Documentation Style

**Module Docstrings**:
- One-line summary
- Longer description if needed
- Examples for complex modules

**Function Docstrings**:
- One-line summary
- Args section
- Returns section
- Example (if helpful)

**Class Docstrings**:
- Purpose of the class
- Key attributes
- Usage example

---

## Commit Guidelines

### Why Conventional Commits Matter

**Automated versioning depends on correct commit messages**:
- `feat:` → Minor version bump (1.1.0)
- `fix:` → Patch version bump (1.0.1)
- `feat: ... BREAKING CHANGE:` → Major version bump (2.0.0)

**Wrong commit messages = broken automation**

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Rules**:
- Lowercase after type: `feat: add`, NOT `feat: Add`
- Imperative mood: `add`, NOT `added` or `adding`
- No period at end
- Max 72 chars for subject line

### Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat: add multi-hop search` |
| `fix` | Bug fix | `fix: handle empty input` |
| `docs` | Documentation only | `docs: update README` |
| `style` | Code style (formatting) | `style: fix whitespace` |
| `refactor` | Code refactoring | `refactor: simplify parser` |
| `test` | Test additions/changes | `test: add edge cases` |
| `chore` | Maintenance tasks | `chore: update dependencies` |

### Good vs Bad Examples

```bash
# ✅ Good
git commit -m "feat: add multi-hop association search"
git commit -m "fix: handle empty input gracefully"
git commit -m "docs: update installation guide"
git commit -m "refactor: simplify PageRank calculation"

# ❌ Bad (avoid these)
git commit -m "Added new feature"           # Wrong tense
git commit -m "FIX: something"              # Uppercase type
git commit -m "feat: Added new feature"     # Past tense
git commit -m "fix bug"                     # Missing type
git commit -m "WIP"                         # Too vague
git commit -m "asdfasdf"                    # Nonsense
```

### Breaking Changes

Add `BREAKING CHANGE:` in the footer:

```bash
git commit -m "feat: remove deprecated API

BREAKING CHANGE: old_api() is removed, use new_api() instead"
```

→ Triggers **Major** version bump (2.0.0)

### Git Email

**Use GitHub noreply email**:
```bash
git config user.email "YOUR_ID+username@users.noreply.github.com"
```

This protects your privacy while linking commits to your GitHub account.

**Learn more**: [Conventional Commits Specification](https://www.conventionalcommits.org/)

---

## Pull Request Process

### Before Opening a PR

1. **Test your changes**
   ```bash
   pytest
   ```

2. **Update documentation**
   - README.md if behavior changes
   - Docstrings if API changes
   - Examples if usage changes

3. **Check git history**
   - Squash small commits if appropriate
   - Ensure commit messages are clear

### Opening a PR

1. **Title**: Clear and descriptive
   - ✅ `feat(cli): add --verbose flag`
   - ❌ `Update cli.py`

2. **Description**: Use the template
   ```markdown
   ## What does this PR do?
   
   ## Why is it needed?
   
   ## How to test?
   
   ## Related issues
   ```

3. **Labels**: Add appropriate labels
   - `bug`, `enhancement`, `documentation`, etc.

### After Opening a PR

1. **Respond to feedback** promptly
2. **Keep the PR focused** - don't add unrelated changes
3. **Be patient** - maintainers have limited time

---

## Issue Reporting

### Bug Reports

**Template**:
```markdown
**Describe the bug**
Clear description of what's wrong.

**To Reproduce**
Steps to reproduce:
1. Install traceflux: `pipx install ...`
2. Run command: `traceflux search "pattern" .`
3. See error

**Expected behavior**
What should happen.

**Actual behavior**
What actually happened.

**Environment**
- Python version: 3.11
- OS: Ubuntu 22.04
- traceflux version: 1.0.0

**Additional context**
Screenshots, logs, etc.
```

### Feature Requests

**Template**:
```markdown
**Is your feature request related to a problem?**
Clear description of the problem.

**Describe the solution you'd like**
What you want to happen.

**Describe alternatives you've considered**
Other solutions you've thought about.

**Use case**
How would this be used? Why is it valuable?

**Additional context**
Examples, mockups, etc.
```

---

## Design Principles

When contributing, keep these principles in mind:

### UNIX Philosophy

1. **Do One Thing Well**: Each module/command has a single purpose
2. **Composability**: Works well with other tools (pipes, stdin/stdout)
3. **Simplicity**: Simple interfaces, minimal complexity
4. **Clarity**: Clear over clever

### traceflux Values

1. **Discoverability**: Help users find what they don't know to search for
2. **Performance**: Fast enough for typical use cases (<100MB files)
3. **Privacy**: No telemetry, no data collection, local processing only
4. **Maintainability**: Code is written for humans, not just machines

### What We Reject

- ❌ Features that add complexity without clear value
- ❌ Dependencies without strong justification
- ❌ Breaking changes without migration path
- ❌ Premature optimization (before measuring)

---

## Security

### Reporting Vulnerabilities

**DO NOT** open a public issue for security vulnerabilities.

**DO**:
1. Go to [Security tab](https://github.com/tracer-mohist/traceflux/security)
2. Click "Report a vulnerability"
3. Provide details privately

See [SECURITY.md](SECURITY.md) for full guidelines.

### Security Best Practices

- Sanitize all user input
- Validate file paths (prevent path traversal)
- Handle errors gracefully
- No hardcoded credentials
- No external network calls without explicit user action

---

## Questions?

**Need help?**

- [Discussions](https://github.com/tracer-mohist/traceflux/discussions) - General questions
- [Issues](https://github.com/tracer-mohist/traceflux/issues) - Bug reports and feature requests
- [SECURITY.md](SECURITY.md) - Security issues (private)

---

## Thank You!

Every contribution matters, no matter how small.

- Fixed a typo? Thank you!
- Reported a bug? Thank you!
- Added a feature? Thank you!
- Improved documentation? Thank you!

**Together, we make traceflux better for everyone.**

---

**License**: MIT (same as traceflux)

**Inspired by**: [Contributing.md template](https://contributing.md/)
