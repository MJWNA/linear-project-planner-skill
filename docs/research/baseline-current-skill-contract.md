# Baseline Current Skill Contract

Linear issue: MAS-690
Project: Linear Project Planner Expanded Mode
Captured: 2026-04-29
Repository: `/Users/ronniemeagher/Desktop/Curssor/mta-pt-workspace/projects/linear-project-planner-skill`
Branch: `main`
Repo version: `3.2.0`
Installed version: `3.2.0`

## Purpose

This snapshot freezes the current `linear-project-planner` skill contract before
any implementation of an expanded, long-horizon planning mode. Future expanded
mode work must compare against this baseline and prove the normal mode remains
available, concise, and behaviorally stable.

## Current Worktree State

The repository was already dirty when MAS-690 started. These files had existing
modifications and must be treated as pre-existing work unless explicitly
reviewed:

- `AGENTS.md`
- `CHANGELOG.md`
- `SKILL.md`
- `VERSION`
- `references/execution-hygiene.md`
- `references/project-structure.md`
- `templates/EXECUTION.md`
- `tests/test-linear-agent.sh`
- `tools/linear-front-door-evaluator.py`
- `tools/linear-skill-audit-evaluator.py`

The baseline snapshot itself adds this file:

- `docs/research/baseline-current-skill-contract.md`

## Router Contract

The skill front door currently activates for Linear project planning,
restructuring, auditing, remediation, production hardening, parallel agent work,
companion ledgers, milestones, dependencies/blockers, verification gates, and
Codex/Claude agent coordination.

It explicitly should not activate for a simple one-off Linear issue lookup
unless the user also asks for planning, remediation, execution tracking, or
project-level coordination.

The trigger preservation contract lives in:

- `references/trigger-preservation.md`

Any expanded mode must preserve these router-visible concepts:

- `Linear project`
- create, plan, restructure, or execute
- audit or remediation
- production hardening
- parallel agent or multi-agent
- milestones
- dependencies or blockers
- companion ledger
- verification gates
- completion comments
- Codex and Claude

## Normal Mode Outputs

The current normal mode creates an execution system rather than a flat todo
list. Expected outputs include:

- Linear project or project update.
- Required guide issues:
  - `Guide: Agent Operating Guide`
  - `Guide: Verification Matrix`
- Parent workstreams as ownership envelopes.
- Child issues with problem, evidence, acceptance criteria, verification,
  reference links, local rules, and agent notes.
- Labels such as `agent-ready`, `parallel-safe`, `serial-required`,
  `overlap-zone`, `needs-human-review`, `verification-missing`, and
  production/touch-surface labels where relevant.
- Sparse link graph using formal Linear relationships and high-signal Markdown
  links.
- Companion execution ledger at
  `../.codex-linear-ledgers/<linear-project-slug>/EXECUTION.md`.
- Safe parallelism checkpoint after project creation/read-back and after
  material completions, blockers, or scope changes.
- Standard validation for every issue before marking it done.
- Optional deep auto-research validation only when explicitly requested,
  approved, or clearly triggered.

## Companion Ledger Contract

The ledger complements Linear and does not replace Linear issues, statuses,
comments, relationships, or read-back verification.

The ledger must preserve:

- Original prompt or project brief.
- Linear project URL/name.
- Operating guide and verification matrix issue IDs.
- Repository path, base branch, active branch/worktree state.
- Overall state, active issue, active agent, active worktree, last verified
  time, and next safest action.
- Project creation checklist.
- Execution checklist.
- Parallel agent allocation table.
- Safe parallelism decisions.
- Issue progress table.
- Decisions, blockers, risks, handoff notes, and activity log.

Checklist markers are:

- `[ ]` pending
- `[x]` complete
- `[~]` not applicable with a reason

## Execution Contract

The `linear-agent` wrapper is the preferred local transition tool. It updates
the ledger and prints the Linear MCP actions that still need to be performed and
read back.

