# Linear Project Command Schemas

This reference describes the stable command contract behind the `linear-agent`
CLI and a future structured tool or MCP surface. Keep the shell CLI compatible;
move implementation behind these contracts in small, tested steps.

## Namespace

Use `linear_project.*` for future function-tool, MCP, or tool-search metadata.

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

## Shared Parameters

- `ledger`: absolute path to the companion execution ledger.
- `agent`: agent name recorded in the ledger and comments.
- `issue`: Linear issue identifier, for issue-scoped commands.
- `worktree`: absolute path to the owning worktree when write work is active.
- `note`: optional human-readable context.
- `apply_linear`: explicit opt-in for direct Linear writes.
- `json`: emit stable machine-readable output.
- `from`: path to a graph plan file for graph and allocation commands.

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
- `smoke` never runs on normal PRs or forks; live mode is manual and secret-gated.

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
      "parent": "",
      "blockedBy": [],
      "blocks": ["MAS-436"],
      "writeSet": ["references/command-schemas.md"],
      "serial": true
    }
  ]
}
```

The graph is applied in phases: validate, dry-run, apply, read-back, then repair/report. Existing objects are matched by stable keys before creating anything new.

## Tool Description Checklist

Future structured tools should describe:

- when to use the tool
- required inputs
- side effects
- retry safety
- common error modes
- read-back or evidence requirements
