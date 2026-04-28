# Linear Token Scope And Redaction

Use the least-privilege Linear token that can perform the requested operation.

## Local Development

- Prefer dry-run mode unless the user asked for live Linear mutation.
- Use `LINEAR_API_KEY` for direct Linear writes only in trusted local shells or secret-gated CI jobs.
- Use `LINEAR_ACCESS_TOKEN` only when OAuth is the configured workspace path.
- Never commit tokens, generated ledgers with private Linear data, or smoke-test secrets.

## CI Smoke Tests

The live smoke workflow is manual and requires a disposable project. It should not run on normal pull requests or forks.

## Redaction Rule

Failure messages must not echo token values. Tests should cover HTTP and GraphQL errors containing token-like values and verify the output replaces them with `[REDACTED]`.

## Safe Bug Reports

When reporting a bug, include:

- command name
- redacted environment summary
- relevant ledger row
- fake transport fixture if possible

Do not include:

- real Linear tokens
- private customer data
- unredacted project exports
