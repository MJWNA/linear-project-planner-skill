# OpenAI Codex Capability Map For Expanded Mode

Linear issue: MAS-697
Project: Linear Project Planner Expanded Mode
Captured: 2026-04-29
Repository: `/Users/ronniemeagher/Desktop/Curssor/mta-pt-workspace/projects/linear-project-planner-skill`
Source policy: official OpenAI developer, API, Codex, and Help Center sources only.

## Source Scope

This research maps OpenAI-documented capabilities that matter for a robust
expanded mode in `linear-project-planner`. It intentionally prioritizes
official OpenAI sources:

- OpenAI API docs for GPT-5.5, Responses API, reasoning, structured outputs,
  function calling, tool search, skills, prompt caching, conversation state,
  compaction, and Sandbox Agents.
- OpenAI Codex docs for `config.toml`, `agents.max_threads`, local sandboxing,
  MCP, subagents, skills, and the CLI/app operating model.
- OpenAI Help Center only where product-level Codex app/cloud behavior is
  documented more directly than the API pages.

This file does not verify non-OpenAI claims, third-party agent frameworks, or
implementation details inside this repository. It is a capability requirements
map, not an implementation plan.

## Confirmed Capabilities

### GPT-5.5 And Responses API

OpenAI's GPT-5.5 migration guidance says to use the Responses API for
reasoning, tool-calling, and multi-turn use cases. It also says expanded
coding-agent workflows should be explicit about reuse, subagent delegation,
test expectations, acceptance criteria, and when to continue versus ask for
help.

Implication for expanded mode: require a Responses-first orchestration model in
the design contract. Expanded mode should not be framed as a longer prompt
alone; it needs explicit state handling, tool replay, acceptance criteria, and
verification gates.

OpenAI documents `reasoning.effort` values for GPT-5.5 as `low`, `medium`,
`high`, and `xhigh`, with `medium` as the default. The docs warn that higher
effort is not automatically better and can regress quality when instructions,
stopping criteria, or tool access are weak.

Implication for expanded mode: require clear stopping rules and measurable
success criteria before recommending high or xhigh reasoning. Offer higher
reasoning effort for hard asynchronous planning or eval work, but do not make
it mandatory for ordinary Linear graph maintenance.

### State, Compaction, And Continuity

The Responses API supports multi-turn state through `previous_response_id`,
Conversations, or manual replay of response output items. The migration guide
also documents `store: true` for preserving reasoning and tool context across
turns, while conversation-state docs explain that `store: false` disables
default response storage.

Implication for expanded mode: require a durable state continuity strategy that
survives context growth and agent handoffs. For this repo, the companion ledger
and Linear comments remain the human-readable source of continuity; API state is
an execution optimization, not a replacement for durable project state.

OpenAI's compaction guide says server-side compaction can be enabled with
`context_management` and `compact_threshold`, and that the returned compaction
item carries forward prior state and reasoning in fewer tokens. It also
documents a standalone `/responses/compact` endpoint for explicit stateless
control.

Implication for expanded mode: require compaction-aware handoff behavior. The
mode should preserve current issue, owned write scope, blockers, verification
state, and next action in durable artifacts before relying on opaque compaction
items.

### Tools, Structured Outputs, And Tool Descriptions

OpenAI documents Structured Outputs as JSON-schema-constrained generation that
prevents missing required keys and invalid enum hallucinations. GPT-5.5
guidance recommends removing schema definitions from prompts where possible and
using Structured Outputs instead.

Implication for expanded mode: require structured outputs for machine-consumed
plans, issue graphs, dependency maps, verification matrices, handoff summaries,
and evaluator results. Markdown remains useful for human review, but generated
state should have a schema when downstream tooling depends on it.

OpenAI function-calling guidance says function names, parameter descriptions,
instructions, outputs, examples, and edge cases should be clear. It recommends
keeping initially available functions small, aiming for fewer than 20 functions
at the start of a turn, and using tool search for large or infrequently used
tool surfaces.

Implication for expanded mode: require explicit tool descriptions for every
future command or MCP action. Tool descriptions should say what the tool does,
when to use it, required inputs, output shape, side effects, retry safety, and
common error modes. Do not bury tool-use rules only in prose prompts.

GPT-5.5 guidance also says tool-heavy or long-running workflows must handle
`phase`, preambles, and assistant-item replay correctly.

Implication for expanded mode: require orchestration that can store and replay
assistant tool-call items and tool outputs. Offer user-facing preambles for
observability, but treat them as operational status, not as durable state.

