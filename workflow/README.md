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

Some workflows import from workflow-as-list:

```bash
# Example: Import commit workflow
curl -O https://raw.githubusercontent.com/tracer-mohist/workflow-as-list/refs/heads/main/examples/git/commit.workflow.list
```

See: workflow/commit.workflow.list

---

## Decision Capture

Use: .github/ISSUE_TEMPLATE/decision.yml
- Temporary decisions (< 6 months)
- Project-specific choices

Use: docs/
- Permanent rules
- General principles

See: workflow/decision-capture.workflow.list

---

See: workflow-as-list (parent project)
