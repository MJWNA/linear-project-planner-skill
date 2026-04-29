# Linear Planner Continuous Discovery Upgrade

Project: Linear Planner Continuous Discovery Upgrade
Linear project: https://linear.app/master-group-holdings/project/linear-planner-continuous-discovery-upgrade-8e33e3b5674b
Status: implementation and release tracking
Companion ledger: `../.codex-linear-ledgers/linear-planner-continuous-discovery-upgrade/EXECUTION.md`

## Purpose

Dogfood expanded mode while upgrading the `linear-project-planner` skill's own
planning behavior. The project improves normal-mode recovery, expanded-mode
charter and issue detail, and global Continuous Issue Discovery.

## Source Scope

- `SKILL.md`
- `references/project-structure.md`
- `references/expanded-mode.md`
- `references/command-schemas.md`
- `templates/EXECUTION.md`
- `tests/fixtures/linear_issue_templates.md`
- `tools/linear-front-door-evaluator.py`
- `tools/linear-agent-evaluator.py`
- `tools/linear-skill-audit-evaluator.py`
- `README.md`
- `CHANGELOG.md`
- `.github/workflows/release.yml`

## Discovery Decisions

- Existing Project Principles / Fundamentals work was treated as relevant
  in-progress planning behavior and integrated into the `v3.4.0` scope.
- MAS-795 was created as emergent release-blocking work after research found
  the release workflow changelog check did not match the repo's changelog
  heading convention.
- Implementation stayed coordinator-owned because the active write files
  overlapped across normal mode, expanded mode, discovery, evaluators, and
  release metadata.

## Verification Plan

- Shell syntax and shell regression tests.
- Python syntax and unit tests.
- Front-door, CLI, and all-vertical evaluators.
- Local release-gate changelog/tag checks before publishing.
- GitHub PR checks before merge.
- Installed user-scope skill parity check after merge/release.
- Parent workspace submodule pointer assessment after merge.
