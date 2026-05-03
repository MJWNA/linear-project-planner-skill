# Expanded Mode Trigger Contract

Linear issue: MAS-699
Project: Linear Project Planner Expanded Mode
Status: implementation contract draft
Owner: spec agent
Inputs:

- `docs/research/baseline-current-skill-contract.md`
- `docs/research/expanded-mode-adr.md`
- `docs/research/expanded-mode-operating-model.md`
- `docs/research/docs-grounding-provenance-policy.md`

## Purpose

This document defines the trigger contract for adding expanded mode to the
`linear-project-planner` skill without contaminating the current baseline mode.

Expanded mode is an explicit, additive, opt-in mode for long-horizon Linear
planning and execution. It should give future agents a richer operating model
only when the user's request justifies more research, local documentation,
dependency mapping, and multi-agent coordination than the baseline skill
already provides.

Baseline mode remains the default for ordinary Linear project planning,
execution, audit remediation, project restructuring, companion ledgers, sparse
link graphs, and verification gates.

## Triggers

Expanded mode should activate only when the user explicitly asks for one or more
expanded-mode concepts, or when the request clearly combines several of them at
a scale where baseline mode would under-specify the work.

Strong explicit triggers:

- `expanded mode`
- `long-horizon project`
- `detailed multi-phase plan`
- `software-firm-grade planning`
- `deep research first`
- `dependency mapping`
- `multi-team delivery model`
- `create local project docs`
- `create local references`
- `maximize safe parallel agents`
- `agent-heavy project with detailed ownership`
- `research dossier`
- `ADR-first planning`
- `dogfood before release`

Strong compound triggers:

- A Linear project request that also asks for deep research, current-doc
  grounding, dependency maps, and local docs.
- A production-hardening or release-readiness project that needs explicit
  source provenance, QA planning, and staged implementation gates.
- A multi-agent plan where the user asks for broad parallel execution and the
  coordinator must first define ownership, dependencies, non-owned scopes, and
  verification gates.
- A self-editing skill or framework project where baseline behavior must be
  protected while the project modifies its own instructions, evaluators, or
  release process.
- A project expected to survive many sessions, worktrees, or agents where local
  docs are needed to preserve design context outside transient chat.

Trigger interpretation rules:

- Prefer baseline mode when the request is ordinary, small, or already covered
  by the current front-door contract.
- Prefer expanded mode when the user names the mode directly.
- If the request is ambiguous, ask a short clarifying question or proceed with
  baseline mode and note that expanded mode is available if they want the
  heavier planning path.
- Do not infer expanded mode merely because a task is important; infer it from
  explicit scope, detail, research, dependency, documentation, or multi-agent
  signals.

## Non-Triggers

Expanded mode must not activate for small or ordinary work where the current
skill is already sufficient.

Non-triggers:

- A simple request to create a small Linear project.
- A one-off Linear issue lookup, status summary, or issue comment.
- A normal audit remediation plan with clear scope and no request for deep
  research or detailed dependency mapping.
- A small repo documentation edit.
- A pure Linear graph cleanup.
- A concise issue breakdown for a known implementation task.
- Routine companion-ledger usage.
- Routine safe-parallelism checkpointing.
- Normal labels, milestones, blockers, guide issues, or verification matrices.
- Standard validation before closing issues.
- A request to preserve business outputs or production gates when baseline mode
  can express the needed checks.
- A request to use `linear-agent` for issue state transitions.

Boundary examples:

- "Create a Linear project for this bug bash" stays baseline unless the user
  asks for deep research, local docs, or expanded mode.
- "Plan the release with milestones, dependencies, and verification gates" stays
  baseline unless the request adds long-horizon research, source provenance, or
  multi-agent allocation depth.
- "Use as many agents as safely useful, with owned write scopes and verification
  gates" may trigger expanded mode when the work is broad enough to need a
  documented allocation matrix; it does not trigger expanded mode for two small,
  independent doc edits.

## Router Addition

Future implementation should add only a small router-visible concept to
`SKILL.md`. The addition should name expanded mode, list the strongest trigger
phrases, and route detailed behavior to a reference file. It should not copy the
full operating model into `SKILL.md`.

Conceptual shape:

```md
## Expanded Mode

Use expanded mode only when the user explicitly asks for expanded mode,
long-horizon planning, detailed multi-phase planning, deep research first,
dependency mapping, local project docs/references, software-firm-grade planning,
multi-team delivery, or heavy safe parallel-agent coordination.

Baseline mode remains the default for ordinary Linear planning, execution,
audits, remediation, companion ledgers, dependencies, and verification gates.
Load `references/expanded-mode.md` only after an expanded-mode trigger is
present.
```

Router addition constraints:

- Preserve existing frontmatter identity and description.
- Preserve the current normal-mode trigger language.
- Keep the addition compact enough that `SKILL.md` remains a front door, not a
  full handbook.
- State that baseline mode remains the default.
- Include at least one explicit non-trigger sentence or boundary sentence.
- Do not require external research or local docs for ordinary baseline projects.
- Do not change `linear-agent` command semantics.

## Reference Map

Future implementation should add one focused reference-map entry for expanded
mode. The entry should point to a new `references/expanded-mode.md` file and
make clear that it is loaded only after an expanded-mode trigger is present.

Conceptual reference-map entry:

