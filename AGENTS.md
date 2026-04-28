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

## Name And Location Map

The same artifact has different names depending on where it is being used:

| Surface | Name / Path | Purpose |
|---|---|---|
| Public GitHub repo | `MJWNA/linear-project-planner-skill` | Canonical source repo for publishing, PRs, tags, CI, and releases |
| MTA/PT workspace checkout | `projects/linear-project-planner-skill` | Local development workspace under `/Users/ronniemeagher/Desktop/Curssor/mta-pt-workspace` |
| Codex installed skill | `~/.codex/skills/linear-project-planner` | Runtime copy loaded by Codex skill discovery |
| Skill name | `linear-project-planner` | Name in `SKILL.md` frontmatter and user-facing invocation |
| CLI launcher | `~/.local/bin/linear-agent` | Installed wrapper command for ledger and Linear transitions |

Do not confuse the repo name (`linear-project-planner-skill`) with the installed
skill name (`linear-project-planner`). The repo contains the skill source; the
installed skill path is the runtime copy.

## Parent Workspace / Submodule Behavior

This checkout lives inside the MTA/PT workspace under `projects/`, alongside
other standalone projects and submodules.

Treat this folder as its own Git repository. Run git commands from this
directory when changing the skill:

```bash
cd /Users/ronniemeagher/Desktop/Curssor/mta-pt-workspace/projects/linear-project-planner-skill
```

When pushing public changes:

1. Commit inside this repository.
2. Push this repository to `MJWNA/linear-project-planner-skill`.
3. Open and merge the PR against the public repo's `main`.
4. Only update the parent MTA/PT workspace pointer or submodule metadata if the
   user explicitly asks. The parent workspace is often dirty with unrelated
   project state.

Do not run broad parent-workspace cleanup, resets, or commits just because this
repo changed.

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

## Updating The Local Installed Skill

Whenever a change is intended to affect how Codex uses the skill, update the
local installed skill copy from this repository after verification:

```bash
./install.sh --with-docs
./install.sh --check
```

This keeps `~/.codex/skills/linear-project-planner` aligned with the public
repo source. Do this after merging or pulling public repo changes, and after
local changes that should be available to Codex immediately.

If a change is only a repo-development note, CI setting, or contributor doc that
does not affect runtime skill behavior, installing is optional. When unsure,
install and check.

Never manually edit files under `~/.codex/skills/linear-project-planner` to
make durable changes. Edit this repo, run verification, then install from here.

If Claude is also being used, follow `docs/claude-portability.md` for the manual
Claude skill copy. The Codex installer does not yet update Claude's skill path.

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
