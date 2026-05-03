#!/usr/bin/env python3
"""Evaluator for the slimmed linear-project-planner skill front door.

The checks are semantic enough to tolerate wording changes, but strict about
the router-visible concepts that keep the skill discoverable.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAX_SKILL_LINES = 500


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def words(text: str) -> str:
    return re.sub(r"\s+", " ", text.casefold())


def any_phrase(text: str, phrases: tuple[str, ...]) -> bool:
    normalized = words(text)
    return any(words(phrase) in normalized for phrase in phrases)


def section_before(text: str, heading: str) -> str:
    index = text.find(heading)
    if index == -1:
        return text
    return text[:index]


def line_count(text: str) -> int:
    return len(text.splitlines())


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}

    payload: dict[str, str] = {}
    current_key = ""
    current_value: list[str] = []
    for raw_line in text[4:end].splitlines():
        if raw_line.startswith((" ", "\t")) and current_key:
            current_value.append(raw_line.strip())
            continue
        if ":" not in raw_line:
            continue
        if current_key:
            payload[current_key] = " ".join(current_value).strip()
        key, value = raw_line.split(":", 1)
        current_key = key.strip()
        current_value = [value.strip().strip(">")]
    if current_key:
        payload[current_key] = " ".join(current_value).strip()
    return payload


def check_concepts(text: str, concepts: dict[str, tuple[str, ...]]) -> tuple[bool, str]:
    missing = [name for name, phrases in concepts.items() if not any_phrase(text, phrases)]
    if missing:
        return False, "missing concepts: " + ", ".join(missing)
    return True, ""


def contains_all(path: str, phrases: tuple[str, ...]) -> tuple[bool, str]:
    text = read(path)
    missing = [phrase for phrase in phrases if phrase not in text]
    if missing:
        return False, "missing phrases: " + ", ".join(missing)
    return True, ""


def main() -> int:
    skill = read("SKILL.md")
    trigger_contract = read("references/trigger-preservation.md")
    execution_hygiene = read("references/execution-hygiene.md")
    project_structure = read("references/project-structure.md")
    expanded_mode = read("references/expanded-mode.md")
    ledger_template = read("templates/EXECUTION.md")
    fm = frontmatter(skill)
    front_door_text = section_before(skill, "## First Pass")
    parallelism_text = " ".join(
        (skill, execution_hygiene, project_structure, ledger_template)
    )

    checks: list[tuple[str, int, bool, str]] = []

    description = fm.get("description", "")
    checks.append(
        (
            "frontmatter identity and action description",
            15,
            fm.get("name") == "linear-project-planner"
            and any_phrase(description, ("plan", "create", "restructure", "execute"))
            and any_phrase(description, ("linear project", "linear projects")),
            "frontmatter must name linear-project-planner and describe Linear project actions",
        )
    )

    router_concepts = {
        "Linear project": ("Linear project", "Linear projects"),
        "create/plan/restructure/execute": ("create", "plan", "restructure", "execute"),
        "audit/remediation": ("audit", "audits", "remediation"),
        "production hardening": ("production hardening", "production-readiness", "production readiness"),
        "parallel/multi-agent": ("parallel agent", "parallel agents", "multi-agent"),
        "companion ledger": ("companion ledger", "companion execution ledger"),
        "milestones/dependencies": ("milestones", "dependencies", "blockers"),
        "verification gates": ("verification gates", "verification evidence"),
        "completion comments": ("completion comments", "final comment"),
        "Codex and Claude": ("Codex", "Claude"),
    }
    ok, detail = check_concepts(front_door_text, router_concepts)
    checks.append(("router-visible trigger concepts", 20, ok, detail))

    contract_concepts = {
        "required concepts heading": ("## Required Router-Visible Concepts",),
        "negative boundaries": ("## Negative Boundaries",),
        "research belongs in plan": ("## Research Belongs In The Plan",),
        "safe slimming rules": ("## Safe Slimming Rules",),
        "front-door evaluator": ("tools/linear-front-door-evaluator.py",),
    }
    ok, detail = check_concepts(trigger_contract, contract_concepts)
    checks.append(("trigger preservation contract", 10, ok, detail))

    checks.append(
        (
            "negative boundary for one-off issue lookup",
            10,
            any_phrase(
                front_door_text,
                (
                    "one-off Linear issue lookup",
                    "one existing Linear issue",
                    "simple question about one existing Linear issue",
                ),
            )
            and any_phrase(front_door_text, ("Do not use it", "should not activate")),
            "front door must say not to use the skill for simple one-off Linear issue lookup",
        )
    )

    reference_targets = (
        "references/trigger-preservation.md",
        "references/project-structure.md",
        "references/project-principles.md",
        "references/execution-hygiene.md",
        "references/validation-modes.md",
        "references/expanded-mode.md",
    )
    ok, detail = contains_all("SKILL.md", reference_targets)
    checks.append(("reference map links deeper refs", 10, ok, detail))

    checks.append(
        (
            "research stays inside Linear plan",
            10,
            any_phrase(
                front_door_text + trigger_contract,
                (
                    "inside the Linear plan",
                    "Research Belongs In The Plan",
                    "tracked research issues inside the Linear project",
                ),
            ),
            "missing research-as-planned-work language",
        )
    )

    checks.append(
        (
            "SKILL.md below 500 lines",
            10,
            line_count(skill) < MAX_SKILL_LINES,
            f"SKILL.md is {line_count(skill)} lines; expected below {MAX_SKILL_LINES}",
        )
    )

    prior_evaluator_phrases = (
        "## Quick Path",
        "## Reference Map",
        "## Sparse Link Graph",
        "## Optional Deep Auto-Research Validation",
        "Standard validation is mandatory for every project",
        "Do you want standard validation only",
        "LINEAR_API_KEY",
        "Create an execution system, not a flat todo list",
    )
    ok, detail = contains_all("SKILL.md", prior_evaluator_phrases)
    checks.append(("prior evaluator core phrases preserved", 15, ok, detail))

    mapped_phrases = (
        "templates/EXECUTION.md",
        "templates/project-principles.md",
        "scripts/linear-agent",
        "references/command-schemas.md",
        "references/runtime-state.md",
        "templates/production-gates.md",
        "tests/fixtures/linear_issue_templates.md",
    )
    ok, detail = contains_all("SKILL.md", mapped_phrases)
    checks.append(("legacy deep guidance mapped to references", 10, ok, detail))

    safe_parallelism_concepts = {
        "checkpoint cadence": (
            "safe parallelism checkpoint",
            "after project creation/read-back",
        ),
        "agent-ready candidates": ("independent, unblocked `agent-ready` issues",),
        "candidate grouping": (
            "dependency order, write scope, risk, and verification overlap",
            "dependency/write scope/risk/verification overlap",
        ),
        "worktree isolation": ("one branch, one worktree", "branches/worktrees"),
        "assignment contract": (
            "owned write scope",
            "non-owned areas",
            "verification command",
        ),
        "context isolation": ("context isolation", "coordinator context"),
        "coordinator ownership": (
            "coordinator responsible for decisions",
            "coordinator-level decisions",
        ),
        "serial constraints": (
            "shared file/module",
            "unclear ownership",
            "production/sink gate",
            "verification coupling",
            "coordinator-level decision context",
        ),
        "follow-up splitting": ("create follow-up Linear issues", "follow-up issues"),
    }
    ok, detail = check_concepts(parallelism_text, safe_parallelism_concepts)
    checks.append(("safe parallelism contract", 15, ok, detail))

    principles_text = " ".join(
        (
            skill,
            project_structure,
            expanded_mode,
            ledger_template,
            read("references/project-principles.md"),
            read("templates/project-principles.md"),
        )
    )
    project_principles_concepts = {
        "global principles surface": (
            "Every project needs a durable principles surface",
            "Every Linear project gets a principles surface",
        ),
        "compact baseline section": (
            "Small baseline projects",
            "compact section",
        ),
        "promotion threshold": ("Promotion Threshold", "promote to a separate companion"),
        "artifact boundaries": (
            "Tasks belong in Linear",
            "execution state belongs in the ledger",
            "detailed decisions belong in ADRs",
        ),
        "amendment model": ("Proposed", "Accepted", "Superseded"),
        "template exists": ("templates/project-principles.md",),
        "baseline remains concise": (
            "Keep baseline mode concise",
            "Do not create expanded-mode docs folders",
        ),
    }
    ok, detail = check_concepts(principles_text, project_principles_concepts)
    checks.append(("project principles surface contract", 15, ok, detail))

    continuous_discovery_front_door = {
        "named behavior": ("Continuous Issue Discovery",),
        "plan not sacred": (
            "original Linear plan as a starting model, not a sacred list",
            "original Linear plan is not sacred",
        ),
        "classification blocker": ("Blocker",),
        "classification dependency": ("Dependency",),
        "classification defect": ("Defect",),
        "classification research follow-up": ("Research follow-up",),
        "classification implementation follow-up": ("Implementation follow-up",),
        "classification decision required": ("Decision required",),
        "classification qa gap": ("QA / verification gap",),
        "classification documentation gap": ("Documentation gap",),
        "classification scope expansion": ("Scope expansion",),
        "classification risk mitigation": ("Risk / mitigation",),
        "create rule": ("Create a Linear issue immediately",),
        "propose rule": ("Propose an issue candidate",),
        "log rule": ("Log it only",),
        "created issue context": (
            "why the work was discovered",
            "which issue or workstream surfaced it",
            "future agents need to know",
        ),
    }
    ok, detail = check_concepts(skill, continuous_discovery_front_door)
    checks.append(("continuous issue discovery front door", 10, ok, detail))

    normal_discovery_concepts = {
        "normal lightweight": ("In normal mode, keep discovery lightweight",),
        "normal concise candidates": ("concise candidates or issues",),
        "normal blocker links": ("blocker/dependency links",),
    }
    ok, detail = check_concepts(project_structure, normal_discovery_concepts)
    checks.append(("normal-mode discovery placement", 10, ok, detail))

    expanded_discovery_concepts = {
        "expanded formal": (
            "formal discovery protocol",
            "local dependency map",
            "coordinator deduplicates",
        ),
        "expanded docs updates": ("Update the companion ledger",),
        "expanded candidate context": ("surfacing issue/workstream",),
    }
    ok, detail = check_concepts(expanded_mode, expanded_discovery_concepts)
    checks.append(("expanded-mode discovery protocol", 10, ok, detail))

    ledger_discovery_concepts = {
        "ledger discovery log": ("## Continuous Issue Discovery Log",),
        "ledger why discovered": ("Why Discovered",),
        "ledger future-agent context": ("Future-Agent Context",),
    }
    ok, detail = check_concepts(ledger_template, ledger_discovery_concepts)
    checks.append(("ledger discovery log captures recovery context", 10, ok, detail))

    structured_normal_concepts = {
        "normal project description": ("Normal-Mode Project Description",),
        "normal project goal": ("Project goal",),
        "normal source of truth": ("Source of truth",),
        "normal handoff recovery": ("Handoff/context recovery expectations",),
        "normal issue body": ("Normal-Mode Issue Body",),
        "normal dependencies blockers": ("Dependencies / Blockers",),
        "normal future-agent notes": ("Notes For Future Agents",),
        "normal remains compact": (
            "Keep normal-mode issues concise",
            "not bureaucracy",
        ),
    }
    ok, detail = check_concepts(project_structure, structured_normal_concepts)
    checks.append(("normal-mode structured output contract", 10, ok, detail))

    structured_expanded_concepts = {
        "expanded project charter": ("Project Charter Description",),
        "expanded ledger path": ("companion ledger path",),
        "expanded coordinator responsibilities": ("coordinator responsibilities",),
        "expanded issue body": ("Step-by-step working instructions",),
        "expanded follow-up candidates": ("Follow-up issue candidates",),
        "expanded required updates": (
            "Required updates to local docs, ledger, or dependency map",
        ),
        "expanded remains richer": (
            "Expanded-mode issue bodies should include",
            "future agents need after context loss",
        ),
    }
    ok, detail = check_concepts(expanded_mode, structured_expanded_concepts)
    checks.append(("expanded-mode structured output contract", 10, ok, detail))

    fixture_output_concepts = {
        "normal fixture": ("## Normal-Mode Project Description",),
        "normal issue fixture": ("## Normal-Mode Child Issue",),
        "expanded charter fixture": ("## Expanded-Mode Project Charter",),
        "expanded issue fixture": ("## Expanded-Mode Issue Body",),
        "discovery fixture": ("## Continuous Discovery Issue Candidate",),
    }
    ok, detail = check_concepts(
        read("tests/fixtures/linear_issue_templates.md"), fixture_output_concepts
    )
    checks.append(("fixture examples cover output modes", 10, ok, detail))

    expanded_mode_concepts = {
        "opt-in mode": ("Use expanded mode only", "Load only after an expanded-mode trigger"),
        "baseline default": ("Baseline mode remains the default",),
        "trigger phrases": ("long-horizon planning", "deep research first", "dependency mapping"),
        "non-trigger boundary": ("ordinary Linear planning", "ordinary baseline projects"),
        "expanded reference": ("references/expanded-mode.md",),
        "local docs": ("local project docs", "docs/expanded-mode"),
        "provenance": ("Context7", "OpenAI/Codex"),
        "dependency map": ("Dependency Mapping", "serial-hard", "parallel-safe"),
        "multi-agent allocation": ("Multi-Agent Allocation", "owned write scope", "non-owned scope"),
        "dogfood and baseline verification": ("Dogfood expanded mode", "baseline preservation"),
    }
    ok, detail = check_concepts(skill + expanded_mode, expanded_mode_concepts)
    checks.append(("expanded mode additive contract", 15, ok, detail))

    expanded_templates = (
        "templates/expanded-mode/research-dossier.md",
        "templates/expanded-mode/decision.md",
        "templates/expanded-mode/dependency-map.md",
        "templates/expanded-mode/qa-plan.md",
        "templates/expanded-mode/agent-brief.md",
        "templates/expanded-mode/handoff.md",
    )
    checks.append(
        (
            "expanded mode templates exist",
            10,
            all((ROOT / path).exists() for path in expanded_templates),
            "missing expanded-mode templates",
        )
    )

    score = 0
    max_score = sum(points for _, points, _, _ in checks)
    for name, points, ok, detail in checks:
        if ok:
            score += points
            print(f"PASS {points:02d} {name}")
        else:
            print(f"FAIL {points:02d} {name}")
            if detail:
                print(detail.rstrip())

    print(f"SCORE {score}/{max_score}")
    return 0 if score == max_score else 1


if __name__ == "__main__":
    raise SystemExit(main())
