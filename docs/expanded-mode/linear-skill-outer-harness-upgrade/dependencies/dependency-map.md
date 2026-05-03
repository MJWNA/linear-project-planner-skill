# Dependency Map

Status: draft for project creation

## Milestones

1. Mode gate and project system
2. Research dossiers and source synthesis
3. Harness contract and implementation
4. Sensors, evaluators, and recursive loop
5. Dogfood, install parity, release readiness

## Parallel Batches

Research dossiers can run in parallel once the operating guide and verification
matrix exist. Write-capable implementation remains serial until the synthesis
and dependency map are accepted because the likely write set overlaps
`SKILL.md`, `references/`, `templates/`, `tools/`, and tests.

## Serial Gates

- API-primary/MCP-fallback contract must be clarified before implementation.
- Research synthesis must land before new evaluator expectations are frozen.
- Baseline behavior checks must run before installed runtime sync or release.
- Release/publish work must wait for source repo verification.

## Coordinator-Owned State

- Linear project state and issue graph
- Companion ledger
- Dependency map and project principles
- Release metadata, changelog, version, tag/release creation
- Installed runtime sync

