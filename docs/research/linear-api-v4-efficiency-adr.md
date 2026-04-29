# ADR: Linear API v4 Efficiency And Schema Alignment

Accepted for `v4.0.0`.

## Context

The direct GraphQL implementation introduced in `v3.6.0` removed the Linear MCP
dependency for graph creation. A follow-up review against Linear's official API
documentation and live GraphQL schema found several places where the skill could
use the API more accurately and efficiently:

- project teardown used a stale `projectArchive` mutation name
- issue creation did not use `issueBatchCreate`
- project read-back accepted pagination inputs but callers only fetched one page
- relation support covered blockers but not related or duplicate edges
- attachment creation omitted source metadata
- rate-limit handling retried limit errors but did not inspect response headers

## Decision

The v4 implementation aligns the skill with the live schema and treats Linear's
GraphQL API as the primary execution engine:

- use `projectDelete` for disposable smoke teardown
- batch-create absent issue groups with `issueBatchCreate`
- scan `project.issues` starting with `first: 250` and cursor pagination until
  `pageInfo.hasNextPage` is false, reducing page size when Linear reports that
  the rich read-back query is too complex
- support `blocks`, `related`, and `duplicate` relation types in graph plans
- include `linear-project-planner` attachment metadata and group attachments by
  source
- record rate-limit and complexity headers and slow down before the request or
  complexity budget is exhausted

## Consequences

Graph bootstrap is faster, reconcile is accurate for larger projects, and
smoke teardown no longer depends on a mutation that is absent from the live
schema. The implementation still keeps the dry-run default, fake transport
safety gate, token redaction, and read-back-after-mutation behavior.

The Linear Agent Session and Agent Activity APIs are intentionally deferred.
They are best suited to a future OAuth/app integration, while `v4.0.0` remains
usable with a personal API key.
