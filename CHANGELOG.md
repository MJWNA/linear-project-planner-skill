# Changelog

All notable changes to this public skill repo are tracked here.

This project uses lightweight SemVer tags for stable skill snapshots. Until the first tagged release, use the `main` branch and GitHub commit history as the source of truth.

## Unreleased

## 2.1.1 - 2026-04-28

- Changed deep auto-research validation from default behavior to an opt-in, trigger-based planning gate.
- Kept standard validation mandatory for every project: issue verification, Linear read-back, final reconciliation, and completion evidence.
- Added ledger fields and `linear-agent init` defaults for validation mode and deep auto-research loop state.
- Updated README, regression tests, and evaluator checks for the new gated validation contract.

## 2.1.0 - 2026-04-28

- Added compact Quick Path and Reference Map sections to reduce active context while preserving safety rules.
- Added structured `linear_project.*` command schema reference docs for future function-tool or MCP surfaces.
- Added runtime/model guidance for coordinator, read-only worker, implementation worker, and Responses API state continuity.
- Added `lib/linear_agent/ledger.py` and moved Markdown ledger row parsing into typed Python shared by the shell wrapper and GraphQL reconciler.
- Hardened direct Linear mode with a planned state-change summary before GraphQL writes.
- Hardened `linear-agent finalize` to require explicit `--evidence` and record it in the final ledger comment.
- Expanded evaluator coverage for structured tool contracts, runtime state guidance, and generated Linear issue/final-comment fixtures.
- Raised the frozen evaluator release target from `SCORE 100/100` to `SCORE 130/130`.

## 2.0.1 - 2026-04-28

- Added sparse link graph guidance for high-signal task, docs, PR, ledger, and verification references.
- Added final auto-research validation task guidance for binary/frozen evaluator checks before project completion.
- Hardened `linear-agent finalize` so it refuses empty ledgers and unfinished issue rows.
- Hardened `linear-agent reconcile` so empty Issue Progress tables fail closed instead of reporting success.
- Changed canceled Linear issue reconciliation to `agent:blocked` instead of `agent:pr-ready`.
- Documented fallback sparse-link graph handling when Linear issue or relationship creation is blocked.

## 2.0.0 - 2026-04-28

- Added README trust badges for live CI and license status.
- Documented the manual release surface for public skill snapshots.
- Added direct Linear GraphQL automation mode for issue transitions behind `--apply-linear` / `LINEAR_AGENT_APPLY=1`.
- Added fake Linear GraphQL transport tests and `linear-agent reconcile`.
- Added a frozen CLI reliability evaluator for recursive autoresearch-style validation.
- Hardened fake transport gating, Linear API URL validation, partial-apply recovery, reconcile ledger updates, and finalization honesty checks.

## 0.1.0 - Pending

- Initial public skill baseline.
- Adds the `linear-project-planner` Codex skill.
- Adds the `linear-agent` ledger wrapper.
- Adds the companion execution ledger template.
- Adds regression tests, GitHub Actions CI, MIT license, public repo community files, and publisher baseline metadata.
- Enforces parallel-agent and git worktree safety policy for agent-heavy Linear projects.
