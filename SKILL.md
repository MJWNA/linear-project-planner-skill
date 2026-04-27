---
name: linear-project-planner
description: >
  Plan, create, restructure, or execute Linear projects for audits, remediation,
  production hardening, and parallel agent work. Standardise Linear issues,
  milestones, labels, dependencies, verification gates, companion ledgers, agent
  execution hygiene, and completion comments for Codex or Claude agents working
  across any codebase.
metadata:
  short-description: Create agent-ready Linear remediation projects
---

# Linear Project Planner

Use this skill when creating or restructuring a Linear project so future Codex/Claude sessions can execute consistently across any codebase.

Also use it when executing a Linear project created for agents. The same structure that makes a backlog useful must be kept accurate while work happens.

## Core Rule

Create an execution system, not a flat todo list. Every project should tell a future agent:

- what order to work in
- which tasks can run in parallel
- which tasks are serial or risky
- what docs and local rules apply
- what verification proves completion
- what business outputs must not change
- where durable cross-session execution memory lives

## First Pass

Before creating issues:

1. Identify the repository, production context, and deployment surface.
2. Read project instructions (`AGENTS.md`, `CLAUDE.md`, `.claude/rules/**`, architecture docs).
3. Use Context7 for current docs when tasks touch frameworks, deployment, auth, ORM, validation, or SDKs.
4. If this is a live production app, add production-readiness and output-preservation gates before fix tickets.
5. Prefer milestones and parent issues over one giant issue list.
6. For agent-heavy projects, create a companion execution ledger before or alongside Linear issue creation.

## Standard Milestones

Use these milestone names unless the project calls for a domain-specific variant:

- Agent Bootstrap & Triage
- Security, Auth & Permission Guardrails
- Data Integrity & Business Logic
- Sync, Cron & Integration Reliability
- Database, Performance & Query Safety
- Frontend, UX & Accessibility
- Final Verification, Release & Monitoring

For non-web codebases, adapt labels but keep the same intent.

## Standard Labels

Create or reuse labels:

- `agent-ready`
- `parallel-safe`
- `serial-required`
- `overlap-zone`
- `needs-human-review`
- `verification-missing`
- `context-needed`
- `production-risk`
- `touches-auth`
- `touches-db`
- `touches-money`
- `touches-sync`
- `touches-frontend`
- `touches-security`

Add domain labels as needed, but do not replace these execution labels.

### Optional Agent Execution Labels

If the Linear workspace benefits from queue filtering or crash recovery, create namespaced execution labels and keep exactly one current state label on each active issue:

- `agent:queued`
- `agent:planning`
- `agent:executing`
- `agent:verifying`
- `agent:blocked`
- `agent:pr-ready`
- `agent:failed`

These labels are not replacements for Linear issue status. Status stays simple (`Backlog`, `Todo`, `In Progress`, `Done`, `Canceled`); `agent:*` labels describe agent execution state.

## Parent Issues

Create parent issues as workstream envelopes. Each parent should explain:

- ownership boundary
- non-goals
- sequencing rules
- verification expectation
- cross-issue risks

Typical parents:

- Guide: Agent Operating Guide
- Guide: Verification Matrix
- Workstream: Security/Auth
- Workstream: Data/Business Logic
- Workstream: Sync/Integrations
- Workstream: Database/Performance
- Workstream: Frontend/UX
- Workstream: Final Release/Monitoring

## Child Issue Template

Each issue should include:

```md
## Problem
What is wrong, risky, or missing.

## Evidence
- File paths, route names, logs, CLI findings, or audit references.

## Acceptance Criteria
- Concrete behavioral outcomes.
- Tests or CLI checks required.
- Production/readiness checks if applicable.

## Verification
- Exact commands or checks.
- Before/after comparison when output matters.

## Docs / Local Rules
- Context7 library IDs and direct docs links.
- Local AGENTS/CLAUDE/rule files.

## Agent Notes
- Parallel-safe or serial-required.
- Known overlap files/modules.
- Follow-up/backfill/migration notes.
```

## Required Guide Issues

Always add these two guide issues:

### Guide: Agent Operating Guide

Must include:

- how to choose work
- when to spawn parallel agents
- branch/worktree expectations
- dirty worktree warning
- docs lookup expectations
- how to update Linear while working
- where the companion execution ledger lives and when to update it
- how to hand off unfinished work

### Guide: Verification Matrix

Must include:

- baseline local checks
- domain-specific checks
- production/deployment checks
- browser/UI checks if relevant
- database migration checks
- rollback and post-deploy observation requirements

## Companion Execution Ledger

For agent-heavy Linear projects, create a durable Markdown ledger that survives context compaction and lets future sessions recover the original prompt, current work state, and todo progress without re-deriving the project.

The ledger complements Linear; it does not replace Linear issues, comments, statuses, or dependencies.

Default location:

```txt
.codex/linear-projects/<linear-project-slug>/EXECUTION.md
```

If multiple Git worktrees or parallel write agents will be used, prefer a coordinator-owned shared path outside individual worktrees so workers do not create divergent ledger copies:

