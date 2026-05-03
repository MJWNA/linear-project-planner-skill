# ADR: Expanded Mode As An Explicit Additive Mode

Linear issue: MAS-689
Status: proposed for implementation
Decision owner: Codex coordinator
Review basis: user approved execution on 2026-04-29 with explicit constraint that
parallel agents are encouraged only after ownership, dependencies, and
verification gates are explicit.

## Context

The current `linear-project-planner` skill is intentionally concise. It creates
agent-ready Linear projects with guide issues, verification matrices, parent
workstreams, child issues, labels, dependencies, sparse links, companion
ledgers, and safe parallelism checkpoints.

The new requirement is not to replace that mode. The requirement is to add a
second, opt-in mode for long-horizon, high-detail projects that need deeper
research, richer dependency mapping, local reference documentation, and stronger
multi-agent coordination.

## Decision

Add an explicit **expanded mode** to the skill.

Expanded mode should be invoked only when the user asks for substantially more
than standard Linear project planning, such as:

- "expanded mode"
- "long-horizon project"
- "detailed multi-phase plan"
- "software-firm-grade planning"
- "deep research first"
- "dependency mapping"
- "multi-team delivery model"
- "create local project docs/references"
- "maximize safe parallel agents"

The baseline mode remains the default for ordinary Linear planning and
execution.

## Mode Shape

Expanded mode is documentation/reference behavior first, with minimal CLI or
evaluator support only when the specification proves it is needed.

The expected implementation shape is:

- A small `SKILL.md` router addition that names expanded mode and points to a
  focused reference.
- A new reference such as `references/expanded-mode.md` for the detailed
  workflow.
- Runtime project docs created beside the companion ledger, not inside the
  source repo, unless the files are reusable templates or durable skill docs.
- Templates for research dossiers, ADRs, dependency maps, QA plans, source
  provenance, and agent briefs.
- Evaluator coverage proving normal mode remains trigger-safe and expanded mode
  is opt-in.

## Required Expanded-Mode Outputs

Expanded mode should require:

- Baseline/no-contamination snapshot for the target project when the work is
  self-editing or high-risk.
- Research plan with first-class Linear research issues.
- Local docs folder linked from the companion ledger.
- Source-backed research documents before implementation specs.
- Dependency map represented in both Linear relationships and local docs.
- Agent operating guide and verification matrix with expanded-mode-specific
  parallelization and QA gates.
- Explicit safe-parallelism allocation before dispatch.
- Source provenance rules for Context7, OpenAI docs, framework docs, and web
  research.
- Synthesis gates before implementation issues are unblocked.
- Final dogfood and regression proof before release.

## Optional Expanded-Mode Outputs

Expanded mode may offer, but should not always require:

- Deep auto-research/evaluator loops.
- Separate release project.
- Dedicated CLI graph validation beyond existing `linear-agent` support.
- Large documentation trees with many subfolders.
- Multiple review persona passes on low-risk documentation-only changes.

## Non-Triggers

Expanded mode should not activate for:

- A simple request to create a small Linear project.
- A one-off issue lookup or status summary.
- A normal audit remediation plan where existing baseline mode is enough.
- A small repo doc edit.
- A pure Linear graph cleanup that does not need deep research.
- A project where local docs folders would add ceremony without improving
  sequencing, verification, or handoff.

## Baseline Protection Rules

Implementation must preserve:

- Existing frontmatter identity and normal-mode trigger language.
- The "Create an execution system, not a flat todo list" core rule.
- Required guide issues.
- Companion ledger semantics.
- Sparse link graph rules.
- Standard validation requirement.
- Optional deep auto-research boundaries.
- Safe parallelism checkpoint language.
- `linear-agent` transition and reconciliation behavior.

`SKILL.md` should stay compact. If expanded-mode detail grows, move it to
references/templates and keep only the router-visible contract in `SKILL.md`.

## Human Review Gate

This ADR was drafted after the user explicitly said to go ahead and execute, and
repeated the constraint that parallel agents should be used only after
ownership, dependencies, and verification gates are explicit. Treat that as
approval to proceed with research, specification, and additive implementation.

Before release, the final implementation should still be reviewed against:

- `docs/research/baseline-current-skill-contract.md`
- expanded-mode research synthesis
- normal-mode evaluator results
- installed-runtime parity checks

## Consequences

Benefits:

- Baseline mode remains fast and readable.
- Long-horizon work gets a first-class operating model.
- Research artifacts become durable and linkable from Linear.
- Parallel agent use becomes safer because allocation is explicit.

Tradeoffs:

- More artifacts must be maintained.
- Expanded mode can drift into ceremony if templates are too broad.
- The skill front door needs evaluator coverage so trigger language stays
  reliable.

## Implementation Notes

Prefer this implementation order:

1. Complete research dossiers.
2. Synthesize operating model and docs provenance policy.
3. Write expanded-mode reference and templates.
4. Add a small `SKILL.md` router addition.
5. Add evaluator assertions for opt-in expanded mode and baseline preservation.
6. Dogfood on a clearly marked test project.
7. Release and install only after verification passes.