Core commands:

```bash
linear-agent init --ledger <path> --project "<project>" --prompt "<prompt>"
linear-agent start MAS-123 --ledger <path> --agent Codex --worktree <path>
linear-agent verify MAS-123 --ledger <path> --verification "<check>: <result>"
linear-agent complete MAS-123 --ledger <path> --verification "<check>: <result>"
linear-agent reconcile --ledger <path>
linear-agent finalize --ledger <path> --verification "<checks>" --evidence "<links>" --linear-reconciled --dependencies "satisfied" --production-gates "not-applicable:<reason>" --sink-gates "not-applicable:<reason>"
```

The wrapper supports direct Linear mode only when the expected Linear token is
available and `--apply-linear` is explicitly used. Fake transport is test-only.

## Parallelism Contract

Parallel execution is encouraged only after ownership, dependencies, and
verification gates are explicit.

Read-only/context-heavy agents may run in parallel for research, audits,
read-back, verification, large docs/logs/diffs, issue histories, and reference
material.

Write-capable agents require:

- One Linear issue.
- One branch.
- One worktree.
- One owned write scope.
- Explicit non-owned areas.
- One verification command.
- Coordinator-owned integration and final verification.

Use `serial-required` or `overlap-zone` when write scopes overlap, dependencies
exist, ownership is unclear, verification is coupled, production/sink gates
apply, or coordinator-level decisions are required.

## Baseline Protection Rules

Expanded mode must be additive and opt-in. It must not:

- Remove or dilute the current normal-mode trigger language.
- Replace normal mode with long-form project ceremony.
- Make local documentation folders mandatory for ordinary concise projects.
- Require Context7/OpenAI research for pure Linear issue graph changes.
- Mark issues done without acceptance criteria, verification, and read-back.
- Edit the installed runtime copy directly for durable changes.

If implementation touches `SKILL.md`, the addition should remain small and
router-safe. Long expanded-mode detail should live in references and templates.

## Verification Commands

Baseline verification for normal mode:

```bash
bash tests/test-linear-agent.sh
python3 -m unittest tests/test_linear_agent_graphql.py tests/test_linear_agent_graph_features.py
python3 tools/linear-front-door-evaluator.py
python3 tools/linear-agent-evaluator.py
python3 tools/linear-skill-audit-evaluator.py
```

Syntax and metadata checks when release, install, CI, or metadata files change:

```bash
bash -n install.sh
bash -n scripts/linear-agent
bash -n tests/test-linear-agent.sh
python3 -m py_compile lib/linear_agent/__init__.py lib/linear_agent/ledger.py lib/linear_agent/graphql.py lib/linear_agent/graph.py lib/linear_agent/cli.py tools/linear-front-door-evaluator.py tools/linear-agent-evaluator.py tools/linear-skill-audit-evaluator.py
ruby -e 'require "yaml"; skill = File.read("SKILL.md"); frontmatter = skill.match(/\A---\n(.*?)\n---/m)[1]; YAML.safe_load(frontmatter); YAML.load_file("agents/openai.yaml"); puts "yaml ok"'
./install.sh --check
```

Run `shellcheck install.sh scripts/linear-agent tests/test-linear-agent.sh` when
`shellcheck` is available.

## Installed Runtime Parity

`./install.sh --check` passed at capture time and reported:

```txt
linear-project-planner install looks healthy
```

The repo and installed skill both reported version `3.2.0`.

## Expanded Mode Comparison Gate

Before expanded mode implementation is marked complete, compare the post-change
state against this snapshot and confirm:

- Normal-mode trigger concepts are still router-visible.
- Required guide issues are still required.
- Companion ledger behavior is still supported.
- Safe parallelism remains explicit and ownership-bound.
- Baseline verification commands pass or failures are documented as pre-existing
  and unrelated.
- Expanded mode is invoked only by explicit expanded/long-horizon/detailed
  planning language.
