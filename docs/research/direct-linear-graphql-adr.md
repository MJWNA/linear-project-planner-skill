# ADR: Direct Linear GraphQL For Project Graph Creation

## Status

Accepted for `v3.6.0`.

## Context

The skill frontmatter promises that agents can create Linear projects, but the
live implementation previously depended on whatever Linear MCP server a runtime
provided. The CLI only performed direct GraphQL writes for issue transitions and
comments; graph creation stayed gated or delegated.

That made project creation runtime-dependent, blocked idempotent re-runs after
partial failure, and kept graph read-back weaker than the graph plan contract.

## Decision

`linear-agent graph-apply --apply-linear` now writes project graph mutations
directly to `https://api.linear.app/graphql` when `LINEAR_API_KEY` or
`LINEAR_ACCESS_TOKEN` is available.

The implementation keeps dry-run as the default and preserves the manual
fallback path for runtimes without credentials. Direct API mode owns:

- project create/update
- label create/update
- milestone create/update
- issue create/update
- issue relation create
- attachment create/update
- project read-back for graph drift and project-scan reconcile

## Consequences

- Linear MCP is no longer required for graph creation.
- The fake transport must mirror every live operation used by graph apply.
- Attachment URLs must be valid HTTP(S) URLs; local `file://` ledger paths stay
  in issue bodies or the companion ledger.
- Rich project read-back must stay under Linear's complexity budget, so scans
  use bounded nested fields and pagination.
- Every mutation path must check the `success` flag and read Linear back before
  reporting completion.
