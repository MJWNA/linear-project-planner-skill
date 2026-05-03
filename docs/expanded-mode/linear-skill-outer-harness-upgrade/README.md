# Linear Skill Outer Harness Upgrade

Status: active expanded-mode dogfood
Linear project: pending API/MCP read-back
Companion ledger: `../.codex-linear-ledgers/linear-skill-outer-harness-upgrade/EXECUTION.md`
Repository: `/Users/ronniemeagher/Desktop/Curssor/mta-pt-workspace/projects/linear-project-planner-skill`

## Purpose

Use the `linear-project-planner` skill in expanded mode to turn the skill into
a stronger outer harness for long-running, agent-heavy work. The project uses
research-backed issue creation, API-primary Linear execution with MCP fallback,
continuous issue discovery, recursive research-to-implementation loops,
deterministic and inferential sensors, and dogfood verification.

## Source Links

These sources are part of the Linear project and must be owned by research
issues, not handled as pre-project side reading:

- OpenAI Symphony article:
  `https://openai.com/index/open-source-codex-orchestration-symphony/`
- OpenAI Harness Engineering article:
  `https://openai.com/index/harness-engineering/`
- Martin Fowler / Thoughtworks Harness Engineering article:
  `https://martinfowler.com/articles/harness-engineering.html`
- OpenAI Symphony repository:
  `https://github.com/openai/symphony`
- OpenAI Symphony spec:
  `https://github.com/openai/symphony/blob/main/SPEC.md`

## Non-Negotiables

- Linear is the project control plane.
- Direct Linear API is primary whenever credentials are available.
- MCP is an immediate fallback whenever API execution is unavailable, blocked,
  unimplemented, or fails read-back.
- Research findings become Linear issues, sub-issues, decisions, or local docs.
- Expanded mode remains opt-in and must not contaminate baseline mode.
- The loop is research -> issue graph -> implementation -> sensors/tests ->
  synthesis -> discovered work -> next loop.
- Coordinator owns Linear state, ledger state, dependency map, release metadata,
  installed runtime sync, and final verification.

## Working Loop

1. Read the current source material and repo contract.
2. Create or update Linear issues for research, implementation, QA, and release.
3. Run safe parallel research agents for independent dossiers.
4. Synthesize source-backed principles and decision rules.
5. Make one focused implementation change.
6. Run deterministic sensors: tests, evaluators, syntax/YAML, install checks,
   graph-plan/graph-apply dry-run checks, and direct read-back where possible.
7. Run inferential sensors: reviewer agents or focused self-review against the
   research docs and issue acceptance criteria.
8. Create or update follow-up Linear issues for missed requirements.
9. Repeat until the verification matrix, research synthesis, and repo behavior
   agree.

