# Runtime, Model, And State Guidance

This reference keeps model/runtime guidance separate from the core skill path so
future agents can load it only when they are building API-level or hosted-agent
integrations.

## Model And Runtime Roles

- Use the strongest available reasoning model for coordinator work when the
  project is ambiguous, long-running, or tool-heavy.
- Use lower-latency or lower-cost workers for bounded read-only research when
  the runtime permits subagents and the task is independently verifiable.
- Use stronger implementation agents for code changes that touch shared
  contracts, direct-write tooling, security behavior, or release gates.
- If subagents are unavailable or policy-gated, keep the Linear issues
  parallel-ready but execute them serially.

## Responses API State

For API users building around this skill:

- Prefer `previous_response_id` for multi-turn state when possible.
- For stateless or Zero Data Retention flows, pass back the relevant returned
  output items each turn.
- Preserve the `phase` field on assistant output items when manually replaying
  state across repeated tool calls.
- Use the companion ledger as the durable cross-session summary: completed
  actions, active assumptions, IDs, tool outcomes, blockers, and next goal.

## Date And Time

Do not add generic current-date instructions just to help the model. Add explicit
date or timezone context only when the workflow needs a business-specific
timezone, policy-effective date, due date, or user-local calendar interpretation.
