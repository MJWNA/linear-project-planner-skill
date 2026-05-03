# Symphony Control Plane Dossier

Status: complete first pass
Linear issue: MAS-1007

## Source-Backed Facts

- OpenAI published Symphony on April 27, 2026 as an open-source Codex
  orchestration spec that treats a project-management board such as Linear as a
  control plane for coding agents.
- The core model maps active Linear issues to isolated agent workspaces. A
  scheduler polls the tracker, dispatches eligible work, restarts failed or
  stalled runs, and reconciles state.
- Symphony is explicitly a spec and engineering preview, not a polished product
  or generic workflow engine.
- Its repo-level runtime contract centers on workflow configuration, issue
  eligibility, workspace lifecycle, agent runner invocation, state tracking,
  logging, and proof-of-work.
- Proof of work is first-class: CI status, PR review feedback, complexity
  analysis, and walkthrough evidence are treated as part of the result.

## Inferences For This Skill

- `linear-project-planner` already has the right outer-harness spine: Linear as
  canonical tracker, companion ledgers, dependency links, verification gates,
  guide issues, and safe parallelism.
- The next useful layer is scheduler-readiness vocabulary, not a daemon rewrite:
  eligible states, blocked states, terminal states, attempts, retry/backoff,
  stalled work, proof of work, and handoff states.
- The companion ledger maps to Symphony observability, but long-running
  scheduler work would also need structured per-issue run metadata.
- Agent-owned Linear ticket writes should remain the default for now. The
  planner should not become a full workflow engine until reconciliation,
  idempotency, and recovery tests are mature.

## Recommendations

- Add a scheduler contract reference for control-plane, runner, workspace,
  retry, proof-of-work, and handoff semantics.
- Add optional proof-of-work blocks to issue templates and completion comments.
- Add scheduler-readiness checks for eligible states, terminal states,
  blockers, workspace root, concurrency, approval posture, and sandbox posture.
- Keep `SKILL.md` as a router/map; put scheduler depth into references,
  templates, and future CLI/tool surfaces.
- Consider a future `templates/WORKFLOW.md` only when unattended runner work is
  actually in scope.

## Implementation Surfaces

- `SKILL.md`: short scheduler-aware planning note.
- `references/scheduler-contract.md`: Symphony-derived lifecycle model.
- `templates/EXECUTION.md`: run attempts and proof-of-work metadata.
- `tests/`: future idempotency, blocker eligibility, terminal cleanup, and
  proof-of-work formatting tests.
- `scripts/linear-agent`: future `watch`, `claim`, `reconcile`, or `proof`
  subcommands.

## Refresh Triggers

- OpenAI changes Symphony from draft/spec preview into a maintained product.
- Codex app-server protocol, sandbox, approval, or tool registration behavior
  changes.
- Linear issue relationship, project slug, or workflow-state semantics change.
- This repo starts implementing a real daemon/runner.

