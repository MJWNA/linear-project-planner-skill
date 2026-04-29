# Expanded Mode Linear Graph Schema

Project: Linear Project Planner Expanded Mode
Linear issue: MAS-701
Status: schema spec

## Purpose

Expanded mode needs a Linear issue graph that is useful to both humans and
agents. The graph must make sequencing, ownership, dependency risk, and
verification visible before implementation work is delegated.

Linear remains canonical for execution state, parent-child structure, issue
status, and formal blockers. Local dependency docs preserve the wider
agent-readable map: why edges exist, which work can run in parallel, which
interfaces are risky, and what evidence keeps the graph honest.

## Inputs

- `docs/research/expanded-mode-operating-model.md`
- `docs/research/mit-complex-projects.md`
- `docs/research/delivery-operating-models.md`
- `docs/research/docs-grounding-provenance-policy.md`

## Issue Hierarchy

Expanded-mode projects should use a four-layer issue structure.

### Project Milestones

Milestones are stage gates, not simple date buckets. They group work by the
kind of coordination and verification required.

Recommended milestone sequence:

1. Mode gate and baseline protection.
2. Research and discovery.
3. System decomposition and dependency mapping.
4. Issue graph construction and agent briefing.
5. Implementation and integration batches.
6. Verification, dogfood, and release readiness.
7. Final reconciliation and handoff.

Each milestone should define:

- The decision or artifact needed to exit the stage.
- The workstreams allowed to run inside the stage.
- The verification evidence required before downstream issues can start.
- The serial gate or parallel batch unlocked by completion.

### Guide Issues

Every expanded-mode project should include at least two coordinator-owned guide
issues:

- `Guide: Agent Operating Guide`
- `Guide: Verification Matrix`

For expanded mode, add a third guide issue when dependency mapping is material:

- `Guide: Dependency Map And Parallelism Rules`

Guide issues should not be used as dumping grounds for all project detail. They
should link to local docs, name the dependency map artifact, explain how agents
choose unblocked work, and define the read-back checks used before work is
marked complete.

### Parent Workstreams

Parent workstreams represent outcome-owned streams, architecture boundaries, or
high-coupling integration zones. They should not merely mirror job roles such as
research, implementation, or QA unless those are temporary enabling streams.

Recommended parent workstream types:

- `workstream:baseline-protection`
- `workstream:research-synthesis`
- `workstream:architecture-decomposition`
- `workstream:linear-graph`
- `workstream:agent-platform`
- `workstream:implementation`
- `workstream:verification`
- `workstream:release-handoff`

Each parent workstream must include:

- Outcome owner or coordinator role.
- Outcome statement.
- Included child issue types.
- Excluded or non-owned areas.
- Stage or milestone alignment.
- Exit criteria.
- Verification owner.

### Child Issues

Child issues are the unit of agent execution. Each child should be small enough
for one agent to own without editing unrelated state, but large enough to
produce a meaningful artifact or verified behavior.

Child issue categories:

- Research dossier.
- Synthesis or decision record.
- Dependency map update.
- Agent brief or template.
- Implementation change.
- Test or evaluator change.
- Integration/reconciliation task.
- Verification/dogfood task.
- Release or handoff task.

Child issues should inherit milestone and parent-workstream context, then state
their specific owned scope, dependencies, verification gate, and artifact path.
If a child cannot be made agent-ready, it should be labeled as blocked,
coordinator-only, or needs decomposition.

## Dependency Edges

The graph uses Linear relationships for formal execution dependencies and local
dependency docs for rationale, batches, and interface detail.

### Formal Linear Edges

Use Linear blocker relationships when one issue cannot start or complete until
another issue has produced verified evidence.

Edge types:

- `blocks`: upstream issue must finish before downstream issue starts or exits.
- `blocked-by`: inverse of `blocks`.
- `related`: issues share context, interface, or verification evidence but do
  not impose a hard ordering constraint.
- `parent-child`: hierarchy and ownership boundary, not automatically a blocker.
- `duplicate`: same work or same acceptance target; one issue should close or
  absorb the other.

Only use `blocks` for real sequencing constraints. Overusing blockers makes the
graph look precise while hiding which work could safely run in parallel.

### Local Dependency Edge Classes

The local dependency map should classify every meaningful edge with one primary
edge class:

- `serial-hard`: downstream work cannot begin until the upstream artifact or
  decision is verified.
- `serial-soft`: downstream work may begin as a spike, but cannot be completed
  until upstream evidence lands.
- `parallel-safe`: issues can run at the same time because write scopes,
  decisions, and verification gates do not overlap.
- `parallel-review`: issues can run in parallel, but require coordinator
  reconciliation before merge, release, or runtime sync.
- `cyclic-planned`: a planned learning, prototype, review, or integration loop.
- `cyclic-risk`: an unknown or likely rework loop that must be reduced before
  broad delegation.
- `integration-zone`: multiple workstreams touch the same behavior, interface,
  release path, or verification surface.
- `human-gate`: human approval or product judgment is required before
  downstream execution.
- `external-gate`: third-party docs, API behavior, provider setup, deployment
  state, or credential access must be confirmed before implementation.

### Edge Attributes

Every local dependency edge should capture:

- `from`: upstream issue ID or local artifact.
- `to`: downstream issue ID or local artifact.
- `class`: one local edge class.
- `linear_relationship`: `blocks`, `related`, `parent-child`, `duplicate`, or
  `none`.
- `reason`: short explanation of the dependency.
- `unblocks`: issue ID, milestone, workstream, or parallel batch unlocked.
- `verification`: evidence that proves the dependency is satisfied.
- `owner`: coordinator, agent role, or human reviewer responsible for read-back.
- `risk`: `low`, `medium`, or `high`.

## Labels

