# Docs Grounding And Provenance Policy

Project: Linear Project Planner Expanded Mode
Linear issue: MAS-698
Status: synthesis from MAS-696 and MAS-697

## Purpose

Expanded mode should use external docs and local project evidence deliberately:
enough grounding to prevent stale, invented, or vague plans, but not so much
lookup ceremony that every issue becomes slow and noisy.

The policy separates three surfaces:

- Research docs: source-backed analysis and synthesis.
- Runtime instructions: concise skill instructions and references loaded by
  agents.
- Execution state: Linear issues and companion ledgers that track work status.

Research can be detailed. Runtime instructions should stay compact and route to
references only when expanded mode is explicitly requested.

## Inputs

- `docs/research/context7-injection-matrix.md`
- `docs/research/openai-codex-capability-map.md`

## Evidence Types

### Local Repo Evidence

Use for:

- Existing project conventions.
- Existing test commands.
- Current dirty worktree state.
- Local skill contract and installed runtime parity.
- Repo-specific style, templates, scripts, and evaluators.

Local repo evidence is primary for implementation decisions inside this repo.

### Linear Evidence

Use for:

- Issue state.
- Dependency graph.
- Project milestones.
- Agent-ready labels.
- Verification history and comments.

Linear is canonical for work state, but large research and design artifacts
should live in local docs and be linked or named from issues.

### Context7 Evidence

Use Context7 when the work depends on current third-party technical docs,
version-specific API behavior, SDK usage, framework patterns, auth, payments,
database tooling, provider integrations, or user-requested current docs.

Expanded-mode issues should record:

- `context7.required`: `true`, `false`, or `conditional`.
- `context7.library_id` when used.
- `context7.query` or topic searched.
- `context7.local_version_source` when local package versions matter.
- `verification.source`: `context7` when verification depends on the lookup.

Do not require Context7 for pure internal planning, Linear-only graph changes,
repo-only refactors with no external API claim, copywriting, changelog drafting,
or summaries of local artifacts.

### OpenAI/Codex Evidence

Use official OpenAI/Codex docs when expanded mode changes or relies on:

- Skills behavior.
- MCP or hosted tool usage.
- Tool search or deferred tool loading.
- Subagents and parallelism.
- `agents.max_threads`.
- Sandbox or approval behavior.
- Compaction, state handling, reasoning controls, structured outputs, or tool
  descriptions.

OpenAI docs should be checked after the software-delivery and project-management
research has shaped the desired operating model, so capability choices serve
the delivery goal instead of driving it prematurely.

## Local Docs Folder Convention

For an expanded-mode project, create a local docs folder with a stable root.
The root may be inside the target repo or in a sibling project ledger area when
repo pollution or privacy is a concern.

Recommended structure:

```text
docs/expanded-mode/
  README.md
  research/
  decisions/
  dependencies/
  agent-briefs/
  qa/
  handoff/
```

For this skill-development project, `docs/research/` remains the research root
until the runtime expanded-mode reference and templates are implemented.

## Frontmatter And Metadata

Each substantive research, decision, dependency, or QA document should include
a compact metadata block near the top. YAML frontmatter is optional; a plain
Markdown block is acceptable if it is easier for agents to maintain.

Minimum metadata:

- Project name.
- Linear issue ID.
- Status.
- Owner or agent role.
- Created or last-updated date when useful.
- Inputs.
- Verification method.

For external-doc-backed artifacts, add:

- Source policy.
- Source URLs.
- Context7 library IDs or official-doc URLs where applicable.
- Refresh trigger.

## Source Recording Rules

Research docs must include:

- A `Source Scope` or equivalent section.
- A `Source Links` section with exact URLs or Context7 library IDs.
- A clear distinction between confirmed source-backed facts and implications
  inferred for expanded mode.
- Staleness or refresh guidance when the source is likely to change.

Issue descriptions should not paste entire research docs. They should name the
local artifact and include only the decision-relevant summary.

## Staleness Rules

Refresh official docs or Context7 lookups when:

- The user asks for latest/current docs.
- The plan depends on API behavior, SDK syntax, provider configuration, model
  capabilities, sandbox behavior, tool contracts, or package-specific commands.
- The existing source note is older than the project phase and the claim is
  central to implementation or verification.
- A test, evaluator, install check, or release workflow starts failing in a way
  that may reflect changed external behavior.

Existing project docs may be reused without refresh when:

- They describe repo-local decisions already made in this project.
- They are used as historical context rather than current external facts.
- The issue is pure Linear graph maintenance, local documentation synthesis, or
  baseline behavior comparison.

## Runtime Loading Policy

Do not load every research file by default. Expanded mode should:

- Keep `SKILL.md` compact.
- Add a reference map entry for expanded mode.
- Load the expanded-mode reference only after explicit expanded-mode trigger.
- Load specific project docs based on phase: research, dependency mapping,
  implementation, verification, release, or handoff.
- Summarize long docs before passing them to worker agents.

This keeps the baseline skill uncontaminated and keeps expanded mode from
spending context on irrelevant references.

## Provenance In Linear Issues

Each expanded-mode issue that depends on research or docs should include a
small provenance block:

```md
## Evidence

- Local docs: `docs/...`
- External docs: URL or Context7 library ID
- Source freshness: checked YYYY-MM-DD or inherited from synthesis
- Refresh required before implementation: yes/no/conditional
```

Each agent-ready issue should also include:

- Owned scope.
- Non-owned scope.
- Verification gate.
- Human-review gate if needed.

## Verification Requirements

For research and provenance docs:

- File exists and is non-empty.
- Required source links are present.
- The doc separates facts from expanded-mode implications.
- Refresh rules or source policy are present.

For runtime changes based on docs:

- The relevant official docs or Context7 source is named in the issue or local
  artifact.
- Tests/evaluators prove baseline behavior remains intact.
- Install parity is checked before claiming runtime sync.

## Risks And Mitigations

- Risk: source cargo-culting. Mitigation: require implications and enforce vs
  offer sections, not just source summaries.
- Risk: context overload. Mitigation: compact `SKILL.md`, reference map, and
  phase-specific docs loading.
- Risk: stale capability assumptions. Mitigation: refresh OpenAI/Codex and
  Context7 docs before implementation claims that depend on current behavior.
- Risk: Linear-only opacity. Mitigation: store large research and design
  artifacts in local docs, then reference them from Linear issues.
- Risk: baseline contamination. Mitigation: expanded-mode docs are loaded only
  after explicit trigger and runtime edits are tested against baseline
  evaluators.
