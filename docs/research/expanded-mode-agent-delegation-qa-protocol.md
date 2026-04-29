# Expanded Mode Agent Delegation And QA Protocol

Project: Linear Project Planner Expanded Mode
Linear issue: MAS-702
Status: protocol specification for future implementation

## Purpose

Expanded mode should support multi-agent work without turning coordination into
an unbounded swarm. This protocol defines how a coordinator assigns work, how
workers operate, how reviewers verify outputs, and where humans remain the
approval authority.

The protocol builds on the expanded-mode operating model, frontier AI delivery
patterns, Google-style review principles, and the OpenAI Codex capability map.
It is intentionally heavier than baseline mode and should only apply after an
expanded-mode gate confirms that the project needs explicit decomposition,
parallel-agent allocation, context isolation, and planned QA.

## Roles

### Coordinator

The coordinator is the single owner of the delivery system. The coordinator:

- Confirms expanded mode is appropriate and records the baseline behavior that
  must not be contaminated.
- Reads the authoritative project instructions, Linear issue state, companion
  ledger, dependency map, and local docs before allocating work.
- Defines milestones, workstreams, dependencies, ownership, non-owned scope,
  verification gates, and human review gates.
- Decides which tasks are parallel-safe, which are serial, and which require a
  synthesis checkpoint before implementation begins.
- Assigns one active owner for every writable artifact and prevents multiple
  agents from writing the same file, release metadata, ledger section, or
  Linear state unless a later integration step is explicitly serialized.
- Keeps Linear state, companion ledger state, PR descriptions, and local docs
  coherent when those surfaces are inside the coordinator's owned scope.
- Reconciles isolated worker outputs, resolves conflicts, and records residual
  risk or follow-up work.
- Runs or delegates final verification, then accepts or rejects the work based
  on evidence rather than activity volume.

The coordinator must not abdicate integration to worker agents. Worker outputs
are evidence, drafts, or bounded implementation artifacts until the coordinator
accepts them.

### Worker

Workers own narrow, explicitly assigned tasks. A worker:

- Receives a role, issue, owned write scope, non-owned scope, inputs,
  dependencies, expected output, and verification gate.
- Uses only the files, tools, source links, and project context needed for the
  task.
- Keeps edits inside the owned write scope and treats all other files, Linear
  state, release state, and companion ledgers as read-only unless explicitly
  assigned.
- Reports changed files, evidence gathered, commands run, results, blockers,
  deviations from scope, and residual risks.
- Stops and asks the coordinator when the task requires editing a non-owned
  file, crossing a dependency boundary, using secrets, changing production
  behavior, or resolving a product/business decision.

Workers may be research-only, implementation-capable, review-only, or
specialist verification agents. Their permissions and done conditions must
match the assignment.

### Reviewer

Reviewers provide independent assessment after research, implementation, or
integration. A reviewer:

- Checks the diff or artifact against acceptance criteria, non-owned scope,
  dependency constraints, and the relevant review pass.
- Separates blocking findings from optional suggestions, nits, and follow-up
  ideas.
- Grounds findings in source links, local code evidence, command output,
  screenshots, test logs, or explicit reviewer judgment.
- States the reviewed scope and the areas not reviewed.
- Avoids rewriting implementation unless explicitly given a write-capable
  remediation scope.

Reviewers are not rubber stamps. A reviewer without independent criteria,
fresh context, or a clear pass definition should not be counted as a QA gate.

### Human

Humans remain the approval authority for product scope, release readiness, and
high-risk decisions. Human review is required before:

- Merging or releasing public/runtime behavior changes.
- Changing baseline behavior, trigger behavior, permissions, credentials,
  production data semantics, billing, authentication, RBAC, deployment,
  migrations, or external integrations.
- Accepting unresolved security, privacy, data integrity, legal/licensing, or
  customer-impact risk.
- Broad refactors, destructive operations, or changes whose rollback path is
  unclear.

The coordinator should present humans with a compact decision packet: what
changed, why, evidence, risks, alternatives considered, and the exact approval
needed.

## Safe Parallelism

