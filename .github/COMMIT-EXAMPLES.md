# Commit Examples

Purpose: Examples of Conventional Commits for traceflux.

REFERENCE: CONTRIBUTING.md for full guidelines
REFERENCE: .github/COMMIT_CONVENTION.md for detailed rules

---

## Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

---

## Types

| Type | Version Bump | When to Use |
|------|-------------|-------------|
| feat | MINOR | New features (user-facing) |
| fix | PATCH | Bug fixes |
| perf | PATCH | Performance improvements |
| refactor | None | Code restructuring (no behavior change) |
| style | None | Formatting, linting |
| docs | None | Documentation only |
| test | None | Test files only |
| chore | None | Development tools, scripts |
| ci | None | CI/CD configuration |
| build | None | Build system, dependencies |

---

## Examples by Type

### feat - New Features

```bash
# CLI command
git commit -m "feat(cli): add search command"

# With body
git commit -m "feat(associations): add multi-hop traversal

Add support for 2-hop and 3-hop association discovery.

Closes: #42"

# Breaking change
git commit -m "feat(api)!: change scanner output format

BREAKING CHANGE: Scanner now returns dict instead of list."
```

---

### fix - Bug Fixes

```bash
# Simple fix
git commit -m "fix(scanner): handle empty input"

# With body
git commit -m "fix(cli): prevent crash on missing path

Return error message instead of crashing.

Closes: #56"
```

---

### perf - Performance

```bash
git commit -m "perf(index): improve search speed"

git commit -m "perf(graph): optimize PageRank calculation"
```

---

### refactor - Code Restructuring

```bash
git commit -m "refactor(scanner): simplify pattern detection"

git commit -m "refactor(graph): reduce memory usage"
```

---

### style - Formatting

```bash
git commit -m "style: format code with black"

git commit -m "style: fix flake8 errors"

git commit -m "style: sort imports with isort"
```

---

### docs - Documentation

```bash
git commit -m "docs(readme): update installation guide"

git commit -m "docs: add API documentation"

git commit -m "docs(contributing): add commit examples"
```

---

### test - Tests

```bash
git commit -m "test: add unit tests for scanner"

git commit -m "test(associations): add integration tests"

git commit -m "test: fix flaky test"
```

---

### chore - Maintenance

```bash
# Scripts
git commit -m "chore(scripts): add release.sh"

# Dependencies
git commit -m "chore(deps): upgrade pytest to v8"

# Config files
git commit -m "chore: update .gitignore"

# Pre-commit
git commit -m "chore: add pre-commit configuration"
```

---

### ci - CI/CD

```bash
git commit -m "ci: add GitHub Actions workflow"

git commit -m "ci: update test matrix"

git commit -m "ci: add commitlint"
```

---

### build - Build System

```bash
git commit -m "build: configure setuptools"

git commit -m "build: add PDM configuration"
```

---

## Common Mistakes

### Wrong Type

```bash
# ❌ Wrong: Scripts are chore, not feat
git commit -m "feat(scripts): add release.sh"

# ✅ Correct
git commit -m "chore(scripts): add release.sh"
```

```bash
# ❌ Wrong: Lint is style, not fix
git commit -m "fix: lint errors"

# ✅ Correct
git commit -m "style: fix lint errors"
```

```bash
# ❌ Wrong: Scripts refactor is chore
git commit -m "refactor(scripts): simplify release.sh"

# ✅ Correct
git commit -m "chore(scripts): simplify release.sh"
```

---

### Missing Scope

```bash
# ❌ Vague
git commit -m "feat: add new feature"

# ✅ Specific
git commit -m "feat(cli): add search command"
```

---

### Wrong Mood

```bash
# ❌ Past tense
git commit -m "feat: added search command"

# ✅ Imperative mood
git commit -m "feat: add search command"
```

---

## Scope Guidelines

### Valid Scopes

| Scope | When to Use |
|-------|-------------|
| cli | CLI commands, argument parsing |
| scanner | Text scanning, pattern detection |
| graph | Co-occurrence graph, PageRank |
| associations | Association discovery |
| patterns | Pattern extraction |
| index | Index building, search |
| scripts | Development scripts |
| tests | Test files |
| docs | Documentation |
| ci | CI/CD configuration |
| deps | Dependencies |

### Scope Rules

1. Use scope when change affects specific component
2. Omit scope for cross-cutting changes
3. Keep scope lowercase, short, and clear

---

## Breaking Changes

Add `!` after type/scope:

```bash
git commit -m "feat(api)!: change output format"

git commit -m "refactor(scanner)!: simplify API

BREAKING CHANGE: Scanner API signature changed."
```

---

## Related Files

- CONTRIBUTING.md - Full contribution guidelines
- .github/COMMIT_CONVENTION.md - Detailed commit convention
- .github/RELEASE_PROTOCOL.md - Release process

---

Last Updated: 2026-03-10