Labels should make graph traversal and safe delegation possible at a glance.
They are not a substitute for issue bodies or dependency docs.

### Sequencing Labels

- `expanded-mode`: issue belongs to the heavier operating mode.
- `serial-required`: issue has a hard ordering constraint.
- `parallel-safe`: issue can be delegated alongside other explicitly compatible
  work.
- `parallel-review`: issue can run in parallel but needs coordinator
  reconciliation before finalization.
- `blocked`: issue has an unsatisfied blocker.
- `integration-zone`: issue touches a shared interface, behavior, or release
  surface.
- `cyclic-planned`: issue participates in an intentional learning or review
  loop.
- `cyclic-risk`: issue has unresolved rework risk.

### Ownership Labels

- `agent-ready`: issue contains the minimum agent-ready fields and has no
  hidden ownership ambiguity.
- `coordinator-owned`: issue should stay with the coordinator because it
  updates shared state, Linear graph, ledger state, release state, or final
  integration.
- `human-review`: downstream execution or completion needs human approval.
- `needs-decomposition`: issue is too broad, unclear, or coupled for safe
  delegation.

### Evidence Labels

- `source-backed`: issue depends on local research or external docs evidence.
- `context7-required`: issue needs current third-party technical docs before
  implementation.
- `openai-docs-required`: issue needs official OpenAI/Codex docs before
  implementation.
- `local-evidence`: issue depends mainly on repo inspection, tests, or existing
  project artifacts.
- `verification-gate`: issue owns a required check, evaluator, dogfood pass, or
  acceptance review.

## Agent-Ready Contract

An issue is agent-ready only when another Codex or Claude session can execute it
without rediscovering scope, ownership, dependencies, or verification.

Minimum fields:

- Title with issue type and outcome.
- Parent workstream.
- Milestone or stage.
- Owner or intended agent role.
- Objective or outcome statement.
- Owned write scope.
- Non-owned scope and forbidden files/systems.
- Inputs and required reading.
- Local docs or source links.
- Formal Linear dependencies.
- Local dependency map references.
- Expected output artifact or behavior.
- Acceptance criteria.
- Verification command, review method, or read-back check.
- Context7/OpenAI/source requirements when applicable.
- Human-review gate when applicable.
- Completion comment requirements.

Agent-ready issues must not assign workers to update shared state unless that is
the owned scope. Shared state includes Linear project structure, dependency
relationships, companion ledgers, release metadata, changelog/version files, and
installed runtime copies.

Recommended issue body shape:

```md
## Objective

## Owned Scope

## Non-Owned Scope

## Inputs

## Dependency Context

## Expected Output

## Acceptance Criteria

## Verification

## Evidence
```

## Local Dependency Map

Expanded mode should keep a local dependency map alongside Linear. Linear shows
the live execution graph; the local map explains the planning model that agents
need for safe work allocation.

Recommended location:

```text
docs/expanded-mode/dependencies/<project-slug>-dependency-map.md
```

For this skill-development project, design-stage dependency specs may live in:

```text
docs/research/
```

Minimum local dependency map sections:

- Metadata: project, Linear project, owner, status, last updated, source policy.
- Milestones and exit gates.
- Parent workstreams and owners.
- Issue table with ID, title, parent, milestone, labels, owned scope, and
  verification gate.
- Edge table with `from`, `to`, `class`, `linear_relationship`, `reason`, and
  `verification`.
- Parallel batches with compatible issue IDs and non-overlap rationale.
- Serial gates with blocker IDs and required evidence.
- Integration zones and cyclic-risk areas.
- Human-review and external-doc gates.
- Linear read-back checklist.

### Alignment Rules

Keep Linear and the local map aligned with these rules:

- Linear is canonical for current issue status, assignee, parent-child
  relationships, and formal blockers.
- The local map is canonical for dependency rationale, batch design, edge class,
  interface risk, and agent allocation notes.
- Every `serial-hard` local edge should have a matching Linear `blocks`
  relationship unless Linear relationship creation is unavailable.
- Every `parallel-safe` batch must name the non-overlapping write scopes and
  verification gates that make parallelism safe.
- Every `integration-zone`, `cyclic-risk`, `human-gate`, or `external-gate`
  edge must be visible either as a Linear blocker/related edge or as a linked
  local map entry from the affected issue.
- When Linear and local docs disagree, pause delegation, read back Linear, and
  update the stale surface before claiming the issue graph is ready.
- Worker agents should not update the local map or Linear graph unless their
  issue explicitly owns that graph-maintenance scope.

## Verification

Future implementation should pass these acceptance checks before expanded-mode
graph creation is considered ready:

- Project includes guide issues for agent operation, verification matrix, and
  dependency/parallelism rules.
- Milestones represent stage gates with exit evidence, not only calendar phases.
- Parent workstreams map to outcomes, architecture boundaries, or integration
  zones.
- Child issues include the minimum agent-ready fields before receiving the
  `agent-ready` label.
- Every hard dependency has a Linear blocker edge or a documented exception.
- Every local edge has `from`, `to`, `class`, `reason`, and `verification`.
- Every `parallel-safe` issue has disjoint owned scope and independent
  verification.
- Serial, cyclic, integration, human-review, and external-doc gates are labeled.
- Local dependency map names the Linear project or issue IDs it mirrors.
- Linear read-back confirms parent-child relationships, blockers, labels, and
  guide issues before implementation agents are spawned.
- Verification comments include changed/inspected artifacts, checks run,
  residual risks, and follow-ups.
- Baseline mode remains unchanged unless the user explicitly requested runtime
  behavior changes.

Targeted file checks for this spec:

- File exists and is non-empty.
- Required sections are present: Issue Hierarchy, Dependency Edges, Labels,
  Agent-Ready Contract, Local Dependency Map, and Verification.
