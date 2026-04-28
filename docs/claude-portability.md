# Claude Portability

This repository is **Codex-first** and **Claude-compatible by manual install**.

The skill contract is written in portable `SKILL.md` form, and the CLI is a
plain shell/Python wrapper. However, the install script defaults to Codex paths
because this repository is maintained from a Codex environment.

## Supported Today

- Codex install target: `~/.codex/skills/linear-project-planner`
- Codex launcher: `~/.local/bin/linear-agent`
- Portable skill files: `SKILL.md`, `references/`, `templates/`, `scripts/`,
  `lib/`, `docs/`
- Manual Claude Code install by copying the skill directory to
  `~/.claude/skills/linear-project-planner`

## Manual Claude Code Install

From the repository root:

```bash
mkdir -p ~/.claude/skills/linear-project-planner
rsync -a --delete \
  --exclude '.git' \
  --exclude '.github' \
  --exclude 'install.sh' \
  ./ ~/.claude/skills/linear-project-planner/
chmod +x ~/.claude/skills/linear-project-planner/scripts/linear-agent
```

Claude Code can then discover the skill as a personal skill. The `description`
frontmatter and first operating section are intentionally trigger-oriented so
Claude can invoke it automatically for Linear project planning, and users can
invoke it manually by name where supported.

## Caveats

- The included `install.sh` does not yet provide a first-class
  `--runtime claude` mode.
- MCP tool names and connector availability differ between Codex and Claude
  environments. Agents should use whichever Linear integration is available and
  keep the same ledger/status/comment/read-back discipline.
- The recommended ledger path uses `.codex-linear-ledgers/` in this repo because
  the current workspace is Codex-owned. Claude agents may use the same path for
  continuity or a project-agreed equivalent.
- `agents/openai.yaml` is an OpenAI/Codex-oriented manifest. It is not a Claude
  manifest.

## What Full Claude Parity Would Require

- `install.sh --runtime claude` or equivalent.
- A documented Claude-specific install/check mode.
- Optional Claude plugin or manifest support if using a supported Claude format.
- A verification path that proves Claude can discover the skill and run the
  `linear-agent` wrapper from the copied location.

Until those are implemented, describe the project as Codex-first with
Claude-compatible manual install rather than fully cross-runtime.
