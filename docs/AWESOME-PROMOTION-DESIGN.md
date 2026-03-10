<!-- docs/AWESOME-PROMOTION-DESIGN.md -->
# traceflux Awesome List Promotion Design

**Date**: 2026-03-07  
**Status**: Design Draft  
**Author**: Tracer

---

## Overview

Automated system to promote traceflux by submitting to relevant GitHub awesome lists.

**Core Concept**: 
- Search for relevant awesome lists
- Check submission requirements
- Submit PRs automatically
- Track submission status

---

## Target Awesome Lists

### Priority 1 (High Relevance)

| Repo | Category | Why |
|------|----------|-----|
| `vinta/awesome-python` | Python | Most popular Python list |
| `frutik/awesome-search` | Search | Direct category match |
| `awesomelistsio/awesome-nlp` | NLP/Text | Text analysis tools |
| `fighting41love/funNLP` | Chinese NLP | Chinese community |

### Priority 2 (Medium Relevance)

| Repo | Category | Why |
|------|----------|-----|
| `krzjoa/awesome-python-data-science` | Data Science | Pattern discovery |
| `mahmoud/awesome-python-applications` | Applications | CLI tools |
| `hastagAB/Awesome-Python-Scripts` | Scripts | Automation scripts |

---

## State Management

### State File: `.github/awesome-submissions.json`

```json
{
  "version": 1,
  "lastUpdated": "2026-03-07T20:00:00Z",
  "searchProgress": {
    "awesome-python": {
      "searchedAt": "2026-03-07T20:00:00Z",
      "found": true,
      "category": "Text Processing",
      "requirements": "CONTRIBUTING.md exists"
    }
  },
  "submissions": [
    {
      "id": "awesome-python-001",
      "repo": "vinta/awesome-python",
      "category": "Text Processing",
      "submittedAt": "2026-03-07T20:00:00Z",
      "prNumber": 12345,
      "prUrl": "https://github.com/vinta/awesome-python/pull/12345",
      "status": "pending",
      "statusHistory": [
        {"status": "pending", "timestamp": "2026-03-07T20:00:00Z"}
      ],
      "notes": "Awaiting review"
    }
  ],
  "results": {
    "accepted": 0,
    "rejected": 0,
    "pending": 1
  }
}
```

### State Fields

| Field | Type | Purpose |
|-------|------|---------|
| `searchProgress` | Object | Track which lists have been searched |
| `submissions` | Array | All submission records |
| `submissions[].status` | String | `pending` / `accepted` / `rejected` / `withdrawn` |
| `submissions[].statusHistory` | Array | Full status change log |
| `submissions[].prNumber` | Integer | GitHub PR number for tracking |
| `results` | Object | Quick summary stats |

---

## OpenClaw Integration

### Session Architecture

```
Main Session (User)
    │
    ├─► sessions_spawn (isolated)
    │   runtime: "subagent"
    │   label: "awesome-promotion"
    │   task: "Check and submit to awesome lists"
    │
    └─► State File: .github/awesome-submissions.json
```

### Cron/Heartbeat Setup

**Option 1: Heartbeat (Recommended for OpenClaw)**

Edit `HEARTBEAT.md`:
```markdown
# Awesome List Promotion Check
# Run every 2-3 days to avoid spam

- [ ] Check PR status for pending submissions
- [ ] Search for new awesome lists (weekly)
- [ ] Submit to 1-2 new lists per week (rate limit)
```

**Option 2: Cron Job (If Available)**

```bash
# Every 3 days at 10:00 AM
0 10 */3 * * openclaw sessions_spawn --label awesome-promotion --task "Check awesome list submissions"
```

### Sub-agent Task Flow

```
1. Load state file (.github/awesome-submissions.json)
2. Check pending PRs status via gh CLI
3. Update state with new status
4. If accepted/rejected → notify user
5. Search for new awesome lists (if weekly)
6. Select 1-2 targets (rate limit)
7. Check CONTRIBUTING.md requirements
8. Prepare submission PR
9. Submit (with user confirmation for first time)
10. Update state file
```

