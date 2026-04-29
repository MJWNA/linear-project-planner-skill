# Expanded Mode Operating Model

Project: Linear Project Planner Expanded Mode
Linear issue: MAS-695
Status: synthesis from MAS-691, MAS-692, MAS-693, and MAS-694

## Purpose

Expanded mode should let `linear-project-planner` behave more like a senior
software delivery office for long-horizon work: research first, dependency map
early, parallelize only after ownership is explicit, and make verification a
planned workstream instead of a final afterthought.

This operating model is intentionally heavier than the baseline skill. The
baseline mode should stay fast and direct for ordinary Linear planning. Expanded
mode should only activate when the user asks for a detailed mode, long-horizon
planning, multi-phase dependency mapping, software-firm-grade planning, deep
research first, local project docs, or heavy safe parallel-agent use.

## Inputs

- `docs/research/mit-complex-projects.md`
- `docs/research/google-engineering-practices.md`
- `docs/research/delivery-operating-models.md`
- `docs/research/frontier-ai-delivery-patterns.md`

## Core Operating Principles

1. Make hidden structure visible before execution.
   MIT's DSM and complex-project framing support mapping interfaces,
   dependencies, feedback loops, and planned versus unplanned iteration before
   assigning execution work.

2. Preserve long-term code health.
   Google's review guidance supports evidence-based decisions, meaningful
   tests, small changes, review as mentoring, and repo-local style authority.

3. Optimize for flow and stability together.
   DORA, SPACE, Team Topologies, and Continuous Delivery sources all point away
   from activity-count metrics and toward outcome flow, quality, team topology,
   and sociotechnical fit.

4. Treat multi-agent work as an operating system, not a swarm.
   Frontier AI delivery patterns support coordinator-led worker agents,
   isolated ownership, explicit verification, and context isolation where it
   improves quality or focus.

## Delivery Phases

### 0. Mode Gate And Baseline Protection

Expanded mode starts with a gate:

- Confirm the request needs expanded mode rather than baseline mode.
- Create or update a baseline snapshot documenting the current skill contract.
- Record what must not change in baseline behavior.
- Mark any intended baseline-adjacent edit as additive, behind an explicit
  expanded-mode trigger, or blocked until redesigned.

Required outputs:

- Baseline/no-contamination note.
- Explicit trigger and non-trigger interpretation.
- Verification commands that prove baseline still behaves the same.

### 1. Research And Discovery

Research is a first-class phase when the project depends on external practice,
current docs, strategic design, or unknown architecture.

Required outputs:

- Research issues with owned deliverables.
- Source-backed local docs.
- Source freshness and provenance notes.
- A synthesis issue before implementation starts.

Parallelism rule:

- Research agents are the safest early parallelism because their write scopes
  can be one file each and their findings can be reconciled before specs.

### 2. System Decomposition And Dependency Mapping

Before implementation issues are created, expanded mode should map:

- Workstreams and phases.
- Dependencies and blockers.
- Interfaces between modules, tools, teams, agents, and docs.
- Feedback loops and likely rework cycles.
- Serial gates, parallel-safe batches, and risky shared files.

Required outputs:

- A dependency map in Linear issue relationships.
- A local dependency document or table for agent-readable context.
- Labels such as `parallel-safe`, `serial-required`, `needs-human-review`, and
  `agent-ready`.

### 3. Project Docs Workspace

Expanded mode creates a local project documentation folder so the plan is not
trapped inside transient chat context or only scattered across Linear issues.

Recommended taxonomy:

- `docs/research/` for source-backed research and synthesis.
- `docs/expanded-mode/` or a project-specific docs root for generated operating
  artifacts.
- `docs/expanded-mode/decisions/` for ADRs and major tradeoffs.
- `docs/expanded-mode/dependencies/` for dependency maps and sequencing.
- `docs/expanded-mode/agent-briefs/` for worker ownership and verification
  briefs.
- `docs/expanded-mode/qa/` for verification plans, review notes, and dogfood
  results.

