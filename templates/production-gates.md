# Production And Sink Gate Templates

Use these as draft gates. The agent must adapt them to the actual repo before treating them as source of truth.

## Next.js / Vercel App

- Env/deploy: `vercel.json`, framework version, build command, required env vars, preview/prod parity.
- Auth/RBAC: route middleware, server actions, API routes, role checks, session handling.
- Jobs: cron routes, queue consumers, revalidation paths.
- Data: migrations, schema ownership, caching, stale data risk.
- Sinks: forms, webhooks, analytics, emails, exports.
- Rollback/monitoring: previous deployment, logs, error tracking, smoke URL.

## Cron-Heavy Backend

- Schedule inventory, owner, timezone, retry behavior, idempotency key.
- Downstream APIs, rate limits, dead-letter or alert path.
- Last successful run and rollback/suspend instructions.

## Data Sync / ETL Project

- Source systems, target systems, high-water marks, dedupe keys.
- Backfill strategy and replay protection.
- Sink/output preservation checks with before/after snapshots.

## Auth / RBAC App

- User model, memberships, roles, permissions, tenant boundary.
- Negative tests for unauthorized access.
- Admin bypass and audit log policy.

## Reporting / Dashboard App

- Metric definitions, timezones, filters, aggregation grain.
- Sink/report outputs that must not change without approval.
- Before/after numeric comparison and known tolerances.
