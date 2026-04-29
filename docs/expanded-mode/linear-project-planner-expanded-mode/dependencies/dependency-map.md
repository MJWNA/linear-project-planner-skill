# Dependency Map

- Project: Linear Project Planner Expanded Mode
- Linear project / guide issue: MAS-681
- Owner: Codex coordinator
- Status: dogfood read-back
- Updated: 2026-04-29
- Source policy: Linear read-back, companion ledger, and local docs generated
  during this execution.

## Milestones And Exit Gates

| Milestone | Exit Evidence | Unlocks |
|---|---|---|
| Baseline Isolation & Mode Contract | MAS-689 and MAS-690 complete with baseline snapshot and ADR | Deep research and spec work |
| Deep Delivery Research | MAS-691 through MAS-695 complete with source-backed dossiers and synthesis | Expanded-mode operating model |
| Context7 & OpenAI Capability Design | MAS-696 through MAS-698 complete with provenance policy | Runtime reference and templates |
| Expanded Mode Specification | MAS-699 through MAS-702 complete with trigger/docs/graph/QA specs | Implementation |
| Implementation & Regression | MAS-703 through MAS-705 complete with full verification and installed read-back | Dogfood and release/runtime sync |
| Dogfood, Release & Runtime Sync | MAS-706 dogfood and MAS-707 release/install decision | Final handoff |

## Workstreams

| Workstream | Owner | Outcome | Exit Criteria |
|---|---|---|---|
| MAS-683 | Coordinator | Baseline behavior protected | ADR and baseline snapshot done |
| MAS-684 | Research agents + coordinator | Delivery operating model | Research dossiers and synthesis done |
| MAS-685 | Research agents + coordinator | Docs/provenance policy | Context7/OpenAI research and synthesis done |
| MAS-686 | Spec workers + coordinator | Expanded-mode specs | Trigger, docs, graph, and QA specs done |
| MAS-687 | Coordinator | Runtime implementation and tests | Reference/templates/evaluators installed and verified |
| MAS-688 | Coordinator + human review | Dogfood and release decision | Dogfood complete and MAS-707 scoped |

## Issues

| Issue | Title | Parent | Milestone | Labels | Owned Scope | Verification |
|---|---|---|---|---|---|---|
| MAS-690 | Baseline snapshot | MAS-683 | 0 | serial-required | `docs/research/baseline-current-skill-contract.md` | Full baseline verification |
| MAS-691..694 | Research dossiers | MAS-684 | 1 | parallel-safe | One research doc each | Source links and required sections |
| MAS-695 | Operating model synthesis | MAS-684 | 1 | serial-required | `docs/research/expanded-mode-operating-model.md` | Synthesis section checks |
| MAS-696..697 | Context7/OpenAI research | MAS-685 | 2 | parallel-safe | One capability doc each | Source links and required sections |
| MAS-698 | Provenance policy | MAS-685 | 2 | serial-required | `docs/research/docs-grounding-provenance-policy.md` | Policy section checks |
| MAS-699..702 | Expanded-mode specs | MAS-686 | 3 | serial-required | One spec doc each | Spec section checks |
| MAS-703..705 | Runtime implementation | MAS-687 | 4 | overlap-zone | `SKILL.md`, references, templates, tests, evaluators | Full suite and install read-back |
| MAS-706 | Dogfood | MAS-688 | 5 | serial-required | `docs/expanded-mode/linear-project-planner-expanded-mode/**` | Dogfood doc and Linear read-back |
| MAS-707 | Release/install sync | MAS-688 | 5 | serial-required | Release/install surfaces | Human-gated public release decision |

## Dependency Edges

| From | To | Class | Linear Relationship | Reason | Verification |
|---|---|---|---|---|---|
| MAS-690 | MAS-691..698 | serial-hard | blocks | Baseline must be frozen before research/spec changes | MAS-690 Done |
| MAS-691..694 | MAS-695 | serial-hard | blocks | Delivery synthesis requires completed research | MAS-695 Done |
| MAS-696..697 | MAS-698 | serial-hard | blocks | Provenance synthesis requires Context7/OpenAI research | MAS-698 Done |
| MAS-695, MAS-698 | MAS-699..702 | serial-hard | blocks | Specs depend on synthesized model and policy | MAS-699..702 Done |
| MAS-699..702 | MAS-703..705 | serial-hard | blocks | Runtime implementation depends on specs | MAS-703..705 Done |
| MAS-703..705 | MAS-706 | serial-hard | blocks | Dogfood should test implemented runtime behavior | MAS-706 In Progress |
| MAS-706 | MAS-707 | human-gate | blocks | Release/install closeout depends on dogfood and approval | Pending |

## Parallel-Safe Batches

| Batch | Issues | Non-Overlap Rationale | Verification |
|---|---|---|---|
| Research wave 1 | MAS-691, MAS-692, MAS-693, MAS-694, MAS-696, MAS-697 | One owned research doc per agent, no shared runtime files | Targeted doc checks |
| Spec wave | MAS-699, MAS-700, MAS-701, MAS-702 | One owned spec doc per agent, no shared runtime files | Targeted spec checks |

## Serial Gates

| Gate | Blocked Work | Required Evidence | Owner |
|---|---|---|---|
| Baseline protection | All expanded-mode work | Snapshot and baseline verification | Coordinator |
| Synthesis | Specs and implementation | MAS-695 and MAS-698 complete | Coordinator |
| Runtime implementation | Dogfood/release | Full test/evaluator/install read-back | Coordinator |
| Public release | GitHub tag/release | Human approval, PR/checks, release read-back | Human + coordinator |

## Integration Zones / Cyclic Risks

- `SKILL.md` is a baseline-sensitive integration zone.
- `CHANGELOG.md` and `VERSION` are release-sensitive and should stay
  coordinator-owned.
- Installed runtime sync is allowed only after source repo verification.

## Linear Read-Back Checklist

- [x] Child issue states read back from Linear.
- [x] Completed research/spec/implementation issues read back as Done.
- [x] MAS-706 read back as In Progress before dogfood.
- [ ] MAS-707 release/install decision resolved.
