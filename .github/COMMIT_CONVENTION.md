# Commit Message Convention

**Based on**: [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)

---

## Quick Reference

### Commit Types

| Type | When to Use | SemVer Impact |
|------|-------------|---------------|
| `feat` | New **product** feature (user-facing) | MINOR (v1.0.0 → v1.1.0) |
| `fix` | **Product** bug fix | PATCH (v1.0.0 → v1.0.1) |
| `chore` | Development tools, scripts, maintenance | None |
| `style` | Formatting, linting (no logic change) | None |
| `refactor` | Code restructuring (no behavior change) | None |
| `docs` | Documentation only | None |
| `ci` | CI/CD configuration | None |
| `test` | Test files only | None |
| `build` | Build system, dependencies | None |
| `perf` | Performance improvements | None |

### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Rules**:
- Type: lowercase (feat, fix, chore, ...)
- Scope: lowercase, optional (cli, scanner, graph, ...)
- Description: imperative mood ("add" not "added")
- Body: optional context, wrap at 72 chars
- Footer: BREAKING CHANGE, Closes #123, etc.

---

## Type Guidelines

### ✅ DO Use `feat` For

- New CLI commands: `feat(cli): add search command`
- New features: `feat(scanner): add multi-language support`
- New output formats: `feat(output): add JSON output option`

### ❌ DON'T Use `feat` For

- Development scripts: `chore(scripts): add release.sh`
- Test files: `test: add unit tests for scanner`
- Documentation: `docs(readme): update installation`

---

### ✅ DO Use `fix` For

- Product bugs: `fix(scanner): handle empty input`
- CLI crashes: `fix(cli): prevent crash on missing path`
- Logic errors: `fix(graph): correct co-occurrence counting`

### ❌ DON'T Use `fix` For

- Lint errors: `style: fix flake8 errors`
- Formatting: `style: format code with black`
- Test fixes: `test: fix flaky test`

---

### ✅ DO Use `chore` For

- Scripts: `chore(scripts): add release.sh`
- Dependencies: `chore(deps): upgrade pytest to v8`
- Config files: `chore: update .gitignore`
- Scripts refactor: `chore(scripts): simplify release.sh`

---

### ✅ DO Use `style` For

- Lint fixes: `style: resolve flake8 errors`
- Formatting: `style: format code with black`
- Import order: `style: sort imports with isort`

---

### ✅ DO Use `refactor` For

- Product code restructuring: `refactor(scanner): simplify pattern detection`
- Simplifying logic: `refactor(graph): optimize memory usage`

### ❌ DON'T Use `refactor` For

- Scripts: `chore(scripts): refactor release.sh`

---

### ✅ DO Use `docs` For

- README updates: `docs(readme): add installation guide`
- API documentation: `docs: document scanner API`
- Comments: `docs: add docstrings to scanner`

---

### ✅ DO Use `ci` For

- GitHub Actions: `ci: add release workflow`
- CI configuration: `ci: update test matrix`

---

### ✅ DO Use `test` For

- Unit tests: `test: add unit tests for scanner`
- Integration tests: `test: add pipeline integration test`
- E2E tests: `test: add E2E workflow tests`

---

## Examples

### Good Commits

```
feat(cli): add search command

Add new 'search' subcommand for text pattern search.

Supports regex patterns and case-insensitive search.

Closes: #42
```

```
fix(scanner): handle empty input

Return empty result instead of crashing on empty input.
```

```
chore(scripts): add release.sh automation

Shell script for automated releases.

- Version validation (SemVer)
- Test execution
- Commit and tag creation
```

```
style: resolve flake8 errors

- Fix import ordering (I001)
- Remove unused imports (F401)
- Fix line length (E501)
```

```
refactor(scanner): simplify pattern detection

- Extract validation logic
- Reduce cyclomatic complexity
- Add type hints

BREAKING CHANGE: Scanner API signature changed
```

```
docs(readme): update installation guide

Add pip and uv installation methods.
```

```
ci: add GitHub Actions workflow

- test job (pytest)
- lint job (black/flake8/isort)
- release job (on tag push)
```

---

### Bad Commits

```
❌ feat(scripts): add release.sh
✅ chore(scripts): add release.sh
Reason: Scripts are development tools, not product features
```

```
❌ fix: Resolve flake8 errors
✅ style: Resolve flake8 errors
Reason: Lint is code style, not a bug
```

```
❌ refactor(scripts): simplify release.sh
✅ chore(scripts): simplify release.sh
Reason: Scripts refactor is maintenance, not product refactor
```

```
❌ Updated file.txt
✅ docs(readme): update installation guide
Reason: Missing type and scope
```

```
❌ fix: minor improvements
✅ style: remove trailing whitespace
Reason: Too vague, be specific
```

---

## Breaking Changes

Commits with BREAKING CHANGE introduce incompatible API changes:

```
feat(api)!: change scanner output format

BREAKING CHANGE: Scanner now returns dict instead of list.
```

```
refactor!: drop support for Python 3.10

BREAKING CHANGE: Minimum Python version is now 3.11.
```

---

## Scope Guidelines

### Valid Scopes

| Scope | When to Use |
|-------|-------------|
| `cli` | CLI commands, argument parsing |
| `scanner` | Text scanning, pattern detection |
| `graph` | Co-occurrence graph, PageRank |
| `associations` | Association discovery |
| `patterns` | Pattern extraction |
| `scripts` | Development scripts |
| `tests` | Test files |
| `docs` | Documentation |
| `ci` | CI/CD configuration |
| `deps` | Dependencies |

### Scope Rules

1. Use scope when change affects specific component
2. Omit scope for cross-cutting changes
3. Keep scope lowercase, short, and clear

---

## Tools

### Commit Linting (Future)

Add to CI:
```yaml
- name: Lint commit messages
  uses: wagoid/commitlint-github-action@v5
  with:
    config-file: .commitlintrc.json
```

### Pre-commit Hook (Optional)

```bash
# .git/hooks/commit-msg
#!/bin/sh
npx --no -- commitlint --edit "$1"
```

---

## References

- [Conventional Commits Spec](https://www.conventionalcommits.org/en/v1.0.0/)
- [Angular Convention](https://github.com/angular/angular/blob/master/CONTRIBUTING.md)
- [Semantic Versioning](https://semver.org/)
- [traceflux#35](https://github.com/tracer-mohist/traceflux/issues/35)

---

**Last Updated**: 2026-03-10  
**Status**: Draft (pending review)
