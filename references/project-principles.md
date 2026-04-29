# Project Principles / Fundamentals

Use this reference when creating the durable principles surface for a Linear
project. The surface preserves governing intent: core principles, quality bars,
tradeoff rules, non-negotiables, and anti-goals that should guide repeated
decisions across the project.

This is not an execution log. Tasks belong in Linear, current state belongs in
the companion ledger, detailed technical decisions belong in ADRs, verification
belongs in QA or verification artifacts, and sequencing belongs in Linear
relationships or dependency maps.

## Scaling Rule

Every Linear project gets a principles surface, scaled to project size:

- Small baseline projects: add a compact section to the operating guide,
  verification matrix, or companion ledger.
- Larger or ambiguous baseline projects: create a separate companion principles
  document from `templates/project-principles.md`.
- Expanded-mode projects: create a first-class living companion document with
  research-seeded principles, amendment controls, and links into dependency
  mapping, QA, ADRs, and agent workflow.

Keep baseline mode concise. Do not create expanded-mode docs folders,
provenance dossiers, or amendment tables for ordinary small projects unless the
promotion threshold below is met.

## Compact Baseline Section

Use the compact section when the project is short, low ambiguity, or already
has a clear brief. Keep it to one screen where possible.

Recommended headings:

- Project principles / fundamentals
- Non-negotiables
- Quality bar
- Decision rules
- Anti-goals

Prefer 5-9 load-bearing bullets total. A principle belongs here only when it
would change issue shape, sequencing, parallelism, verification, escalation, or
tradeoff decisions.

## Promotion Threshold

Promote to a separate companion principles document when any of these are true:

- the project is long-running or likely to survive context compaction;
- multiple agents or teams need a stable decision reference;
- the project has ambiguous tradeoffs, one-way-door decisions, or repeated
  disagreement risk;
- principles need source links, approval evidence, or a review cadence;
- expanded mode is active;
- the compact section no longer fits one screen or starts duplicating other
  artifacts.

Do not promote merely because a template exists.

## Full Companion Document

Use `templates/project-principles.md` for a full document. Include only sections
that help future agents make consistent decisions:

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

Principles are stable by default. Additions require at least one source:

- research finding;
- human decision;
- repeated implementation lesson;
- failed verification or dogfood result;
- major tradeoff discovered during build.

Use a small status vocabulary:

- `Proposed`: stable ID, owner, problem, source, affected section, alternatives
  or rejected ideas, implementation impact, and Linear/GitHub evidence links.
- `Accepted`: explicit review or approval evidence, date, source, required
  verification, and follow-up links for docs/templates/evaluators if needed.
- `Superseded`: old principle remains visible with `Superseded-By`,
  replacement ID, date, and reason. The replacement records `Replaces`.
- `Rejected` or `Withdrawn`: keep the rationale so future agents do not reopen
  the same debate without new evidence.

Do not silently rewrite accepted principles. Correct typos and broken links
directly; record semantic changes as amendments.

## Agent Usage

During planning:

- create or locate the principles surface before finalizing the issue graph;
- choose compact section versus separate document with the promotion threshold;
- link the surface from the operating guide or ledger.

During execution:

- consult the surface when choosing between valid approaches, changing scope,
  altering verification, assigning parallel agents, or resolving tradeoffs;
- propose an amendment when repeated execution shows a missing, wrong, or stale
  principle;
- keep tasks, blockers, current status, and detailed test commands out of the
  principles surface.

During closeout:

- confirm the surface still reflects accepted project intent;
- preserve superseded or rejected principles instead of deleting history;
- leave a handoff note pointing future agents to the surface.
