---
name: linear-project-planner
description: >
  Plan, create, restructure, or execute Linear projects for audits, remediation,
  production hardening, and parallel agent work. Use when the user asks to
  create a Linear project, run the Linear skill, execute a Linear plan, organize
  multi-agent work, preserve a companion ledger, add milestones/dependencies,
  or close work with verification gates for Codex or Claude agents.
metadata:
  short-description: Create agent-ready Linear remediation projects
---

# Linear Project Planner

Use this skill when creating, restructuring, auditing, or executing a Linear
project so future Codex/Claude sessions can work from the same execution system.
Do not use it for a simple one-off Linear issue lookup unless the user also asks
for planning, remediation, execution tracking, or project-level coordination.

## Core Rule

Create an execution system, not a flat todo list. Every project should tell a
future agent:

- what order to work in
- which tasks can run in parallel
- which tasks are serial or risky
- what docs and local rules apply
- what verification proves completion
- what business outputs must not change
- where durable cross-session execution memory lives
- what project principles or fundamentals should guide repeated decisions
- how newly discovered work becomes issues, candidates, or durable notes

## Quick Path

1. Read local project rules and create or open the companion ledger.
2. Create or update the Linear project with guide issues, parent workstreams,
   child issues, labels, milestones, dependencies, and sparse reference links.
3. Put user-requested research, source review, audits, and exploratory discovery
   inside the Linear plan when the user is asking for a Linear project. Minimal
   repo inspection needed to shape the plan is allowed before issue creation;
   substantive findings belong in tracked issues.
4. Apply Continuous Issue Discovery throughout planning and execution: create
   required issues, propose useful non-blocking candidates, and log context-only
   findings.
5. Run a safe parallelism checkpoint after project creation or read-back, then
   claim work with `linear-agent start`; use separate branches and worktrees for
   independent write-capable agents.
6. Verify every issue before `linear-agent complete`, then mirror the Linear
   status/comment and read it back.
7. Run final verification, reconcile Linear, and finalize only with explicit
   evidence.

## Expanded Mode

Use expanded mode only when the user explicitly asks for expanded mode,
long-horizon planning, detailed multi-phase planning, deep research first,
dependency mapping, local project docs or references, software-firm-grade
planning, multi-team delivery, or heavy safe parallel-agent coordination.

Baseline mode remains the default for ordinary Linear planning, execution,
audits, remediation, companion ledgers, dependencies, safe-parallelism
checkpoints, and verification gates. Do not create expanded-mode docs folders,
research dossiers, or provenance policies for ordinary baseline projects.

When expanded mode is triggered, load `references/expanded-mode.md` after the
normal local project rules and before creating the project graph.

## Reference Map

Load deeper references only when the current task needs them:

- `references/operator-cheatsheet.md`: one-page minimal safe path.
- `references/project-structure.md`: milestones, labels, parent issues, child
  issue template, safe parallelism planning, sparse link graph, and
  research-as-planned-work template.
- `references/project-principles.md`: scaled Project Principles / Fundamentals
  surfaces, compact baseline sections, promotion rules, and amendments.
- `references/execution-hygiene.md`: companion ledger, `linear-agent`,
  issue-state hygiene, safe parallelism checkpoints, worktrees, completion
  comments, and finalization.
- `references/source-checkpoints.md`: phase-based source rereading model for
  kickoff, planning, issue creation, implementation, parallel delegation, scope
  changes, verification, handoff, and closeout.
- `references/validation-modes.md`: standard validation, optional deep
  auto-research validation, production gates, and sink/output preservation.
- `references/trigger-preservation.md`: trigger-safe front-door contract for
  maintaining this skill.
- `references/command-schemas.md`: structured `linear_project.*` command
  contract for future MCP/function-tool layers.
- `references/runtime-state.md`: model/runtime guidance, Responses API state
  continuity, and compaction recovery.