---

## Submission Requirements

### Common Requirements

| Requirement | Check Method |
|-------------|--------------|
| Project age (>30 days) | `git log --date=short --format=%ad` |
| Stars (>50) | `gh api repos/tracer-mohist/traceflux --jq '.stargazers_count'` |
| License (MIT) | Check LICENSE file |
| README quality | Manual review |
| CONTRIBUTING.md format | Parse submission template |

### Submission Template

```markdown
## traceflux

**Description**: A text search engine with associative discovery. Discovers what you don't know to search for.

**URL**: https://github.com/tracer-mohist/traceflux

**Tags**: search, text-analysis, pattern-discovery, python, cli

**Why**: Unlike traditional search (find what you know), traceflux discovers related concepts you didn't know to search for using co-occurrence graphs and PageRank.
```

---

## Rate Limiting & Etiquette

### Rules

1. **Max 2 submissions per week** - Avoid spam perception
2. **Wait 1 week between submissions** - Give maintainers time
3. **Check if project fits** - Don't submit to irrelevant lists
4. **Follow CONTRIBUTING.md exactly** - Respect maintainer rules
5. **Respond to feedback promptly** - Be professional

### Blacklist

```json
"blacklist": [
  {
    "repo": "some-repo/awesome-list",
    "reason": "Rejected - not enough stars",
    "cooldownUntil": "2026-06-07"
  }
]
```

---

## Failure Handling

### Failure Types

| Type | Action | Retry |
|------|--------|-------|
| Rejected (not relevant) | Log, don't retry | Never |
| Rejected (too new) | Log, retry after 30 days | Yes (1x) |
| Rejected (low stars) | Log, retry after reaching threshold | Yes (1x) |
| No response (>2 weeks) | Gentle ping comment | Yes (1x) |
| PR closed without merge | Ask reason, decide retry | Maybe |

### Notification Template

```markdown
**traceflux Awesome List Submission Update**

Repo: vinta/awesome-python
Status: ✅ Accepted / ❌ Rejected / ⏳ Pending
PR: #12345

Notes: [Maintainer comment if any]

Next action: [Wait / Retry different list / Stop]
```

---

## Implementation Phases

### Phase 1: Manual (Current)

- [ ] Create state file
- [ ] Manually search awesome lists
- [ ] Submit first PR manually
- [ ] Document process

### Phase 2: Semi-Auto (Next)

- [ ] OpenClaw sub-agent checks PR status
- [ ] Auto-update state file
- [ ] Notify user of changes
- [ ] User approves new submissions

### Phase 3: Full Auto (Future)

- [ ] Auto-search new awesome lists
- [ ] Auto-check requirements
- [ ] Auto-submit (with rate limits)
- [ ] Auto-respond to common feedback

---

## Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Acceptance rate | >50% | - |
| Lists submitted | 5-10 | 0 |
| Time to acceptance | <2 weeks | - |
| Traffic increase | +20% stars | - |

---

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Perceived as spam | High | Rate limit, quality submissions |
| Repeated rejections | Medium | Learn from feedback, improve |
| Maintainer burnout | Medium | Be respectful, follow rules |
| State file corruption | Low | Git version control, backups |

---

## Next Steps

1. **Create state file** - `.github/awesome-submissions.json`
2. **Search top 5 awesome lists** - Use gh CLI
3. **Check CONTRIBUTING.md** - Understand requirements
4. **Prepare first submission** - awesome-python or awesome-search
5. **Submit manually** - Test the process
6. **Build automation** - OpenClaw sub-agent for status checks

---

## Related Files

- `.github/awesome-submissions.json` - State tracking
- `CONTRIBUTING.md` - Submission guidelines (for incoming PRs)
- `docs/PROMOTION.md` - General promotion strategy

---

**Design Decision**: Start manual, automate gradually  
**Why**: Learn the process before encoding it  
**Assumptions**: traceflux meets basic requirements (stars, age, docs)
