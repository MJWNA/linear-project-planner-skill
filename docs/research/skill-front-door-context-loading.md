# Skill Front Door, Triggering, And Context Loading Research

Retrieved: 2026-04-28 AEST

## Question

How should `linear-project-planner` shrink `SKILL.md` without weakening skill
activation, routing, or future-agent execution behavior?

## Summary

The right implementation term is not just one phrase.

- For Claude Skills, **progressive disclosure** is the official Anthropic term
  for keeping the entrypoint small and loading supporting files only when
  needed.
- For OpenAI Apps/tools and Microsoft Semantic Kernel, the closest concepts are
  **metadata-driven discovery**, **tool selection**, and concise semantic
  descriptions.
- For Google ADK, the same pressure appears as clear agent instructions,
  meaningful tool/function names, focused tool definitions, and debuggable
  sessions.

For this repo, use the phrase **trigger-safe progressive disclosure**: keep
router-visible activation language in the `SKILL.md` frontmatter and first
operating section, then move deep operating contracts into referenced files.

## Source-Backed Guidance

### OpenAI

OpenAI Apps SDK planning docs say discovery is driven almost entirely by
metadata, and recommend action-oriented names plus descriptions that start with
`Use this when...` so the model knows when to pick a tool.

Source: https://developers.openai.com/apps-sdk/plan/tools#capture-metadata-for-discovery

OpenAI ChatGPT developer-mode docs recommend explicit tool/app requests,
disambiguating similar tools, saying what not to use, specifying sequencing, and
improving tool descriptions with `Use this when...`, edge cases, and parameter
descriptions.

Source: https://developers.openai.com/api/docs/guides/developer-mode#how-to-use

Implication for this skill: preserve explicit activation phrases in metadata
and first-section text, and include negative boundaries so the Linear planner
does not over-trigger for ordinary Linear issue lookups.

### Anthropic / Claude

Claude Code Skills docs say every skill needs `SKILL.md`, with YAML frontmatter
that tells Claude when to use the skill and markdown instructions followed when
the skill is invoked. The `description` helps Claude decide when to load the
skill automatically.

Source: https://code.claude.com/docs/en/skills

The same docs recommend supporting files for templates, examples, scripts, or
detailed reference documentation, and say to reference those files from
`SKILL.md` so Claude knows what each file contains and when to load it. They
also explicitly advise keeping `SKILL.md` under 500 lines and moving detailed
reference material to separate files.

Source: https://code.claude.com/docs/en/skills

Anthropic's Claude API skill page states that the skill uses progressive
disclosure to keep context efficient by loading documentation relevant to the
language, surface, and task rather than everything at once. It also documents
activation rules and non-activation boundaries.

Source: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/claude-api-skill

Implication for this skill: `SKILL.md` should be an overview/navigation file
with strong activation text and a reference map. Long policy sections should
move into references, but only if the map says when to load them.

### Google ADK

Google ADK positions agents as workers that use instructions and tools to
achieve goals, with sessions, state, memory, artifacts, debugging, evaluation,
and deployment as first-class concepts.

Source: https://google.github.io/adk-docs/get-started/about/

ADK custom-tool guidance says the LLM relies heavily on function names,
parameters, type hints, and docstrings/source comments, and recommends
descriptive verb-noun names while avoiding generic names.

Source: https://google.github.io/adk-docs/tools-custom/

ADK also recommends meaningful function and parameter names, fewer parameters,
and simple data types for tool usability.

Source: https://google.github.io/adk-docs/tools-custom/function-tools/

Implication for this skill: concise routing language, simple command surfaces,
and focused references are more important than packing every edge case into the
front door.

### Microsoft Semantic Kernel

Semantic Kernel plugin docs say LLMs use semantic descriptions to choose the
best functions for a user's ask. They recommend descriptive, concise function
names and warn that ambiguous names should be renamed for clarity.

Source: https://learn.microsoft.com/en-us/semantic-kernel/concepts/plugins/

The same page notes that large tool sets reduce model selection quality and
that definitions consume token budget, so concise descriptions and
single-responsibility functions matter.

Source: https://learn.microsoft.com/en-us/semantic-kernel/concepts/plugins/

Implication for this skill: shrink duplication, keep concepts distinct, and
avoid broad wording that makes one skill compete with unrelated Linear tools.

## Trigger Contract For This Repo

Keep these concepts in `SKILL.md` frontmatter and first operating section:

- Linear project planning, creation, restructuring, and execution
- audits, remediation, production hardening, and parallel agent work
- milestones, parent workstreams, child issues, labels, dependencies, blockers
- companion ledger and cross-session execution memory
- verification gates, Linear read-back, completion comments, and finalization
- Codex and Claude agents
- explicit phrases like `create a Linear project`, `run the Linear skill`, and
  `execute a Linear plan`

Also keep negative boundaries:

- do not trigger for simple one-off Linear issue lookups unless the user asks
  for planning, project execution, remediation, or coordination
- do not do substantial online research before creating a requested Linear plan;
  make research a tracked issue

## What Can Move Out Of SKILL.md

Move these into references when linked from the Reference Map:

- standard milestones and labels
- full child issue templates
- long sparse-link graph rules
- deep auto-research loop details
- production and sink gate examples
- parallel worktree examples
- `linear-agent` command details
- repository hardening, release, and CI policy
- portability notes for non-Codex runtimes

## Implementation Recommendation

Use a slim `SKILL.md` as the trigger-safe front door:

1. Frontmatter describes when to use the skill in direct language.
2. The first paragraph repeats the main activation scope and negative boundary.
3. Quick Path carries the shortest safe behavior.
4. Reference Map names all deeper files and when to load them.
5. A trigger/readiness evaluator fails if required activation concepts or
   reference links disappear.

This keeps the skill discoverable while reducing context cost.