- `references/expanded-mode.md`: opt-in long-horizon planning workflow for deep
  research, local docs, dependency maps, provenance, multi-agent allocation,
  synthesis gates, dogfood, and baseline contamination safeguards. Load only
  after an expanded-mode trigger is present.
- `references/repository-hardening.md`: CI, release, CodeQL, branch/ruleset, and
  solo-maintainer hardening policy.
- `templates/EXECUTION.md`: companion ledger shape and checklist semantics.
- `templates/project-principles.md`: full companion principles document for
  larger, ambiguous, or expanded-mode projects.
- `templates/production-gates.md`: production and sink/output inventory gates.
- `scripts/linear-agent`: local transition wrapper, direct Linear mode,
  reconciliation, and finalization guards.
- `tests/fixtures/linear_issue_templates.md`: expected issue and final comment
  output shape.

## First Pass

Before creating issues:

1. Identify the repository, production context, deployment surface, and whether
   business outputs or sync sinks are in scope.
2. Read project instructions such as `AGENTS.md`, `CLAUDE.md`,
   `.claude/rules/**`, architecture docs, and relevant local runbooks.
3. Use Context7, official docs, or tracked research issues for current
   framework, SDK, API, deployment, auth, database, or validation decisions.
4. Add production-readiness and output-preservation gates before risky
   implementation tickets when the work touches a live app or sink.
5. Prefer milestones, guide issues, and parent workstreams over one giant issue
   list.
6. Create a companion execution ledger before or alongside Linear issue
   creation.
7. Capture a Project Principles / Fundamentals surface; keep it compact for
   small baseline projects and promote it only when the project needs a
   separate durable decision reference.
8. Add a compact project description with goal, source of truth, scope,
   non-scope, workstreams, dependency/blocker policy, Continuous Issue
   Discovery rule, verification expectations, and handoff/context recovery
   notes when relevant.
9. Use issue bodies that survive context loss: objective, context, scope,
   dependencies/blockers, acceptance criteria, verification, and future-agent
   notes.
10. Build a sparse link graph across tasks, docs, source artifacts, and
   verification evidence.
11. Apply `references/source-checkpoints.md` when the project will span
    planning, execution, parallel agents, scope changes, verification, handoff,
    or closeout.
12. Classify validation depth: standard by default; deep auto-research only when
   explicitly requested, approved, or clearly triggered.

## Required Guide Issues

Always add these two guide issues:

### Guide: Agent Operating Guide

Include how to choose work, safe parallelism checkpoint cadence, dependency
order, branch/worktree expectations, dirty worktree warnings, docs lookup
expectations, Linear update rules, ledger path, handoff expectations, and the
first safest issue.

### Guide: Verification Matrix

Include baseline local checks, domain-specific checks, production/deployment
checks when relevant, browser/UI checks when relevant, database migration checks
when relevant, rollback/post-deploy observation requirements, binary/frozen
evaluators, validation mode, and final read-back requirements.

## Continuous Issue Discovery

Treat the original Linear plan as a starting model, not a sacred list. During
research, implementation, testing, review, documentation, handoff, release, and
coordination, classify newly discovered work as one of:

- Blocker
- Dependency
- Defect
- Research follow-up
- Implementation follow-up
- Decision required
- QA / verification gap
- Documentation gap
- Scope expansion
- Risk / mitigation

Create a Linear issue immediately when the work blocks current execution,
affects correctness, is required for acceptance, or creates a real dependency.
Propose an issue candidate when it may be useful but needs coordinator review.
Log it only when it is contextually useful but not yet actionable.

Created and proposed issues must include why the work was discovered, which
issue or workstream surfaced it, whether it blocks or depends on anything, which
phase or workstream owns it, what acceptance criteria prove completion, and what
future agents need to know after context clears.

