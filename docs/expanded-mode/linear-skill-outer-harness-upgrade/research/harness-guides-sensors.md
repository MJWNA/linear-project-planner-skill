# Harness Guides And Sensors Dossier

Status: complete first pass
Linear issue: MAS-1008

## Source-Backed Facts

- Harness engineering treats the model as only one part of an agentic system.
  In coding-agent use, the outer harness is the user or team layer around the
  coding agent.
- Guides are feedforward controls: `AGENTS.md`, skills, reference docs, scripts,
  language servers, codemods, examples, and operating guides.
- Sensors are feedback controls: tests, linters, static analysis, browser
  checks, logs, metrics, review agents, and other checks that help the agent
  self-correct.
- Sensors can be computational or inferential. Computational checks are
  deterministic and cheap; inferential checks use semantic judgment.
- Quality should move left: fast deterministic checks should run before costly
  review or integration, with broad/expensive checks later.
- Humans move upward in the stack: prioritizing, translating feedback into
  acceptance criteria, validating outcomes, and converting repeated failures
  into docs, tools, guardrails, or checks.

## Inferences For This Skill

- The skill is already an outer harness for Linear-driven agent work.
- Existing guides include `SKILL.md`, references, templates, guide issues,
  dependency rules, and the companion ledger.
- Existing deterministic sensors include shell tests, Python unit tests,
  evaluator tools, syntax checks, YAML checks, install checks, graph-plan,
  graph-readback, and optional `shellcheck`.
- Missing or underdeveloped sensors are mostly inferential: issue quality, graph
  coherence, guide clarity, dependency risk, future-agent recoverability, and
  proof quality in completion comments.
- The strongest upgrade is to turn repeated review taste into small runnable
  evaluators and bounded review prompts, not to bloat `SKILL.md`.

## Harness Matrix

| Surface | Type | Timing | Implementation |
|---|---|---|---|
| `AGENTS.md`, `SKILL.md`, references | Guide | Before planning and implementation | Keep concise, route to deeper refs |
| Guide issues and verification matrix | Guide | Project creation | Linear issues plus ledger links |
| `graph-plan`, dependency map | Computational sensor | Before issue creation and delegation | Validate graph shape and ownership |
| Tests/evaluators/syntax/YAML | Computational sensor | Before Done and release | Frozen final-loop evaluator set |
| Research synthesis review | Inferential sensor | Before implementation | Review docs against accepted sources |
| Dogfood review | Inferential sensor | Before release | Ask if future agent can resume safely |

## Recommendations

- Add sensor timing to validation guidance.
- Add a steering-loop log for repeated failures.
- Add an inferential expanded-mode review pass: can a future agent resume from
  Linear plus ledger, with safe sequencing and proof of work?
- Prefer evaluator changes over more prose when failures repeat.

## Refresh Triggers

- New OpenAI/Codex harness guidance changes tooling assumptions.
- Thoughtworks updates the harness taxonomy.
- MAS projects show repeated failures despite green evaluators.
- `SKILL.md` starts growing beyond router/reference-map size.

