# API Primary / MCP Fallback Decision

Status: accepted for this project
Linear issue: MAS-1010

## Decision

The skill must treat direct Linear GraphQL as the primary path whenever
`LINEAR_API_KEY` or `LINEAR_ACCESS_TOKEN` is available, and must use the Linear
MCP connector as the fallback whenever the direct API path cannot complete and
prove the requested Linear state.

## Fallback Triggers

Use MCP fallback when:

- credentials are unavailable to the current runtime;
- the user explicitly requests the connector;
- the direct API operation is not implemented in `linear-agent`;
- the API is unavailable or blocked;
- Linear rejects or blocks a valid operation;
- direct API read-back cannot confirm the requested state;
- the available API path would require unsafe manual guessing.

## Evidence Rule

Every fallback must record:

- the attempted primary API command or operation;
- the failure or block reason;
- the MCP fallback action;
- the read-back or comment evidence proving the resulting state;
- any follow-up issue if the fallback exposed a missing direct API capability.

## Project Evidence

During this dogfood project, `linear-agent graph-apply --apply-linear` was tried
first. Linear rejected the project creation payload because project descriptions
must be 255 characters or shorter. The project shell was then created with the
Linear MCP connector using a compact description. After the graph description
was compacted, `linear-agent graph-apply --apply-linear` succeeded and
`linear-agent graph-readback --from ... --json` returned `drift=[]`.

The MCP project status update tool was unavailable in this workspace, so a
fallback comment was posted on MAS-1018 and recorded in the ledger.

## Implementation Surfaces

- `SKILL.md`: hard user-facing rule.
- `references/execution-hygiene.md`: transition and evidence behavior.
- `references/operator-cheatsheet.md`: minimal safe path.
- `references/command-schemas.md`: structured command contract.
- `README.md`: operator-facing docs and troubleshooting.
- Evaluators/tests: assert the fallback rule stays present.
