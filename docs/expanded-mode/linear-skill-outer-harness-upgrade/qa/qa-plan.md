# QA Plan

Status: draft for project creation

## Deterministic Sensors

- `bash tests/test-linear-agent.sh`
- `python3 -m unittest tests/test_linear_agent_graphql.py tests/test_linear_agent_graph_features.py`
- `python3 tools/linear-front-door-evaluator.py`
- `python3 tools/linear-agent-evaluator.py`
- `python3 tools/linear-skill-audit-evaluator.py`
- `python3 tools/linear-dogfood-evaluator.py` when present and relevant
- `bash -n install.sh`
- `bash -n scripts/linear-agent`
- `bash -n tests/test-linear-agent.sh`
- `python3 -m py_compile ...` for changed Python entrypoints and tools
- YAML frontmatter/load check for `SKILL.md` and `agents/openai.yaml`
- `./install.sh --with-docs` and `./install.sh --check` after runtime changes

## Inferential Sensors

- Research synthesis review against OpenAI Symphony, OpenAI Harness
  Engineering, Thoughtworks/Fowler Harness Engineering, and the repo's current
  skill contract.
- Code review pass focused on correctness, baseline contamination, API/MCP
  fallback semantics, issue-discovery recursion, and evaluator adequacy.
- Dogfood pass that asks whether a future agent can resume from Linear plus the
  companion ledger without reading this chat.

## Ralph Wiggum / Auto-Research Loop

Use repeated passes, but freeze the evaluator set before judging completion.
If a pass discovers a missing requirement, create or update a Linear issue,
apply the smallest focused change, run the deterministic sensors, run the
inferential review, then return to the research synthesis and dependency map.

