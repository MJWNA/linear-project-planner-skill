# Changelog

All notable changes to this public skill repo are tracked here.

This project uses lightweight SemVer tags for stable skill snapshots. Until the first tagged release, use the `main` branch and GitHub commit history as the source of truth.

## Unreleased

- Added sparse link graph guidance for high-signal task, docs, PR, ledger, and verification references.
- Added final auto-research validation task guidance for binary/frozen evaluator checks before project completion.

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
