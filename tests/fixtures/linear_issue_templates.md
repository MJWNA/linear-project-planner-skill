# Linear Issue Template Fixtures

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

## Final Completion Comment

Changed files:
- `SKILL.md`

Verification:
- `python3 tools/linear-agent-evaluator.py`: SCORE 130/130

Residual risks:
- Real Linear API smoke tests require credentials and issue capacity.

Follow-ups:
- Create linked issues for any blocked binary checks.
