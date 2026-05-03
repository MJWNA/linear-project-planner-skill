# Frontier AI Delivery Patterns Research

Date: 2026-04-29

## Source Scope

This research prioritizes current primary or high-credibility engineering sources:

- OpenAI Codex and Agents documentation for isolated coding tasks, parallel work, AGENTS.md guidance, sandboxing, review, guardrails, handoffs, and agent internet-access risks.
- Anthropic Claude Code and engineering documentation for subagents, context isolation, multi-agent research architecture, verification, and agentic coding practices.
- GitHub Copilot cloud agent documentation for issue-to-branch-to-PR delivery, custom agents, planning-before-code, and outcome metrics.
- Thoughtworks Technology Radar and Looking Glass for delivery-team implications, harness engineering, team topology shifts, adoption cautions, and realistic productivity expectations.

Weak evidence was deliberately avoided. Reddit threads, vendor-adjacent hype posts, and third-party trend pieces were not used as decision-grade evidence. Where secondary sources overlap with primary sources, the primary source is treated as authoritative.

## Confirmed Practices

### 1. Isolate Agent Work By Task

OpenAI Codex cloud provisions a separate sandboxed container for each task, and OpenAI's launch notes describe each task as independent and preloaded with the repository. The same pattern appears in GitHub Copilot cloud agent, which works in a GitHub Actions-powered environment, creates a branch, and can open a pull request.

Confirmed practice:

- Give each write-capable agent one task, one branch or worktree, and one owned write scope.
- Avoid multiple agents writing the same files, templates, release metadata, or shared test harness unless a coordinator serializes the integration.
- Treat independent sandboxes as a safety primitive, not just a speed feature.

Implication for Expanded Mode: parallel agents help when task boundaries are file-level or module-level independent. They hurt when the main risk is integration judgment, shared context, migration ordering, or preserving a subtle business invariant.

### 2. Make Repositories Agent-Ready

OpenAI says Codex works best with configured development environments, reliable tests, clear documentation, and AGENTS.md guidance. Anthropic similarly emphasizes configured project instructions, clear verification paths, and context management. Thoughtworks frames this as teams needing to become "agent-ready" rather than simply buying tools.

Confirmed practice:

- Keep concise agent instructions close to the repo.
- Provide deterministic setup, test, lint, and verification commands.
- Make success criteria explicit before asking agents to code.
- Prefer durable docs and runbooks over chat-only tribal context.

Implication for Expanded Mode: requiring an operating guide and verification matrix is aligned with frontier practice. Expanded Mode should reject or downshift requests that lack setup, acceptance criteria, or a reviewable output path.

### 3. Separate Exploration, Planning, Implementation, And Verification

Anthropic's Claude Code best practices recommend exploring first, then planning, then coding. GitHub Copilot cloud agent explicitly supports repository research and planning before code changes. OpenAI Codex supports both ask mode for analysis and code mode for changes.

Confirmed practice:

- Use read-only investigation agents for discovery-heavy work.
- Use implementation agents only after the coordinator has narrowed scope.
- Run verification or review agents after implementation, preferably with a different prompt and context boundary.

Implication for Expanded Mode: a multi-agent plan should not mean "everyone starts coding." It should allow research agents, planner agents, implementation agents, and verification agents with different permissions and done conditions.

### 4. Use Context Isolation Deliberately

Anthropic's subagent docs state that subagents operate in their own context and return summaries, specifically to prevent exploration from flooding the main conversation. The Claude Agent SDK docs also describe subagents as a way to isolate context, run analyses in parallel, and apply specialized instructions without bloating the main prompt.

Confirmed practice:

- Delegate noisy searches, log review, large-file reading, and broad audits to bounded subagents.
- Require structured summaries back to the coordinator.
- Do not assume subagents automatically share complete context with each other.
- Pass only the context each worker needs, plus its constraints and output contract.

Implication for Expanded Mode: context isolation is a first-class reason to use parallel agents even when wall-clock speed is not the only goal. It also creates a coordinator responsibility to reconcile outputs, because isolated agents can miss cross-cutting dependencies.

### 5. Keep A Coordinator Responsible For Integration

Anthropic's multi-agent research system uses an orchestrator-worker architecture: the lead agent forms a strategy, spawns specialized subagents, and synthesizes their outputs. OpenAI's agent guide describes handoffs and guardrails, but handoff patterns still need explicit control of state, outputs, and validation. Thoughtworks warns that agentic systems require rethinking feedback cycles and team or agent topologies.

Confirmed practice:

