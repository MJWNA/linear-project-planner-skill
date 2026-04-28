# Example: Parallel Remediation Project

## Intended Linear Graph

- Guide: Agent Operating Guide
- Guide: Verification Matrix
- Workstream: Shared Contracts
- Workstream: Independent Fix Lanes
- Workstream: Final Reconcile

## Allocation

Run:

```bash
linear-agent allocate --from graph.json --ledger EXECUTION.md
```

Each write-capable lane gets:

- one issue
- one branch
- one worktree
- one write set
- one merge/reconcile order

## Sparse Links

Link each issue to only the files, docs, and verification artifacts required for that issue. Avoid linking every issue to every other issue.

## Final Completion Comment

Record each lane, merge order, conflict resolution, tests, and final graph read-back.
