# Expanded Mode Docs Folder And Template Spec

Project: Linear Project Planner Expanded Mode
Linear issue: MAS-700
Status: proposed runtime docs convention and template inventory

## Purpose

Expanded mode should create a local documentation workspace when a Linear
project needs durable research, decisions, dependency mapping, agent briefs,
QA evidence, or handoff context that is too large for issue bodies.

The docs folder is a context-compression surface. Linear remains canonical for
work state, dependencies, issue ownership, and completion status. The companion
ledger remains canonical for execution continuity across agents and context
compaction.

## Folder Layout

Use a stable root named after the Linear project or expanded-mode workstream:

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

For repositories where a project-specific nested root would be noisy, a shared
root is acceptable:

```text
docs/expanded-mode/
  README.md
  research/
  decisions/
  dependencies/
  qa/
  agent-briefs/
  handoff/
```

For early research before runtime implementation exists, `docs/research/` may
remain the temporary root. Once expanded mode becomes a runtime feature, new
expanded-mode projects should prefer `docs/expanded-mode/<project-slug>/`.

### `README.md`

Useful when:

- The project spans multiple Linear milestones or agent handoffs.
- Future agents need a single index of active docs, issue links, and current
  phase.
- The folder contains more than two substantive artifacts.

Too ceremonial when:

- The folder contains one short dossier or one decision note that is already
  linked directly from a Linear issue.

Minimum contents:

- Project name and Linear project or guide issue.
- Docs root purpose.
- Current phase.
- Index of local artifacts.
- Pointer to the companion ledger when one exists.

### `research/`

Useful when:

- The work depends on external practice, current technical docs, competitive
  research, source-backed synthesis, or repo discovery.
- Multiple research agents need disjoint write scopes.

Too ceremonial when:

- The task only summarizes local files already named in the issue.
- The implementation can be verified from existing tests and repo conventions
  without external or strategic research.

### `decisions/`

Useful when:

- The project has a tradeoff that future agents may otherwise relitigate.
- A decision changes sequencing, scope, architecture, verification, or release
  behavior.
- Human review is required before implementation or release.

Too ceremonial when:

- The decision is a minor naming choice or follows an obvious existing repo
  pattern.

### `dependencies/`

Useful when:

- Several workstreams can run in parallel only after blockers are explicit.
- Shared files, shared verification, risky integrations, or external systems
  determine sequencing.
- The Linear issue graph needs a readable companion map.

Too ceremonial when:

- The project has one or two serial issues and no ambiguous ownership boundary.

### `qa/`

Useful when:

- Verification is a workstream, not a final command.
- The project needs baseline protection, dogfood results, release gates,
  browser checks, migration checks, sink/output preservation, or human review.

Too ceremonial when:

- One targeted local check fully proves the change and the issue body already
  records it.

### `agent-briefs/`

Useful when:

- Parallel agents need issue-scoped ownership, non-owned scope, inputs,
  expected outputs, and verification gates.
- The coordinator wants context isolation without giving every worker the whole
  project history.

Too ceremonial when:

- A single agent is doing a small, local edit with all constraints already in
  the Linear issue.

### `handoff/`

Useful when:

- Work will pause across sessions or context compaction.
- A coordinator must reconcile multiple agent outputs.
- Release, install, or Linear closeout is not complete.

Too ceremonial when:

- The issue can be closed in the same turn and the completion comment plus
  ledger state are enough.

## Template Inventory

Expanded mode should ship templates that can be copied into the local docs root
only when the project needs them. Templates should be concise, frontmatter-like
metadata first, and optimized for future agents.

### Research Dossier Template

Path:

```text
templates/expanded-mode/research-dossier.md
```

Required fields:

- Project
- Linear issue
- Owner or agent role
- Status
- Created or updated date
- Research question
- Source scope
- Source links or Context7 library IDs
- Confirmed findings
- Inferences for this project
- Staleness or refresh trigger
- Recommended next action
- Verification method

Acceptance criteria:

- Separates source-backed facts from project implications.
- Records exact URLs, official-doc source names, or Context7 library IDs.
- States whether refresh is required before implementation.

### ADR / Decision Template

Path:

```text
templates/expanded-mode/decision.md
```

Required fields:

- Project
- Linear issue
- Status: proposed, accepted, superseded, or rejected
- Decision owner
- Context
- Decision
- Options considered
- Consequences
- Baseline behavior impact
- Human review requirement
- Related docs and issues
- Verification or rollback signal

Acceptance criteria:

- Names the chosen decision and rejected alternatives.
- Explains baseline impact as none, additive, gated, or risky.
- Links the issue or artifact that proves review or verification.

### Dependency Map Template

Path:

```text
templates/expanded-mode/dependency-map.md
```

Required fields:

- Project
- Linear project or guide issue
- Status
- Workstreams
- Serial gates
- Parallel-safe batches
- Blockers and dependencies
- Shared files or systems
- Risky interfaces
- Verification overlap
- Linear relationship checklist
- Coordinator notes

Acceptance criteria:

- Identifies at least one first-safe task or explains why none exists.
- Distinguishes formal Linear dependencies from local explanatory notes.
- Marks work as `parallel-safe`, `serial-required`, or `needs-human-review`
  only when the reasoning is documented.