Normal mode keeps this lightweight: concise issues or candidates, useful
blocker/dependency links, and no ceremony for small projects. Expanded mode uses
a formal discovery protocol with dependency-aware issue creation, ledger/local
docs updates when project shape changes, rich issue context, and coordinator
review/deduplication before non-blocking scope expansions are created.

## Sparse Link Graph

Use links as context compression, not decoration. Always use formal Linear
relationships for parent/child structure, blockers, related issues, and
duplicates. Use Markdown links for docs, source files, PRs, commits, branches,
ledger paths, verification artifacts, dashboards, and logs only when they affect
implementation, sequencing, verification, or recovery.
In short: links should compress context, not clutter tasks.

Normal child issues should usually carry 3-7 high-signal links. If Linear
relationship creation is blocked, preserve the intended graph in the companion
ledger and do not mark graph creation complete until Linear read-back proves it.

## Companion Ledger

Every agent-heavy project needs a durable Markdown ledger. Prefer a coordinator
owned path outside individual worktrees:

```txt
../.codex-linear-ledgers/<linear-project-slug>/EXECUTION.md
```

Initialize with the original prompt when the wrapper is available:

```bash
linear-agent init \
  --ledger <path> \
  --project "<project name>" \
  --prompt "<original user prompt or project brief>" \
  --repo <repo-path> \
  --base-branch main
```

The ledger complements Linear; it does not replace Linear issues, comments,
statuses, or dependencies. Keep checklist state honest with `[ ]`, `[x]`, and
`[~] not applicable:<reason>`.

## Linear Transition Wrapper

Use `linear-agent` for execution-state transitions and graph creation when
available. With credentials and `--apply-linear`, the CLI writes directly to
Linear's GraphQL API and verifies read-back before confirming success. Without
credentials, keep using dry-run output as the manual fallback plan.

Common commands:

```bash
linear-agent start MAS-123 --ledger <path> --agent Codex --worktree <path>
linear-agent block MAS-123 --ledger <path> --note "<blocker>"
linear-agent verify MAS-123 --ledger <path> --verification "<check>: <result>"
linear-agent complete MAS-123 --ledger <path> --verification "<check>: <result>"
linear-agent handoff --ledger <path> --note "<handoff>"
linear-agent reconcile --ledger <path>
linear-agent finalize --ledger <path> --verification "<checks>" --evidence "<links>" --linear-reconciled --dependencies "satisfied" --production-gates "not-applicable:<reason>" --sink-gates "not-applicable:<reason>"
```

Direct Linear mode requires `LINEAR_API_KEY` or `LINEAR_ACCESS_TOKEN` and
`--apply-linear`. Endpoint overrides are validated to `https://api.linear.app`
unless explicitly allowed for trusted testing. Fake transport is test-only and
requires `LINEAR_AGENT_TEST_MODE=1`.

## Live API Mode

`linear-agent graph-apply --apply-linear --from <plan>.json` creates and
updates Linear project graphs directly through `https://api.linear.app/graphql`.
Linear MCP is no longer required for graph creation when credentials are
available.

Supported live operations:

- `projectCreate` / `projectUpdate`
- `projectDelete` for disposable smoke teardown
- `issueLabelCreate` / `issueLabelUpdate`
- `projectMilestoneCreate` / `projectMilestoneUpdate`
- `issueCreate` / `issueBatchCreate` / `issueUpdate`
- `issueRelationCreate` for `blocks`, `related`, and `duplicate` relations
- `attachmentCreate` / `attachmentUpdate` with source metadata
- paginated project issue read-back for `graph-readback` and
  `reconcile --project`, starting at 250 issues per page and reducing the page
  size if Linear reports query complexity pressure

Idempotence keys:

- Project: `(team.id, name)`
- Milestone: `(project.id, name)`
- Label: `(team.id, name)`
- Issue: explicit `identifier` when supplied, otherwise `(team.id, title)`
- Relation: `(issueId, relatedIssueId, type)`
- Attachment: `(issueId, url)`

