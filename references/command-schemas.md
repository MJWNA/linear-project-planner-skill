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

## Shared Parameters

- `ledger`: absolute path to the companion execution ledger.
- `agent`: agent name recorded in the ledger and comments.
- `issue`: Linear issue identifier, for issue-scoped commands.
- `worktree`: absolute path to the owning worktree when write work is active.
- `note`: optional human-readable context.
- `apply_linear`: explicit opt-in for direct Linear writes.

## Safety Contract

- Default mode is dry-run for Linear side effects.
- Direct mode must read Linear back before confirming the ledger.
- Fake transport is test-only and requires `LINEAR_AGENT_TEST_MODE=1`.
- `complete` requires verification evidence.
- `finalize` requires Linear reconciliation, explicit gate outcomes, completed
  issue rows, and a final evidence string or artifact.

## Tool Description Checklist

Future structured tools should describe:

- when to use the tool
- required inputs
- side effects
- retry safety
- common error modes
- read-back or evidence requirements
