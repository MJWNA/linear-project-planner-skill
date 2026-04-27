# Linear Project Planner Skill

Agent-ready Linear project planning and execution workflow for Codex-style skill runtimes.

This skill turns a Linear project into an execution system rather than a flat todo list. It standardises milestones, parent workstreams, guide issues, labels, dependency notes, companion Markdown ledgers, transition hygiene, verification gates, and handoff comments.

## What It Provides

- A reusable `SKILL.md` for planning, creating, restructuring, and executing Linear projects.
- A companion `EXECUTION.md` ledger template that survives context compaction.
- A `linear-agent` wrapper for deterministic local ledger transitions.
- Regression tests for wrapper behaviour and ledger finalisation.
- Agent metadata in `agents/openai.yaml`.

## Repository Layout

```txt
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   └── linear-agent
├── templates/
│   └── EXECUTION.md
└── tests/
    └── test-linear-agent.sh
```

## Install

From this repository root:

```bash
./install.sh
```

That copies the skill into `~/.codex/skills/linear-project-planner` and installs a `linear-agent` launcher into `~/.local/bin`.

## Test

```bash
bash tests/test-linear-agent.sh
```

Optional, if installed locally:

```bash
shellcheck scripts/linear-agent tests/test-linear-agent.sh
```

## Usage

Invoke the skill when a task involves creating or executing a Linear project for agents:

```txt
Use the linear-project-planner skill to create an agent-ready Linear remediation project.
```

Use the transition wrapper while executing issues:

```bash
linear-agent init --ledger /path/to/EXECUTION.md --project "Project Name" --prompt "Original prompt"
linear-agent start MAS-123 --ledger /path/to/EXECUTION.md --agent Codex --worktree /path/to/repo
linear-agent verify MAS-123 --ledger /path/to/EXECUTION.md --verification "tests pass"
linear-agent complete MAS-123 --ledger /path/to/EXECUTION.md --verification "tests pass"
linear-agent finalize --ledger /path/to/EXECUTION.md --verification "Linear read-back complete; checks pass"
```

The wrapper updates the Markdown ledger and prints the Linear MCP actions that still need to be performed and read back.

## Notes

- Linear remains the canonical issue/status system.
- The Markdown ledger is durable cross-session memory for agents.
- Checklist state must be honest: `[ ]` pending, `[x]` complete, `[~]` not applicable with a reason.
- No licence is included yet; add one before treating this as open-source software.
