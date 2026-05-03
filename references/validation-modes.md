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

## Ralph Wiggum / Auto-Research Loop

For expanded-mode or explicitly recursive projects, use two related but
separate loops:

- Ralph Wiggum loop: repeated review and correction until deterministic and
  inferential reviewers are satisfied.
- Auto-research loop: metric-driven optimization with a frozen evaluator,
  one focused change, benchmark/check, keep or revert, and learning capture.

Before the loop starts, record the loop type, source scope, frozen evaluator
set, issue-creation threshold, and stop condition in the ledger or verification
matrix. A miss becomes a Linear issue only when it affects correctness,
acceptance criteria, dependency order, verification, or future-agent recovery.
Otherwise, record it as a learning or issue candidate.

Return failed passes to the smallest responsible issue rather than restarting
the whole project. Do not mark an issue `Done` until frozen deterministic
sensors pass, inferential review is resolved or explicitly deferred, Linear
read-back is clean, and the ledger/handoff agree.

## Sensor Timing

Use sensors as an outer-harness feedback stack:

| Phase | Computational Sensors | Inferential Sensors |
|---|---|---|
| Before planning | Graph/schema/template checks | Source-scope and problem-framing review |
| Before issue creation | `graph-plan`, dependency cycle checks | Issue actionability and future-agent recovery review |
| Before implementation | Dirty tree, write-scope, dependency checks | Ownership and sequencing review |
| Before Done | Tests, evaluators, syntax/YAML, read-back | Acceptance evidence and residual-risk review |
| Before closeout | `reconcile`, install checks, release checks | Handoff, proof-of-work, and baseline-contamination review |

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
