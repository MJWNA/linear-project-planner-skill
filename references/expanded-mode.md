# Expanded Mode

Expanded mode is an opt-in operating model for long-horizon Linear projects
that need deep research, local project docs, dependency mapping, provenance,
multi-agent allocation, planned QA, dogfood, and release or handoff gates.

Baseline mode remains the default. Do not use this reference for ordinary
Linear planning, concise audit remediation, one-off issue lookup, routine safe
parallelism checkpoints, or small projects that do not need the extra structure.

## Mode Gate

Use expanded mode when the user explicitly asks for one of these signals:

- expanded mode
- long-horizon project
- detailed multi-phase plan
- deep research first
- dependency mapping
- software-firm-grade planning
- multi-team delivery model
- local project docs or references
- research dossier or ADR-first planning
- heavy safe parallel-agent coordination
- dogfood before release

Compound triggers also count when a Linear project request combines deep
research, source provenance, local docs, dependency maps, and broad parallel
agent allocation.

Stay in baseline mode when the request is a small Linear project, one-off issue
lookup, normal remediation plan, pure Linear graph cleanup, routine companion
ledger use, or standard validation gate.

## Baseline Protection

Before creating expanded-mode issues:

1. Capture a baseline/no-contamination snapshot.
2. Record which current behavior must not change.
3. Keep normal mode as the default path.
4. Keep expanded-mode detail in this reference, templates, local docs, and
   Linear issues, not in a bloated `SKILL.md`.
5. Verify baseline evaluators before claiming runtime behavior is ready.

Expanded mode must not make deep research, local docs folders, Context7,
OpenAI docs, dogfood, or multi-agent allocation mandatory for baseline
projects.

## Local Docs

Create a local docs workspace when the project needs durable evidence outside
chat and issue bodies. Prefer a project-specific root:

```text
docs/expanded-mode/<project-slug>/
  README.md
  research/
  decisions/
  dependencies/
  qa/
  agent-briefs/
  handoff/
```

Use the smallest useful folder set. A one-session project may need only a
decision note and QA note. A multi-phase project may need the full tree.

Each substantive doc should include project, Linear issue, status, owner or
agent role, inputs, source scope, verification method, and links back to the
owning issue. Do not paste full docs into Linear issue descriptions; link the
artifact and summarize the decision-relevant part.

## Project Charter Description

Expanded-mode project descriptions should behave like a compact charter. Include
these fields when relevant:

- project purpose
- operating mode
- source of truth
- companion ledger path
- local docs root
- current phase
- workstream map
- dependency policy
- research-to-issue policy
- Continuous Issue Discovery policy
- verification policy
- agent handoff policy
- coordinator responsibilities

Keep the charter current when the project shape changes. Link large local docs
instead of pasting them into the project description.

## Research And Provenance

Run research before implementation when the project depends on external
practice, current docs, unknown architecture, SDK/API behavior, or strategic
delivery design.

Research artifacts must separate:

- source-backed facts
- local repo evidence
- inferences for this project
- recommendations
- refresh triggers

Use Context7 when work depends on current third-party technical docs,
version-specific API behavior, SDK usage, framework patterns, auth, payments,
database tooling, provider integrations, or user-requested current docs.

Use official OpenAI/Codex docs when work relies on Skills behavior, MCP,
hosted tools, tool search, subagents, `agents.max_threads`, sandboxing,
compaction, structured outputs, reasoning controls, or Codex configuration.

## Project Principles / Fundamentals

Expanded-mode projects should create a first-class companion principles
document from `templates/project-principles.md`. Seed it from the research
synthesis and keep it linked from the operating guide, dependency map, QA plan,
and companion ledger.

The principles document is the stable decision reference for non-negotiables,
quality bar, tradeoff rules, anti-goals, accepted principles, superseded
principles, and amendment history. It must not replace Linear tasks, execution
ledger state, ADRs, QA plans, or dependency maps.

## Dependency Mapping

Build a dependency map before broad implementation. Linear remains canonical
for issue state, parent/child structure, and formal blockers. The local
dependency map explains why sequencing, parallel batches, integration zones,
human gates, and external-doc gates exist.

Recommended local dependency map sections:

- milestones and exit gates
- parent workstreams and owners
- issue table with owned scope and verification gate
- edge table with `from`, `to`, `class`, `linear_relationship`, `reason`, and
  `verification`
- parallel-safe batches and non-overlap rationale
- serial gates and required evidence
- integration zones, cyclic risks, human gates, and external-doc gates
- Linear read-back checklist

Use Linear blockers only for real sequencing constraints. Use local edge
classes such as `serial-hard`, `serial-soft`, `parallel-safe`,
`parallel-review`, `integration-zone`, `human-gate`, and `external-gate` to
explain the graph.

## Issue Graph

Expanded-mode projects should usually include:

