# Linear Project Structure

Use this reference when creating or restructuring a Linear project.

## Standard Milestones

Use these names unless the project calls for domain-specific variants:

- Agent Bootstrap & Triage
- Security, Auth & Permission Guardrails
- Data Integrity & Business Logic
- Sync, Cron & Integration Reliability
- Database, Performance & Query Safety
- Frontend, UX & Accessibility
- Final Verification, Release & Monitoring

For non-web codebases, adapt the names but keep the same intent.

## Standard Labels

Create or reuse:

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

Optional execution labels:

- `agent:queued`
- `agent:planning`
- `agent:executing`
- `agent:verifying`
- `agent:blocked`
- `agent:pr-ready`
- `agent:failed`

Execution labels do not replace Linear issue status.

## Parent Issues

Create parent workstreams as ownership envelopes. Each parent should explain:

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

## Reference Links
- Related Linear issues, blockers, docs, PRs, commits, source files, or ledger anchors.
- Only include links that change implementation, sequencing, verification, or recovery.

## Docs / Local Rules
- Context7 library IDs and direct docs links.
- Local AGENTS/CLAUDE/rule files.

## Agent Notes
- Parallel-safe or serial-required.
- Known overlap files/modules.
- Owned write scope and non-owned areas.
- Required verification command.
- Follow-up/backfill/migration notes.
```

## Safe Parallelism Planning

After project creation/read-back, mark a checkpoint in the operating guide or
ledger. Repeat the checkpoint after material completions, blockers, or scope
changes.

Checkpoint questions:

- Which `agent-ready` issues are independent and unblocked?
- What is the dependency order, write scope, risk level, and verification
  overlap?
- Which issues need separate branches/worktrees for write-capable agents?
- Which read-only/context-heavy tasks can run in bounded parallel for context
  isolation across research, audit, read-back, verification, large
  docs/logs/diffs, issue histories, or reference material?
- Does any issue need splitting into follow-ups before safe parallel execution?

Mark issues `serial-required` when they have dependencies, shared files/modules,
unclear ownership, production or sink gates, verification coupling, or
coordinator-level decision context.

## Research As Planned Work

When the user asks for a Linear project and also asks for research, source
review, or exploratory discovery, create first-class research issues.

Research issue acceptance criteria should include:

- source scope and priority order
- output artifact path
- citation or source-link requirements
- what counts as confirmed versus inferred
- downstream blockers that wait for the research result

Minimal inspection before plan creation is allowed when it is needed to shape
the issue graph, but substantive findings should live in tracked Linear work.

## Sparse Link Graph

Use links as context compression:

- parent/child structure shows execution shape
- `blocks`, `blockedBy`, and `relatedTo` show sequencing and risk
- docs links explain technical choices
- source file, PR, commit, and branch links show where work happened
- ledger links preserve execution memory
- verification links prove completion

Normal child issues should usually have 3-7 high-signal links. Guide issues,
verification matrices, and final release gates may carry more.

If Linear rejects optional relationships, preserve the intended graph in the
ledger and mark it blocked or not applicable with a reason. Do not pretend the
board is complete until read-back proves it.
