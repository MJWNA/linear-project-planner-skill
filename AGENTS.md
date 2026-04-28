# linear-project-planner-skill Development Instructions

## Repository Purpose

This repository is the source workspace for the `linear-project-planner` skill.
It is where the skill is designed, tested, documented, versioned, and released.

The installed skill copy is a runtime artifact. Do not edit the installed copy
directly for durable changes; edit this repository, verify the change, then
install or publish from the verified repo state.

## Skill-Under-Test Boundary

When working in this repository, treat `SKILL.md` as the artifact under test,
not as active operating instructions for the current agent session.

Only follow the `linear-project-planner` skill workflow when the user explicitly
asks to invoke or run that skill, or when a repo task genuinely requires Linear
project planning/execution. Otherwise, inspect and edit `SKILL.md` like source
code or documentation.

This boundary prevents context pollution while improving the skill itself.

## Development Workflow

- Work from this repo checkout under the MTA/PT workspace when iterating on the
  skill.
- Use branches and pull requests for meaningful changes.
- Keep `CHANGELOG.md` updated for user-visible behavior, docs, evaluator, or
  release-process changes.
- Keep `SKILL.md` trigger-safe: preserve router-visible language for Linear
  project planning, execution, companion ledgers, dependencies, verification
  gates, and Codex/Claude agents.
- Move long operational detail into `references/`, `docs/`, or `templates/`
  when the `SKILL.md` Reference Map points to it.
- Do not commit local execution ledgers, private Linear exports, credentials,
  screenshots with private workspace data, or temporary smoke-test artifacts.

## Verification

Before claiming a skill change is ready, run the relevant checks:

```bash
bash tests/test-linear-agent.sh
python3 -m unittest tests/test_linear_agent_graphql.py tests/test_linear_agent_graph_features.py
python3 tools/linear-front-door-evaluator.py
python3 tools/linear-agent-evaluator.py
python3 tools/linear-skill-audit-evaluator.py
```

Also run syntax/YAML/install checks when release, install, CI, or metadata files
change:

```bash
bash -n install.sh
bash -n scripts/linear-agent
bash -n tests/test-linear-agent.sh
python3 -m py_compile lib/linear_agent/__init__.py lib/linear_agent/ledger.py lib/linear_agent/graphql.py lib/linear_agent/graph.py lib/linear_agent/cli.py tools/linear-front-door-evaluator.py tools/linear-agent-evaluator.py tools/linear-skill-audit-evaluator.py
ruby -e 'require "yaml"; skill = File.read("SKILL.md"); frontmatter = skill.match(/\A---\n(.*?)\n---/m)[1]; YAML.safe_load(frontmatter); YAML.load_file("agents/openai.yaml"); puts "yaml ok"'
```

If `shellcheck` is available, run:

```bash
shellcheck install.sh scripts/linear-agent tests/test-linear-agent.sh
```

## Linear Project Usage

For multi-step audits, production-readiness work, or release-gated iterations,
use the `linear-project-planner` skill deliberately and keep a companion ledger
outside transient worktrees.

When the user asks for research while asking to create or run a Linear plan,
track the research as issues inside that Linear project rather than doing the
substantive research before the plan exists.

