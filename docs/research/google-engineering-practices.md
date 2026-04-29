# Google Engineering Practices Research

Linear issue: MAS-692
Project: Linear Project Planner Expanded Mode
Captured: 2026-04-29

## Source Scope

This research prioritizes public, primary Google engineering practice sources
that are directly relevant to an expanded mode for `linear-project-planner`.
The seed source was Google's Engineering Practices documentation, especially
the code review standard and reviewer guidance.

Primary sources reviewed:

- Google Engineering Practices landing page.
- Google's Code Review Guidelines: reviewer standard.
- Google's Code Review Guidelines: what to look for in a review.
- Google's Code Review Guidelines: review speed.
- Google's Code Review Guidelines: review comments.
- Google's Code Review Guidelines: small CLs.
- Google Style Guides landing page.

These sources are review-process and code-health standards rather than a full
software delivery lifecycle model. The implications below therefore translate
Google-style review principles into expanded-mode planning, evidence, and
handoff behavior instead of copying Google's internal process wholesale.

## Confirmed Practices

Google frames code review around long-term code health. The review standard is
not "perfect code before approval"; it is that reviewers should approve once a
change clearly improves the system's overall code health, while never accepting
changes that definitely make code health worse outside a true emergency.

Forward progress and quality are deliberately balanced. Reviews should avoid
blocking useful improvements over minor polish, but reviewers remain
responsible for consistency, maintainability, readability, and system health.
Continuous improvement is the target: better code over time, not an impossible
perfection bar.

Evidence outranks preference. Google's review principles state that technical
facts and data overrule opinions and personal preference. Design disagreements
should be resolved against engineering principles, evidence, and system
context; if several approaches are equally valid, the author's preference can
stand.

Style has an authority hierarchy. The relevant style guide is the authority for
pure style matters. If no style rule applies, the local codebase style should be
followed as long as doing so does not worsen code health. Pure personal style
preferences should not block approval.

Reviews should inspect the substance of the change. Google's reviewer checklist
covers design, functionality, complexity, tests, naming, comments,
documentation, every assigned line, and broader system context. Reviewers are
also expected to consider user impact, developer impact, edge cases, concurrency
risks, and whether the change adds unnecessary complexity.

Tests are part of maintainable code. Google expects appropriate unit,
integration, or end-to-end tests for the change, and reviewers should assess
whether tests are correct, useful, likely to fail when behavior is broken, and
not more complex than necessary.

Small, self-contained changes are preferred. Google's CL guidance says small
changes review faster, get reviewed more thoroughly, are easier to reason
about, introduce fewer bugs, merge more easily, and roll back more simply.
Large changes should usually be split into smaller self-contained changes,
potentially by stack layer, file group, vertical feature, or prerequisite
refactoring.

Refactoring should usually be separated from feature or bug-fix work. Google
allows small local cleanups inside a focused change, but larger refactors should
be separate so reviewers can understand, test, merge, and roll back each change
more safely.

Review speed matters at the team level. Google optimizes for whole-team
velocity rather than individual coding speed alone. Review responses should be
prompt, with one business day described as the maximum response time, while
still avoiding needless interruption of focused coding work.

Review comments are a mentoring surface. Google's guidance emphasizes kindness,
reasoning, clear severity labels, and teaching. Reviewers should explain why a
comment matters, distinguish required changes from optional suggestions, and
also call out strong work so authors learn what to repeat.

Review-tool explanations are not enough for future maintainers. If code is hard
to understand, the preferred outcome is clearer code or durable code comments
and documentation, not a private explanation trapped in the review thread.

## Implications For Expanded Mode

Expanded mode should make code health an explicit planning and verification
axis. Every implementation workstream should ask whether the planned sequence
improves maintainability, readability, understandability, testability, and
developer usability over time, not merely whether it completes tickets.

Expanded mode should require evidence-based review gates. Issues and synthesis
docs should separate facts, cited source guidance, local code evidence,
verified behavior, and reviewer judgment. When an agent recommends a design
choice, it should name the evidence or principle behind the recommendation.

Expanded mode should preserve reviewer mentoring as a first-class outcome.
Agent review notes should include the reason behind important findings,
severity labels such as required/optional/nit/fyi, and positive examples worth
repeating. This matters because expanded mode often coordinates many agents who
need consistent standards, not just task completion.

Expanded mode should encode style authority. Plans should first defer to the
repo's configured formatters, linters, style guides, and local conventions. An
agent should not request broad style churn unless the style authority requires
it or the work is explicitly scoped as a separate formatting/refactoring task.

Expanded mode should protect consistency without freezing poor patterns. If a
local pattern exists and no stronger rule applies, new work should match it.
If the local pattern harms code health, expanded mode should capture a cleanup
follow-up or separate refactor rather than silently spreading the problem.

