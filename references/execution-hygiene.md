# Execution Hygiene

Use this reference when executing an agent-ready Linear project.

## Ledger Discipline

The companion ledger is the durable execution memory. It must record:

- original user prompt or project brief
- Linear project URL or name
- operating guide issue and verification matrix issue
- repo path, base branch, active branches, and worktree paths
- overall state, active issue, current agent, last verified time, and next safest
  action
- project creation checklist
- issue progress table
- decisions, blockers, risks, and handoff notes

Update it after every material state transition. If Linear and the ledger
disagree, trust Linear for canonical issue status, trust comments for audit
history, and record reconciliation.

## `linear-agent` Workflow

Use the wrapper when available:

```bash
linear-agent start MAS-123 --ledger <path> --agent Codex --worktree <path>
linear-agent verify MAS-123 --ledger <path> --verification "<check>: <result>"
linear-agent complete MAS-123 --ledger <path> --verification "<check>: <result>"
linear-agent reconcile --ledger <path>
```

After a dry-run wrapper transition, perform the printed Linear MCP actions and
read the issue back. If direct mode is used, verify that the CLI confirms Linear
state and comment read-back.

## Issue State Hygiene

- Move an issue to `In Progress` when work starts.
- Add an acknowledgement comment before long-running work.
- Add progress comments when a material discovery changes scope.
- Do not mark an issue `Done` until acceptance criteria and verification pass.
- Completion comments must include changed/inspected files, checks run, result,
  residual risks, and follow-ups.
- Parent workstreams stay open until their child issues and final gate are done.

## Safe Parallelism Checkpoints

Run a lightweight parallelism checkpoint after project creation/read-back and
after material completions, blockers, or scope changes.

At each checkpoint:

- identify independent, unblocked `agent-ready` issues
- group candidates by dependency order, write scope, risk, and verification
  overlap
- split work into follow-up issues before dispatch if ownership is too broad
- keep dependent, shared-scope, or unclear work serial until reconciled
- record the decision in Linear comments and the ledger

Bounded read-only agents may run in parallel for context isolation when
research, audit, read-back, verification, large docs, logs, diffs, issue
histories, or reference material would otherwise overload coordinator context.
Give them a time or scope limit and do not allow write access unless promoted to
a write-capable assignment.

## Parallel Code Execution With Worktrees

Use separate Git worktrees for parallel write-capable agents unless the runtime
already provides separate forked workspaces.

Coordinator responsibilities:

- assign one Linear issue per agent
- assign one branch and worktree per write-capable agent
- define exact owned write set
- define non-owned areas
- tell agents they are not alone in the codebase
- prevent reverts or cleanups outside ownership
- make coordinator-level decisions, integration calls, and dependency changes
- merge only after issue verification and coordinator reconciliation
- maintain Linear status, comments, ledger updates, and final verification

Example:

```bash
git worktree add ../repo-mas-123 -b codex/mas-123-feature main
git worktree add ../repo-mas-124 -b codex/mas-124-docs main
```

Each write-capable assignment must state the Linear issue, branch/worktree,
owned write scope, non-owned areas, and verification command.

Use serial execution when there is a dependency, a shared file/module, unclear
ownership, a production or sink gate, verification coupling, or
coordinator-level decision context. If work is almost parallel-safe but too
large, create follow-up issues that split the scope before dispatch.

## Finalization

Only finalize when:

- all issue rows are `Done` or `Completed`
- Linear read-back shows no unfinished Todo/In Progress issues
- dependency outcomes are explicit
- production gate outcomes are explicit
- sink/output gate outcomes are explicit
- evidence links to checks, release artifacts, or read-back summaries

Use:

```bash
linear-agent finalize \
  --ledger <path> \
  --verification "<Linear read-back and final checks>" \
  --evidence "<read-back summary, CI link, release link, or artifact>" \
  --linear-reconciled \
  --dependencies "satisfied" \
  --production-gates "not-applicable:<reason>" \
  --sink-gates "not-applicable:<reason>"
```

`finalize` must fail closed. Empty tables, blocked rows, canceled rows, missing
issues, or reconciliation drift are not project completion.
