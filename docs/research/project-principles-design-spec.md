# Project Principles Design Spec

Project: Linear Planner Principles Surface
Linear issue: MAS-719
Date: 2026-04-29
Status: accepted implementation spec

## Goal

Every Linear project planned with this skill should capture a durable Project
Principles / Fundamentals surface. The surface answers: what core decision
principles, quality bars, tradeoff rules, non-negotiables, and anti-goals guide
this project?

The surface must preserve intent for future agents without changing baseline
mode into expanded mode.

## Research Inputs

- MAS-715: team principles and engineering handbooks favor small,
  decision-changing, owner-backed principles.
- MAS-716: ADR/RFC governance favors stable records, small status vocabulary,
  explicit approval evidence, and supersession instead of silent rewrites.
- MAS-717: living-doc patterns favor a linked system: principles as a tiny
  constitution, operating guide as how-to, ledger as current state.
- MAS-718: over-documentation research favors strict artifact boundaries and
  small accurate docs over broad stale manuals.
- Baseline snapshot: `SKILL.md` is compact, baseline mode is default, expanded
  mode is opt-in, and existing evaluators pass.

Useful external patterns included Linear Method, GitLab handbook decision
guidance, AWS ADR guidance, Diataxis, Atlassian working agreements, Google
documentation best practices, Agile simplicity, DORA documentation quality,
Thoughtworks lightweight governance, and PEP/RFC amendment patterns.

## Global Model

Every project gets a principles surface, scaled by project size:

- Small baseline projects: compact section in the operating guide,
  verification matrix, or companion ledger.
- Larger or ambiguous baseline projects: separate companion principles document.
- Expanded-mode projects: first-class living companion document with
  research-seeded principles, amendment controls, and links into dependency
  mapping, QA, ADRs, and agent workflow.

## Compact Baseline Section

Use a short section when the project is small, low ambiguity, short-lived, or
already has a clear brief. The section should fit in the operating guide,
verification matrix, or ledger.

Required headings:

- Project principles / fundamentals
- Non-negotiables
- Quality bar
- Decision rules
- Anti-goals

Keep each heading to bullets. Prefer 5-9 load-bearing bullets total. A baseline
section should not carry amendment tables unless principles are expected to
change over time.

## Promotion Threshold

Promote to a separate companion principles document when any of these are true:

- the project is long-running or likely to survive context compaction;
- multiple agents or teams need a stable decision reference;
- the project contains ambiguous tradeoffs, one-way-door decisions, or
  recurring disagreement risk;
- principles need sources, approval evidence, or review cadence;
- expanded mode is active;
- the compact section exceeds one screen or starts duplicating other artifacts.

Do not promote merely because the template exists.

## Expanded Mode Additions

Expanded mode adds:

- research-derived fundamentals;
- proposed, accepted, rejected/withdrawn, and superseded principle states;
- amendment log and review cadence;
- links to dependency maps, QA plans, ADRs, agent briefs, and handoffs;
- explicit agent behavior rules for when to consult the principles surface.

Expanded mode must remain opt-in and must not make local docs folders,
provenance dossiers, or amendment logs mandatory for ordinary baseline
projects.

## Do Not Grow When

Keep the surface compact when:

- the project is short and low-risk;
- the principles are obvious from the user prompt and acceptance criteria;
- the material is volatile execution state;
- the content is a task, blocker, or next action;
- the choice is a one-time architectural decision that belongs in an ADR;
- verification details belong in the verification matrix or QA plan;
- dependency structure belongs in Linear relationships or a dependency map.

## Relationship To Other Surfaces

- Linear issues: tasks, ownership, dependencies, labels, current status, and
  acceptance criteria.
- Companion execution ledger: current execution state, active issue, worktree,
  blockers, verification evidence, handoffs, and next safest action.
- Agent operating guide: how agents choose work and update the system.
- Verification matrix and QA plans: what proves completion.
- ADRs: consequential one-time technical decisions, alternatives, context, and
  consequences.
- Dependency maps: sequencing, blockers, integration zones, safe parallel
  batches, and relationship rationale.
- Principles surface: durable rules that shape repeated decisions across the
  project.

## Separate Document Sections

A full companion document should contain:

- Project name / Linear project / owning issue
- Purpose
- Non-negotiables
- Quality bar
- Decision principles
- Tradeoff rules
- Anti-goals
- Research-derived fundamentals
- Agent behavior rules
- Proposed amendments
- Accepted principles
- Superseded principles
- Amendment log
- Review/update cadence

## Amendment Model

Principles are stable by default.

Allowed sources for new principles:

- research finding;
- human decision;
- repeated implementation lesson;
- failed verification or dogfood result;
- major tradeoff discovered during build.

Lifecycle:

- Proposed: stable ID, owner, problem, source, affected section, alternatives
  or rejected ideas, implementation impact, and Linear/GitHub evidence links.
- Accepted: explicit review or approval evidence, date, source, required
  verification, and follow-up links for docs/templates/evaluators if needed.
- Superseded: old principle remains visible with `Superseded-By`, replacement
  ID, date, and reason. The replacement records `Replaces`.
- Rejected/Withdrawn: keep the record and rationale so future agents do not
  reopen the same debate without new evidence.

Do not silently rewrite accepted principles. Correct typos and broken links
directly; record semantic changes as amendments.

## Agent Reference Rules

During planning:

- create or locate the principles surface before finalizing the issue graph;
- decide compact vs separate document using the promotion threshold;
- link the surface from the operating guide or ledger.

During execution:

- consult principles when choosing between valid approaches, changing scope,
  altering verification, assigning parallel agents, or resolving tradeoffs;
- propose an amendment when repeated execution shows the principle is missing,
  wrong, or stale;
- do not add tasks, blockers, current status, or detailed test commands to the
  principles surface.

During closeout:

- verify the principles surface still reflects the accepted project intent;
- record superseded or rejected principles rather than deleting history;
- leave a handoff note pointing future agents to the surface.

## Implementation Shape

Smallest additive runtime change:

- add `references/project-principles.md`;
- add `templates/project-principles.md`;
- add a compact principles section to `templates/EXECUTION.md`;
- add concise guidance to `references/project-structure.md`;
- add one compact expanded-mode mention/link;
- add tiny `SKILL.md` Core Rule and Reference Map updates;
- add evaluator coverage proving the surface exists and baseline remains
  concise.

No `linear-agent` CLI behavior change is needed.