- normal guide issues for agent operation and verification
- a dependency-map/parallelism guide when dependency mapping is material
- milestone gates for mode gate, research, decomposition, implementation,
  verification, dogfood, release, and handoff
- a project principles/fundamentals guide or companion document when principles
  are material to sequencing, tradeoffs, or agent behavior
- parent workstreams organized around outcomes, architecture boundaries, or
  integration zones
- child issues small enough for one agent to own

An `agent-ready` issue must include objective, owned scope, non-owned scope,
inputs, dependencies, expected output, acceptance criteria, verification,
evidence links, Context7/OpenAI/source requirements when applicable, and human
review gates when needed.

Expanded-mode issue bodies should include the sections future agents need after
context loss:

- Objective
- Background context
- Why this matters
- Inputs / required reading
- Owned scope
- Non-owned scope
- Dependencies
- Blockers
- Step-by-step working instructions
- Expected outputs
- Acceptance criteria
- Verification requirements
- Handoff / context recovery notes
- Follow-up issue candidates
- Required updates to local docs, ledger, or dependency map

Omit sections that are genuinely not relevant, but do not omit ownership,
dependencies, acceptance criteria, verification, or handoff notes for
write-capable or long-running work.

## Continuous Issue Discovery Protocol

Expanded mode uses a formal discovery protocol because the plan is expected to
evolve. At research, implementation, review, verification, docs, release, and
handoff checkpoints, classify new work as Blocker, Dependency, Defect, Research
follow-up, Implementation follow-up, Decision required, QA / verification gap,
Documentation gap, Scope expansion, or Risk / mitigation.

Create a new issue immediately when the discovery blocks current work, affects
correctness, is required for acceptance, or creates a real dependency. Link
formal blockers/dependencies in Linear and update the local dependency map when
sequencing changes.

For non-blocking expansions, first record an issue candidate with discovery
reason, surfacing issue/workstream, owner workstream, acceptance criteria,
verification, and compaction-safe context. The coordinator deduplicates,
accepts, rejects, or defers the candidate before creating extra scope.

Update the companion ledger and any relevant local docs when discovery changes
project shape, dependency order, verification gates, agent allocation, release
readiness, or handoff expectations.

## Multi-Agent Allocation

Parallel agents are encouraged only after ownership, dependencies, and
verification gates are explicit.

Before dispatching agents, record:

- agent role and issue
- mode: read-only, write-capable, or review-only
- owned write scope
- non-owned scope
- inputs and dependencies
- expected output
- allowed tools and network policy
- data sensitivity
- verification gate
- handoff target
- stop conditions

Research agents are usually safe early parallelism when each owns a single
dossier. Write-capable agents need exclusive file/module ownership and should
not update Linear state, ledger state, release metadata, changelog/version
files, installed runtime copies, or shared dependency maps unless explicitly
assigned.

Keep the coordinator responsible for Linear state, ledger state, issue graph
changes, integration decisions, final verification, and human review packets.

## QA And Review

Plan QA as a workstream. Choose review passes by risk:

- architecture
- correctness
- security
- data
- testing
- product
- docs
- release

Verification must include baseline preservation when runtime behavior changes.
Dogfood expanded mode on itself or a contained project before release when the
mode changes skill behavior, templates, evaluators, or installed runtime
instructions.

## Recursive Loop Protocol

When the user asks for recursive, long-horizon, Ralph Wiggum, or auto-research
style execution, make the loop explicit in Linear and the ledger:

1. Define the loop type, frozen evaluator set, source scope, issue-creation
   threshold, and stop condition.
2. Run research or review against the smallest responsible issue.
3. Apply one focused implementation change.
4. Run computational sensors first, then inferential review.
5. Classify misses through Continuous Issue Discovery.
6. Create or update Linear issues for actionable blockers, defects,
   dependencies, QA gaps, docs gaps, or future-agent recovery failures.
7. Return to the relevant research or implementation issue and repeat until the
   stop condition is met.

Keep this protocol in expanded mode or explicit deep validation. Baseline
projects still use standard validation unless the user opts into the deeper
loop.

## Templates

Use the templates in `templates/expanded-mode/` when they reduce recovery cost:

- `research-dossier.md`
- `decision.md`
- `dependency-map.md`
- `qa-plan.md`
- `agent-brief.md`
- `handoff.md`

Copy only the templates the project needs. Avoid ceremony when the Linear issue
body and companion ledger already preserve enough context.

## Completion Gate

Before closing expanded-mode implementation or release work:

1. Confirm expanded mode remained opt-in.
2. Confirm baseline mode stayed concise and stable.
3. Run the repo's standard tests and evaluators.
4. Record local docs, Linear issues, ledger path, verification evidence,
   residual risks, and follow-ups.
5. Sync installed runtime only after source repo verification when runtime
   behavior changed.