Parallelism is safe only when the coordinator can prove that work boundaries
are independent enough to reduce risk rather than increase synthesis cost.
Agent count is never a success metric.

### Prerequisites

Before assigning parallel work, the coordinator must record:

- Expanded-mode gate outcome and reason.
- Current baseline or no-contamination snapshot.
- Dependency map with blocked, serial, and parallel-safe work.
- One active coordinator and one authoritative state surface.
- A concurrency budget, including any `agents.max_threads` cap and practical
  review capacity.
- Each worker's owned write scope, non-owned scope, inputs, outputs,
  dependencies, and verification gate.
- A collision check showing no two write-capable workers share writable files,
  release artifacts, ledger sections, Linear state, migration files, or
  deployment/config surfaces.
- A tool and permission check covering network access, MCP availability,
  sandbox boundaries, secrets, production access, and fallback paths.
- A handoff and synthesis checkpoint for each batch.

If any prerequisite is unclear, the coordinator should downshift to read-only
research, serial execution, or a human decision point.

### Allocation Table Fields

Every parallel batch should use an allocation table with these fields:

| Field | Purpose |
|---|---|
| `agent_id` | Stable worker or reviewer identifier. |
| `role` | Coordinator-delegated role: research, implementation, reviewer, QA, docs, release, or specialist. |
| `linear_issue` | Issue key or local task identifier. |
| `mode` | `read-only`, `write-capable`, or `review-only`. |
| `owned_scope` | Exact files, folders, modules, docs, or surfaces the agent may modify. |
| `non_owned_scope` | Files, systems, state, or actions explicitly forbidden. |
| `inputs` | Allowed files, docs, source links, prior artifacts, or command outputs. |
| `dependencies` | Issues, artifacts, decisions, or verification gates that must be complete first. |
| `expected_output` | Artifact, diff, report, test result, PR note, or decision packet. |
| `tools_allowed` | Shell, MCP, web, browser, file editing, test runner, or other permitted tools. |
| `network_policy` | Offline, allowlisted research, official-docs-only, or unrestricted with guardrails. |
| `data_sensitivity` | Public, repo-local, internal, customer data, secret-adjacent, or production data. |
| `verification_gate` | Commands, review checklist, evaluator, screenshot, or human review required. |
| `handoff_target` | Coordinator, reviewer, issue comment, ledger section, PR, or local doc. |
| `stop_conditions` | Events requiring pause, escalation, or coordinator approval. |

## Delegation Rules

### Read-Only Research Delegation

Read-only research agents are appropriate when the project needs source
discovery, broad codebase exploration, log inspection, competitive research,
policy lookup, docs synthesis, or risk analysis before implementation.

Rules:

- Research agents may read assigned files, approved source links, and allowed
  tool outputs.
- Research agents must not edit code, docs, Linear state, ledgers, release
  metadata, configs, tests, or generated artifacts unless the allocation gives
  them one owned output file.
- Research agents must distinguish confirmed facts, source claims, local
  evidence, inferences, and recommendations.
- Research agents must include source links or file paths for decision-grade
  claims.
- Research agents should return compact synthesis, not raw transcripts, unless
  the coordinator requests full evidence capture.
- Research findings do not automatically authorize implementation. The
  coordinator must synthesize and approve the next step.

Good research delegations include one source family, one subsystem, one risk
category, one product question, or one artifact review.

### Write-Capable Implementation Delegation

Write-capable agents are appropriate only after the coordinator has narrowed
scope, confirmed dependencies, and assigned an exclusive writable surface.

Rules:

- One write-capable agent owns a file or module at a time unless the
  coordinator explicitly serializes pairwise integration.
- Implementation agents must read relevant local conventions and surrounding
  tests before editing.
- Implementation agents must keep changes small, reviewable, and aligned with
  repo style and the issue's acceptance criteria.
- Broad refactors, formatting churn, release metadata, migrations, dependency
  upgrades, and shared test harness changes require explicit ownership.
- Agents must preserve existing business behavior and sink/output semantics
  unless the issue explicitly changes them.
- Agents must run the assigned verification gate when feasible and report exact
  results. If verification cannot run, they must say why and identify the
  residual risk.
