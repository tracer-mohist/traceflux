# GitHub Branch Protection Research

PURPOSE: GitHub API reference and technical details for maintainers.

For contributor rules: See BRANCH_PROTECTION.md

---

Date: 2026-03-10
Repository: tracer-mohist/traceflux

---

## Question

Is main branch protection effective for repo owner?

Answer: YES - When `enforce_admins: true`, protection applies to everyone including owner.

---

## Current Protection Settings

Retrieved via GitHub API:
```bash
gh api /repos/tracer-mohist/traceflux/branches/main/protection
```text

### Settings

| Setting | Value | Impact |
|---------|-------|--------|
| `enforce_admins` | `true` | Applies to repo owner |
| `allow_force_pushes` | `false` | No force push |
| `required_pull_request_reviews` | `1 approval` | PR + approval required |
| `required_status_checks` | `["CI"]` | CI must pass |

---

## Why Protection Applies to Owner

### GitHub's Design Philosophy

1. Prevent Accidents
   - Even owners make mistakes
   - Protection prevents accidental breaks

2. Audit Trail
   - All changes via PR
   - Creates clear history

3. CI Enforcement
   - Tests must pass before merge
   - Protects code quality

4. Team Consistency
   - Same rules for everyone
   - No special privileges

---

## Can Owner Bypass Protection?

### Option 1: Temporarily Disable (via API)

```bash
# Delete protection
gh api -X DELETE /repos/tracer-mohist/traceflux/branches/main/protection

# Push directly
git push origin main

# Re-enable protection
gh api -X PUT /repos/tracer-mohist/traceflux/branches/main/protection \
  -F required_status_checks='{"contexts":["CI"]}' \
  -F required_pull_request_reviews='{"required_approving_review_count":1}'
```text

RISK: Temporarily removes all protection

---

### Option 2: Modify Settings (via API)

```bash
# Allow force pushes for admin
gh api -X PUT /repos/tracer-mohist/traceflux/branches/main/protection \
  -F enforce_admins=false \
  -F allow_force_pushes=true
```text

RISK: Reduces protection level permanently

---

### Option 3: Use PR Workflow (Recommended)

```bash
# Create PR
gh pr create --title "Phase 8: Infrastructure" --body "See status report"

# Wait for CI

# Merge
gh pr merge --merge
```text

Benefit: Follows best practices, tests CI/CD

---

## GitHub API Endpoints

### Get Protection
```javascript
GET /repos/{owner}/{repo}/branches/{branch}/protection
```text

### Update Protection
```javascript
PUT /repos/{owner}/{repo}/branches/{branch}/protection
```text

Parameters:
- `required_status_checks`
- `required_pull_request_reviews`
- `enforce_admins`
- `allow_force_pushes`
- `allow_deletions`
- etc.

### Delete Protection
```javascript
DELETE /repos/{owner}/{repo}/branches/{branch}/protection
```text

---

## Recommendation

Use PR Workflow (Option 3)

Why:
1.  Follows best practices
2.  Tests CI/CD workflows
3.  Creates audit trail
4.  No security risk
5.  Proper Git workflow

---

## Related Files

- `.github/BRANCH-PROTECTION-ANALYSIS.md` - Detailed analysis
- `.github/PHASE8-STATUS.md` - Current status

---

Last Updated: 2026-03-10