Expanded mode should design for continuous improvement. Completion criteria
should ask whether the change leaves the system easier to understand, test,
operate, or extend than before. Optional polish can be logged without blocking
shipping when code health is clearly improving.

Expanded mode should turn large projects into reviewable increments. The Linear
graph should favor small, self-contained issues with tests and docs in the same
unit of work. Large milestones should split by dependency, layer, vertical
feature, file ownership, or refactor-before-feature sequencing.

Expanded mode should make broad-context review explicit. Before unblocking
implementation, agents should inspect enough surrounding files, docs,
interfaces, tests, and production/user impact to know whether the change fits
the system. If a reviewer only covers a slice, the issue or handoff should state
what was and was not reviewed.

Expanded mode should make documentation updates part of acceptance criteria
when behavior, build, test, release, operator workflow, or public interface
changes. Missing docs should be treated as a review finding, not a nice-to-have
afterthought.

Expanded mode should route specialist concerns to qualified reviewers or
dedicated issues. Privacy, security, concurrency, accessibility,
internationalization, deployment, and data-integrity risks should not be
rubber-stamped by a general agent when the project needs deeper review.

## What To Require vs Offer

Require in expanded mode:

- A code-health gate for each implementation workstream covering
  maintainability, readability, understandability, testability, and developer
  impact.
- Evidence-backed findings that distinguish source facts, local code evidence,
  command output, and reviewer judgment.
- Explicit review severity labels so agents know what blocks completion and
  what is optional mentoring or polish.
- Style-authority lookup before requesting formatting, naming, or convention
  changes.
- Consistency checks against existing code, with separate follow-ups when local
  consistency conflicts with better code health.
- Small, reviewable issue decomposition with related tests and docs included in
  the same issue where appropriate.
- Separate issues for broad refactors, mechanical formatting, or generated
  changes unless the cleanup is tiny and local to the main change.
- Verification that tests are meaningful, not just present.
- Documentation acceptance criteria for changes that affect build, test,
  release, operator behavior, or user/developer interfaces.
- A continuous-improvement closeout note: what became healthier, what remains
  risky, and what follow-up should not block the current change.

Offer in expanded mode:

- Reviewer mentoring prompts that help agents phrase comments kindly and teach
  the engineering principle behind a finding.
- Optional "LGTM with comments" style handling for minor non-blocking items
  when the project coordinator trusts the implementing agent and verification
  gate has passed.
- Suggested decomposition patterns for oversized work: horizontal layer split,
  vertical feature split, prerequisite tests, prerequisite refactor, or
  config/experiment split.
- Optional positive-review notes that call out good design, test coverage,
  simplification, or docs decisions worth repeating.
- Optional time-boxed review-response expectations for projects with many
  parallel agents, modeled on fast response loops without interrupting focused
  implementation work.
- Optional escalation guidance for unresolved technical disagreements:
  consensus attempt, evidence recap, maintainer/coordinator decision, then
  recorded outcome in the issue or companion docs.

Do not require for every expanded-mode project:

- A Google-specific style guide when the repository already has its own style
  authority.
- Large review ceremony for documentation-only or low-risk planning changes.
- Perfect-code signoff or exhaustive polish before useful, verified,
  code-health-positive work can move forward.
- Separate refactor issues for tiny local cleanups that make the focused change
  easier to understand.

## Risks/Anti-Patterns

- Turning expanded mode into perfectionism. Google's standard favors continuous
  improvement, not blocking indefinitely for non-critical polish.
- Letting "team velocity" become permission to lower standards. Google's speed
  guidance explicitly preserves review standards and code health.
- Accepting opinion-driven review findings. Expanded mode should require facts,
  data, repo rules, source links, or software design principles for blocking
  claims.
- Treating style preferences as blockers when no style authority supports them.
- Spreading inconsistent or unhealthy local patterns without recording a
  cleanup path.
- Combining large refactors, formatting churn, feature work, and behavior
  changes in one issue. This makes review, merge, rollback, and evidence
  gathering harder.
- Counting "tests exist" as verification without reviewing whether the tests
  would fail for broken behavior.
- Allowing review explanations to live only in comments or chat. Important
  rationale should land in code, docs, issue comments, ADRs, or durable handoff
  notes.
- Assigning broad, cross-cutting review to an agent without making its reviewed
  scope explicit.
- Missing mentoring opportunities. Expanded mode can improve future agent work
  by recording why a pattern was good or why a requested change matters.

## Source Links

- [Google Engineering Practices Documentation](https://google.github.io/eng-practices/)
- [The Standard of Code Review](https://google.github.io/eng-practices/review/reviewer/standard.html)
- [What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
- [Speed of Code Reviews](https://google.github.io/eng-practices/review/reviewer/speed.html)
- [How to write code review comments](https://google.github.io/eng-practices/review/reviewer/comments.html)
- [Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)
- [Google Style Guides](https://google.github.io/styleguide/)
