# Validation Modes, Production Gates, And Sink Preservation

Use this reference when deciding how deep verification should be.

## Standard Validation

Standard validation is mandatory for every project:

- clear acceptance criteria
- issue-level verification before `Done`
- Linear read-back after state changes
- final reconciliation
- completion/finalization evidence

Record standard mode in the ledger:

```md
- Validation mode: standard
- Deep auto-research loop: not requested
```

## Optional Deep Auto-Research

Deep auto-research is optional. Add it only when:

- the user explicitly asks for auto-research, dogfooding, recursive testing,
  repeated evaluator passes, long-horizon iteration, or failure-discovery loops
- the user approves the deeper loop during planning
- the project is a release/publish gate, production-risk remediation,
  high-uncertainty migration, or safety-critical change and the user has agreed
  to the extra depth

If unclear, ask:

```txt
Do you want standard validation only, or the deeper auto-research loop with repeated evaluator passes and follow-up task creation?
```

When enabled:

1. Define a fixed binary or numeric evaluator.
2. Freeze the evaluator before the final loop.
3. Make one focused change or hypothesis at a time.
4. Run the benchmark or check.
5. Keep the change only if correctness remains green.
6. Revert or create a follow-up task when the experiment fails.
7. Record learnings in the ledger.
8. Repeat until stable and no high-priority binary failures remain.

Do not mutate the evaluator mid-loop unless the issue is explicitly to repair an
invalid evaluator.

## Good Evaluators

- test pass/fail
- lint or typecheck error counts
- build success
- API contract checks
- route/auth/RBAC matrices
- database migration validation
- output snapshot comparisons
- accessibility or performance scores
- repo readiness score
- `linear-agent reconcile` drift result

## Production App Gates

For live production apps, add first-class issues for:

- production env/deployment readiness
- cron/job inventory
- auth/RBAC route inventory
- data/business-output semantics
- sink/output behavior-lock matrix

These prevent agents from improving internals while breaking business outcomes.

## Sink / Output Preservation

For syncs, imports, ETL, webhooks, crons, reporting, AI pipelines, and other
sinks:

- document destination tables, UI surfaces, reports, alerts, and downstream jobs
- capture the current correct practical output before refactoring
- require before/after comparison, not only unit tests
- treat output changes as product changes requiring explicit approval
- include backfill/migration notes if historical data changes

Use wording like:

```md
Preserve existing practical output unless this issue explicitly changes it.
Internals may be messy; business-facing populated data is the contract.
```
