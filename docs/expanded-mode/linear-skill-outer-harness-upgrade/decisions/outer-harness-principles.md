# Outer Harness Principles

Status: accepted first pass
Linear issue: MAS-1011

## Accepted Principles

1. Linear is the control plane, but the ledger is the recovery memory.
2. API-primary is mandatory when credentials exist; MCP fallback is mandatory
   when the API path blocks, is missing, or cannot prove read-back.
3. Expanded mode is the outer-harness layer; baseline mode remains concise.
4. Guides improve first-pass quality; sensors make misses self-correcting.
5. Computational sensors run before inferential sensors wherever possible.
6. Recursive loops create issues only for actionable misses.
7. Future-agent recoverability is a quality gate, not a nice-to-have.
8. Proof of work should be structured enough for a coordinator to trust after
   context compaction.

## Implementation Decisions

- Keep `SKILL.md` short and route deeper behavior into references.
- Put API/MCP fallback policy in `SKILL.md`, `references/execution-hygiene.md`,
  `references/operator-cheatsheet.md`, `references/command-schemas.md`, and
  README.
- Put recursive loop and sensor timing in validation/expanded-mode references
  and the ledger template.
- Treat scheduler/runner work as a future reference and test surface, not part
  of this immediate patch.

## Follow-Up Candidates

- Add `references/scheduler-contract.md` in a later issue if unattended runner
  behavior becomes in scope.
- Add proof-of-work blocks to issue fixtures and completion comment templates.
- Add inferential review prompts for future-agent recoverability.

