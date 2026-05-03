# Linear Project Planner Skill

[![CI](https://github.com/MJWNA/linear-project-planner-skill/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/MJWNA/linear-project-planner-skill/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/MJWNA/linear-project-planner-skill?style=flat)](LICENSE)

Agent-ready Linear project planning, execution tracking, and cross-session handoff for Codex-first, Claude-compatible skill runtimes.

> **Live API mode:** Linear MCP is no longer required for graph creation. With
> `LINEAR_API_KEY` or `LINEAR_ACCESS_TOKEN`, `linear-agent graph-apply
> --apply-linear` creates and updates projects, labels, milestones, issues,
> relations, and attachments directly through `https://api.linear.app/graphql`.
> Version 4.0 adds schema-current teardown, batch issue creation, full
> project-scan pagination, richer attachment metadata, and rate-limit budget
> awareness.

For this skill's own workflow, direct GraphQL is the primary route whenever
`LINEAR_API_KEY` or `LINEAR_ACCESS_TOKEN` is available. Use the Codex Linear
app/MCP connector only as a fallback for credentials-free runtimes, explicit
connector requests, operations that have not yet been implemented in
`linear-agent`, direct API blocks/rejections, or failed read-back confirmation.
Record the API attempt, fallback path, and read-back evidence in the ledger or
relevant Linear comment.

This skill helps an AI agent turn a Linear project into a real execution system. Instead of producing a flat backlog and hoping future agents remember what happened, it creates a structured operating model: milestones, parent workstreams, guide issues, labels, verification gates, issue-state hygiene, and a companion Markdown execution ledger that survives context resets.

The core idea is simple: Linear is the canonical project tracker, but agents also need a durable local memory file that explains the original prompt, the current state, which tasks are done, which issue is active, what was verified, and what the next safest action is.

## What This Solves

AI agents are good at doing work, but long-running project execution has a few recurring failure modes:

- The agent creates a Linear project, then forgets the original intent after context compaction.
- Issues move through the board inconsistently, or not at all.
- A future session cannot tell whether a checkbox is unfinished or simply not applicable.
- Verification is mentioned in chat but not recorded anywhere durable.
- Handoffs depend on conversation history rather than a stable project artifact.
- Parallel agents can collide because ownership, worktrees, and dependency order are unclear.

This skill fixes those problems by making project execution explicit. It gives the agent a repeatable structure to create the Linear project, keep issue progress accurate, write completion comments, preserve verification evidence, and maintain a living Markdown ledger alongside Linear.

## How It Works

The skill has two halves:

1. `SKILL.md` teaches the agent how to design and execute an agent-ready Linear project.
2. `linear-agent` gives the agent a deterministic command-line wrapper for updating the companion ledger during execution.

Together they help an agent:

- Create Linear projects with useful milestones instead of one giant task list.
- Add parent workstreams that explain sequencing, parallel safety, non-goals, and verification expectations.
- Create required guide issues for agent operating instructions and verification matrices.
- Build a sparse link graph between issues, docs, source files, PRs, ledgers, and verification artifacts.
- Apply consistent labels such as `agent-ready`, `parallel-safe`, `serial-required`, `production-risk`, `touches-db`, and `verification-missing`.
- Add production-readiness and output-preservation gates when the work touches live systems.
- Maintain a Markdown execution ledger with source-of-truth links, active state, issue progress, decisions, blockers, risks, and handoff notes.
- Move issues through `In Progress` and `Done` only when the local ledger, Linear comment, and verification evidence agree.
- Require standard validation for every project, and add deeper auto-research validation only when it is explicitly requested, approved, or clearly triggered by the user's wording.
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
- Validation mode, including whether the optional deep auto-research loop was requested or skipped.
- Project creation checklist.
- Execution checklist.
- Per-issue progress table.
- Decisions, blockers, risks, handoff notes, and activity log.

The checklist supports three states:

- `[ ]` pending
- `[x]` complete
- `[~]` not applicable, with a reason

That third state matters. Without it, future agents cannot tell the difference between "not done yet" and "intentionally not needed for this project." For example, a production gate may be mandatory for a live application, but not applicable for a local skill packaging project.

## Technical Workflow

### Quick Path

The shortest safe operating flow is:

1. Read local project rules and create or open the companion ledger.
2. Create the Linear project with guide issues, parent workstreams, child issues, labels, dependencies, and sparse links.
3. Put user-requested research, source review, audits, and exploratory discovery inside the Linear plan when the user is asking for a Linear project.
4. Claim one issue at a time with `linear-agent start`; use separate worktrees for independent write-capable agents.
5. Verify each issue before `linear-agent complete`, then mirror the Linear status/comment and read it back.
6. Run standard final verification, reconcile Linear, and finalize only with explicit evidence. Use the deeper auto-research loop only when it was explicitly requested, approved during planning, or clearly triggered by the user's wording.

### Trigger-Safe Progressive Disclosure

The skill uses trigger-safe progressive disclosure: `SKILL.md` stays as a compact routing and operating front door, while longer contracts live in referenced files that agents load only when needed.

The front door intentionally keeps trigger language visible for prompts such as "create a Linear project", "run the Linear skill", "execute a Linear plan", "audit remediation", "companion ledger", "verification gates", and Codex or Claude agent coordination. It also keeps a negative boundary for simple one-off Linear issue lookups so the planner does not compete with ordinary Linear search or update workflows.

The research basis for this approach is recorded in [docs/research/skill-front-door-context-loading.md](docs/research/skill-front-door-context-loading.md), and the maintenance contract is in [references/trigger-preservation.md](references/trigger-preservation.md).

### Reference Map

The skill keeps the front-door instructions compact and moves deeper contracts into focused references:

- `SKILL.md`: project design and execution contract.
- `references/trigger-preservation.md`: trigger-safe front-door contract.
- `references/project-structure.md`: milestones, labels, parent issues, child issue template, sparse link graph, and research-as-planned-work template.
- `references/project-principles.md`: scaled Project Principles / Fundamentals surfaces for baseline and expanded projects.
- `references/execution-hygiene.md`: companion ledger, `linear-agent`, issue-state hygiene, worktrees, completion comments, and finalization.
- `references/source-checkpoints.md`: phase-based source rereading checkpoints for kickoff, planning, issue creation, implementation, delegation, scope changes, verification, handoff, and closeout.
- `references/validation-modes.md`: standard validation, optional deep auto-research validation, production gates, and sink/output preservation.
- `templates/EXECUTION.md`: living ledger template.
- `templates/project-principles.md`: full companion principles document for larger, ambiguous, or expanded-mode projects.
- `scripts/linear-agent`: shell CLI for ledger transitions, direct Linear mode, reconciliation, and finalization.
- `references/command-schemas.md`: implemented `linear_project.*` CLI contract and future structured tool contract.
- `references/runtime-state.md`: model/runtime and Responses API state guidance.
- `references/expanded-mode.md`: opt-in long-horizon workflow for deep research, local docs, dependency maps, provenance, safe multi-agent allocation, dogfood, and baseline contamination safeguards.
- `references/operator-cheatsheet.md`: one-page operator path and minimal safe issue set.
- `references/repository-hardening.md`: CI, release, CodeQL, branch/ruleset, and solo-maintainer hardening policy.
- `templates/production-gates.md`: reusable production and sink inventory gates for common project types.
- `templates/expanded-mode/`: reusable research dossier, decision, dependency map, QA plan, agent brief, and handoff templates for expanded-mode projects.
- `docs/claude-portability.md`: Codex-first and Claude-compatible runtime positioning.
- `docs/manual-linear-smoke.md`: manual live Linear smoke-test release gate pattern.
- `docs/examples/`: worked examples for local audits, production hardening, and parallel remediation.
- `tests/fixtures/linear_issue_templates.md`: expected issue and final comment shapes for agent-output evaluation.

### 1. Plan The Project

When asked to create or execute a Linear project, the agent reads this skill and builds a structured plan:

- Identify the repository and production surface.
- Read local project rules.
- Use current documentation when frameworks, SDKs, deployments, auth, ORM, or validation are involved.
- Decide which workstreams can run in parallel and which must be serial.
- Add verification gates before risky implementation work.
- Create or update the companion ledger.
- Add a compact project description with goal, source of truth, scope, non-scope, workstreams, dependency policy, discovery rule, verification, and handoff notes when relevant.

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
- High-signal reference links.
- Parallel-safety notes.
- Known overlap files or modules.
- Notes for future agents after context clears.

The result is a backlog that an agent can actually execute without needing to rediscover the whole project.

Normal mode keeps issue bodies compact: Objective, Context, Scope, Dependencies / blockers, Acceptance criteria, Verification, and Notes for future agents. The goal is enough structure for handoff and context recovery, not expanded-mode ceremony.

### Continuous Issue Discovery

The initial Linear plan is a working model, not a sacred list. During research, implementation, testing, review, documentation, release, and handoff, agents classify discovered work as Blocker, Dependency, Defect, Research follow-up, Implementation follow-up, Decision required, QA / verification gap, Documentation gap, Scope expansion, or Risk / mitigation.

Create a new issue immediately when the discovery blocks current work, affects correctness, is required for acceptance, or creates a real dependency. Propose an issue candidate when the work may be useful but needs coordinator review. Log context-only observations when they are not actionable yet.

Created or proposed issues should explain why they were discovered, which issue or workstream surfaced them, whether they block or depend on anything, which phase/workstream owns them, what acceptance criteria prove completion, and what a future agent needs to know after context compaction.

### Sparse Link Graph

The skill now treats links as context compression. A good Linear project should behave like a small, useful web:

- parent and child workstreams show execution shape
- `blocks`, `blockedBy`, and `relatedTo` show sequencing and related risk
- docs links show why a technical choice was made
- source file, PR, commit, and branch links show where the work happened
- ledger links show where durable execution memory lives
- verification links show what proved the work was done

The point is not to link everything. Normal child issues should stay sparse, usually 3-7 high-signal links. Guide issues, verification matrices, and final release gates can carry more. Links should compress context, not clutter tasks.

If Linear rejects issue creation or relationships, do not silently downgrade the graph to memory. Freeze the intended graph in the companion ledger and, where possible, the Linear project description:

- list the guide, parent, and child issues that still need to be created
- record intended `blocks`, `blockedBy`, and `relatedTo` edges
- store high-signal URLs for docs, source files, commits, PRs, evaluator commands, and ledger anchors
- mark relationship creation as blocked or not applicable with a reason
- retry the Linear graph once the workspace/tooling blocker is resolved

This keeps the project recoverable without pretending the board is more complete than it is.

### Reactive Issue Spillover

Linear remains the first place the issue body is written. The direct GraphQL path only creates local per-issue spillover docs after Linear rejects the actual issue create or update with a size, length, or character-limit error.

When that happens, `linear-agent graph-apply --apply-linear` writes the full issue description to a local Markdown file, retries Linear with a compact pointer body, and includes spillover records in the apply result. By default, spillover files live under:

```txt
../.codex-linear-ledgers/<project-slug>/spillover/
```

Use `--spillover-dir <path>` or `project.spilloverDir` in a graph plan when a project needs a different local docs root. Small and normal-sized issues do not get extra local files.

### Parallel-Agent Operating Model

For agent-heavy projects, the coordinator should not treat "parallel-safe" as a nice-to-have label. If there are two or more independent, unblocked child issues with separate write scopes, the coordinator should dispatch parallel sub-agents and give each one a clear lane.

In plain English:

- The coordinator breaks the project into child issues that can be owned independently.
- Each write-capable agent gets one Linear issue, one branch, one git worktree, and one explicit write set.
- The write set names the files, folders, modules, migrations, scripts, or docs the agent may change.
- Agents must not edit outside their owned scope, revert other agents' work, or "clean up" shared files unless the coordinator gives that ownership explicitly.
- If two issues need the same file or helper, they are no longer parallel-safe. Mark them `serial-required` or `overlap-zone` and reconcile the order first.
- Read-only research agents can share a worktree, but implementation agents should use separate worktrees.
- The coordinator merges branches deliberately after each issue is verified and after any shared contracts are reconciled.

Worktrees matter because git branches alone do not protect the working directory. Two agents editing the same checkout can overwrite each other's files, run formatters across unrelated changes, or accidentally revert work they did not create. Separate worktrees give each agent its own filesystem checkout, while still keeping the branches connected to the same repository for review and merge.

Example split across child issues:

```txt
Parent: Workstream: Linear Planner Policy Docs

MAS-224: Make parallel dispatch mandatory in SKILL.md
- Agent: Codex A
- Branch: codex/mas-224-parallel-dispatch
- Worktree: ../linear-planner-mas-224
- Owned write set: SKILL.md
- Do not edit: README.md, scripts/**, templates/**, tests/**, CI files
- Verification: markdown review plus targeted diff check

MAS-228: Document the parallel-agent operating model in README.md
- Agent: Codex B
- Branch: codex/mas-228-readme-operating-model
- Worktree: ../linear-planner-mas-228
- Owned write set: README.md
- Do not edit: SKILL.md, scripts/**, templates/**, tests/**, CI files
- Verification: markdown review plus targeted diff check
```

Those two issues can run in parallel because each agent writes a different file and neither issue depends on the other's implementation. If both issues needed to edit `SKILL.md`, the coordinator would either split the ownership by section with extra care or make the work serial.

### Expanded Mode

Expanded mode is an opt-in path for long-horizon projects that need more than the baseline Linear planning contract. Use it when the user explicitly asks for expanded mode, detailed multi-phase planning, deep research first, dependency mapping, local project docs, software-firm-grade planning, multi-team delivery, or heavy safe parallel-agent coordination.

Baseline mode remains the default for ordinary Linear planning, execution, audits, remediation, companion ledgers, dependencies, safe-parallelism checkpoints, and verification gates. Expanded mode adds a stricter mode gate, baseline/no-contamination snapshot, local docs workspace, source provenance rules, dependency map, agent allocation table, planned QA passes, dogfood, and release or handoff gate.

Expanded-mode project descriptions behave like charters: project purpose, operating mode, source of truth, companion ledger path, local docs root, current phase, workstream map, dependency policy, research-to-issue policy, Continuous Issue Discovery policy, verification policy, agent handoff policy, and coordinator responsibilities.

Expanded-mode issues are richer than normal-mode issues. They should include objective, background context, why the work matters, inputs, owned and non-owned scope, dependencies, blockers, step-by-step working instructions, expected outputs, acceptance criteria, verification requirements, handoff/context recovery notes, follow-up issue candidates, and required updates to local docs, the ledger, or dependency map when relevant.

The detailed workflow lives in [references/expanded-mode.md](references/expanded-mode.md). Reusable artifacts live under [templates/expanded-mode/](templates/expanded-mode/).

### 3. Execute With `linear-agent`

The wrapper updates the local ledger and, when `--apply-linear` or
`LINEAR_AGENT_APPLY=1` is set, writes the matching Linear state/comment through
the GraphQL API before read-back verification. With credentials loaded, this
direct API path is preferred. Dry-run mode remains available for
credentials-free runtimes and prints the Linear app/MCP/manual fallback actions.

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

The CLI also exposes the 10/10 project automation surface:

```bash
linear-agent graph-plan --from tests/fixtures/linear_graph_plan.json
linear-agent graph-apply --from tests/fixtures/linear_graph_plan.json
linear-agent graph-readback --from tests/fixtures/linear_graph_plan.json
linear-agent allocate --from tests/fixtures/linear_graph_plan.json --ledger EXECUTION.md
linear-agent inventory --repo /path/to/repo
linear-agent smoke --project disposable-linear-project
linear-agent validate-ledger --ledger EXECUTION.md
```

Every command supports `--json` where structured output is useful. Exit code `0` means success, `1` means recoverable drift or failed validation, and `2` means usage/input error.

### 4. Verify Before Done

Completion requires a verification string:

```bash
linear-agent complete MAS-123 \
  --ledger /path/to/EXECUTION.md \
  --verification "npm test: pass; npm run lint: pass"
```

If `--verification` is missing, the command fails. This is deliberate. It prevents agents from marking work complete without evidence.

### 5. Optional Deep Auto-Research Validation

Standard validation is always required. Every project still needs concrete acceptance criteria, issue-level verification before `Done`, Linear read-back, final reconciliation, and evidence in completion/finalization comments.

The deeper Andrej Karpathy-style auto-research loop is optional. The skill should add it only when the user explicitly asks, agrees during planning, or has already used trigger language such as `dogfood`, `recursive`, `auto-research`, `keep iterating`, `long horizon`, or `publish after stable`.

Ask after the agent understands the project type and risk, but before it creates final validation tasks:

```txt
Do you want standard validation only, or the deeper auto-research loop with repeated evaluator passes and follow-up task creation?
```

Record the decision in the ledger:

```md
- Validation mode: standard
- Deep auto-research loop: not requested
```

or:

```md
- Validation mode: deep-autoresearch
- Deep auto-research loop: approved by user
- Frozen evaluator: <command>
- Stability threshold: <passes / score>
```

When opted in, the deep loop uses this pattern:

1. define a fixed evaluator
2. freeze the evaluator
3. make one focused change or hypothesis
4. run the benchmark/check
5. keep the change if correctness remains green
6. revert or create a follow-up task if it fails
7. record learnings in the ledger
8. repeat until the score is stable

For this skill's own release work, the evaluator is:

```bash
python3 tools/linear-agent-evaluator.py
```

For other opted-in projects, the evaluator might be tests, lint/typecheck counts, build success, API contract checks, output snapshots, accessibility scores, repo readiness, or `linear-agent reconcile` drift results. The important part is that the evaluator is binary or numeric and does not move during the final loop.

When deep auto-research is enabled, the final Linear tasks should be explicit enough that a future agent can execute them without inventing the loop:

- `Freeze evaluator command and success threshold`
- `Run baseline evaluator and record score`
- `Probe failure modes with focused experiments`
- `Keep only changes that preserve correctness`
- `Create follow-up tasks for non-green or inconclusive checks`
- `Re-run evaluator until stable across repeated passes`

For this skill, a valid final loop means the frozen evaluator prints `SCORE 200/200`, shell and Python regression tests pass, `linear-agent reconcile` has no drift for real issue rows, and any blocked Linear behavior is recorded as blocked rather than completed.

### 6. Handoff Or Finalize

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
  --verification "Linear read-back complete; all checks pass" \
  --evidence "Linear read-back: all rows Done; CI passed" \
  --linear-reconciled \
  --dependencies "not-applicable:no blocking dependencies were required" \
  --production-gates "not-applicable:not a production application" \
  --sink-gates "not-applicable:no sync or output sink in scope"
```

`finalize` updates the ledger to a no-active-issue state, marks completed checklist items, removes placeholder progress rows, and prints the final Linear comment/read-back actions. It requires explicit dependency, production, sink/output gate outcomes, and evidence so an agent cannot silently mark risky project gates as not applicable or completed without an inspectable read-back.

`finalize` also refuses to run when the Issue Progress table is empty or any issue row is still not `Done` or `Completed`. A canceled, missing, blocked, unstarted, or In Progress issue is not project completion; it needs a blocker note, a follow-up issue, or a human decision before the project can be finalized.

## Commands

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

`init` refuses to overwrite an existing ledger. Add `--force` only when you deliberately want to replace the file:

```bash
linear-agent init \
  --ledger /path/to/EXECUTION.md \
  --project "Project Name" \
  --prompt "Original user prompt" \
  --force
```

The `--prompt` value is required. Use the user's original request or the shortest faithful project brief so resumed agents can recover the intent after context compaction.

### Start Work

```bash
linear-agent start MAS-123 \
  --ledger /path/to/EXECUTION.md \
  --agent Codex \
  --worktree /path/to/worktree \
  --note "Claimed for implementation"
```

By default, `linear-agent` updates the ledger and prints the safest next action.
To apply the transition through the primary direct Linear GraphQL API path, set
credentials and add `--apply-linear`:

```bash
LINEAR_API_KEY=lin_api_... linear-agent start MAS-123 \
  --ledger /path/to/EXECUTION.md \
  --agent Codex \
  --worktree /path/to/worktree \
  --apply-linear \
  --note "Claimed for implementation"
```

Direct mode updates the Linear issue state, creates the progress comment, reads the issue back, and then confirms the ledger row. It also supports `LINEAR_ACCESS_TOKEN` for OAuth tokens and `LINEAR_API_URL` for non-default endpoints. The default endpoint is `https://api.linear.app/graphql`; endpoint overrides must use `https://api.linear.app` unless you intentionally set `LINEAR_AGENT_ALLOW_NON_LINEAR_API_URL=1` for a trusted proxy or `LINEAR_AGENT_ALLOW_UNSAFE_API_URL=1` for local testing.

Use reconciliation to compare ledger rows with Linear:

```bash
linear-agent reconcile --ledger /path/to/EXECUTION.md
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
  --verification "No To Do/In Progress issues remain; final checks pass" \
  --evidence "Linear read-back: no To Do/In Progress issues; evaluator passed" \
  --linear-reconciled \
  --dependencies "satisfied" \
  --production-gates "satisfied" \
  --sink-gates "not-applicable:no sync or output sink in scope"
```

Gate values must be either `satisfied` or `not-applicable:<reason>`.

### Responses API State

When this skill is used from a custom OpenAI API client, keep the agent state chain explicit rather than relying only on chat history:

- Preserve `previous_response_id` between turns so the model can continue the same reasoning/tool-use chain.
- Replay required output items when a tool result needs to be resumed after compaction or an external workflow pause.
- Store the current `phase`, active issue, active worktree, ledger path, and last verification result outside the prompt so an API restart can recover cleanly.
- Treat the companion ledger as the durable compaction summary: if API state and the ledger disagree, reconcile against Linear and record the outcome before continuing.

## Why It Matters

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

## Who It Is For

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
├── lib/
│   └── linear_agent/
│       ├── cli.py
│       ├── graph.py
│       ├── graphql.py
│       └── ledger.py
├── docs/
│   ├── claude-portability.md
│   ├── examples/
│   ├── research/
│   ├── linear-token-scope.md
│   ├── manual-linear-smoke.md
│   └── migration-guide.md
├── references/
│   ├── command-schemas.md
│   ├── execution-hygiene.md
│   ├── operator-cheatsheet.md
│   ├── project-structure.md
│   ├── repository-hardening.md
│   ├── runtime-state.md
│   ├── trigger-preservation.md
│   └── validation-modes.md
├── scripts/
│   └── linear-agent
├── templates/
│   ├── EXECUTION.md
│   └── production-gates.md
├── tests/
│   ├── fixtures/
│   ├── test-linear-agent.sh
│   ├── test_linear_agent_graph_features.py
│   └── test_linear_agent_graphql.py
└── tools/
    ├── linear-agent-evaluator.py
    ├── linear-front-door-evaluator.py
    └── linear-skill-audit-evaluator.py
```

## Quick Start

Install from this repository root:

```bash
./install.sh
```

Install with local docs and license visibility:

```bash
./install.sh --with-docs
```

Validate or remove an install:

```bash
./install.sh --check
./install.sh --uninstall
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

Create a project graph plan, preview it, then apply it live:

```bash
linear-agent graph-plan --from tests/fixtures/linear_graph_plan.json
LINEAR_API_KEY=lin_api_... linear-agent graph-apply \
  --from tests/fixtures/linear_graph_plan.json \
  --apply-linear
linear-agent graph-readback --from tests/fixtures/linear_graph_plan.json
```

Default mode is still dry-run. Linear mutations require `--apply-linear` or
`LINEAR_AGENT_APPLY=1`.

### Finding Your Linear API Key

For local development, a personal Linear API key is enough:

1. Open Linear in the browser.
2. Go to Settings -> Workspace settings -> API -> Personal API keys.
3. Create a key with access to the workspace/team you want this skill to manage.
4. Store it outside this public repo, for example:

```bash
mkdir -p ../.codex-linear-secrets
printf 'LINEAR_API_KEY=lin_api_...\\n' > ../.codex-linear-secrets/linear.env
chmod 600 ../.codex-linear-secrets/linear.env
source ../.codex-linear-secrets/linear.env
```

Never commit the key, `.env` files, local ledgers, or Linear workspace exports.

## Configuration

The skill is configured through committed files:

- `SKILL.md` defines the agent workflow and mandatory Linear execution rules.
- `agents/openai.yaml` declares Codex-facing metadata, interfaces, policies, and dependencies.
- `templates/EXECUTION.md` defines the live Markdown ledger created for each project.
- `.repo-publisher.yml` records the GitHub publishing profile and repo settings contract.

Runtime state should stay outside the repo. Local execution ledgers belong under ignored workspace paths such as `.codex-linear-ledgers/`.

Direct Linear automation is configured with environment variables:

- `LINEAR_API_KEY`: personal API key for direct GraphQL writes
- `LINEAR_ACCESS_TOKEN`: OAuth token alternative
- `LINEAR_API_URL`: optional GraphQL endpoint override, validated to `https://api.linear.app` by default
- `LINEAR_AGENT_APPLY=1`: deliberate session-level write mode that opts every transition command into direct mode; prefer visible `--apply-linear` for one-off writes
- `LINEAR_STATE_IN_PROGRESS`: optional state ID override for `In Progress`
- `LINEAR_STATE_DONE`: optional state ID override for `Done`
- `LINEAR_AGENT_ALLOW_NON_LINEAR_API_URL=1`: allow a trusted non-Linear HTTPS API URL
- `LINEAR_AGENT_ALLOW_UNSAFE_API_URL=1`: allow a non-HTTPS API URL for intentional local testing only
- `LINEAR_AGENT_TEST_MODE=1`: required before fake transport variables are honored
- `LINEAR_AGENT_FAKE_STATE`: test-only fake Linear state file
- `LINEAR_AGENT_FAKE_REQUESTS`: test-only JSONL request log path
- `LINEAR_AGENT_TIMEZONE`: timestamp timezone, defaulting to `Australia/Brisbane`

### Portability

This repo is Codex-first and Claude-compatible.

Codex-first means the installer targets `~/.codex/skills/linear-project-planner`, installs `linear-agent` into `~/.local/bin`, and includes `agents/openai.yaml` metadata for Codex runtimes.

Claude-compatible means the skill follows the shared `SKILL.md` plus references/scripts shape and can be installed manually under `~/.claude/skills/linear-project-planner`. The Python CLI and ledger format are runtime-neutral. Full Claude parity would need a first-class Claude install target and runtime-specific MCP/tooling notes.

See [docs/claude-portability.md](docs/claude-portability.md) for the exact support matrix.

The skill is tested on macOS/Linux style shells. On Windows, use WSL with Bash and Python 3, then run the repo checkout directly or install into the WSL home directory. For no-install mode, run `scripts/linear-agent` from the repo checkout.

### Live Linear Smoke Tests

Normal CI uses hermetic fake Linear transport so pull requests do not mutate a real Linear workspace or require secrets. Live Linear smoke testing is secret-gated because it creates or updates real workspace objects, consumes API quota, and needs a disposable target project.

Run the smoke workflow for release candidates, GraphQL transport changes, state transition changes, install/runtime changes, or before major version releases. The scheduled workflow is skipped unless `LINEAR_API_KEY` is configured, and the dispatch path still requires an explicit `apply-linear` input. Record the disposable target, commands, cleanup, and result in the release notes or Linear verification issue.

See [docs/manual-linear-smoke.md](docs/manual-linear-smoke.md) for the checklist and evidence pattern.

## Testing

Run the regression suite:

```bash
bash tests/test-linear-agent.sh
python3 -m unittest tests/test_linear_agent_graphql.py
python3 -m unittest tests/test_linear_agent_graph_features.py
python3 tools/linear-front-door-evaluator.py
python3 tools/linear-agent-evaluator.py
python3 tools/linear-skill-audit-evaluator.py
```

The front-door evaluator protects trigger reliability after `SKILL.md` changes. The main evaluator is the frozen Karpathy-style release score for this skill. A release candidate should print `SCORE 200/200`; if the score drops, treat the change as a failed experiment and fix or revert before publishing.

Run syntax checks:

```bash
bash -n install.sh
bash -n scripts/linear-agent
bash -n tests/test-linear-agent.sh
python3 -m py_compile lib/linear_agent/__init__.py lib/linear_agent/ledger.py lib/linear_agent/graphql.py lib/linear_agent/graph.py lib/linear_agent/cli.py tools/linear-front-door-evaluator.py tools/linear-agent-evaluator.py tools/linear-skill-audit-evaluator.py
```

Optional, if installed locally:

```bash
shellcheck install.sh scripts/linear-agent tests/test-linear-agent.sh
```

## Deployment / Release

Current production release: `v4.0.1`.

The repository is published as a public GitHub repo and installed locally with `./install.sh`. Releases use the manual release workflow after a known-good commit is tagged, [CHANGELOG.md](CHANGELOG.md) is updated, and CI passes.

The repository includes GitHub Actions workflows for CI, CodeQL, a manual release gate, and a scheduled/manual live Linear smoke check. CI runs shell syntax, shellcheck, Python syntax, YAML parsing, secret scanning, regression tests, fake Linear GraphQL tests, graph feature tests, evaluators, and trailing-whitespace checks on every push and pull request.

The live Linear smoke workflow is not expected to run on normal pull requests. Treat it as a scheduled and manual release/readiness gate when the change could affect real Linear API behavior.

## Troubleshooting

- If `linear-agent` is not found after install, ensure `~/.local/bin` is on your `PATH`.
- If `init` refuses to write the ledger, the file already exists. Use `--force` only when replacing it is intentional.
- If `complete` fails, add a concrete `--verification` string.
- If `start --parallel-write` fails, provide a `--worktree` path so write-capable agents do not share one checkout.
- If `--apply-linear` fails with missing credentials, set `LINEAR_API_KEY`, set `LINEAR_ACCESS_TOKEN`, or use default dry-run mode and perform the printed Linear app/MCP/manual fallback actions.
- If `--apply-linear` reports a post-update confirmation failure, run `linear-agent reconcile --ledger <path>`, use the Linear MCP fallback when the API path cannot prove the state, and record both the failure and fallback evidence before manually confirming the ledger.
- If direct mode reports a read-back mismatch, run `linear-agent reconcile --ledger /path/to/EXECUTION.md` before continuing.
- If Linear state names differ in your workspace, set the `LINEAR_STATE_*` override variables or record the mismatch in the ledger before continuing.
- If Linear rejects optional project metadata such as `icon`, retry without that cosmetic field and record the workspace validation note in the operating guide or ledger.

## Support

Open a GitHub issue for bugs, feature requests, or usage questions. Include the command you ran, the relevant ledger snippet, and verification output where possible.

## Security

Do not commit secrets, credentials, private Linear workspace exports, customer data, production dumps, or local runtime ledgers. Report vulnerabilities privately through the repository security policy.

## Status

This repo is maintained as a public Codex skill utility. The current implementation is shell, Python, and Markdown based, with CI covering syntax, YAML metadata, regression tests, fake Linear GraphQL tests, evaluator checks, and whitespace checks.

## License

This project is released under the MIT License. See [LICENSE](LICENSE).

## Design Principles

- Linear remains the canonical issue/status system.
- The Markdown ledger is durable execution memory, not a replacement for Linear.
- Every state transition should be recorded locally, reflected in Linear, and read back.
- `Done` should mean verified, not merely attempted.
- Conditional checklist items should be marked `[~]` with a reason, not left ambiguous.
- Handoffs should tell the next agent exactly where to restart.
- The wrapper should be deterministic, local-first, and easy to test.

## Current Limitations

- Linear attachments require allowed HTTP(S) URLs. Local `file://` ledger paths should stay in issue bodies or ledger text, not attachment URLs.
- Project read-back starts at 250 issues per page and follows Linear cursor pagination so large projects can be reconciled without hiding issues after the first page. If Linear reports query complexity pressure, the page size is reduced automatically and the scan continues.
- Large graph bootstraps use `issueBatchCreate` where parent or child issue groups can be created safely in one API mutation; existing or drifted issues are still handled idempotently one issue at a time.
- Attachments created by this skill include source metadata so links can be audited as `linear-project-planner` references in Linear.
- The transport retries `RATELIMITED` and HTTP 429 responses and records Linear rate-limit or complexity headers to slow down before exhausting the budget.
- Default dry-run mode still avoids Linear API calls unless `--apply-linear` or `LINEAR_AGENT_APPLY=1` is set.
- Workspace-specific Linear state names may vary. The skill assumes simple state names such as `To Do`, `In Progress`, `Done`, and `Canceled`.
- The included install script targets Codex-style local skill paths; Claude use is currently manual and documented in `docs/claude-portability.md`.

## Quick Start Prompt

Use a prompt like this with an agent that has access to the skill:

```txt
Use the linear-project-planner skill to create an agent-ready Linear remediation project for this repository. Create the companion execution ledger, add guide issues, structure the work into milestones and parent workstreams, and use linear-agent transitions while executing.
```
