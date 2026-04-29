# Project Principles / Fundamentals: Linear Planner Principles Surface

## Project Identity

- Linear project: Linear Planner Principles Surface
- Owning issue: MAS-722
- Repository: `/Users/ronniemeagher/Desktop/Curssor/mta-pt-workspace/projects/linear-project-planner-skill`
- Companion ledger: `../.codex-linear-ledgers/linear-planner-principles-surface/EXECUTION.md`
- Status: accepted dogfood surface
- Last reviewed: 2026-04-29

## Purpose

Add a global Project Principles / Fundamentals surface to the
`linear-project-planner` skill without making baseline mode heavy. This project
should prove the new surface can preserve intent while staying selective.

## Non-Negotiables

- Preserve baseline mode as concise default behavior.
- Keep `SKILL.md` small, router-safe, and reference-map oriented.
- Edit the repo source; treat the installed skill copy as a runtime artifact.
- Do not change `linear-agent` behavior unless a verified spec proves it is
  necessary.
- Do not publish, tag, or create a public release without explicit approval.

## Quality Bar

- Every planned Linear project gets some principles/fundamentals surface.
- Small projects can satisfy the rule with a compact section.
- Larger, ambiguous, or expanded-mode projects get a companion document.
- Evaluators prove the new surface exists and baseline mode remains concise.
- Full verification passes before installed runtime sync.

## Decision Principles

- Principles must change repeated decisions; otherwise they do not belong here.
- Escalate by project risk and ambiguity, not by template habit.
- Prefer links to source-of-truth artifacts over duplicated content.
- Preserve history through proposed, accepted, superseded, and rejected records.
- Keep current state in Linear and the ledger, not in principles.

## Tradeoff Rules

- If a rule guides many issues or agents, record it as a principle.
- If a choice is one-time and technical, record it in an ADR or decision note.
- If a detail proves completion, keep it in QA or the verification matrix.
- If a detail describes order or ownership, keep it in Linear or dependency
  maps.
- If a section grows beyond one screen, promote or split it instead of stuffing
  more into the baseline surface.

## Anti-Goals

- No philosophy handbook for ordinary projects.
- No amendment ceremony for small baseline projects.
- No duplicated execution state across docs.
- No hidden rewrite of accepted principles.
- No CLI behavior change for documentation-only intent capture.

## Research-Derived Fundamentals

- Linear-style planning favors clarity, brevity, ownership, and small scoped
  work.
- ADR/RFC models favor stable accepted records and explicit supersession.
- Living-doc patterns work best when each surface has one job.
- Over-documentation risk rises when templates attract non-load-bearing
  content.

## Agent Behavior Rules

- Consult this document when implementation choices threaten baseline
  contamination, scope expansion, amendment semantics, or verification scope.
- Propose an amendment if dogfood or verification proves a principle missing or
  wrong.
- Keep issue progress in Linear and the companion ledger.

## Proposed Amendments

| ID | Date | Owner | Source | Proposal | Affected Section | Evidence / Discussion | Status |
|---|---|---|---|---|---|---|---|
| P-001 | 2026-04-29 | Codex | User prompt + MAS-715 to MAS-718 research | Add a global scaled principles surface to the skill. | Runtime references and templates | MAS-719 design spec | Accepted |

## Accepted Principles

| ID | Date | Principle | Source | Approval / Review Evidence | Verification / Follow-Up |
|---|---|---|---|---|---|
| A-001 | 2026-04-29 | Every Linear project needs a principles/fundamentals surface scaled to project size. | User prompt + MAS-719 spec | MAS-719 completion comment | MAS-720 and MAS-721 |
| A-002 | 2026-04-29 | Baseline projects may use a compact section; separate documents are promotion-based. | MAS-715, MAS-717, MAS-718 | MAS-719 completion comment | `references/project-principles.md` |
| A-003 | 2026-04-29 | Accepted principles should be superseded rather than silently rewritten. | MAS-716 | MAS-719 completion comment | `templates/project-principles.md` |

## Superseded Principles

| ID | Superseded By | Date | Reason | Original Source |
|---|---|---|---|---|
| None | n/a | n/a | n/a | n/a |

## Rejected Or Withdrawn Amendments

| ID | Date | Proposal | Reason | Reopen Only If |
|---|---|---|---|---|
| R-001 | 2026-04-29 | Make every baseline project create a full companion principles document. | Would contaminate concise baseline mode. | A project class repeatedly loses intent with compact sections. |
| R-002 | 2026-04-29 | Add new `linear-agent` commands for principles management now. | Documentation/template changes satisfy the requirement without changing CLI behavior. | Repeated dogfood shows manual principles handling is unreliable. |

## Amendment Log

- 2026-04-29: Accepted initial principles surface for this enhancement based on
  user prompt, baseline snapshot, and MAS-715 to MAS-718 research.

## Review / Update Cadence

- Review before final verification and runtime install sync.
- Review if evaluator failures, dogfood findings, or implementation conflicts
  reveal a missing or stale principle.
