# Self-Hosted Workflows

Purpose: Use workflow-as-list to manage traceflux development.

Not here: Generic templates - workflow-as-list/examples/

---

## What

Workflows in this directory manage traceflux development.

Bound to traceflux project (not reusable templates).

---

## Why

NOTE: Three reasons for self-hosting

1. Validation - Real usage validates workflow-as-list DSL
2. Feedback - Issues in traceflux - Improve workflow-as-list
3. Trust - We eat our own dogfood

---

## Usage

```bash
# From traceflux root
workflow check workflow/<name>.workflow.list
workflow approve <name>
workflow run <name>
```

Query structure: `ls workflow/`

---

## Remote Imports

Workflows use `import:` to reuse templates from workflow-as-list:

Example (workflow/commit.workflow.list):
```text
import: https://raw.githubusercontent.com/tracer-mohist/workflow-as-list/refs/heads/main/examples/git/commit.workflow.list
```

Benefits:
- Single source of truth (update once, all projects benefit)
- Test import functionality (DSL feature validation)
- Reduce duplication

---

## Decision Capture

Use: .github/ISSUE_TEMPLATE/decision.yml
- Temporary decisions (< 6 months)
- Project-specific choices

Use: docs/
- Permanent rules
- General principles

See: workflow/decision-capture.workflow.list (imports base + traceflux customization)

---

See: workflow-as-list (parent project)