### Hosted Tools, Tool Search, Skills, And MCP

OpenAI's GPT-5.5 docs recommend hosted tools where they fit, including web
search, file search, code interpreter, image generation, and computer use. The
Responses API migration docs also list remote MCPs among the built-in agentic
tooling surfaces.

Implication for expanded mode: offer hosted tools for research and validation
where the runtime supports them, but require local fallback behavior because
Codex sessions and installed skills may expose different tools.

OpenAI tool-search docs say `tool_search` lets the model load deferred tools at
runtime instead of injecting every tool definition up front. Hosted tool search
is best when the full candidate inventory is known at request time; client
executed tool search is better when discovery depends on project, tenant, or
application state. The docs recommend grouping deferred tools into namespaces
or MCP servers with clear high-level descriptions.

Implication for expanded mode: require tool-search-ready organization for large
future tool catalogs. Keep the front door small, group actions by namespace,
and defer specialized tools until the active workstream needs them.

OpenAI Skills docs define a skill as a versioned bundle of files plus a
`SKILL.md` manifest. When skills are available, the platform adds the skill
name, description, and path to prompt context, and the model chooses whether to
load the full `SKILL.md` from that metadata.

Implication for expanded mode: preserve concise, router-visible skill metadata.
Expanded mode should be discoverable through the skill description and reference
map, but deep operating detail should live in referenced docs rather than
ballooning the front door.

OpenAI Codex MCP docs say MCP connects models to third-party tools and context,
supports Codex CLI and IDE extension, and can be configured through
`config.toml` at user or trusted-project scope.

Implication for expanded mode: treat MCP as an optional capability layer for
Linear, docs, browser, or repository tools. Require clear fallback instructions
when MCP tools are missing, disabled, or approval-gated.

### Codex Config, Subagents, And Sandboxes

OpenAI Codex config reference documents `agents.max_threads` as the maximum
number of concurrently open agent threads, defaulting to `6` when unset. It
also documents `agents.max_depth`, default per-worker runtime, agent role
config files, descriptions, and nickname candidates.

Implication for expanded mode: require safe parallelism controls separate from
usage quota. `agents.max_threads` should be treated as a concurrency cap, not a
permission to spawn unbounded agents or a way to increase plan limits.

OpenAI Codex subagent docs say Codex can spawn specialized agents in parallel
and collect results in one response, especially for codebase exploration or
multi-step feature plans. They also support custom agents with different model
configs and instructions.

Implication for expanded mode: offer parallel read-only research and bounded
write-capable workstreams, but require explicit ownership, dependencies, write
scope, worktree/branch, and verification overlap before spawning agents.

OpenAI Codex sandbox docs say the sandbox is the boundary that lets Codex act
autonomously without unrestricted machine access. Spawned commands inherit the
same sandbox boundaries, and `workspace-write` permits reading, workspace
editing, and routine local commands inside that boundary.

Implication for expanded mode: require every parallel agent to know its sandbox
and write scope. Never infer that sandbox permission is equivalent to project
ownership.

OpenAI Sandbox Agents docs say a `SandboxAgent` is appropriate when the answer
depends on work done in a sandbox workspace. Default capabilities include
filesystem, shell, and compaction; custom capability lists replace the default
list, so defaults must be included explicitly when still needed.

Implication for expanded mode: offer Sandbox Agent patterns for long-running
workspace-heavy expanded mode, but require capability manifests that include
filesystem, shell, and compaction when those are expected.

## Capability Map For Expanded Mode

| Expanded-mode need | OpenAI capability | Requirement implication |
|---|---|---|
| Long-horizon project state | Responses `previous_response_id`, Conversations, compaction, durable ledger | Require explicit state strategy and durable human-readable recovery state. |
| Large context and parallel research | Compaction, prompt caching, subagents | Require static-first prompts, compaction checkpoints, and issue-scoped handoffs. |
| Multi-agent execution | Codex subagents, `agents.max_threads`, sandboxing | Require concurrency budget, write ownership, and verification gates before parallel spawning. |
| Tool-heavy workflows | Function calling, hosted tools, MCP, tool search | Require clear tool descriptions, namespaces, deferred loading, and fallback paths. |
| Machine-readable plans | Structured Outputs | Require schemas for issue graph, dependencies, milestones, verification matrix, and handoff state. |
| Runtime portability | Skills, MCP config, hosted tools, Sandbox Agents | Offer richer integrations, but keep normal-mode fallback as Markdown plus printed actions. |
| Cost and latency control | Prompt caching, tool search, `text.verbosity`, reasoning effort | Require static instructions first, defer large tools, and tune effort by validation need. |
| Compaction recovery | Server-side and standalone compaction | Require durable summaries before and after compaction-sensitive transitions. |

