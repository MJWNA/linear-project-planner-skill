# Trigger Preservation Contract

Use this file when editing `SKILL.md`, frontmatter, README activation language,
or docs that affect when agents choose the skill.

## Goal

`SKILL.md` can be short, but it must remain easy for agents to trigger when the
user needs Linear project planning, audit remediation, execution tracking,
companion ledgers, or verification gates.

## Required Router-Visible Concepts

These concepts must remain in `SKILL.md` frontmatter or the first operating
section:

- `Linear project`
- `create`, `plan`, `restructure`, or `execute`
- `audit` or `remediation`
- `production hardening`
- `parallel agent` or `multi-agent`
- `milestones`
- `dependencies` or `blockers`
- `companion ledger`
- `verification gates`
- `completion comments`
- `Codex` and `Claude`

The exact wording can change, but the concepts must stay router-visible.

## Positive Trigger Examples

The skill should activate for prompts like:

- "Create a Linear project for this audit remediation."
- "Run the Linear skill and build the plan."
- "Execute this Linear project end to end."
- "Break this repo hardening work into Linear issues for agents."
- "Use Linear as the source of truth and keep a companion ledger."
- "Make a project with milestones, dependencies, verification gates, and final
  closeout."

## Negative Boundaries

The skill should not activate for:

- a simple question about one existing Linear issue
- a request to list or search issues without planning or execution
- a casual status summary that does not need project restructuring
- work where another dedicated skill is a better match and Linear is only
  incidental

## Research Belongs In The Plan

When the user asks to create a Linear project and also asks for online research,
source review, audits, or exploratory discovery, create tracked research issues
inside the Linear project. Minimal repo inspection needed to create an accurate
plan is fine; substantive research findings should not happen before the plan
exists.

## Safe Slimming Rules

1. Keep the frontmatter description action-oriented and explicit.
2. Keep a first paragraph that says when to use the skill and when not to.
3. Preserve the Core Rule and Quick Path.
4. Move long explanations into references only when the Reference Map points to
   them.
5. Add or update evaluator checks when trigger language changes.
6. Do not chase a line-count target if it weakens activation reliability.

## Verification

Run:

```bash
python3 tools/linear-front-door-evaluator.py
python3 tools/linear-agent-evaluator.py
python3 tools/linear-skill-audit-evaluator.py
```

The front-door evaluator is deliberately semantic enough to allow wording
changes but strict enough to catch missing trigger concepts.
