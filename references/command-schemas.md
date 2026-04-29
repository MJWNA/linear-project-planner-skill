# Linear Project Command Schemas

This reference describes the stable command contract behind the implemented
`linear-agent` CLI and any future structured tool or MCP surface. Keep the
shell CLI compatible; move implementation behind these contracts in small,
tested steps.

## Namespace

Use `linear_project.*` for function-tool, MCP, or tool-search metadata. The
shell CLI is the implemented reference surface.

| Tool | Purpose | Side effects |
|---|---|---|
| `linear_project.init` | Create a companion execution ledger from a template. | Writes a local ledger file. Refuses overwrite unless forced. |
| `linear_project.start` | Claim an issue for execution. | Updates ledger; optionally writes Linear state/comment in direct mode. |
| `linear_project.verify` | Record in-progress verification. | Updates ledger; optionally writes Linear state/comment in direct mode. |
| `linear_project.complete` | Complete an issue after verification. | Updates ledger; optionally moves Linear issue to Done after read-back. |
| `linear_project.block` | Record a blocker and next safest action. | Updates ledger; optionally writes Linear comment/state. |
| `linear_project.handoff` | Preserve context for the next agent. | Updates ledger; prints or writes handoff comment. |
| `linear_project.reconcile` | Compare ledger issue rows with Linear read-back. | Reads Linear; updates drift rows in ledger. |
| `linear_project.finalize` | Finalize a project ledger after all issue rows are complete. | Updates ledger only after reconciliation, gate outcomes, and evidence. |
| `linear_project.graph_plan` | Validate and preview a full Linear project graph. | Reads a graph plan file only. |
| `linear_project.graph_apply` | Idempotently create or update project, labels, milestones, issues, and relationships. | Writes Linear only with explicit apply mode. |
| `linear_project.graph_readback` | Compare Linear state against a graph plan. | Reads Linear; reports drift and repair guidance. |
| `linear_project.allocate` | Convert graph and write scopes into parallel agent lanes. | Writes ledger allocation rows only when requested. |
| `linear_project.inventory` | Draft production/sink gate matrix from a repo scan. | Reads local files only. |
| `linear_project.smoke` | Run dry-run or secret-gated live Linear smoke checks. | Writes Linear only with explicit apply mode and credentials. |
| `linear_project.discover` | Capture Continuous Issue Discovery as a proposed ledger row or live Linear issue. | Writes ledger; writes Linear only with `--create` and credentials. |
| `linear_project.promote` | Promote a proposed Continuous Issue Discovery row into a live Linear issue. | Writes Linear and records the created identifier in the ledger. |

## Shared Parameters

- `ledger`: absolute path to the companion execution ledger.
- `agent`: agent name recorded in the ledger and comments.
- `issue`: Linear issue identifier, for issue-scoped commands.
- `worktree`: absolute path to the owning worktree when write work is active.
- `note`: optional human-readable context.
- `apply_linear`: explicit opt-in for direct Linear writes.
- `json`: emit stable machine-readable output.
- `from`: path to a graph plan file for graph and allocation commands.

## Planning Output Modes

Normal-mode planning output should stay compact but recoverable:

- project descriptions carry goal, source of truth, scope, non-scope,
  workstreams, dependency/blocker policy, Continuous Issue Discovery,
  verification, and handoff fields when relevant;
- issue bodies carry objective, context, scope, dependencies/blockers,
  acceptance criteria, verification, and future-agent notes.

Expanded-mode planning output should behave like a delivery charter:

- project descriptions carry operating mode, companion ledger path, local docs
  root, phase, workstream map, dependency policy, research-to-issue policy,
  Continuous Issue Discovery policy, verification policy, handoff policy, and
  coordinator responsibilities;
- issue bodies carry background, why it matters, inputs, owned/non-owned scope,
  dependencies, blockers, working instructions, expected outputs, acceptance
  criteria, verification, handoff notes, follow-up candidates, and required
  ledger/local-doc/dependency-map updates where relevant.