- The coordinator owns task decomposition, dependencies, permissions, integration, conflict resolution, and final acceptance.
- Workers own bounded subtasks and evidence.
- The coordinator should preserve the authoritative execution state somewhere durable: Linear issue, ledger, PR description, or repo doc.

Implication for Expanded Mode: coordinator duties must be required, not optional. Expanded Mode should not let worker agents independently decide to broaden scope, merge work, close Linear issues, or update release state.

### 6. Treat Review And Verification As Separate Agent Roles

OpenAI Codex supports code review workflows and can run tests, linters, and type checkers. OpenAI Codex Security separates identification, validation, remediation, human review, and revalidation. Anthropic recommends giving Claude a way to verify its work and using subagents to review edge cases after implementation.

Confirmed practice:

- Use verification agents after implementation for edge cases, tests, security review, docs consistency, and acceptance criteria.
- Require test outputs, screenshots, logs, or concrete evidence rather than unsupported "looks good" summaries.
- Keep human or coordinator review in the loop for merge, release, and production-impact decisions.

Implication for Expanded Mode: verification agents are valuable when they have clear acceptance criteria and independent context. They hurt when used as rubber stamps or when they share the same flawed assumptions as the implementer.

### 7. Build Harnesses, Guardrails, And Feedback Loops

OpenAI's Agents SDK treats guardrails as first-class concepts around inputs, outputs, and tool calls. OpenAI also warns that enabling internet access for Codex agents increases risks including prompt injection, exfiltration, malware, vulnerabilities, and license issues. Thoughtworks identifies "coding agent harnesses" as a response to the risk of humans stepping out of the loop.

Confirmed practice:

- Put permissions, allowed tools, network policy, output contracts, and tests around agents.
- Use allowlists for internet access where possible.
- Require review of agent work logs and outputs, especially when untrusted web content enters context.
- Prefer small feedback loops: tests, lint, typecheck, evaluator, screenshot, review, re-run.

Implication for Expanded Mode: guardrails should be defaulted into the project structure: owned write scopes, non-owned areas, verification commands, source-link requirements, and coordinator approval gates.

### 8. Measure Outcomes, Not Agent Activity

GitHub documents pull request lifecycle metrics for Copilot cloud agent, including PRs created, merged, and median time to merge. Thoughtworks cautions that AI speed claims are often exaggerated and cites more modest observed delivery uplift, while emphasizing reliability and product-learning benefits.

Confirmed practice:

- Track merged PRs, time to merge, review burden, defect rate, rework, and verification pass rate.
- Avoid treating number of agents, number of commits, or volume of generated code as success.
- Prefer small, reviewable outputs that reduce human attention cost.

Implication for Expanded Mode: success metrics should focus on verified issue completion and integration quality, not maximal parallelism for its own sake.

## Implications For Expanded Mode

Expanded Mode should model a real delivery system, not an unbounded swarm.

Parallel agents help when:

- Work has independent write scopes.
- Research can be split by source family, subsystem, or risk category.
- Context volume would otherwise bury the coordinator.
- Verification can be performed independently from implementation.
- Tasks have clear acceptance criteria and bounded output contracts.

Parallel agents hurt when:

- Agents need to edit the same files or shared release artifacts.
- The task depends on one sequence of business decisions.
- Requirements are ambiguous and need user/coordinator judgment first.
- Tests, migrations, deployment, or sink outputs are tightly coupled.
- Workers would need broad secrets, production access, or internet access without guardrails.
- Output synthesis is more expensive than doing the work serially.

Coordinator responsibilities:

- Read the project instructions and authoritative issue state.
- Define owned write scopes, non-owned areas, dependencies, and verification commands.
- Decide which tasks are parallel-safe and which are serial.
- Keep Linear, ledger, PR, and documentation state coherent when the owned scope allows it.
- Reconcile findings across isolated agents.
- Run or delegate final verification.
- Preserve residual risks and follow-ups.

Review and verification agent roles:

- Review diffs against acceptance criteria and non-owned boundaries.
- Check tests, evaluator output, docs links, and evidence.
- Look for edge cases, security concerns, missing rollback plans, and integration risks.
- Provide findings with file paths, line numbers where applicable, severity, confidence, and recommended action.
- Avoid rewriting implementation unless explicitly assigned a write scope.

Context isolation requirements:

- Each worker receives only the prompt, files, source links, and constraints it needs.
- Workers return compact evidence summaries, not raw transcripts unless requested.
- Coordinators must not treat isolated findings as globally complete until reconciled.
- Long-running projects need durable state outside any one agent context.

## What To Require vs Offer

Require:

