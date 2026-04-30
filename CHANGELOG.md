# Changelog

All notable changes to this public skill repo are tracked here.

This project uses lightweight SemVer tags for stable skill snapshots. Until the first tagged release, use the `main` branch and GitHub commit history as the source of truth.

## Unreleased

- Nothing yet.

## 4.1.0 - 2026-04-30

- Added reactive Linear issue spillover for direct GraphQL graph apply: issue
  descriptions are written to Linear normally first, and only size/length
  rejection errors trigger local Markdown spillover plus a compact retry body.
- Added `--spillover-dir` and `project.spilloverDir` support so projects can
  route overflow context into a known local docs root when Linear rejects an
  oversized issue payload.
- Added fake Linear limit coverage and graph read-back handling for spillover
  pointer descriptions.
- Initialized the dogfood evaluator fake Linear state before apply/read-back so
  its delivery checks exercise the graph path instead of failing before setup.

## 4.0.1 - 2026-04-30

- Made direct Linear GraphQL the documented primary path whenever
  `LINEAR_API_KEY` or `LINEAR_ACCESS_TOKEN` is available; Linear app/MCP/manual
  actions are now explicitly framed as fallback-only unless requested.
- Updated dry-run transition output so agents see the direct API path first and
  fallback connector actions second.
- Scoped graph-apply title idempotence to the target project to avoid reusing
  generic guide issue titles from unrelated Linear projects.
- Added Context7/official Linear docs checkpoint coverage to the v4.0.1 project
  and evaluator coverage for API-primary routing.

## 4.0.0 - 2026-04-30

- Aligned live GraphQL mutations with Linear's current schema by replacing the
  stale project teardown mutation with `projectDelete`.
- Added `issueBatchCreate` for efficient graph bootstrap while preserving
  idempotent lookup/update behavior and per-issue read-back verification.
- Upgraded live project read-back and project-scan reconciliation to follow
  cursor pagination across all project issues at 250 issues per page.
- Expanded direct graph support for `related` and `duplicate` issue relations,
  richer attachment metadata, and attachment read-back drift detection.
- Added header-aware rate-limit budget tracking on top of the existing
  `RATELIMITED` / HTTP 429 exponential backoff path.
- Re-pinned the frozen CLI evaluator for the v4 API contract and refreshed
  documentation for the direct API mode.

## 3.6.0 - 2026-04-30

- Lifted the live `graph-apply --apply-linear` gate so project graphs can be
  created directly through Linear's GraphQL API without requiring a Linear MCP
  server for project creation.
- Added idempotent direct GraphQL operations for projects, labels, milestones,
  issues, issue relations, and attachments, with fake transport handlers,
  rate-limit retries, mutation success checks, and read-back verification.
- Added live graph read-back and project-scan reconciliation so the CLI can
  detect Linear issues missing from the ledger and ledger rows missing from
  Linear.
- Added `linear-agent discover` and `linear-agent promote` for Continuous Issue
  Discovery rows and optional live Linear issue creation.
- Updated live Linear smoke coverage, docs, evaluator expectations, and the ADR
  trail for direct API mode. Linear MCP remains a fallback for runtimes without
  credentials, not the graph-creation source of truth.

## 3.5.0 - 2026-04-30

- Added a live dogfood evaluator with small, medium, large, expanded-mode, and
  continuous-discovery sandbox plans.
- Added source material checkpoint guidance and companion-ledger tracking for
  kickoff, planning, issue creation, implementation, parallel delegation, scope
  changes, verification, handoff, and closeout.
- Extended graph plan fake apply/read-back to preserve and verify issue
  descriptions, milestones, and links so dogfood tests validate agent-ready
  issue quality.
- Added dogfood fixture coverage and expanded audit coverage for source
  checkpoint discipline.

## 3.4.0 - 2026-04-30

- Added a scaled Project Principles / Fundamentals surface for Linear projects,
  with compact baseline guidance, a full companion-document template,
  amendment rules, ledger placeholders, expanded-mode links, and evaluator
  coverage.