Both modes support emergent work capture. Created or proposed issue records
should preserve discovery reason, surfacing issue/workstream, relationship to
blockers/dependencies, owner phase/workstream, acceptance criteria, and
compaction-safe notes.

## Safety Contract

- Default mode is dry-run for Linear side effects.
- Direct mode must read Linear back before confirming the ledger.
- Fake transport is test-only and requires `LINEAR_AGENT_TEST_MODE=1`.
- `complete` requires verification evidence.
- `finalize` requires Linear reconciliation, explicit gate outcomes, completed
  issue rows, and a final evidence string or artifact.
- `graph-plan` must not call Linear.
- `graph-apply` must be idempotent and dry-run by default.
- `graph-readback` reports drift without mutating unless paired with explicit apply.
- `allocate` refuses or reports overlapping write sets before dispatch.
- `smoke` never runs on normal PRs or forks; live mode is scheduled/manual and secret-gated.

## Stable Exit Codes

| Code | Meaning |
|---:|---|
| 0 | Success, or dry-run found no blocking problem. |
| 1 | Recoverable drift, validation failure, missing credential, or unsafe operation. |
| 2 | CLI usage or input error. |

## Graph Plan Shape

```json
{
  "project": { "name": "Linear Planner 10/10 Production Readiness" },
  "labels": ["agent-ready", "serial-required"],
  "milestones": ["Linear Graph Automation"],
  "issues": [
    {
      "key": "MAS-435",
      "title": "Define full Linear graph plan schema and command contract",
      "description": "## Objective\nDefine the schema.\n\n## Acceptance Criteria\n- Schema is documented.\n\n## Verification\nRun graph-plan.",
      "parent": "",
      "milestone": "Linear Graph Automation",
      "labels": ["agent-ready", "serial-required"],
      "links": [
        {
          "title": "Command schemas",
          "url": "file://references/command-schemas.md"
        }
      ],
      "blockedBy": [],
      "blocks": ["MAS-436"],
      "writeSet": ["references/command-schemas.md"],
      "serial": true
    }
  ]
}
```

The graph is applied in phases: validate, dry-run, apply, read-back, then repair/report. Existing objects are matched by stable keys before creating anything new. The local fake transport preserves and verifies issue descriptions, milestone assignment, and links so dogfood tests can prove issue actionability instead of only proving title/dependency shape.

## Live API Mode

`graph-apply --apply-linear` mutates `https://api.linear.app/graphql` directly
when `LINEAR_API_KEY` or `LINEAR_ACCESS_TOKEN` is present. It applies the graph
in this order:

1. Project
2. Labels
3. Milestones
4. Parent issues, using `issueBatchCreate` when multiple new parents are absent
5. Child issues, using `issueBatchCreate` when parents are already known
6. Relations
7. Attachments

Idempotence keys:

| Entity | Lookup key | On create | On match | On drift |
|---|---|---|---|---|
| Project | `(team.id, name)` | create | reuse | update changed fields |
| Milestone | `(project.id, name)` | create | reuse | update changed fields |
| Label | `(team.id, name)` | create | reuse | update explicit color/description drift |
| Issue | explicit `identifier`; else `(team.id, title)` | create or batch-create | reuse | update body/labels/parent/milestone |
| Relation | `(issueId, relatedIssueId, type)` | create | reuse | n/a |
| Attachment | `(issueId, url)` | create with source metadata | reuse | update title drift |

Every mutation checks `success`, reads back the affected graph, and fails closed
with recovery guidance when confirmation disagrees. Linear attachment URLs must
be allowed HTTP(S) URLs; keep local file paths in issue bodies or ledgers.
Project scans start at 250 issues per page and follow cursor pagination until
`pageInfo.hasNextPage` is false. If Linear reports that the rich read-back query
is too complex, the implementation must reduce page size and continue the scan
rather than silently dropping later pages.

## Tool Description Checklist

Future structured tools should describe:

- when to use the tool
- required inputs
- side effects
- retry safety
- common error modes
- read-back or evidence requirements
