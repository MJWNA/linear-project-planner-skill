# Linear Issue Template Fixtures

## Normal-Mode Project Description

## Project Goal
Create a durable Linear execution system for a compact project.

## Source Of Truth
Linear project and companion ledger.

## Scope
- Planned issues and verification gates.

## Non-Scope
- Expanded-mode local docs unless promoted.

## Workstreams
- Research
- Implementation
- Verification

## Dependency / Blocker Policy
- Link real blockers with Linear relationships.
- Keep optional related work as proposed candidates.

## Continuous Issue Discovery
- Create issues for blockers, correctness, acceptance-required work, or real dependencies.
- Propose useful non-blocking candidates.
- Log context-only findings.

## Verification
- Run named checks before Done.

## Handoff / Context Recovery
- Future agents start from Linear, ledger, and latest completion comments.

## Guide Issue

## Problem
Future agents need the operating context.

## Evidence
- Companion ledger path.
- Project URL.

## Acceptance Criteria
- Agent can choose the next dependency-ready task.

## Verification
- Guide links to ledger and verification matrix.

## Reference Links
- Linear project URL.
- Official docs URL.

## Docs / Local Rules
- AGENTS.md or project rule files.

## Agent Notes
- Parallel-safe documentation task.

## Normal-Mode Child Issue

## Objective
Implement a compact, observable change.

## Context
The issue must be understandable after context loss.

## Scope
- Owned work: one focused file or module.
- Non-scope: unrelated refactors.

## Dependencies / Blockers
- Blocks: none.
- Blocked by: research issue if applicable.

## Acceptance Criteria
- The behavior is present in the relevant instruction surface.

## Verification
- Targeted evaluator or read-back check passes.

## Notes For Future Agents
- Create or propose follow-up issues for discovered blockers, defects, QA gaps, or documentation gaps.

## Workstream Issue

## Problem
Agents need a clear ownership boundary and sequencing rule.

## Evidence
- Parent workstream is linked to child issues.

## Acceptance Criteria
- Standard labels include `agent-ready`, `parallel-safe` or `serial-required`, and any risk labels.
- Dependencies are represented with `blocks` or `blockedBy` relationships when order matters.
- Verification gates are named before implementation starts.

## Reference Links
- Companion ledger.
- Related parent or child issue.

## Child Issue

## Problem
A concrete change is missing or risky.

## Evidence
- Source file, command output, audit note, or official docs URL.

## Acceptance Criteria
- Implementation outcome is observable.
- Sparse links stay focused on docs, source, dependency, PR, or verification evidence.

## Verification
- Binary command or read-back check passes.

## Agent Notes
- Worktree ownership is explicit when files can be edited.
- Overlap zones are marked serial when ownership is shared.

## Expanded-Mode Project Charter

## Project Purpose
Run a long-horizon Linear project from Linear plus local docs.

## Operating Mode
Expanded mode.

## Source Of Truth
Linear is canonical; ledger and local docs preserve execution memory.

## Companion Ledger Path
`../.codex-linear-ledgers/project/EXECUTION.md`

## Local Docs Root
`docs/expanded-mode/project/`

## Current Phase
Research, implementation, verification, release, or handoff.

## Workstream Map
- Guide and coordination
- Research
- Implementation
- Verification
- Release

## Dependency Policy
Formal blockers in Linear; rationale in dependency map.

## Research-To-Issue Policy
Required work becomes issues; non-blocking expansions become candidates.

## Continuous Issue Discovery Policy
Classify as Blocker, Dependency, Defect, Research follow-up, Implementation follow-up, Decision required, QA / verification gap, Documentation gap, Scope expansion, or Risk / mitigation.

## Verification Policy
Issue-level verification before Done and final read-back before closeout.

## Agent Handoff Policy
Each issue preserves ownership, dependencies, verification, and context recovery notes.

## Coordinator Responsibilities
Deduplication, dependencies, Linear state, ledger updates, final integration, and release readiness.

## Expanded-Mode Issue Body

## Objective
Own one delivery outcome.

## Background Context
Why this issue exists and what prior work matters.

## Why This Matters
What breaks if this is skipped.

## Inputs / Required Reading
- Operating guide
- Dependency map
- Relevant source files

## Owned Scope
- Exact files, docs, modules, or workstream area.

## Non-Owned Scope
- Shared release metadata unless explicitly assigned.

## Dependencies
- Upstream issues and docs.

## Blockers
- Human gates, external docs, or unresolved decisions.

## Step-By-Step Working Instructions
1. Read inputs.
2. Implement the owned scope.
3. Update required local docs or ledger entries.

## Expected Outputs
- Changed files or research artifact.

## Acceptance Criteria
- Outcome is reviewable without chat context.

## Verification Requirements
- Exact commands, read-back, or review gates.

## Handoff / Context Recovery Notes
- What future agents need after compaction.

## Follow-Up Issue Candidates
- Proposed non-blocking discoveries.

## Required Updates
- Ledger, local docs, dependency map, or Linear relationships when project shape changes.

## Continuous Discovery Issue Candidate

## Why It Was Discovered
Found during implementation while checking acceptance criteria.

## Surfaced By
MAS-123 / Workstream: Verification.

## Classification
QA / verification gap.

## Blocks / Depends On
Blocks release gate.

## Phase / Workstream
Verification and release.

## Acceptance Criteria
- The missing check is documented and passes.

## Future-Agent Context
- Re-run the gate before marking release work Done.

## Final Completion Comment

Changed files:
- `SKILL.md`

Verification:
- `python3 tools/linear-agent-evaluator.py`: SCORE 130/130

Residual risks:
- Real Linear API smoke tests require credentials and issue capacity.

Follow-ups:
- Create linked issues for any blocked binary checks.
