# Expanded Mode Dogfood

- Project: Linear Project Planner Expanded Mode
- Linear issue: MAS-706
- Status: completed dogfood pass
- Validation mode: standard plus expanded-mode dogfood
- Owner: Codex coordinator
- Updated: 2026-04-29

## Scenario

Dogfood the implemented expanded-mode workflow against the skill's own
long-horizon planning project. The project included research, local docs,
dependency mapping, parallel-agent allocation, synthesis gates, implementation,
verification, and installed runtime sync.

## Checks

| Check | Result | Evidence |
|---|---|---|
| Explicit expanded-mode trigger present | Pass | User requested second/expanded mode, deep research, local docs, and heavy safe parallelism |
| Baseline snapshot created first | Pass | `docs/research/baseline-current-skill-contract.md` and MAS-690 |
| Research happened before implementation | Pass | MAS-691 through MAS-698 completed before MAS-703 |
| Parallel agents used only after ownership gates | Pass | Research and spec waves each had one owned file per worker |
| Local docs folder created | Pass | `docs/expanded-mode/linear-project-planner-expanded-mode/` |
| Dependency map created | Pass | `dependencies/dependency-map.md` |
| Runtime reference and templates installed | Pass | `./install.sh --with-docs` and installed read-back |
| Baseline verification passed | Pass | Full test/evaluator/syntax/YAML/install suite passed |
| Linear graph read back | Pass | MAS-691 through MAS-706 states read back from Linear |

## Findings

- Expanded mode produced useful structure for this project because the work was
  genuinely long-horizon, self-editing, research-heavy, and dependency-heavy.
- The local docs folder is useful once implementation exists, but early research
  docs still belong in `docs/research/` until the runtime convention is stable.
- The mode gate is important: ordinary Linear projects should not inherit this
  folder structure or research burden.
- No new CLI command was needed for the first implementation. Evaluator
  coverage was enough to prove the additive mode contract.

## Follow-Ups

- Public GitHub release remains a human-gated decision under MAS-707.
- Future enhancement: add an optional fake expanded-mode graph fixture if the
  CLI later generates the docs folder automatically.

## Verification Run

```bash
bash tests/test-linear-agent.sh
python3 -m unittest tests/test_linear_agent_graphql.py tests/test_linear_agent_graph_features.py
python3 tools/linear-front-door-evaluator.py
python3 tools/linear-agent-evaluator.py
python3 tools/linear-skill-audit-evaluator.py
bash -n install.sh
bash -n scripts/linear-agent
bash -n tests/test-linear-agent.sh
python3 -m py_compile lib/linear_agent/__init__.py lib/linear_agent/ledger.py lib/linear_agent/graphql.py lib/linear_agent/graph.py lib/linear_agent/cli.py tools/linear-front-door-evaluator.py tools/linear-agent-evaluator.py tools/linear-skill-audit-evaluator.py
ruby -e 'require "yaml"; skill = File.read("SKILL.md"); frontmatter = skill.match(/\A---\n(.*?)\n---/m)[1]; YAML.safe_load(frontmatter); YAML.load_file("agents/openai.yaml"); puts "yaml ok"'
./install.sh --check
```

Result: all checks passed. `shellcheck` was not available locally.