```txt
../.codex-linear-ledgers/<linear-project-slug>/EXECUTION.md
```

Use `templates/EXECUTION.md` as the starting template when available.

The ledger must record:

- original user prompt or project brief
- Linear project URL or name
- operating guide issue and verification matrix issue
- repo path, base branch, active branches, and worktree paths
- overall state, active issue, current agent state, last verified time, and next safest action
- project creation checklist
- issue progress table with Linear status, agent state, worktree, last update, and verification
- decisions, blockers, risks, and handoff notes

Checklist state must be honest: keep `[ ]` for pending work, use `[x]` only for completed work, and use `[~]` with a short reason for conditional items that do not apply. Do not leave a conditional production, dependency, or sink/output item unchecked at project completion if it was deliberately not needed.

Update the ledger:

- after creating or restructuring the Linear project
- after creating guide issues, milestones, parents, children, labels, and dependencies
- when claiming an issue or starting implementation/investigation
- when a material discovery changes scope
- when blocked, handing off, or assigning work to another agent
- when verification passes or fails
- before marking an issue `Done`
- after the final Linear reconciliation, using a project-level finalize pass
- before context handoff or session completion

At the start of a resumed session, read the ledger, then reconcile it against Linear before choosing the next issue. If Linear and the ledger disagree, trust Linear for canonical issue status, trust comments for issue-level audit history, and update the ledger with the reconciliation result.

## Linear Transition Wrapper

For execution-state transitions, prefer the local `linear-agent` wrapper when available. The wrapper updates the companion ledger first and prints the exact Linear MCP actions the agent must perform and read-back verify.

Use it for:

- claiming work: `linear-agent start MAS-123 --ledger <path> --agent Codex --worktree <path>`
- recording blockers: `linear-agent block MAS-123 --ledger <path> --note "<blocker>"`
- recording verification: `linear-agent verify MAS-123 --ledger <path> --verification "<check>: <result>"`
- completing work: `linear-agent complete MAS-123 --ledger <path> --verification "<check>: <result>"`
- handoff: `linear-agent handoff --ledger <path> --note "<handoff>"`
- final project reconciliation: `linear-agent finalize --ledger <path> --verification "<Linear read-back and final checks>" --dependencies "satisfied" --production-gates "satisfied" --sink-gates "not-applicable:<reason>"`

`linear-agent init` refuses to overwrite an existing ledger unless `--force` is passed. Use `--force` only when replacing the prior ledger is intentional.

`linear-agent finalize` requires explicit dependency, production, and sink/output gate outcomes. Use `satisfied` when the gate was completed, or `not-applicable:<reason>` when the gate genuinely does not apply.

After running the wrapper, perform the printed Linear MCP actions using structured Linear tools, then verify with a read-back call. The wrapper is not a replacement for Linear itself; it is the deterministic transition path that keeps the ledger, comments, and issue status from drifting.

If the wrapper is unavailable, manually follow the same sequence:

1. Update the companion ledger.
2. Update Linear issue status with a structured issue update.
3. Add the progress, blocked, verification, completion, or handoff comment.
4. Read the issue back and confirm the expected state.
5. Record any mismatch in both Linear comments and the ledger.

## Production App Gates

For live production apps, add first-class issues for:

- production env/deployment readiness
- cron/job inventory if scheduled jobs exist
- auth/RBAC route inventory if user data exists
- data/business-output semantics if money, reporting, or compliance is involved
- sink/output behavior-lock matrix if sync/import/export flows exist

These are not optional. They prevent agents from fixing internals while breaking business outcomes.

## Sink / Output Preservation

For syncs, imports, ETL, webhooks, crons, reporting, AI pipelines, and other "sinks":

- Document the destination tables, UI surfaces, reports, alerts, and downstream jobs.
- Capture the current correct practical output before refactoring.
- Require before/after comparison, not only unit tests.
- Treat output changes as product changes requiring explicit approval.
- Include backfill/migration notes if historical data changes.

Use wording like:

> Preserve existing practical output unless this issue explicitly changes it. Internals may be messy; business-facing populated data is the contract.

## Sequencing Rules

Use dependencies when:

- one issue changes a shared predicate/helper used by another
- one issue changes a shared state machine
- one issue discovers scope for another
- docs/inventory must precede implementation
- production env must be verified before fail-closed behavior is enabled

Use `parallel-safe` only when write scopes and behavior contracts do not overlap.

## Mandatory Parallel Dispatch

When there are 2+ independent, dependency-ready workstreams with disjoint write scopes, the coordinator must dispatch parallel sub-agents instead of serialising the work in one session.

This is mandatory when all of these are true:

- at least two child issues are unblocked and `agent-ready`
- the issues do not depend on each other's implementation or discovery
- the owned files, modules, data contracts, migrations, or docs are disjoint
- verification for one issue does not require unmerged code from the other issue
- each agent can work in its own branch/worktree or the work is read-only

Do not dispatch parallel write-capable agents when ownership is unclear, when two issues may edit the same file/module, when one issue changes a shared helper/state machine used by another, or when a production/sink-output gate must be resolved first. Mark those issues `serial-required` or `overlap-zone` until the boundary is safe.

