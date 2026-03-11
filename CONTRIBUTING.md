# Contributing to traceflux

Thank you for contributing!

Start: docs/GETTING_STARTED.md, TESTING.md

---

## Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/traceflux.git
cd traceflux
pipx install -e .
git checkout -b issue/42-feature
# Changes, test, commit, push, PR
```

PRs required. No direct pushes to main.

---

## Commit Convention

Conventional Commits for versioning.

### Format

```text
<type>: <description>
```

### Types

| Type | Description | Version |
|------|-------------|---------|
| feat: | Feature | Minor |
| fix: | Bug fix | Patch |
| docs: | Docs | None |
| refactor: | Refactor | None |
| chore: | Maintenance | None |

### Breaking

```text
feat: remove API

BREAKING CHANGE: old_api() removed
```

-> Major bump.

### Examples

```bash
git commit -m "feat: add search"
git commit -m "fix: handle empty"
git commit -m "docs: update README"
```

Learn: https://www.conventionalcommits.org/

---

## What We Want

### High Priority

Bug Reports: Description, steps, expected vs actual, env.

Bug Fixes: Fix, test, docs.

Docs: Typos, examples.

Features: Use case, value.

### Not Wanted

- Premature optimization
- UNIX violations
- Unjustified breaking changes
- Unreviewed dependencies

---

## Setup

### Install

```bash
git clone https://github.com/YOUR_USERNAME/traceflux.git
cd traceflux
pipx install -e .
pytest -v
```

### Tests

```bash
pytest                    # All
pytest --cov=src/traceflux
pytest tests/test_x.py
pytest -k "pattern"
```

### Quality

```bash
pip install -e ".[dev]"
pip install black flake8 mypy
black src/ tests/
flake8 --max-line-length=100 src/
```

### Hooks

```bash
git config core.hooksPath .githooks
```

---

## PR Process

### Branch: issue/<num>-<desc>

### Before PR

1. Update docs
2. Add tests
3. Run pytest
4. Check black, flake8
5. Update CHANGELOG.md

### Submit

```bash
git checkout main && git pull
git checkout issue/42-feature
git rebase main
git commit -m "feat: add"
git push -u origin issue/42-feature
# Open PR
```

### Review

- Manual review
- CI/CD pass
- 1 maintainer approval

### Merge

Use merge commit. Delete branch after.

See .github/BRANCH_PROTECTION.md

---

## Code Style

- PEP 8
- Type hints (public APIs)
- Google/NumPy docstrings
- Max 100 chars
- Std lib first

```python
"""Module docstring."""

from typing import List


def func(param: str) -> List[str]:
    """Docstring.

    Args:
        param: Desc

    Returns:
        Desc
    """
    pass
```

---

## Commit Rules

- Lowercase: feat: add
- Imperative: add (not added)
- No period
- Max 72 chars

### Git Email

```bash
git config user.email "ID+user@users.noreply.github.com"
```

---

## Issue Templates

### Bug

```markdown
**Bug**: Desc
**Steps**: 1. Install 2. Run 3. Error
**Expected**: Should...
**Actual**: Did...
**Env**: Python 3.11, Ubuntu, v1.0.0
```

### Feature

```markdown
**Problem**: Desc
**Solution**: Want...
**Use case**: How?
```

---

## Principles

### UNIX

1. One Thing Well
2. Composability
3. Simplicity
4. Clarity

### traceflux

1. Discoverability
2. Performance
3. Privacy
4. Maintainability

---

## Security

Report privately via GitHub Security tab.

See SECURITY.md

---

## Questions?

- Discussions: github.com/tracer-mohist/traceflux/discussions
- Issues: github.com/tracer-mohist/traceflux/issues
License: MIT
