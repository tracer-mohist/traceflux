# Contributing to traceflux

**Thank you for your interest in contributing!**

This document provides guidelines and instructions for contributing to traceflux.

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

# 4. Create a branch
git checkout -b feature/your-feature-name

# 5. Make your changes, test, and commit
# 6. Push and open a Pull Request
```

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

### Before Submitting

1. **Update documentation** if behavior changes
2. **Add tests** for new features or bug fixes
3. **Run all tests** locally: `pytest`
4. **Check code quality**: `black --check`, `flake8`
5. **Update CHANGELOG.md** with your changes

### Submitting a PR

1. Create a branch from `main`:
   ```bash
   git checkout main
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit:
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

3. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Open a Pull Request on GitHub using the PR template

### Review Process

- All PRs require **manual review** before merging
- CI/CD must pass (tests, linting)
- At least one maintainer approval required
- Address review feedback promptly

### After Approval

- Maintainer will merge the PR
- No squash unless requested (preserve commit history)
- Delete your feature branch after merge

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

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test additions or changes
- `chore`: Maintenance tasks

**Examples**:
```
feat(cli): add --verbose flag to search command

Add --verbose flag to show detailed output.
Shows context for each match.

Closes: #42
```

```
fix(patterns): handle empty text input

Return empty dict when text is empty.
Prevents IndexError in PatternDetector.

Fixes: #38
```

```
docs(README): update installation instructions

Clarify pipx installation as recommended method.
Remove pip installation from main section.
```

### Git Email

**Use GitHub noreply email**:
```bash
git config user.email "YOUR_ID+username@users.noreply.github.com"
```

This protects your privacy while linking commits to your GitHub account.

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