- Agents must stop before using secrets, production systems, destructive
  commands, non-owned files, or unresolved product judgment.

Implementation output is not accepted until an independent reviewer or the
coordinator checks scope, behavior, and verification evidence.

### Reviewer And QA Delegation

Reviewer agents should be assigned after a stable artifact, diff, or
implementation batch exists.

Rules:

- Reviewers receive the acceptance criteria, changed files, non-owned scope,
  relevant docs, and pass-specific checklist.
- Reviewers must state whether they inspected the actual diff/artifact or only
  the plan/handoff.
- Blocking findings should include file path, line or section when applicable,
  severity, confidence, evidence, and recommended action.
- Reviewers should not fix issues unless assigned a separate remediation task.
- Reviewers should check that tests are meaningful, not merely present.
- Reviewers should identify unreviewed surfaces and follow-up passes needed.

## Review Passes

Expanded mode should plan QA as a workstream. The coordinator chooses the
passes required for the project risk profile and records which are blocking.

### Architecture

Checks whether the design fits the repo, issue graph, dependencies, module
boundaries, and long-term code health.

Questions:

- Does the plan make hidden dependencies, interfaces, and sequencing visible?
- Are shared files and integration points serialized?
- Is the abstraction level appropriate for the change?
- Does the design preserve baseline behavior unless explicitly changed?
- Is there a rollback or downshift path?

### Correctness

Checks whether the implementation or artifact satisfies the stated behavior.

Questions:

- Does the change meet acceptance criteria and user intent?
- Are edge cases, error states, concurrency, ordering, and failure modes
  handled?
- Are command outputs, evaluator results, or manual checks sufficient evidence?
- Did the agent avoid accidental behavior changes outside scope?

### Security

Checks permissions, secrets, network exposure, prompt-injection risk, supply
chain risk, auth boundaries, and destructive operations.

Questions:

- Did any agent access secrets, credentials, customer data, production systems,
  or unrestricted web content?
- Are tool permissions and sandbox boundaries appropriate?
- Are external sources trusted, allowlisted, and cited?
- Are dangerous commands, dependency changes, or generated code reviewed?

### Data

Checks data semantics, privacy, integrity, retention, migration behavior, and
sink/output preservation.

Questions:

- Does the change preserve existing data meaning and outputs?
- Are migrations, schemas, exports, sync/sink behavior, and reports accounted
  for?
- Is access separated by membership, tenancy, environment, or sensitivity where
  required?
- Are private or regulated data surfaces excluded from worker prompts unless
  needed and authorized?

### Testing

Checks that verification is relevant, executable, and strong enough for the
change.

Questions:

- Were the assigned tests, linters, evaluators, screenshots, or manual checks
  run?
- Would the tests fail if the intended behavior broke?
- Are gaps explained with residual risk and follow-up checks?
- Are baseline and non-trigger behaviors verified when applicable?

### Product

Checks whether the outcome matches the user's workflow, business constraints,
and release expectations.

Questions:

- Does the solution solve the actual user problem rather than only the local
  ticket text?
- Are UX, operator workflow, support burden, and rollout implications covered?
- Are unresolved product decisions escalated to the human?
- Are tradeoffs and alternatives visible enough for approval?

### Docs

Checks whether durable instructions, references, and handoffs are updated where
behavior, workflow, setup, test, release, or operator experience changes.

Questions:

- Are docs placed in the right surface rather than bloating front-door
  instructions?
- Are source-backed claims cited and stale-risk noted?
- Are examples, commands, and file paths accurate?
- Is the handoff useful after context compaction?

### Release

Checks readiness for merge, installation, publishing, tagging, deployment, or
runtime sync.

Questions:

- Are changelog, version, release notes, install checks, CI, and public repo
  state in scope and correct?
- Are release artifacts updated only by their owner?
- Are checks green or explicitly waived by the human?
- Has the released/runtime state been read back when release or install was
  part of the task?

## Context Isolation

Context isolation is a safety and quality mechanism. It keeps noisy
exploration, large source sets, and specialist review from flooding the
coordinator's active reasoning while preserving a clear synthesis path.

