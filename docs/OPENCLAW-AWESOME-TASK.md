<!-- docs/OPENCLAW-AWESOME-TASK.md -->
# OpenClaw Awesome List Promotion Task

**Purpose**: Set up automated status checking for traceflux awesome list submissions using OpenClaw sub-agents.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Main Session (User)                       │
│  - User interacts with OpenClaw                              │
│  - Receives notifications                                    │
│  - Approves new submissions                                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ sessions_spawn (periodic)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Isolated Sub-Agent Session                      │
│  - Loads state file                                          │
│  - Checks PR status via gh CLI                               │
│  - Updates state file                                        │
│  - Notifies user of changes                                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ State File
                            ▼
┌─────────────────────────────────────────────────────────────┐
│         .github/awesome-submissions.json                     │
│  - Submission records                                        │
│  - Status history                                            │
│  - Rate limit tracking                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Setup Instructions

### Step 1: Enable GitHub Auth

Ensure OpenClaw has GitHub access:

```bash
gh auth status
# Should show: Logged in to github.com as <username>
```

### Step 2: Add to HEARTBEAT.md

Edit workspace `HEARTBEAT.md`:

```markdown
# traceflux Awesome List Promotion

**Frequency**: Every 2-3 days (avoid spam)

## Tasks

- [ ] Check pending PR status (`traceflux/scripts/check-awesome-status.py`)
- [ ] Notify user if status changed
- [ ] Weekly: Search for new awesome lists (max 2 per week)
- [ ] Prepare submission PRs for user approval

## Rate Limits

- Max 2 submissions per week
- Min 7 days between submissions
- Respect maintainer decisions
```

### Step 3: Spawn Sub-Agent (Manual Trigger)

From main session:

```python
sessions_spawn(
    runtime="subagent",
    label="traceflux-awesome-check",
    task="""
    Check traceflux awesome list submission status:
    
    1. cd /home/openclaw/tracer/dev-repo/traceflux
    2. python scripts/check-awesome-status.py
    3. Report any status changes
    4. If no changes, reply HEARTBEAT_OK
    """,
    mode="run"  # One-shot execution
)
```

### Step 4: Automated Scheduling (Optional)

If OpenClaw supports cron-like scheduling, add to gateway config:

```yaml
# ~/.openclaw/gateway/config.yaml
scheduled_tasks:
  - name: traceflux-awesome-check
    schedule: "0 10 */3 * *"  # Every 3 days at 10:00
    command: |
      sessions_spawn \
        --runtime subagent \
        --label traceflux-awesome-check \
        --task "Check awesome list PR status"
```

---

## Sub-Agent Task Template

When spawning a sub-agent, use this task template:

```
You are checking traceflux awesome list submission status.

**Steps**:

1. Navigate to traceflux repo:
   cd /home/openclaw/tracer/dev-repo/traceflux

2. Run status checker:
   python scripts/check-awesome-status.py

3. If status changed:
   - Report: which PR, old status, new status
   - Ask user: "Want to prepare next submission?"

4. If no changes:
   - Reply: "No status changes. [X] pending, [Y] accepted, [Z] rejected"
   - Reply: HEARTBEAT_OK

5. If errors:
   - Report error details
   - Ask for help if needed

**State file**: .github/awesome-submissions.json
**Script**: scripts/check-awesome-status.py
```

---

## Notification Examples

### Status Changed (Accepted)

```
📢 **traceflux Awesome List Update**

✅ **Accepted**: vinta/awesome-python
PR: #12345
URL: https://github.com/vinta/awesome-python/pull/12345

Maintainer comment: "Great tool! Added to Text Processing section."

**Stats**: 1 accepted, 0 rejected, 2 pending

Want to prepare next submission? (Rate limit: 1 more this week)
```

### Status Changed (Rejected)

```
📢 **traceflux Awesome List Update**

❌ **Rejected**: frutik/awesome-search
PR: #67890
Reason: "Project needs more stars (current: 45, minimum: 50)"

**Stats**: 0 accepted, 1 rejected, 2 pending

**Recommendation**: Wait until 50+ stars, then retry.
```

### No Changes

```
**traceflux Awesome List Check**

No status changes since last check.

**Current Stats**:
- Accepted: 1
- Rejected: 0
- Pending: 2

Next check: in 3 days (rate limit respected)

HEARTBEAT_OK
```

---

## Submission Workflow

### Phase 1: Search (Weekly)

```python
sessions_spawn(
    label="awesome-search",
    task="""
    Search for new awesome lists for traceflux:
    
    1. Use gh CLI to search:
       gh search repos "awesome-python" --limit 20
       gh search repos "awesome-search" --limit 20
       gh search repos "awesome-text" --limit 20
    
    2. Filter by:
       - Stars > 1000 (popular lists)
       - Updated in last 6 months (maintained)
       - Has CONTRIBUTING.md (clear rules)
    
    3. Check .github/awesome-submissions.json
       - Skip already searched
       - Skip blacklisted
    
    4. Report: Top 5 new candidates with reasons
    """
)
```