For this repository, the research phase uses `docs/research/` because the
expanded-mode implementation is still being designed.

### 4. Planning And Issue Graph Construction

Linear remains the execution source of truth for issue state and dependency
tracking. The local docs folder stores context, research, decisions, and
reviewable artifacts that are too large or too structured for issue bodies.

Every expanded-mode execution issue should define:

- Owned files or system area.
- Non-owned files or forbidden areas.
- Inputs.
- Outputs.
- Dependencies.
- Verification command or review method.
- Context7/OpenAI/source requirements when applicable.
- Human review gate when risk or product judgment is high.

### 5. Delegation And Parallel Execution

Parallel agents are encouraged only after the coordinator writes the allocation
rules.

Before spawning or assigning agents, the coordinator must record:

- Agent name or role.
- Owned write scope.
- Non-owned scope.
- Dependency prerequisites.
- Expected artifact.
- Verification gate.
- What the agent must not update, especially Linear state, ledger state,
  release metadata, or shared runtime files unless explicitly assigned.

Good parallel-agent tasks:

- Independent research dossiers.
- Independent template drafts.
- Independent test/evaluator updates with disjoint files.
- Independent review passes against a stable diff.

Poor parallel-agent tasks:

- Several agents editing `SKILL.md` at the same time.
- Shared changelog/version/release work.
- Subtle integration logic where the next step depends on one unresolved design
  decision.
- Work whose success requires one agent to understand all other agents'
  unmerged changes.

### 6. Review, QA, And Verification

Expanded mode should plan QA as a workstream, not a final line item.

Required gates:

- Research verification: source links and required sections present.
- Spec verification: trigger contract, non-trigger contract, and baseline
  protection are explicit.
- Implementation verification: baseline tests, evaluator checks, syntax checks,
  and install checks as relevant.
- Dogfood verification: run expanded mode on itself or a contained project and
  record where the instructions helped or overloaded the flow.
- Human review gate: required before release when baseline runtime behavior,
  public docs, or installed skill behavior changes.

## Roles

- Coordinator: owns issue sequencing, dependency map, ledger, Linear state,
  synthesis, and final integration.
- Research agent: owns one source-backed dossier or narrow research question.
- Spec agent: owns a bounded design artifact or template draft.
- Implementation agent: owns a disjoint file/module set.
- Verification agent: owns tests, evaluator review, dogfood, or adversarial
  inspection against stated acceptance criteria.
- Human reviewer: approves product-level scope, release readiness, and any
  baseline-adjacent behavior change.

## Enforce vs Offer

Expanded mode should enforce:

- Explicit opt-in mode gate.
- Baseline protection snapshot.
- Local docs folder for long-horizon projects.
- Source-backed research for external or current claims.
- Dependency map before broad implementation.
- Ownership and verification gates before parallel agents.
- Coordinator-owned Linear and ledger state.
- Human review gate before release/runtime sync when behavior changes.

Expanded mode should offer:

- Additional research waves.
- Optional review agents for lower-risk docs.
- Optional metrics dashboards or scorecards.
- Optional deeper team-topology modeling when the project has multiple real
  teams or many agent roles.
- Optional extra project-doc subfolders when the plan is small enough that a
  lighter folder would be clearer.

Expanded mode should avoid:

- Turning every small Linear project into a large program.
- Maximizing agent count as a success metric.
- Treating research docs as runtime instructions without synthesis.
- Letting worker agents update shared state independently.
- Copying external firm practices without adapting to the repo and user.

## Too Heavy For Baseline

These practices belong only in expanded mode:

- Mandatory deep external research.
- Local project docs folder with subfolder taxonomy.
- DSM-style dependency modeling.
- Multi-agent allocation matrix.
- Dedicated provenance policy.
- Formal dogfood/release gate.
- Separate operating model, QA protocol, and dependency schema docs.

Baseline mode should keep its current compact project/issue/ledger behavior and
only escalate to expanded mode when the user's request clearly justifies it.
