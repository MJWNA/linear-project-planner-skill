# Dogfood Loop

Status: active
Linear issue: MAS-1015

## Pass 1 Inputs

- User prompt requesting expanded-mode execution, Ralph Wiggum loop, and
  auto-research style iteration.
- Linear project MAS-1004 through MAS-1022.
- Research docs under
  `docs/expanded-mode/linear-skill-outer-harness-upgrade/research/`.
- Decision docs under
  `docs/expanded-mode/linear-skill-outer-harness-upgrade/decisions/`.
- Changed policy surfaces: `SKILL.md`, `references/execution-hygiene.md`,
  `references/operator-cheatsheet.md`, `references/command-schemas.md`,
  `README.md`, `tools/linear-agent-evaluator.py`.

## Pass 1 Checks

- `python3 tools/linear-front-door-evaluator.py`: `SCORE 235/235`
- `python3 tools/linear-agent-evaluator.py`: first failed at `SCORE 190/200`;
  evaluator caught missing/changed direct-mode wording.
- Corrective patch added the exact fallback/read-back phrase.
- `python3 tools/linear-agent-evaluator.py`: `SCORE 200/200`
- YAML/frontmatter load check: `yaml ok`
- `linear-agent graph-plan --from docs/expanded-mode/linear-skill-outer-harness-upgrade/linear-graph.json --json`: passed
- `linear-agent graph-readback --from docs/expanded-mode/linear-skill-outer-harness-upgrade/linear-graph.json --json`: `drift=[]`

## Findings

- The first graph was too flat; corrected into 5 parent workstreams and 13
  child issues.
- Linear API project creation blocked on description length; MCP fallback
  created the project shell, then API graph apply resumed successfully.
- MCP project status update was unavailable; a fallback comment was posted on
  MAS-1018.
- The evaluator failure was useful sensor evidence: wording checks now protect
  the hard API-primary/MCP-fallback rule.

## Next Loop Decision

Proceed to broader implementation loop: recursive validation guidance, sensor
timing, ledger loop tracking, and final verification suite.
