# Manual Linear Smoke Tests

Live Linear smoke tests prove that the `linear-agent` wrapper, GraphQL transport,
ledger reconciliation, status transitions, dependency writes, and completion
comments still work against the real Linear API.

They complement the hermetic fake-transport suite. They do not replace it.

## Fake Transport Versus Live Smoke

The default CI path uses fake transport fixtures. That path is deterministic,
fast, safe for forks, and suitable for every pull request. It should cover CLI
parsing, GraphQL payload shape, redaction, ledger parsing, dependency handling,
and fail-closed behavior without sending traffic to Linear.

The live smoke path mutates a real Linear workspace. It validates the parts that
fixtures cannot fully prove:

- token scope and authentication
- Linear schema compatibility
- issue/project/state/comment mutations
- dependency edge creation and read-back
- rate-limit and API error handling at the real boundary
- reconciliation between the local ledger and Linear state

Run live smoke tests sparingly and record the evidence. Normal development
should stay on fake transport unless a release, transport change, or Linear API
compatibility question requires a live check.

## Why Manual

Live Linear smoke tests are manual and secret-gated because they require a real
workspace token and create disposable Linear objects.

They should not run automatically on normal pull requests because:

- forked PRs must never receive Linear secrets
- repeated CI runs would create noisy projects, issues, comments, and labels
- API quota and rate-limit failures would make unrelated PRs flaky
- accidental writes to a production planning project could corrupt execution
  state
- cleanup must be confirmed by a human or release operator

Use a manual workflow dispatch, trusted local shell, or protected release job
that only maintainers can run.

## Prerequisites

Required local or CI secrets:

- `LINEAR_API_KEY`: Linear API token with the least privilege needed to create,
  update, comment on, and delete or archive disposable test objects.
- `LINEAR_TEAM_ID` or an equivalent team selector accepted by the smoke script.
- Optional `LINEAR_API_URL`: only use the default `https://api.linear.app/graphql`
  unless intentionally testing a non-production endpoint.

Disposable Linear target requirements:

- use a dedicated test team, sandbox workspace, or clearly named disposable
  project area
- name test objects with a searchable prefix such as
  `linear-agent-smoke-YYYYMMDD-HHMM`
- do not point the smoke run at an active production remediation project
- do not use customer data, private business context, or real release evidence
  in generated test descriptions
- ensure the token can clean up or archive every object the smoke run creates

Before running, confirm:

- the local branch is the intended release or PR branch
- fake-transport CI passes
- the smoke target is disposable
- the operator understands the cleanup plan

## When To Run

Run a live smoke test before merging or tagging when a change touches:

- `scripts/linear-agent`
- `lib/linear_agent/graphql.py`
- `lib/linear_agent/graph.py`
- `lib/linear_agent/ledger.py`
- CLI command wiring in `lib/linear_agent/cli.py`
- GraphQL mutations, query fields, dependency handling, or read-back logic
- release workflows that claim live Linear compatibility

Also run it when:

- Linear returns unexpected schema or permission errors
- a new token scope is introduced
- a release candidate changes the ledger finalization contract
- a maintainer needs evidence that the installed skill can still mutate Linear
  end to end

Do not run live smoke tests for documentation-only changes unless the release
manager explicitly asks for a full release gate.

## Procedure Checklist

Record the command output, Linear URLs, created object identifiers, and cleanup
result in the PR, release issue, or companion ledger.

- [ ] Confirm fake-transport tests pass locally or in CI.
- [ ] Export `LINEAR_API_KEY` in a trusted shell or protected manual CI job.
- [ ] Select a disposable team or project target.
- [ ] Create a unique smoke-run prefix.
- [ ] Run the live smoke command in dry-run mode first if the command supports
  it.
- [ ] Run the live smoke command with real Linear writes enabled.
- [ ] Confirm the smoke project or issues exist in Linear.
- [ ] Confirm status transitions are visible in Linear.
- [ ] Confirm comments are written and redacted where expected.
- [ ] Confirm dependency edges or related links are created when the test covers
  graph behavior.
- [ ] Run reconciliation or read-back and confirm local state matches Linear.
- [ ] Capture links and IDs for evidence.
- [ ] Clean up or archive every disposable object.
- [ ] Re-run read-back or search to confirm cleanup.

Example evidence note:

```md
Live Linear smoke test: PASS
Date: YYYY-MM-DD
Operator: <name>
Branch/commit: <branch>@<sha>
Target: <workspace/team/project>
Prefix: linear-agent-smoke-YYYYMMDD-HHMM
Commands:
- <command>
- <command>
Created objects:
- <Linear project or issue URL>
- <Linear issue URL>
Verified:
- status transition read-back
- completion comment read-back
- dependency edge read-back
- ledger reconciliation
Cleanup:
- archived/deleted <objects>
- post-cleanup search/read-back confirmed no active smoke objects
Residual risk:
- <none or specific limitation>
```

## Cleanup

Cleanup is part of the smoke test, not a follow-up chore.

After the live check:

- archive or delete every disposable project, issue, comment, label, and
  dependency edge created by the run when Linear permissions allow it
- remove temporary local ledgers or generated smoke artifacts that contain
  private Linear URLs
- never commit generated smoke ledgers, tokens, API responses, or screenshots
  containing private workspace data
- if cleanup is blocked, leave a comment in the release issue with the object
  URLs, blocker, owner, and retry plan

The release gate is incomplete until cleanup evidence is recorded.

## Evidence

Minimum evidence for a release gate:

- branch and commit SHA
- command or workflow name
- Linear target workspace/team/project
- created issue/project URLs or IDs
- read-back output proving mutation success
- cleanup output proving disposable objects were removed or archived
- token scope notes without exposing the token
- residual risk or explicit `none`

Store the evidence in the PR, release issue, or companion execution ledger. Use
links instead of long pasted API responses where possible, and redact private
workspace details before sharing outside the trusted team.
