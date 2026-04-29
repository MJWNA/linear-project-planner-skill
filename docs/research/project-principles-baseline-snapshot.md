# Project Principles Baseline Snapshot

Project: Linear Planner Principles Surface
Linear issue: MAS-714
Date: 2026-04-29
Status: baseline snapshot

## Purpose

This snapshot records the current `linear-project-planner` behavior before
adding a global Project Principles / Fundamentals surface. The implementation
must remain additive and must not turn baseline mode into expanded mode.

## Current Front-Door Contract

- `SKILL.md` is the router-visible front door and is currently compact at 275
  lines.
- The core behavior is to create an execution system for Linear projects:
  project graph, guide issues, companion ledger, safe parallelism checkpoints,
  dependencies, and verification gates.
- Baseline mode is the default for ordinary Linear planning, execution, audits,
  remediation, companion ledgers, dependencies, safe parallelism checkpoints,
  and verification gates.
- Expanded mode is opt-in and loads `references/expanded-mode.md` only after
  explicit long-horizon, deep research, dependency mapping, local docs, or heavy
  multi-agent triggers.
- `linear-agent` remains the execution-state wrapper and should not change for
  this enhancement unless implementation evidence proves a CLI change is
  necessary.

## Baseline Verification

Commands run before implementation:

```bash
python3 tools/linear-front-door-evaluator.py
python3 tools/linear-agent-evaluator.py
python3 tools/linear-skill-audit-evaluator.py
bash tests/test-linear-agent.sh
```

Observed results:

- `linear-front-door-evaluator.py`: `SCORE 150/150`
- `linear-agent-evaluator.py`: `SCORE 130/130`
- `linear-skill-audit-evaluator.py`: `ALL_VERTICALS 10/10`
- `tests/test-linear-agent.sh`: `linear-agent tests passed`

## Likely Owned Files

These files are plausible write targets for the principles enhancement:

- `references/project-principles.md`
- `templates/project-principles.md`
- `templates/EXECUTION.md`
- `references/project-structure.md`
- `references/expanded-mode.md`
- `SKILL.md`
- `tools/linear-front-door-evaluator.py`
- `tools/linear-skill-audit-evaluator.py`
- `CHANGELOG.md`

## Non-Owned By Default

These should remain unchanged unless the design spec proves a need:

- `scripts/linear-agent`
- `lib/linear_agent/**`
- release tags, GitHub Releases, and public publishing metadata
- parent MTA/PT workspace state

## Non-Contamination Guardrails

- Add a global principles surface, but keep the baseline path compact.
- Store detailed behavior in references and templates.
- Keep `SKILL.md` updates tiny, router-safe, and Reference Map oriented.
- Do not make local docs folders, research dossiers, amendment logs, or
  expanded-mode companion documents mandatory for small baseline projects.
- Keep principles selective: they guide decisions; they do not replace Linear
  tasks, execution ledgers, ADRs, QA plans, or dependency maps.

## Branch And Repo State

- Repository: `/Users/ronniemeagher/Desktop/Curssor/mta-pt-workspace/projects/linear-project-planner-skill`
- Current branch during snapshot: `codex/expanded-mode-v3-3`
- `git status --short --untracked-files=all` was clean before this snapshot
  artifact was added.
- No public publish, tag, or release is authorized for this enhancement.
