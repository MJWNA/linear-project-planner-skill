# Example: Production Hardening Project

## Intended Linear Graph

- Guide: Agent Operating Guide
- Guide: Verification Matrix
- Workstream: Env And Deploy Readiness
- Workstream: Auth And RBAC
- Workstream: Cron And Integrations
- Workstream: Data Semantics And Sinks
- Workstream: Release And Monitoring

## Gate Matrix

- env/deploy: required variables, preview/prod parity, rollback command
- auth/RBAC: roles, memberships, route protection, audit cases
- cron/jobs: schedule, idempotency, retry behavior, owner
- data semantics: migrations, reporting numbers, money/compliance meaning
- sinks: imports, exports, webhooks, reports, dashboards

## Verification Matrix

- local tests
- migration dry-run
- browser or API smoke tests
- production sink before/after comparison
- post-deploy observation window

## Final Completion Comment

Include changed files, verification commands, deployment URL, monitoring evidence, and residual risks.
