# Context7 Injection Matrix For Expanded Mode

Retrieved: 2026-04-29 AEST

Linear issue: MAS-696

## Source Scope

This research used the Context7 MCP flow directly:

1. `resolve-library-id` for `Context7`
2. `query-docs` against the selected Context7-compatible library ID

Selected Context7 source:

- Library ID: `/websites/context7`
- Title: Context7
- Source reputation: High
- Code snippets: 564
- Benchmark score: 72.95

Context7 returned lower-ranked alternate libraries, but `/websites/context7`
was the highest-reputation and most relevant source for Context7's own docs.
The docs queried were:

- `https://context7.com/docs/overview`
- `https://context7.com/docs`
- `https://context7.com/docs/installation`
- `https://context7.com/docs/api-guide`
- `https://context7.com/docs/api-reference/context/get-documentation-context`
- `https://context7.com/docs/agentic-tools/ai-sdk/tools/query-docs`
- `https://context7.com/docs/clients/cli`

## Confirmed Context7 Value

Context7's core value for expanded mode is prompt grounding. Its docs describe
Context7 MCP as bringing up-to-date, version-specific documentation and code
examples into an AI coding assistant's prompt so generated guidance is less
likely to rely on stale training data or invented APIs.

Confirmed capabilities relevant to the skill:

- Resolve a human library name into an exact Context7-compatible library ID.
- Query documentation by exact library ID plus a task-specific natural language
  question.
- Use version-specific IDs such as `/vercel/next.js/v15.1.8`,
  `/vercel/next.js@v15.1.8`, or CLI-style version paths.
- Retrieve documentation snippets and code snippets that are reranked for the
  specific question.
- Return source metadata such as source page IDs, code IDs, page titles,
  snippets, token counts, and source reputation during resolution.
- Support faster but less precise retrieval, and deeper research mode in API
  surfaces where enabled.

For expanded mode, this means Context7 should not be treated as a generic
search step. It should be an injection gate for decisions where current
framework, SDK, API, or deployment behavior materially affects the correctness
of generated Linear issues, acceptance criteria, or verification gates.

## Injection Matrix

| Expanded-mode moment | Context7 rule | Inject into issue? | Required issue metadata | Why |
|---|---|---:|---|---|
| Project contains framework, SDK, API, CLI, deployment, auth, database, or testing-library work with version-sensitive behavior | Must use | Yes | `context7.required: true`, `context7.library_id`, `context7.query`, `context7.checked_at`, `context7.source_urls` | Prevents stale or hallucinated technical steps becoming agent-ready instructions. |
| Issue acceptance criteria specify exact code shape, migration syntax, config keys, route semantics, middleware behavior, webhook payloads, or SDK calls | Must use | Yes | `context7.required: true`, `context7.library_id`, `context7.query`, `context7.version_or_package`, `context7.source_urls` | Exact implementation details are the highest-risk place for outdated API memory. |
| Verification commands depend on current tool behavior, generated config, CI actions, package manager changes, or deployment provider semantics | Must use | Yes | `context7.required: true`, `context7.library_id`, `context7.query`, `verification.source: context7` | Keeps verification gates aligned with current docs rather than guessed commands. |
| Linear issue is research-only and its purpose is to compare current implementation options | Must use when comparing libraries or APIs; otherwise should use | Usually yes | `context7.required`, `context7.candidates`, selected `context7.library_id`, source URLs | Captures which official docs shaped the decision. |
| Work touches an existing repo pattern but the package version is unknown | Should use after local package/version discovery | Yes if lookup affects instructions | `context7.required: conditional`, `context7.local_version_source`, `context7.library_id`, `context7.query` | Local source remains primary, but Context7 should validate version-specific external behavior. |
| Work is planning, sequencing, dependency graphing, labels, milestones, ledger structure, or Linear state hygiene only | Offer, do not require | No by default | `context7.required: false`, optional `context7.reason_not_required` | These are skill/process concerns, not external docs correctness risks. |
| Issue only asks an agent to inspect local code and report findings without changing behavior | Offer, do not require unless the audit asks about external API correctness | No by default | `context7.required: false`, optional `context7.trigger_if` | Local evidence should not be displaced by external docs. |
| User explicitly asks for current docs, latest behavior, official examples, or Context7 | Must use | Yes | `context7.required: true`, `context7.requested_by_user: true`, `context7.library_id`, `context7.query` | The user's instruction is itself a lookup requirement. |
| User explicitly forbids web/docs lookup or asks for offline/local-only work | Do not require | No | `context7.required: false`, `context7.reason_not_required: user_requested_local_only` | Respect the requested evidence boundary unless safety or policy requires escalation. |
| Work is copywriting, internal comms, release notes, changelog drafting, or issue summarization with no technical API claims | Do not require | No | `context7.required: false`, `context7.reason_not_required: non_technical_or_local_summary` | Context7 would add cost without improving correctness. |
| Emergency unblock where Context7 MCP is unavailable | Do not block the whole plan, but mark risk | Yes if the issue still depends on external docs | `context7.required: true`, `context7.status: unavailable`, `context7.fallback`, `context7.follow_up` | Preserves the requirement and makes the missing evidence visible. |