Every live mutation must check Linear's `success` flag, read the affected graph
back, and fail closed if confirmation disagrees. Project scans must follow
Linear cursor pagination so large plans do not silently hide drift after the
first page, and they should adapt page size when a rich read-back selection
exceeds Linear's query complexity budget. The HTTP transport should respect
`RATELIMITED` / HTTP 429 responses and Linear rate-limit or complexity headers
before retrying. Default mode remains dry-run; mutations require `--apply-linear` or
`LINEAR_AGENT_APPLY=1`.

## Execution State Hygiene

- Read the ledger, operating guide, and verification matrix before choosing
  work.
- Move an issue to `In Progress` when implementation or investigation starts.
- Add an acknowledgement comment before long-running work.
- Add progress comments for material discoveries, blockers, or handoffs.
- Keep blockers, related issues, duplicates, and follow-ups current.
- Re-run the safe parallelism checkpoint after material issue completions,
  blockers, or scope changes.
- Do not mark an issue `Done` until acceptance criteria and verification pass.
- Completion comments must include changed/inspected files, checks run, result,
  residual risks, and follow-ups.
- Parent workstreams should remain open until their child issues and final gate
  are complete.
- Update the companion ledger at each transition so compaction does not erase
  execution state.

## Parallel Work

Default to looking for safe parallel execution opportunities. Run a safe
parallelism checkpoint after creating or reading a Linear project, and repeat it
after material issue completions, blockers, or scope changes.

At each checkpoint:

- Identify independent, unblocked `agent-ready` issues.
- Group candidate issues by dependency order, write scope, risk, and
  verification overlap.
- Spawn as many parallel agents as safely useful when ownership is clear.
- Use `parallel-safe` only when write scopes and behavior contracts do not overlap.
- For write-capable parallel agents, assign one Linear issue, one branch, one
  worktree, one owned write scope, explicit non-owned areas, and one
  verification command.
- Use bounded read-only or context-heavy agents for context isolation when
  research, audit, read-back, verification, large docs, logs, diffs, issue
  histories, or reference material would otherwise overload coordinator context.
- Keep the coordinator responsible for decisions, integration, Linear state,
  dependencies, comments, ledger updates, and final verification.
- Explain serial execution decisions by naming the exact constraint: dependency,
  shared file/module, unclear ownership, production/sink gate, verification
  coupling, or coordinator-level decision context.
- Create follow-up Linear issues when work must be split before safe parallel
  execution.

If write scopes overlap, mark issues `serial-required` or `overlap-zone` until
the coordinator reconciles ownership.

## Optional Deep Auto-Research Validation

Standard validation is mandatory for every project. That means concrete
acceptance criteria, issue-level verification before `Done`, Linear read-back,
final reconciliation, and evidence in completion/finalization comments.

Only add the deeper auto-research loop when the user explicitly asks, approves
it during planning, or uses clear trigger language such as `dogfood`,
`recursive`, `auto-research`, `keep iterating`, `long horizon`, or `publish
after stable`. If unclear, ask:

```txt
Do you want standard validation only, or the deeper auto-research loop with repeated evaluator passes and follow-up task creation?
```

When enabled, freeze a binary or numeric evaluator before the final loop, make
one focused change at a time, keep only changes that preserve correctness, and
create follow-up tasks for failed or inconclusive checks. Do not mutate the
evaluator mid-loop unless the issue is explicitly to fix an invalid evaluator.

## Production And Sink Gates

For live production apps, add first-class issues for deployment readiness, cron
or job inventory, auth/RBAC inventory, data/business-output semantics, and sink
or output behavior locks. Preserve existing practical output unless an issue
explicitly changes it.

## Status Update

After project creation or restructuring, post a project status update or
operating-guide comment summarizing the issue range, highest-priority gates,
serial dependencies or exact serial constraints, safe parallel batches,
production risks, first execution order, and companion ledger path.