- One active coordinator for each Expanded Mode project.
- Explicit issue ownership and write scope for every worker.
- Explicit non-owned areas for every worker.
- A safe-parallelism checkpoint before spawning write-capable agents.
- Read-only research agents for broad source discovery before implementation.
- Separate verification/review agent roles for non-trivial changes.
- Concrete acceptance criteria and verification commands per issue.
- Durable handoff notes when context compaction or multi-session work is likely.
- Source links for research claims.
- Human/coordinator approval before merge, release, production, credential, or broad refactor actions.

Offer:

- Multiple worker agents when write scopes are independent.
- Read-only context-isolation agents for noisy investigation.
- Specialized reviewer agents such as security, tests, docs, UX, data integrity, or release readiness.
- Optional internet-enabled research agents with source-quality constraints.
- Optional deeper harnesses such as policy checks, generated evaluators, or PR outcome metrics.
- Optional custom agent profiles for repeated work types.

Do not require:

- Parallel agents for small single-file changes.
- Multi-agent orchestration when a single expert pass is cheaper and clearer.
- Full Linear/ledger machinery for one-off read-only research unless the project already uses it and scope allows updates.
- Automatic installation, release, or public publishing as part of ordinary research tasks.

## Risks/Anti-Patterns

- Unbounded parallelism: more agents can increase conflict, duplicated work, and synthesis burden.
- Shared-file collisions: multiple write-capable agents touching the same docs, tests, templates, or release files creates merge and intent conflicts.
- Context leakage: giving workers too much unrelated context can produce accidental edits outside scope or false confidence.
- Context starvation: giving workers too little context can make them miss constraints, dependencies, or prior decisions.
- Rubber-stamp verification: a review agent without independent criteria just repeats the implementer's assumptions.
- Hype-driven adoption: vendor demos and social posts can overstate delivery speed while understating review, setup, and integration costs.
- Weak harnesses: agents without tests, permissions, output contracts, or rollback thinking produce impressive but fragile changes.
- Hidden internet risk: web-enabled agents can ingest prompt injection, malicious dependencies, license-restricted content, or secret-exfiltration instructions.
- Coordinator abdication: if no one owns dependency order, final synthesis, and evidence quality, multi-agent output becomes fragmented.
- Activity metrics: counting agents, tokens, commits, or generated lines rewards motion instead of shipped, verified value.

## Source Links

- OpenAI, [Codex cloud](https://platform.openai.com/docs/codex): Codex can read, modify, and run code; cloud tasks run in isolated containers and can work in parallel.
- OpenAI, [Introducing Codex](https://openai.com/index/introducing-codex/): Codex launch details for independent cloud sandboxes, AGENTS.md guidance, tests, and reviewable coding tasks.
- OpenAI, [A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/): handoffs, agent workflow patterns, and layered guardrails.
- OpenAI Agents SDK, [Guardrails](https://openai.github.io/openai-agents-python/guardrails/): input, output, and tool guardrail behavior and limitations.
- OpenAI, [Agent internet access](https://platform.openai.com/docs/codex/agent-network): security risks of internet-enabled coding agents and mitigation guidance.
- OpenAI Help Center, [Codex Security](https://help.openai.com/en/articles/20001107-codex-security): identification, validation, remediation, human review, and revalidation workflow.
- Anthropic, [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system): orchestrator-worker architecture with specialized parallel subagents and lead-agent synthesis.
- Anthropic Claude Code Docs, [Create custom subagents](https://code.claude.com/docs/en/sub-agents): task-specific subagents, independent context windows, tool constraints, and context preservation.
- Anthropic Claude Code Docs, [Subagents in the SDK](https://code.claude.com/docs/en/agent-sdk/subagents): context isolation, parallel analyses, and specialized instructions.
- Anthropic Claude Code Docs, [Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices): verification, explore-plan-code workflow, context management, and subagent investigation/review.
- GitHub Docs, [About Copilot cloud agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent): GitHub Actions-powered autonomous issue work, repository research/planning, custom agents, PRs, and outcome metrics.
- Thoughtworks, [Technology Radar](https://www.thoughtworks.com/radar): agent topologies, feedback-cycle shifts, and coding-agent harnesses.
- Thoughtworks, [Technology Radar Vol. 34 PDF](https://www.thoughtworks.com/content/dam/thoughtworks/documents/radar/2026/04/tr_technology_radar_vol_34_en.pdf): Claude Code Adopt assessment, agentic delivery risks, context engineering, and harness engineering.
- Thoughtworks, [AI and software delivery](https://www.thoughtworks.com/insights/looking-glass/looking-glass-2026/AI-and-software-delivery): intent-based coding, agent-readiness, tempered productivity claims, and reliability implications.