```md
- `references/expanded-mode.md`: opt-in long-horizon planning workflow for
  deep research, local docs, dependency maps, provenance, multi-agent allocation,
  synthesis gates, dogfood, and baseline contamination safeguards. Load only
  after an expanded-mode trigger is present.
```

The future `references/expanded-mode.md` should own the detailed workflow for:

- Mode gate and baseline protection.
- Research and discovery.
- Source grounding and provenance.
- Local docs folder convention.
- Dependency mapping.
- Expanded issue graph construction.
- Safe multi-agent allocation.
- QA, dogfood, and final verification.

The reference-map entry should not make expanded mode mandatory for normal
Linear planning. It should be a route for explicit mode escalation.

## Baseline Protection

Expanded mode is additive. It must not weaken, rename, or replace the current
skill contract captured in
`docs/research/baseline-current-skill-contract.md`.

Baseline safeguards:

- Keep normal mode as the default path.
- Preserve router-visible baseline concepts: Linear project planning,
  restructuring, auditing, remediation, production hardening, parallel agents,
  milestones, dependencies/blockers, companion ledger, verification gates,
  completion comments, Codex, and Claude.
- Preserve the rule that the skill does not activate for a simple one-off
  Linear issue lookup unless planning, remediation, execution tracking, or
  project-level coordination is also requested.
- Preserve required guide issues: `Guide: Agent Operating Guide` and
  `Guide: Verification Matrix`.
- Preserve companion ledger semantics: the ledger complements Linear and does
  not replace issue state, statuses, comments, relationships, or read-back
  verification.
- Preserve sparse link graph behavior.
- Preserve standard validation before marking issues done.
- Preserve optional deep auto-research boundaries; do not make deep research a
  baseline requirement.
- Preserve `linear-agent` transition, reconciliation, and direct Linear mode
  boundaries.
- Keep expanded-mode runtime detail in references and templates, not in a large
  `SKILL.md` body.

Contamination risks to test against:

- Baseline prompts start producing expanded-mode documentation trees.
- Ordinary Linear project requests require Context7, OpenAI docs, or web
  research without a current-doc dependency.
- The front door treats "parallel agents" alone as enough to force expanded
  mode.
- The skill becomes verbose enough that router-visible baseline language is
  diluted.
- Worker agents are allowed to update shared Linear or ledger state outside
  coordinator control.
- Expanded-mode docs become active runtime instructions without an explicit
  trigger.

## Verification

Future implementation acceptance checks should prove both opt-in expanded mode
and baseline preservation.

Document-level checks:

- `references/expanded-mode.md` exists and contains sections for mode gate,
  triggers, non-triggers, baseline protection, local docs, provenance,
  dependency mapping, multi-agent allocation, and verification.
- `SKILL.md` contains a compact expanded-mode router addition.
- `SKILL.md` reference map contains exactly one expanded-mode reference entry.
- The expanded-mode reference states that it loads only after an explicit
  expanded-mode trigger.

Baseline evaluator checks:

- Existing normal-mode evaluator cases still pass.
- At least one baseline prompt for ordinary Linear planning does not activate
  expanded mode.
- At least one one-off issue lookup prompt does not activate the skill unless
  planning or execution tracking is requested.
- At least one parallel-agent baseline prompt remains baseline when it only
  needs ordinary safe-parallelism checkpointing.

Expanded-mode evaluator checks:

- A prompt containing `expanded mode` activates expanded mode.
- A prompt asking for `long-horizon`, `deep research first`, and `dependency
  mapping` activates expanded mode.
- A prompt asking for local project docs, source provenance, and safe
  multi-agent allocation activates expanded mode.
- Expanded-mode outputs include baseline/no-contamination protection, research
  issues, local docs, dependency maps, provenance rules, synthesis gates, and
  verification gates when relevant.

Regression commands for implementation work:

```bash
bash tests/test-linear-agent.sh
python3 -m unittest tests/test_linear_agent_graphql.py tests/test_linear_agent_graph_features.py
python3 tools/linear-front-door-evaluator.py
python3 tools/linear-agent-evaluator.py
python3 tools/linear-skill-audit-evaluator.py
```

Additional checks when implementation touches install, shell, metadata, or
runtime files:

```bash
bash -n install.sh
bash -n scripts/linear-agent
bash -n tests/test-linear-agent.sh
python3 -m py_compile lib/linear_agent/__init__.py lib/linear_agent/ledger.py lib/linear_agent/graphql.py lib/linear_agent/graph.py lib/linear_agent/cli.py tools/linear-front-door-evaluator.py tools/linear-agent-evaluator.py tools/linear-skill-audit-evaluator.py
ruby -e 'require "yaml"; skill = File.read("SKILL.md"); frontmatter = skill.match(/\A---\n(.*?)\n---/m)[1]; YAML.safe_load(frontmatter); YAML.load_file("agents/openai.yaml"); puts "yaml ok"'
./install.sh --check
```

Use `shellcheck install.sh scripts/linear-agent tests/test-linear-agent.sh` when
`shellcheck` is available.

Completion gate:

- Compare implementation against this contract and
  `docs/research/baseline-current-skill-contract.md`.
- Confirm expanded mode is opt-in.
- Confirm baseline mode remains concise and behaviorally stable.
- Confirm no implementation directly edits the installed runtime copy for
  durable changes.