## Required Metadata In Issues

Expanded mode should add a compact docs block to any issue where Context7 is
required or materially used:

```yaml
docs_lookup:
  context7:
    required: true
    library_id: "/owner/project[/version]"
    local_version_source: "package.json|lockfile|pyproject.toml|Gemfile.lock|not-found"
    query: "Task-specific docs question"
    checked_at: "YYYY-MM-DD"
    source_urls:
      - "https://..."
    notes: "One-line summary of the docs constraint that affects implementation"
```

For issues where Context7 is not required, include only a one-line reason when
the absence could be questioned:

```yaml
docs_lookup:
  context7:
    required: false
    reason_not_required: "Local planning issue; no external library/API behavior."
```

## What To Require vs Offer

### Must Use

Require Context7 before an issue is marked `agent-ready` when any of these are
true:

- The issue instructs an agent to implement or verify behavior using an external
  framework, SDK, API, CLI, package, deployment provider, database, auth system,
  queue, webhook, testing framework, or CI action.
- The project plan includes version-specific examples or code snippets.
- The acceptance criteria depend on exact API names, config keys, lifecycle
  hooks, file conventions, routing behavior, migration syntax, or command-line
  flags.
- The user asks for current docs, latest docs, official docs, version-specific
  examples, hallucination reduction, or Context7 specifically.
- The agent is creating a reusable template or reference that future agents may
  copy into implementation work.

### Should Use

Offer or prefer Context7 when:

- The issue is mostly local but has one external library assumption that could
  drift.
- The local repo has a package version but the planned instruction is high-risk
  or unfamiliar.
- The plan is a research issue comparing possible tools, and Context7 can
  ground the current docs for the candidates.
- The issue creates verification gates for a stack where the commands may have
  changed.

### Do Not Require

Do not require Context7 when:

- The work is purely Linear structure, issue hygiene, labels, milestones,
  dependency ordering, companion-ledger updates, or project coordination.
- The work is a local code audit that asks for observed repo behavior only.
- The user explicitly sets a local-only, offline, no-docs, or no-network
  boundary.
- The issue is copy, meeting notes, changelog summarization, or internal
  communication with no technical API assertions.
- The issue only asks for file movement, formatting, or metadata updates where
  external docs cannot affect correctness.

## Risks/Anti-Patterns

- Requiring Context7 on every issue can turn expanded mode into busywork and
  bury the actual dependency graph under low-value lookup metadata.
- Treating Context7 as a replacement for local version discovery is unsafe.
  The agent should inspect local manifests first, then query the matching
  version when available.
- Injecting raw long snippets into Linear issues can overload future agents.
  Expanded mode should store the library ID, query, source URLs, and one-line
  implementation constraint instead.
- Using a generic query such as `auth` or `routing` weakens the value of
  reranking. Queries should name the exact task, framework surface, and desired
  decision.
- Using an unversioned library ID when the repo pins a version can create
  subtle drift. Prefer version-specific IDs when Context7 exposes them or when
  the API docs show a version path convention.
- Blocking all planning when Context7 is unavailable is too brittle. Mark the
  lookup as required but unavailable, record the fallback source, and keep the
  issue out of final `agent-ready` state until the docs check is satisfied.
- Copying code examples without source context can still produce mismatches.
  The issue should say what constraint was learned, not blindly paste snippets.

## Source Links

- Context7 docs overview: `https://context7.com/docs/overview`
- Context7 docs home: `https://context7.com/docs`
- Context7 MCP installation tools: `https://context7.com/docs/installation`
- Context7 API guide: `https://context7.com/docs/api-guide`
- Documentation context API reference:
  `https://context7.com/docs/api-reference/context/get-documentation-context`
- AI SDK `queryDocs` tool:
  `https://context7.com/docs/agentic-tools/ai-sdk/tools/query-docs`
- Context7 CLI version-specific docs:
  `https://context7.com/docs/clients/cli`
