# Operator Cheatsheet

Use this when you need the smallest safe path through the skill.

## Minimal Safe Path

1. Create or open the execution ledger.
2. Create the two guide issues: Agent Operating Guide and Verification Matrix.
3. Create parent workstreams before child issues.
4. Start one dependency-ready issue with `linear-agent start`.
5. Verify before `linear-agent complete`.
6. Reconcile Linear and finalize only after every issue row is done.

## Small Project Issue Set

- Guide: Agent Operating Guide
- Guide: Verification Matrix
- Workstream: Implementation
- Workstream: Verification And Release
- Child: Implement requested change
- Child: Add or update tests
- Child: Final read-back and closeout

## Production Project Path

Add gates before implementation issues:

- env and deploy readiness
- auth/RBAC inventory
- cron/job inventory
- data semantics and migration safety
- sink/output preservation
- rollback and monitoring

## Live Linear Graph Path

1. Draft a graph file.
2. Run `linear-agent graph-plan --from graph.json`.
3. Run `linear-agent allocate --from graph.json` to check lanes.
4. Apply with `linear-agent graph-apply --apply-linear` when Linear API
   credentials are available. Use Linear app/MCP/manual actions only as the
   fallback when credentials are unavailable, the user explicitly requested
   the connector path, the direct API operation is not implemented, the API
   blocks a valid request, or read-back cannot confirm the result.
5. Run `linear-agent graph-readback --from graph.json`.

## Local-Only Audit

Use local-only output when the user asks for an audit, scorecard, or proposal and has not asked you to mutate Linear. Preserve the intended Linear graph in the ledger or Markdown report.