### Phase 2: Prepare (User Approval)

```python
sessions_spawn(
    label="awesome-prepare",
    task="""
    Prepare submission for: vinta/awesome-python
    
    1. Read CONTRIBUTING.md
    2. Check requirements:
       - Project age: gh log --since="30 days ago"
       - Stars: gh api repos/tracer-mohist/traceflux --jq .stargazers_count
       - License: Check LICENSE file
    
    3. Draft PR description:
       - Follow template from CONTRIBUTING.md
       - Highlight unique value (associative discovery)
    
    4. Save draft to: .github/drafts/awesome-python-pr.md
    5. Ask user: "Ready to submit? [y/n]"
    """
)
```

### Phase 3: Submit (User Confirmation)

```python
sessions_spawn(
    label="awesome-submit",
    task="""
    Submit traceflux to vinta/awesome-python
    
    1. Fork repo:
       gh repo fork vinta/awesome-python --clone
    
    2. Add entry to README.md:
       - Find correct category section
       - Add: [traceflux](https://github.com/tracer-mohist/traceflux) - Description
    
    3. Commit:
       git commit -m "Add traceflux to Text Processing"
    
    4. Create PR:
       gh pr create --title "Add traceflux" --body-file .github/drafts/awesome-python-pr.md
    
    5. Update state:
       - Add submission record
       - Set status: pending
       - Save PR number
    
    6. Report: PR URL, next check date
    """
)
```

---

## State File Schema

```json
{
  "version": "integer",
  "createdAt": "ISO8601",
  "lastUpdated": "ISO8601",
  
  "searchProgress": {
    "repo/name": {
      "searchedAt": "ISO8601",
      "found": "boolean",
      "category": "string",
      "hasContributing": "boolean",
      "notes": "string"
    }
  },
  
  "submissions": [
    {
      "id": "string (unique)",
      "repo": "string (owner/repo)",
      "category": "string",
      "submittedAt": "ISO8601",
      "prNumber": "integer",
      "prUrl": "string",
      "status": "pending|accepted|rejected|withdrawn",
      "statusHistory": [
        {
          "status": "string",
          "timestamp": "ISO8601",
          "source": "string"
        }
      ],
      "notes": "string"
    }
  ],
  
  "blacklist": [
    {
      "repo": "string",
      "reason": "string",
      "cooldownUntil": "ISO8601"
    }
  ],
  
  "stats": {
    "totalSearched": "integer",
    "totalSubmitted": "integer",
    "accepted": "integer",
    "rejected": "integer",
    "pending": "integer",
    "withdrawn": "integer"
  },
  
  "rateLimit": {
    "maxPerWeek": "integer (default: 2)",
    "minDaysBetween": "integer (default: 7)",
    "lastSubmission": "ISO8601|null"
  }
}
```

---

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `gh: not authenticated` | No GitHub login | Run `gh auth login` |
| `PR not found` | Wrong repo/PR number | Check state file accuracy |
| `Rate limit exceeded` | Too many API calls | Wait 1 hour, retry |
| `State file corrupted` | JSON parse error | Restore from git backup |

### Recovery Steps

```bash
# 1. Check gh auth
gh auth status

# 2. Validate state file
python -m json.tool .github/awesome-submissions.json

# 3. Restore from git if corrupted
git checkout .github/awesome-submissions.json

# 4. Manual status check
gh pr view vinta/awesome-python#12345
```

---

## Best Practices

### Do's

- ✅ Check status every 2-3 days (not daily)
- ✅ Respect rate limits (2/week max)
- ✅ Follow CONTRIBUTING.md exactly
- ✅ Respond to maintainer feedback within 48h
- ✅ Keep state file in git (version control)

### Don'ts

- ❌ Submit to more than 2 lists per week
- ❌ Submit to irrelevant categories
- ❌ Ignore rejection feedback
- ❌ Submit without checking requirements
- ❌ Spam maintainers with ping comments

---

## Success Metrics

Track these in state file `stats` section:

| Metric | Target | Measurement |
|--------|--------|-------------|
| Acceptance rate | >50% | accepted / total_submitted |
| Time to acceptance | <14 days | submitted_at → accepted_at |
| Lists covered | 5-10 | total unique repos |
| Star increase | +20% | before/after campaign |

---

## Related Files

- `docs/AWESOME-PROMOTION-DESIGN.md` - Full design document
- `.github/awesome-submissions.json` - State tracking
- `scripts/check-awesome-status.py` - Status checker script
- `HEARTBEAT.md` - OpenClaw heartbeat tasks

---

**Next Step**: Run first manual check to test the workflow

```bash
cd /home/openclaw/tracer/dev-repo/traceflux
python scripts/check-awesome-status.py
```
