# Branch Protection & PR Workflow

PURPOSE: Branch protection rules for contributors and maintainers.

For API reference and technical details: See GITHUB-BRANCH-PROTECTION-RESEARCH.md

---

## Branch Protection Rules (Required)

Configure in GitHub: Settings -> Branches -> Add branch protection rule

### Rule: `main`

- [x] Require a pull request before merging
  - [x] Require approvals: 1
  - [x] Dismiss stale pull request approvals when new commits are pushed

- [x] Require status checks to pass before merging
  - [x] Require branches to be up to date before merging
  - [x] Status checks that are required:
    - [x] `test` (CI test job)
    - [x] `lint` (CI lint job)

- [x] Do not allow bypassing the above settings
  - (Applies to everyone, including maintainers)

- [x] Require conversation resolution before merging
  - (All review comments must be resolved)

### Why These Rules?

1. Prevent direct pushes - No one can push directly to main
2. Enforce code review - At least 1 approval required
3. Ensure CI passes - Tests and linting must pass
4. Maintain commit history - Preserve PR merge commits with proper messages

---

## Development Workflow

### 1. Create Issue

```bash
# On GitHub: Issues -> New Issue
# Or use GitHub CLI:
gh issue create --title "feat: add multi-hop search" --body "Description..."
```

### 2. Create Branch

Naming convention: `issue/<number>-<short-description>`

```bash
# Fetch latest
git checkout main
git pull origin main

# Create branch (example: issue #42)
git checkout -b issue/42-multi-hop-search
```

EXAMPLES:
- `issue/42-multi-hop-search`
- `issue/38-fix-empty-input`
- `issue/55-update-docs`

### 3. Develop & Commit

Follow Conventional Commits:

```bash
# Good commits
git commit -m "feat: add multi-hop association search"
git commit -m "fix: handle empty input gracefully"
git commit -m "docs: update installation guide"

# Bad commits (avoid)
git commit -m "fix stuff"
git commit -m "WIP"
git commit -m "asdfasdf"
```

Commit often - Small, focused commits are easier to review.

### 4. Push & Create PR

```bash
# Push branch
git push -u origin issue/42-multi-hop-search

# Create PR (using GitHub CLI)
gh pr create \
  --title "feat: add multi-hop association search" \
  --body "Closes #42" \
  --base main \
  --head issue/42-multi-hop-search
```

PR Title: Must follow Conventional Commits (same as commit messages)

PR Body: Use the template, reference the issue.

### 5. Review Process

As Author:
- Respond to feedback promptly
- Keep PR focused (don't add unrelated changes)
- Update branch if main changes: `git rebase origin/main`

As Reviewer:
- Check code quality
- Verify tests pass
- Ensure commit messages follow convention
- Test locally if needed

### 6. Merge Strategy

Use "Create a merge commit" (NOT squash or rebase):

```bash
Merge pull request #42 from tracer-mohist/issue/42-multi-hop-search

feat: add multi-hop association search
```

Why merge commits?
- Preserves individual commit history
- Clear traceability to PR and issue
- Easier to revert if needed
- Maintains context for future debugging

Avoid squash merge unless:
- PR has many small "fix typo" commits
- Commits don't follow convention (fix before merging instead)

---

## Conventional Commits Enforcement

### Automated Checks (Future)

Consider adding:
- [commitlint](https://commitlint.js.org/) - Lint commit messages
- [semantic-pull-requests](https://github.com/zeke/semantic-pull-requests) - Validate PR titles

### Manual Review (Current)

Reviewers must check:
1. PR title follows Conventional Commits
2. All commits follow convention (or will be squashed properly)
3. Merge commit message is correct

Common mistakes:
```bash
# Wrong
git commit -m "Added new feature"
git commit -m "FIX: something"
git commit -m "feat: Added new feature"  # Past tense, capitalized

# Right
git commit -m "feat: add new feature"
git commit -m "fix: handle edge case"
git commit -m "docs: update README"
```

Rules:
- Lowercase after type (feat: add, not feat: Add)
- Imperative mood (add, not added/adding)
- No period at end
- Max 72 chars for subject line

---

## Emergency Bypass

When: Critical hotfix needed immediately

PROCESS:
1. Create branch from main
2. Make minimal fix
3. Create PR with clear explanation
4. Request urgent review
5. Merge after approval (still required!)

Never: Disable branch protection for "quick fixes"

---

## Migration Plan

### Current State
-  Branch protection: Not enabled
-  Direct pushes to main: Allowed
-  PR workflow: Optional

### Target State
-  Branch protection: Enabled
-  Direct pushes to main: Blocked
-  PR workflow: Required

### Steps

1. Update documentation (this file, CONTRIBUTING.md)
2. Announce to contributors (README, discussions)
3. Enable branch protection (GitHub Settings)
4. Monitor first week - Help contributors adapt

---

## Related Files

- `CONTRIBUTING.md` - General contribution guidelines
- `pull_request_template.md` - PR template
- `RELEASE_PROTOCOL.md` - Release process
- `.github/workflows/ci.yml` - CI/CD configuration

---

LAST UPDATED: 2026-03-07
STATUS: Draft (pending branch protection enablement)