## What To Require vs Offer

### Require

- Responses-first design for expanded mode reasoning, tool calling, multi-turn
  state, and assistant-item replay.
- Explicit `reasoning.effort` policy: default to lower or medium effort unless
  hard asynchronous planning, ambiguity, or eval evidence justifies high/xhigh.
- Structured Outputs for any generated artifact consumed by scripts,
  evaluators, MCP actions, or future agents.
- Tool descriptions that include purpose, use conditions, inputs, output,
  side effects, retry safety, and common failure modes.
- Compaction-aware durable state: current issue, next action, blockers,
  ownership, verification state, and source links must survive outside the
  model context.
- Safe parallelism policy that treats `agents.max_threads` as a cap and still
  requires issue ownership, write scope, branch/worktree, dependency checks,
  and verification overlap checks.
- Skill metadata and front-door text that remain concise and trigger-safe.
- MCP and hosted-tool fallback paths when tools are absent, disabled,
  approval-gated, or not available in a given Codex surface.

### Offer

- Hosted tool search for known tool inventories, and client-executed tool
  search when discovery depends on repo or workspace state.
- Sandbox Agent orchestration for workspace-heavy planning or validation runs.
- Higher reasoning effort for the hardest async planning and eval tasks.
- Prompt-cache retention controls for repeated large-prefix expanded-mode
  prompts.
- Custom Codex subagent roles for research, implementation, verification, and
  read-back when their write scopes do not overlap.
- MCP-backed Linear, browser, docs, or repository workflows where configured.

## Risks/Anti-Patterns

- Treating expanded mode as "more prompt" rather than orchestration. OpenAI
  guidance points toward Responses state, tools, schemas, compaction, and
  replay.
- Raising `reasoning.effort` without fixing weak success criteria, vague tool
  access, or missing stopping rules.
- Mistaking `agents.max_threads` for available quota or safe parallelism. It is
  only a concurrency cap.
- Loading every tool definition at the start of a turn. OpenAI recommends
  smaller initial tool surfaces and tool search for large/infrequent tools.
- Putting tool-use policy only in instructions instead of tool descriptions.
- Relying on opaque compaction items as the only state record. Durable project
  state must remain in Linear comments, ledgers, and checked-in docs where
  appropriate.
- Letting Skills/MCP become mandatory for normal mode. Expanded mode can offer
  richer tool surfaces, but the skill should still degrade to Markdown plans
  and printed/manual actions.
- Using sandbox permission as a substitute for explicit write ownership.
- Creating schemas in prompt prose instead of Structured Outputs where
  downstream tooling needs validity.

## Source Links

- OpenAI GPT-5.5 guide:
  https://developers.openai.com/api/docs/guides/latest-model
- OpenAI Responses API migration guide:
  https://developers.openai.com/api/docs/guides/migrate-to-responses
- OpenAI conversation state guide:
  https://developers.openai.com/api/docs/guides/conversation-state
- OpenAI compaction guide:
  https://developers.openai.com/api/docs/guides/compaction
- OpenAI prompt caching guide:
  https://developers.openai.com/api/docs/guides/prompt-caching
- OpenAI Structured Outputs guide:
  https://developers.openai.com/api/docs/guides/structured-outputs
- OpenAI function calling guide:
  https://developers.openai.com/api/docs/guides/function-calling
- OpenAI tool search guide:
  https://developers.openai.com/api/docs/guides/tools-tool-search
- OpenAI Skills guide:
  https://developers.openai.com/api/docs/guides/tools-skills
- OpenAI Sandbox Agents guide:
  https://developers.openai.com/api/docs/guides/agents/sandboxes
- OpenAI Codex config reference:
  https://developers.openai.com/codex/config-reference
- OpenAI Codex subagents guide:
  https://developers.openai.com/codex/subagents
- OpenAI Codex sandboxing guide:
  https://developers.openai.com/codex/concepts/sandboxing
- OpenAI Codex MCP guide:
  https://developers.openai.com/codex/mcp
- OpenAI Help Center Codex overview:
  https://help.openai.com/en/articles/11369540
