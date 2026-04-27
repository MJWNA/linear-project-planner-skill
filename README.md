# Linear Project Planner Skill

Agent-ready Linear project planning, execution tracking, and cross-session handoff for Codex-style skill runtimes.

This skill helps an AI agent turn a Linear project into a real execution system. Instead of producing a flat backlog and hoping future agents remember what happened, it creates a structured operating model: milestones, parent workstreams, guide issues, labels, verification gates, issue-state hygiene, and a companion Markdown execution ledger that survives context resets.

The core idea is simple: Linear is the canonical project tracker, but agents also need a durable local memory file that explains the original prompt, the current state, which tasks are done, which issue is active, what was verified, and what the next safest action is.

## Why This Exists

AI agents are good at doing work, but long-running project execution has a few recurring failure modes:

- The agent creates a Linear project, then forgets the original intent after context compaction.
- Issues move through the board inconsistently, or not at all.
- A future session cannot tell whether a checkbox is unfinished or simply not applicable.
- Verification is mentioned in chat but not recorded anywhere durable.
- Handoffs depend on conversation history rather than a stable project artifact.
- Parallel agents can collide because ownership, worktrees, and dependency order are unclear.

This skill fixes those problems by making project execution explicit. It gives the agent a repeatable structure to create the Linear project, keep issue progress accurate, write completion comments, preserve verification evidence, and maintain a living Markdown ledger alongside Linear.

## What It Does

The skill has two halves:

1. `SKILL.md` teaches the agent how to design and execute an agent-ready Linear project.
2. `linear-agent` gives the agent a deterministic command-line wrapper for updating the companion ledger during execution.

Together they help an agent:

- Create Linear projects with useful milestones instead of one giant task list.
- Add parent workstreams that explain sequencing, parallel safety, non-goals, and verification expectations.
- Create required guide issues for agent operating instructions and verification matrices.
- Apply consistent labels such as `agent-ready`, `parallel-safe`, `serial-required`, `production-risk`, `touches-db`, and `verification-missing`.
- Add production-readiness and output-preservation gates when the work touches live systems.
- Maintain a Markdown execution ledger with source-of-truth links, active state, issue progress, decisions, blockers, risks, and handoff notes.
- Move issues through `In Progress` and `Done` only when the local ledger, Linear comment, and verification evidence agree.
- Produce readable handoffs for future agents.
- Finalize the ledger at project completion so stale checkboxes do not mislead the next session.

## The Living Ledger

The companion ledger is the main durable artifact created by this workflow. It is a Markdown file based on `templates/EXECUTION.md`.

It records:

- The original user prompt or project brief.
- The Linear project name or URL.
- The operating guide issue.
- The verification matrix issue.
- Repository, branch, workspace, and worktree paths.
- Current state, active issue, active agent, last verified time, and next safest action.
- Project creation checklist.
- Execution checklist.
- Per-issue progress table.
- Decisions, blockers, risks, handoff notes, and activity log.

The checklist supports three states:

- `[ ]` pending
- `[x]` complete
- `[~]` not applicable, with a reason

That third state matters. Without it, future agents cannot tell the difference between "not done yet" and "intentionally not needed for this project." For example, a production gate may be mandatory for a live application, but not applicable for a local skill packaging project.

## How The Workflow Works

### 1. Plan The Project

When asked to create or execute a Linear project, the agent reads this skill and builds a structured plan:

- Identify the repository and production surface.
- Read local project rules.
- Use current documentation when frameworks, SDKs, deployments, auth, ORM, or validation are involved.
- Decide which workstreams can run in parallel and which must be serial.
- Add verification gates before risky implementation work.
- Create or update the companion ledger.

### 2. Create Agent-Ready Linear Issues

The skill encourages a project structure like this:

- Guide: Agent Operating Guide
- Guide: Verification Matrix
- Workstream: Security/Auth
- Workstream: Data/Business Logic
- Workstream: Sync/Integrations
- Workstream: Database/Performance
- Workstream: Frontend/UX
- Workstream: Final Release/Monitoring

Each child issue should explain:

- The problem.
- Evidence.
- Acceptance criteria.
- Verification commands.
- Relevant docs and local rules.
- Parallel-safety notes.
- Known overlap files or modules.

The result is a backlog that an agent can actually execute without needing to rediscover the whole project.

### 3. Execute With `linear-agent`

The wrapper updates the local ledger first and prints the Linear MCP actions the agent still needs to perform. This keeps the local execution memory and Linear board from drifting apart.

Example:

```bash
linear-agent start MAS-123 \
  --ledger /path/to/EXECUTION.md \
  --agent Codex \
  --worktree /path/to/repo \
  --note "Claiming the issue for implementation"
```

The command updates the ledger, then prints the required Linear actions:

- Move the issue to `In Progress`.
- Add a progress comment.
- Read the issue back and confirm the state.
- Record any mismatch instead of pretending the transition succeeded.

### 4. Verify Before Done

Completion requires a verification string:

