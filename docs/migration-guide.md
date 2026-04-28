# Migration Guide: Manual Linear To Agent-Ready Linear

## Existing Flat Backlog

1. Create the companion ledger.
2. Add or identify the two guide issues.
3. Group existing tickets into parent workstreams.
4. Add dependencies for true sequencing only.
5. Label parallel-safe, serial-required, overlap-zone, verification-missing, and production-risk work.
6. Add verification criteria to every issue before execution starts.

## New Projects

Start with the graph file and run `linear-agent graph-plan --from graph.json` before creating live issues.

## Cleanup Rules

- Keep historical tickets if they carry useful context.
- Merge duplicate tickets only after preserving evidence.
- Do not mark an old issue Done unless verification exists.
- Record any skipped production or sink gate as not applicable with a reason.

## Before And After

Before: one list of tasks with no order, ownership, or evidence.

After: guide issues, workstreams, child issues, dependency edges, allocation lanes, and a ledger that records verification.