Requirements:

- Each worker receives the smallest complete context bundle needed for the
  task: objective, issue, owned scope, non-owned scope, inputs, constraints,
  tools, stop conditions, and output contract.
- Workers should not receive unrelated private context, stale plans, broad
  repo history, or other agents' scratch work unless necessary.
- Workers should not assume other agents share their context or conclusions.
- Coordinators must reconcile isolated findings before treating them as
  complete project truth.
- Durable state must live outside transient model context: Linear issue,
  companion ledger, PR description, local doc, or structured output artifact.
- Before long-running work, compaction-sensitive transitions, or handoff to a
  new session, the coordinator must preserve current issue, scope, blockers,
  verification state, and next action.

Context isolation is not permission isolation by itself. Sandbox, tool,
network, and write-scope constraints must still be explicit.

## Handoff Format

Every worker, reviewer, and coordinator handoff should be compact, durable, and
actionable.

### Worker Handoff

```markdown
## Worker Handoff

- Agent / role:
- Issue / task:
- Mode:
- Owned scope:
- Non-owned scope respected:
- Inputs used:
- Changed files:
- Summary:
- Evidence:
- Verification run:
- Verification not run:
- Blockers / deviations:
- Residual risks:
- Recommended next action:
```

### Reviewer Handoff

```markdown
## Reviewer Handoff

- Reviewer / pass:
- Artifact or diff reviewed:
- Scope reviewed:
- Scope not reviewed:
- Acceptance criteria checked:
- Findings:
- Blocking status:
- Evidence:
- Verification run:
- Residual risks:
- Recommended decision:
```

### Coordinator Batch Handoff

```markdown
## Coordinator Batch Handoff

- Expanded-mode gate:
- Active milestone:
- Active issues:
- Parallel batch:
- Allocation table link:
- Completed artifacts:
- Integration decisions:
- Verification status:
- Human approvals needed:
- Blockers:
- Next serial action:
- Next parallel-safe batch:
```

Machine-consumed handoffs should use structured outputs with equivalent fields.
Markdown handoffs remain required for human recovery after context compaction.

## Verification

Future implementation of this protocol should be accepted only when the
following checks pass.

### Protocol Acceptance Checks

- Expanded mode has an explicit coordinator role and does not let workers own
  final integration state.
- Role definitions cover coordinator, worker, reviewer, and human
  responsibilities.
- Safe parallelism requires ownership, dependencies, write-scope collision
  checks, tool/permission checks, concurrency budget, and synthesis checkpoint.
- Allocation tables include role, mode, owned scope, non-owned scope, inputs,
  dependencies, expected output, allowed tools, network policy, data
  sensitivity, verification gate, handoff target, and stop conditions.
- Read-only research rules prevent accidental writes and require source-backed
  synthesis.
- Write-capable delegation rules require exclusive ownership, dependency
  readiness, style/local-context checks, verification, and stop conditions.
- Review and QA rules separate independent assessment from implementation.
- Review passes cover architecture, correctness, security, data, testing,
  product, docs, and release.
- Context-isolation guidance requires minimal context bundles and durable
  coordinator synthesis.
- Handoff templates exist for workers, reviewers, and coordinator batches.

### Implementation Verification Checks

When this protocol is wired into `linear-project-planner`, future agents should
verify:

- Baseline mode still behaves as before when expanded mode is not requested.
- Expanded-mode prompts or references route users to this protocol without
  bloating the skill front door.
- Generated Linear issues include owned scope, non-owned scope, dependencies,
  verification gates, and human-review gates where appropriate.
- Companion ledgers can record allocation tables, handoffs, verification
  status, residual risks, and next actions.
- Evaluators check for the required roles, delegation rules, review passes,
  context isolation, handoff format, and verification sections.
- Runtime install or release checks run only when runtime behavior changes and
  are handled by the coordinator or explicitly assigned owner.

This document is a specification artifact only. It does not change runtime
skill behavior until a later implementation task updates the relevant skill,
references, templates, tests, and installation artifacts.
