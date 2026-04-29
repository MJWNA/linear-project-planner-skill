# Source Material Checkpoints

Use this reference when a Linear project spans planning, execution, parallel
agents, scope changes, verification, handoff, or closeout. The checkpoint is
not ceremony: read only the sources needed for the next decision, then record
what changed.

## Kickoff

Read:

- original user brief or prompt
- repo instructions such as `AGENTS.md`, `CLAUDE.md`, and relevant local rules
- `SKILL.md` and only the references needed for the requested mode
- current git state and dirty files
- installed runtime parity when the skill or tool itself is the target

Record the source of truth, ledger path, non-scope, and first safe issue.

## Before Planning

Read:

- original brief
- existing Linear project description if updating an existing project
- existing issue list, parent/child relationships, labels, milestones,
  blockers, and status updates
- companion ledger if one already exists
- relevant local docs, templates, references, and production gates
- official docs or Context7 only when current external behavior affects issue
  instructions, acceptance criteria, or verification

Record assumptions, unknowns, and research issues instead of hiding them in
chat.

## Before Issue Creation

Read:

- planned workstreams and dependency order
- project principles / fundamentals surface
- dependency map when expanded mode or heavy parallel work is active
- QA plan or verification matrix
- source links that should compress future-agent context

Create issues only when each issue has owned scope, non-owned scope,
dependencies, acceptance criteria, verification, and future-agent notes scaled
to the project mode.

## Before Implementation

Read:

- active issue body and comments
- parent workstream and guide issues
- companion ledger current state
- relevant source files and current git diff
- docs or Context7/OpenAI sources named by the issue
- dependency and production/sink gates for risky work

Move the issue to `In Progress`, acknowledge the work, and record the worktree
or workspace before changing files.

## Before Parallel Delegation

Read:

- dependency map or current issue graph
- candidate issue bodies and blocker links
- owned write sets, non-owned areas, verification overlap, and shared files
- current branches/worktrees and dirty state
- safe parallelism decisions already recorded in the ledger

Delegate only when ownership and verification are explicit. Coordinator-only
state such as Linear status, ledger state, dependency map, release metadata, and
installed runtime sync stays with the coordinator unless explicitly assigned.

## When Scope Changes

Read:

- original brief and non-scope
- active issue acceptance criteria
- Continuous Issue Discovery log
- related issues, blockers, and parent workstream
- dependency map and QA plan when sequencing or verification changes

Classify the finding as blocker, dependency, defect, research follow-up,
implementation follow-up, decision required, QA / verification gap,
documentation gap, scope expansion, or risk / mitigation. Create, propose, or
log it according to the Continuous Issue Discovery rules.

## Before Verification

Read:

- active issue acceptance criteria
- verification matrix or QA plan
- changed files and current git diff
- test/evaluator outputs
- production and sink/output preservation gates when applicable
- Linear issue state and latest comments

Record exact checks and evidence before marking an issue done.

## Before Handoff

Read:

- companion ledger current state
- active issue body, comments, blockers, and verification evidence
- current git state and worktree path
- dependency map or next-safe issue list
- unresolved discovery log entries

Leave a handoff that names the active issue, current state, changed files,
checks run, blockers, residual risks, and next safest action.

## Before Closeout

Read:

- Linear project description, issue list, issue states, blockers, and comments
- companion ledger and sidecar state
- verification matrix or QA plan
- dependency map and project principles surface
- final test/evaluator outputs
- release/install/runtime parity evidence when relevant

Do not close until Linear, the ledger, verification evidence, and dependency
state agree. If they do not agree, reconcile first and leave the project open.