Before dispatching, the coordinator must define:

- the Linear issue each agent owns
- the branch and worktree path for each write-capable agent
- the exact owned write set: files, directories, modules, routes, scripts, migrations, or docs
- explicit non-owned areas the agent must not edit
- expected verification commands or checks
- reconciliation order and merge/read-back expectations

Parallel dispatch instructions must tell agents they are not alone in the codebase, must not revert other agents' changes, must stop and comment if ownership overlaps, and must leave completion comments with changed files, checks, residual risks, and follow-ups.

## Context7 Expectations

Use Context7 and direct docs links for:

- Next.js / React / frontend framework behavior
- Vercel / deployment / cron / serverless settings
- Prisma / Drizzle / database migrations
- Auth.js / NextAuth / auth libraries
- Zod / validation
- SDKs and provider APIs

Each issue that depends on current docs should include Context7 library IDs plus direct docs URLs.

## Status Update

After project creation or restructuring, post a project status update or parent comment summarising:

- new issue range
- highest-priority gates
- known serial dependencies
- production risks
- recommended first execution order
- companion execution ledger path

If status-update tooling is unavailable, add the summary as a comment on the operating guide issue.

## Execution State Hygiene

When working through an agent-ready Linear project:

- Read the companion execution ledger, operating guide, and verification matrix before choosing work.
- Choose work from issues that are `agent-ready`, not completed, not blocked, and highest priority within dependency order.
- If Linear's agent/delegate model is available, set the executing agent as delegate while keeping the human owner/assignee responsible where appropriate.
- Use `linear-agent` for execution-state transitions when available, then perform and verify the printed Linear MCP actions.
- Move an issue to `In Progress` when implementation or investigation starts.
- Add an acknowledgement comment before long-running work when the issue is claimed.
- Add a progress comment when a material discovery changes scope, when blocked, or when handing work to another agent.
- Keep issue relationships current: add blockers, related issues, duplicates, or follow-ups when discovered.
- Do not mark an issue `Done` until acceptance criteria and verification pass.
- Completion comments must include:
  - files/modules changed or inspected
  - checks run and results
  - production/log/browser/CLI verification if relevant
  - residual risks
  - follow-up issues created
- If the work changes issue scope, update the issue description or add a clear comment before continuing.
- If work reveals a sink/output behavior risk, stop and attach the risk to the issue before changing output behavior.
- For parallel agents, each agent must own a disjoint write scope before write work starts. If scopes overlap, stop and reconcile ownership through the coordinator and issue comments before continuing.
- Do not rely on parent auto-close for agent projects that need human review. Parents/workstreams should remain open until the final verification/release gate is complete.
- Update the companion execution ledger at each state transition so context compaction does not erase the working todo state.

## Parallel Code Execution With Worktrees

When executing code changes with multiple agents in the same repository, isolate write scopes with Git worktrees unless the work is read-only or the agent runtime already provides separate forked workspaces. Parallel write-capable agents must not share one working tree.

Use this pattern:

1. Start from the intended base branch and inspect dirty state.
2. Create one worktree per issue or tightly-coupled issue group.
3. Use a branch name tied to the issue, e.g. `codex/mas-50-ticket-escalation-cron`.
4. Assign each agent a clear worktree path and owned file/module scope.
5. Tell agents they are not alone in the codebase and must not revert unrelated changes.
6. Record the worktree path and owned write set in Linear and the companion ledger.
7. Merge/integrate branches deliberately after review, verification, and coordinator reconciliation.

Example:

```bash
git worktree add ../smd-mas-50 -b codex/mas-50-ticket-escalation-cron codex/full-codebase-audit
git worktree add ../smd-mas-59 -b codex/mas-59-sync-timeouts codex/full-codebase-audit
```

Avoid running two implementation agents in the same working tree when both can edit files. Use one shared worktree only for read-only audit agents or when a single coordinator is applying all patches.

The coordinator owns worktree safety:

- no overlapping write sets
- no agent reverts or rewrites another agent's changes
- no broad cleanup outside the owned issue scope
- no merge until each branch has passed its issue verification
- reconcile conflicts, shared contracts, and final integration deliberately before merge

Do not delete worktrees until their branches are merged, abandoned intentionally, or handed off with clear notes. Record worktree paths in Linear progress comments when parallel execution starts and in completion comments when work finishes.

### Completion Comment Template

```md
Completed.

Changed/inspected:
- ...

Verification:
- ...

Result:
- ...

Residual risks:
- ...

Follow-ups:
- ...
```

### Blocked Comment Template

```md
Blocked.

Blocker:
- ...

What I learned:
- ...

Safest next parallel issue:
- ...
```

Use this wording in guide issues:

```md
As you work through this Linear project, keep issue state accurate. Move an issue to In Progress when you start it, add progress comments when blocked or materially updated, move it to Done only after verification passes, and leave a completion comment with changed files, checks run, residual risks, and follow-up issues created.
```
