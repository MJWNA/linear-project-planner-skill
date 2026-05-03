# Recursive Loop Design Dossier

Status: complete first pass
Linear issue: MAS-1009

## Facts

- `references/validation-modes.md` already defines optional deep
  auto-research: choose a fixed evaluator, freeze it before the final loop, make
  one focused change, keep only correctness-preserving changes, record
  learnings, and repeat until stable.
- `SKILL.md` keeps deep recursion opt-in through trigger language such as
  `dogfood`, `recursive`, `auto-research`, `keep iterating`, `long horizon`, and
  `publish after stable`.
- The local `autoresearch` skill defines the core experiment loop as one change
  -> benchmark -> keep or revert -> repeat, with immutable benchmark/check
  files and hashes in campaign state.
- OpenAI Harness Engineering frames repeated review as self-review, additional
  agent reviews, response to feedback, and iteration until reviewers are
  satisfied.

## Inferences For This Repo

- Ralph Wiggum loops and auto-research loops should remain separate:
  qualitative review-discovery loops vs. metric-driven optimization loops.
- The planner should borrow auto-research evaluator discipline, not create
  `.autoresearch/` campaign machinery by default.
- Expanded mode and explicit deep validation are the right homes for recursive
  loops; baseline mode should remain standard validation plus an opt-in
  question when ambiguous.
- Misses should become Linear work only when they affect correctness,
  acceptance criteria, dependency order, verification, or future-agent
  recovery. Otherwise they are ledger learnings or issue candidates.

## Loop Stages

1. Define loop type, source scope, frozen evaluator set, issue-creation
   threshold, and stop condition.
2. Claim one issue and make one focused change or review pass.
3. Run deterministic sensors and then inferential review.
4. Classify misses as blocker, defect, dependency, QA gap, docs gap, risk, or
   follow-up.
5. Create or update Linear issues only for actionable misses.
6. Retry from the smallest responsible issue, not the whole project.
7. Mark Done only after frozen sensors pass, follow-up misses are resolved or
   deferred, Linear read-back is clean, and ledger/handoff agree.

## Frozen Evaluator Set

- `bash tests/test-linear-agent.sh`
- `python3 -m unittest tests/test_linear_agent_graphql.py tests/test_linear_agent_graph_features.py`
- `python3 tools/linear-front-door-evaluator.py`
- `python3 tools/linear-agent-evaluator.py`
- `python3 tools/linear-skill-audit-evaluator.py`
- `python3 tools/linear-dogfood-evaluator.py` when dogfood fixtures are in scope
- `bash -n install.sh scripts/linear-agent tests/test-linear-agent.sh`
- Python compile checks for `lib/linear_agent/*.py` and evaluator tools
- YAML/frontmatter checks for `SKILL.md` and `agents/openai.yaml`
- `./install.sh --with-docs && ./install.sh --check` after runtime behavior changes

## Risks

- Recursive review becomes churn without a stop condition.
- Auto-research creates false confidence if the evaluator changes mid-loop.
- Baseline contamination occurs if long-horizon loops become mandatory for
  small projects.
- Dirty worktrees make it easy to mix intended edits with prior work.

