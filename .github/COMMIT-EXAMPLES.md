# Commit Examples

PURPOSE: Examples of Conventional Commits for traceflux.

REFERENCE: CONTRIBUTING.md for full guidelines
REFERENCE: COMMIT_CONVENTION.md for detailed rules

---

## Format

```text
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
| refactor | None | Code restructuring |
| style | None | Formatting, linting |
| docs | None | Documentation only |
| test | None | Test files only |
| chore | None | Tools, scripts, config |
| ci | None | CI/CD configuration |
| build | None | Build system, deps |

---

## Examples by Type

### feat - New Features

```bash
git commit -m "feat(cli): add search command"
git commit -m "feat(associations): add multi-hop traversal"
git commit -m "feat(api)!: change output format"
```

### fix - Bug Fixes

```bash
git commit -m "fix(scanner): handle empty input"
git commit -m "fix(cli): prevent crash on missing path"
```

### perf - Performance

```bash
git commit -m "perf(index): improve search speed"
git commit -m "perf(graph): optimize PageRank"
```

### refactor - Code Restructuring

```bash
git commit -m "refactor(scanner): simplify pattern detection"
git commit -m "refactor(graph): reduce memory usage"
```

### style - Formatting

```bash
git commit -m "style: format code with black"
git commit -m "style: fix flake8 errors"
```

### docs - Documentation

```bash
git commit -m "docs(readme): update installation guide"
git commit -m "docs: add API documentation"
```

### test - Tests

```bash
git commit -m "test: add unit tests for scanner"
git commit -m "test(associations): add integration tests"
```

### chore - Maintenance

```bash
git commit -m "chore(scripts): add release.sh"
git commit -m "chore(deps): upgrade pytest to v8"
git commit -m "chore: update .gitignore"
```

### ci - CI/CD

```bash
git commit -m "ci: add GitHub Actions workflow"
git commit -m "ci: update test matrix"
```

### build - Build System

```bash
git commit -m "build: configure setuptools"
git commit -m "build: add PDM configuration"
```

---

## Common Mistakes

### Wrong Type

```bash
# Wrong: Scripts are chore, not feat
git commit -m "feat(scripts): add release.sh"

# Correct
git commit -m "chore(scripts): add release.sh"
```

```bash
# Wrong: Lint is style, not fix
git commit -m "fix: lint errors"

# Correct
git commit -m "style: fix lint errors"
```

### Missing Scope

```bash
# Vague
git commit -m "feat: add new feature"

# Specific
git commit -m "feat(cli): add search command"
```

### Wrong Mood

```bash
# Past tense
git commit -m "feat: added search command"

# Imperative mood
git commit -m "feat: add search command"
```

---

## Scope Guidelines

### Valid Scopes

| Scope | When to Use |
|-------|-------------|
| cli | CLI commands, args |
| scanner | Text scanning |
| graph | Co-occurrence, PageRank |
| associations | Association discovery |
| patterns | Pattern extraction |
| index | Index, search |
| scripts | Dev scripts |
| tests | Test files |
| docs | Documentation |
| ci | CI/CD |
| deps | Dependencies |

### Rules

1. Use scope for specific components
2. Omit for cross-cutting changes
3. Keep lowercase and short

---

## Breaking Changes

Add `!` after type/scope:

```bash
git commit -m "feat(api)!: change output format"
git commit -m "refactor(scanner)!: simplify API"
```

---

RELATED: CONTRIBUTING.md, COMMIT_CONVENTION.md, RELEASE_PROTOCOL.md

Last Updated: 2026-03-11