```bash
linear-agent complete MAS-123 \
  --ledger /path/to/EXECUTION.md \
  --verification "npm test: pass; npm run lint: pass"
```

If `--verification` is missing, the command fails. This is deliberate. It prevents agents from marking work complete without evidence.

### 5. Handoff Or Finalize

For unfinished work:

```bash
linear-agent handoff \
  --ledger /path/to/EXECUTION.md \
  --note "Blocked on deployment credentials" \
  --next "Reconcile Linear, then continue MAS-124"
```

For completed projects:

```bash
linear-agent finalize \
  --ledger /path/to/EXECUTION.md \
  --verification "Linear read-back complete; all checks pass"
```

`finalize` updates the ledger to a no-active-issue state, marks completed checklist items, marks conditional non-applicable items with `[~]`, removes placeholder progress rows, and prints the final Linear comment/read-back actions.

## Command Reference

### Initialise A Ledger

```bash
linear-agent init \
  --ledger /path/to/EXECUTION.md \
  --project "Project Name" \
  --prompt "Original user prompt" \
  --linear-project "Linear Project Name" \
  --repo /path/to/repo \
  --base-branch main
```

### Start Work

```bash
linear-agent start MAS-123 \
  --ledger /path/to/EXECUTION.md \
  --agent Codex \
  --worktree /path/to/worktree \
  --note "Claimed for implementation"
```

### Record A Blocker

```bash
linear-agent block MAS-123 \
  --ledger /path/to/EXECUTION.md \
  --note "Waiting on API credentials" \
  --next "Continue MAS-124 while blocked"
```

### Record Verification

```bash
linear-agent verify MAS-123 \
  --ledger /path/to/EXECUTION.md \
  --verification "tests/test-linear-agent.sh: pass"
```

### Complete An Issue

```bash
linear-agent complete MAS-123 \
  --ledger /path/to/EXECUTION.md \
  --verification "tests/test-linear-agent.sh: pass" \
  --note "Implementation and read-back complete"
```

### Handoff

```bash
linear-agent handoff \
  --ledger /path/to/EXECUTION.md \
  --note "Session ending with MAS-124 in progress" \
  --next "Read ledger, reconcile Linear, continue MAS-124"
```

### Finalize

```bash
linear-agent finalize \
  --ledger /path/to/EXECUTION.md \
  --verification "No Todo/In Progress issues remain; final checks pass"
```

## Why It Is Useful

This skill is useful because it treats project management as part of the execution system, not as a separate admin chore.

The benefits are practical:

- Better continuity after context compaction.
- Less chance of losing the original prompt.
- Clearer recovery when a session stops halfway through.
- Safer parallel work because ownership and worktrees are recorded.
- More reliable Linear boards because agents are told exactly when to move status.
- Stronger completion discipline because verification is required.
- Better auditability because comments, ledger rows, and activity logs line up.
- More useful future sessions because the next agent can start from the ledger instead of re-deriving context.

It is especially useful for:

- Codebase audits.
- Production hardening projects.
- Multi-agent remediation work.
- Long-running refactors.
- Linear projects that need repeatable verification.
- Work where business outputs must not change accidentally.
- Projects where Codex, Claude, or another agent may resume later.

## Repository Layout

```txt
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── install.sh
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

That copies the skill into:

```txt
~/.codex/skills/linear-project-planner
```

It also installs a launcher at:

```txt
~/.local/bin/linear-agent
```

Make sure `~/.local/bin` is on your `PATH` if you want to run `linear-agent` from anywhere.

## Test

Run the regression suite:

```bash
bash tests/test-linear-agent.sh
```

Run syntax checks:

```bash
bash -n install.sh
bash -n scripts/linear-agent
bash -n tests/test-linear-agent.sh
```

Optional, if installed locally:

```bash
shellcheck scripts/linear-agent tests/test-linear-agent.sh
```

## Design Principles

- Linear remains the canonical issue/status system.
- The Markdown ledger is durable execution memory, not a replacement for Linear.
- Every state transition should be recorded locally, reflected in Linear, and read back.
- `Done` should mean verified, not merely attempted.
- Conditional checklist items should be marked `[~]` with a reason, not left ambiguous.
- Handoffs should tell the next agent exactly where to restart.
- The wrapper should be deterministic, local-first, and easy to test.

## Current Limitations

- The wrapper does not call the Linear API directly. It updates the ledger and prints the required Linear MCP actions for the agent to perform and verify.
- Workspace-specific Linear state names may vary. The skill assumes simple state names such as `Todo`, `In Progress`, `Done`, and `Canceled`.
- The included install script targets Codex-style local skill paths.
- No licence is included yet. Add one before treating this as open-source software.

## Quick Start Prompt

Use a prompt like this with an agent that has access to the skill:

```txt
Use the linear-project-planner skill to create an agent-ready Linear remediation project for this repository. Create the companion execution ledger, add guide issues, structure the work into milestones and parent workstreams, and use linear-agent transitions while executing.
```