- Added Continuous Issue Discovery as a global planning behavior for normal and
  expanded mode, including create/propose/log decision rules and discovery
  classifications for blockers, dependencies, defects, follow-ups, decisions,
  QA gaps, documentation gaps, scope expansions, and risks.
- Added compact normal-mode project description and issue body structures, plus
  expanded-mode charter and rich issue body structures for long-horizon,
  multi-agent delivery.
- Added evaluator and fixture coverage for Continuous Issue Discovery, normal
  planning outputs, expanded planning outputs, and release-gate changelog
  verification.

## 3.3.0 - 2026-04-29

- Added an opt-in expanded mode for long-horizon Linear projects, with a
  compact `SKILL.md` router, detailed `references/expanded-mode.md` workflow,
  and reusable expanded-mode templates.
- Added research-backed design artifacts for software-firm operating models,
  Context7/OpenAI provenance, dependency mapping, and multi-agent QA.
- Added evaluator coverage proving expanded mode is additive and baseline mode
  remains the default.

## 3.2.0 - 2026-04-28

- Added an explicit safe-parallelism contract requiring repeated checkpoints,
  dependency/write-scope/risk/verification grouping, worktree-safe parallel
  agents, bounded context-isolation agents, serial-constraint explanations, and
  follow-up issue splitting.
- Expanded execution references and the companion ledger template with concrete
  safe-parallelism allocation fields and checkpoint recording.
- Added front-door evaluator coverage for the safe-parallelism contract.

## 3.1.0 - 2026-04-28

- Slimmed `SKILL.md` into a trigger-safe front door backed by focused references for project structure, execution hygiene, validation modes, and trigger preservation.
- Added source-backed research on progressive disclosure, metadata-driven discovery, and tool routing for skill activation reliability.
- Added a front-door evaluator and wired it into CI/release verification.
- Clarified Codex-first and Claude-compatible portability, including current manual Claude install caveats.
- Documented the manual, secret-gated live Linear smoke-test pattern separately from hermetic fake-transport CI.

## 3.0.0 - 2026-04-28

- Dogfooded the Linear project planner skill against itself through a new v3.0 Linear self-test project and companion ledger.
- Fixed graph dependency validation so cycles expressed through `blockedBy` fail closed.
- Hardened fake graph apply/readback/smoke paths so `LINEAR_AGENT_FAKE_STATE` requires `LINEAR_AGENT_TEST_MODE=1`.
- Made fake graph apply update existing fake issues idempotently and made graph readback report project, label, milestone, title, parent, and dependency drift.
- Added fake smoke run recording for inspectable local smoke tests.
- Fixed the all-verticals evaluator portability check so `WSL` alone cannot mask missing timezone/Windows evidence.
- Documented the required `linear-agent init --prompt` flag and Linear icon metadata fallback discovered during self-dogfooding.
- Fixed CI checkout depth so the gitleaks action can resolve release-range commits.

## 2.2.0 - 2026-04-28

- Moved the `linear-agent` command engine into typed Python while keeping the shell entrypoint as a thin launcher.
- Added graph planning, graph apply/read-back, allocation, inventory, smoke, JSON output, and ledger validation command surfaces.
- Added `EXECUTION.state.json` sidecar generation for deterministic machine-readable ledger state.
- Added graph feature tests, all-verticals evaluator, graph fixture, production gate templates, operator cheatsheet, migration guide, worked examples, token-scope guidance, and repository hardening policy.
- Hardened install with `--check`, `--uninstall`, `--with-docs`, PATH validation, and installed license visibility.
- Expanded CI/release coverage with shellcheck, secret scanning, CodeQL, manual release gate, and manual live Linear smoke workflow.

## 2.1.2 - 2026-04-28

- Marked the public repository metadata as the current production release line.
- Added a root `VERSION` file so the installable skill snapshot has an explicit version marker outside Git tags.
- Re-ran the publisher verification gate: shell regressions, fake Linear GraphQL tests, evaluator, README completeness, and secret preflight.

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