### QA Plan Template

Path:

```text
templates/expanded-mode/qa-plan.md
```

Required fields:

- Project
- Linear issue or verification guide
- Status
- Validation mode
- Baseline checks
- Implementation checks
- Source/provenance checks
- Dogfood or scenario checks
- Human review gate
- Release/install checks when relevant
- Residual risks
- Evidence links

Acceptance criteria:

- Lists exact commands, review methods, or manual checks.
- Records not-applicable gates with a reason.
- Keeps verification evidence linkable from Linear completion comments.

### Agent Brief Template

Path:

```text
templates/expanded-mode/agent-brief.md
```

Required fields:

- Project
- Linear issue
- Agent role
- Owned write scope
- Non-owned scope
- Inputs
- Expected output
- Dependencies
- Allowed tools or docs lookups
- Forbidden actions
- Verification gate
- Handoff requirement

Acceptance criteria:

- Gives one agent one clear job.
- Prevents worker agents from updating shared Linear, ledger, release, or
  runtime state unless explicitly assigned.
- Includes the exact path or artifact the worker should produce.

### Handoff Template

Path:

```text
templates/expanded-mode/handoff.md
```

Required fields:

- Project
- Current issue
- Current phase
- Completed work
- Changed files or docs
- Verification run
- Open blockers
- Next safest action
- Linear state to reconcile
- Ledger state to reconcile
- Risks and follow-ups

Acceptance criteria:

- Can be read after context compaction without needing chat history.
- Identifies what not to touch if other agents are still active.
- Separates verified facts from pending assumptions.

## Issue Linking

Expanded-mode docs should be linked from Linear only when the link changes how
future work is performed, verified, or recovered.

Required issue links:

- Guide issues should link the docs root `README.md`, dependency map, QA plan,
  and companion ledger when present.
- Research issues should link their research dossier and any synthesis doc that
  consumes it.
- Implementation issues should link only the decision, dependency, agent brief,
  or QA artifact needed to execute that issue.
- Completion comments should link the final evidence artifact when verification
  is too detailed for a short comment.

Do not paste full docs into issue descriptions. Use a short summary plus the
local path. Prefer 3-7 high-signal links per normal issue.

Each doc should link back to its owning issue with a plain `Linear issue:` field
near the top. When a doc supports multiple issues, list the guide issue first
and add a short `Related issues` section.

## Provenance

Every substantive expanded-mode doc should include enough provenance for a
future agent to know why it exists and whether it is still safe to use.

Minimum provenance fields:

- Project
- Linear issue
- Status
- Owner or agent role when useful
- Inputs
- Source scope
- Verification method

External-source-backed docs must also include:

- Source links, official-doc names, or Context7 library IDs.
- Checked date when the claim may drift.
- Refresh trigger.
- A distinction between confirmed facts and project-specific implications.

Context7 is required when a template or issue gives future agents
version-sensitive implementation, SDK, API, CLI, deployment, auth, database,
testing, or CI instructions. It is not required for pure Linear graph hygiene,
local-only summaries, or copy/status docs with no external technical claim.

OpenAI/Codex official docs are required when a doc makes current claims about
skills, subagents, tool search, hosted tools, MCP, sandboxing, compaction,
structured outputs, reasoning controls, or Codex configuration.

## Avoiding Ceremony

Expanded mode should scale down when the work is small.

Use the full folder set when:

- The project has multiple phases or milestones.
- Research, dependency mapping, QA, and handoff are all real workstreams.
- More than one agent will write artifacts.
- Verification is multi-step or release-sensitive.

Use a reduced folder set when:

- The project needs research plus one implementation pass. Use `research/` and
  `qa/`, then link directly from the guide issue.
- The project needs only a decision and verification plan. Use `decisions/` and
  `qa/`.
- The project is mostly coordination. Use `README.md` and a dependency map.

Avoid creating a folder or template when:

- The content would duplicate the Linear issue body.
- The artifact has no owner, reader, or verification consequence.
- The project can finish in one session with one changed file and one targeted
  check.
- A companion ledger already captures transient execution state well enough.

When unsure, start with the smallest doc that preserves future-agent recovery:
usually a `README.md`, one research or decision doc, and a QA note.

## Verification

Future implementation of this spec should verify:

- The runtime docs root convention is documented in expanded-mode references.
- Template files exist for research dossier, ADR/decision, dependency map,
  QA plan, agent brief, and handoff.
- Each template contains project, Linear issue, status, provenance, and
  verification fields.
- Expanded-mode issues can link local docs without pasting full documents into
  issue bodies.
- Provenance guidance distinguishes local evidence, Linear evidence,
  Context7 evidence, and OpenAI/Codex official-doc evidence.
- Anti-ceremony guidance is present so baseline mode and small projects are not
  forced into the full expanded-mode folder tree.
- Existing baseline evaluators still pass after any runtime implementation that
  uses these docs or templates.

Targeted documentation checks:

```bash
test -s docs/research/expanded-mode-docs-folder-template-spec.md
rg -n "## Folder Layout|## Template Inventory|## Issue Linking|## Provenance|## Avoiding Ceremony|## Verification" docs/research/expanded-mode-docs-folder-template-spec.md
```
