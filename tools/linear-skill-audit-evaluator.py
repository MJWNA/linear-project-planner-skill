#!/usr/bin/env python3
"""All-verticals evaluator for the 10/10 linear-project-planner release."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def contains(path: str, text: str) -> bool:
    return text in (ROOT / path).read_text(encoding="utf-8")


def exists(path: str) -> bool:
    return (ROOT / path).exists()


def run(command: list[str]) -> bool:
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return result.returncode == 0


def main() -> int:
    checks: dict[str, bool] = {
        "purpose_fit": contains("SKILL.md", "Create an execution system, not a flat todo list"),
        "contract_clarity": exists("references/operator-cheatsheet.md")
        and contains("references/operator-cheatsheet.md", "Minimal Safe Path"),
        "trigger_safe_front_door": exists("references/trigger-preservation.md")
        and contains("SKILL.md", "create a Linear project")
        and contains("SKILL.md", "run the Linear skill")
        and contains("SKILL.md", "Do not use it for a simple one-off Linear issue lookup"),
        "progressive_disclosure_research": exists("docs/research/skill-front-door-context-loading.md")
        and contains("docs/research/skill-front-door-context-loading.md", "trigger-safe progressive disclosure")
        and contains("SKILL.md", "references/project-structure.md")
        and contains("SKILL.md", "references/execution-hygiene.md")
        and contains("SKILL.md", "references/validation-modes.md"),
        "linear_project_structure": contains("references/command-schemas.md", "linear_project.graph_apply")
        and exists("tests/fixtures/linear_graph_plan.json"),
        "ledger_design": contains("lib/linear_agent/ledger.py", "write_state_sidecar")
        and contains("lib/linear_agent/ledger.py", "validate_ledger"),
        "source_checkpoint_discipline": exists("references/source-checkpoints.md")
        and contains("SKILL.md", "references/source-checkpoints.md")
        and contains("references/source-checkpoints.md", "## Before Parallel Delegation")
        and contains("references/source-checkpoints.md", "## Before Closeout")
        and contains("templates/EXECUTION.md", "## Source Material Checkpoints"),
        "cli_wrapper_ux": contains("scripts/linear-agent", "python3 -m linear_agent.cli")
        and contains("lib/linear_agent/cli.py", "--json"),
        "direct_linear_automation": contains("lib/linear_agent/cli.py", "graph-apply")
        and contains("lib/linear_agent/cli.py", "graph-readback"),
        "verification_tests": exists("tests/test_linear_agent_graph_features.py")
        and contains(".github/workflows/ci.yml", "shellcheck"),
        "frozen_evaluator": run([sys.executable, "tools/linear-agent-evaluator.py"]),
        "parallel_agent_safety": contains("lib/linear_agent/cli.py", "allocate")
        and contains("lib/linear_agent/graph.py", "overlapping_write_sets")
        and contains("SKILL.md", "safe parallelism checkpoint")
        and contains("SKILL.md", "context isolation")
        and contains("SKILL.md", "coordinator-level decision context")
        and contains("references/execution-hygiene.md", "Safe Parallelism Checkpoints")
        and contains("references/project-structure.md", "Safe Parallelism Planning")
        and contains("templates/EXECUTION.md", "Safe Parallelism Decisions"),
        "expanded_mode_additive": exists("references/expanded-mode.md")
        and contains("SKILL.md", "## Expanded Mode")
        and contains("SKILL.md", "Baseline mode remains the default")
        and contains("SKILL.md", "references/expanded-mode.md")
        and contains("references/expanded-mode.md", "## Mode Gate")
        and contains("references/expanded-mode.md", "## Baseline Protection")
        and contains("references/expanded-mode.md", "## Dependency Mapping")
        and contains("references/expanded-mode.md", "## Multi-Agent Allocation")
        and contains("references/expanded-mode.md", "Dogfood expanded mode")
        and exists("templates/expanded-mode/research-dossier.md")
        and exists("templates/expanded-mode/decision.md")
        and exists("templates/expanded-mode/dependency-map.md")
        and exists("templates/expanded-mode/qa-plan.md")
        and exists("templates/expanded-mode/agent-brief.md")
        and exists("templates/expanded-mode/handoff.md"),
        "project_principles_surface": exists("references/project-principles.md")
        and exists("templates/project-principles.md")
        and contains("SKILL.md", "what project principles or fundamentals should guide repeated decisions")
        and contains("SKILL.md", "references/project-principles.md")
        and contains("references/project-principles.md", "Every Linear project gets a principles surface")
        and contains("references/project-principles.md", "Small baseline projects")
        and contains("references/project-principles.md", "Promotion Threshold")
        and contains("references/project-principles.md", "Do not silently rewrite accepted principles")
        and contains("templates/EXECUTION.md", "## Project Principles / Fundamentals")
        and contains("templates/project-principles.md", "## Accepted Principles"),
        "continuous_issue_discovery": contains("SKILL.md", "## Continuous Issue Discovery")
        and contains("SKILL.md", "Create a Linear issue immediately")
        and contains("SKILL.md", "Propose an issue candidate")
        and contains("SKILL.md", "Normal mode keeps this lightweight")
        and contains("references/project-structure.md", "## Continuous Issue Discovery")
        and contains("references/expanded-mode.md", "## Continuous Issue Discovery Protocol")
        and contains("templates/EXECUTION.md", "## Continuous Issue Discovery Log")
        and contains("tests/fixtures/linear_issue_templates.md", "## Continuous Discovery Issue Candidate"),
        "structured_normal_expanded_outputs": contains("references/project-structure.md", "## Normal-Mode Project Description")
        and contains("references/project-structure.md", "## Normal-Mode Issue Body")
        and contains("references/expanded-mode.md", "## Project Charter Description")
        and contains("references/expanded-mode.md", "Step-by-step working instructions")
        and contains("tests/fixtures/linear_issue_templates.md", "## Expanded-Mode Project Charter")
        and contains("tests/fixtures/linear_issue_templates.md", "## Expanded-Mode Issue Body")
        and contains("references/command-schemas.md", "## Planning Output Modes"),
        "production_sink_gates": exists("templates/production-gates.md")
        and contains("lib/linear_agent/cli.py", "inventory"),
        "documentation": exists("docs/examples/local-skill-audit.md")
        and exists("docs/migration-guide.md"),
        "packaging_install": contains("install.sh", "--uninstall")
        and contains("install.sh", "--with-docs")
        and contains("install.sh", "--check"),
        "ci_release": exists(".github/workflows/release.yml")
        and contains(".github/workflows/ci.yml", "gitleaks"),
        "security": exists("docs/linear-token-scope.md")
        and contains("lib/linear_agent/cli.py", "[REDACTED]"),
        "maintainability": exists("lib/linear_agent/cli.py")
        and exists("lib/linear_agent/graph.py"),
        "portability": contains("lib/linear_agent/ledger.py", "LINEAR_AGENT_TIMEZONE")
        and exists("docs/claude-portability.md")
        and (contains("README.md", "Windows") or contains("README.md", "WSL"))
        and contains("README.md", "Codex-first and Claude-compatible"),
        "manual_linear_smoke_docs": exists("docs/manual-linear-smoke.md")
        and contains("README.md", "Live Linear Smoke Tests"),
    }
    payload = {
        "score": sum(1 for ok in checks.values() if ok),
        "maxScore": len(checks),
        "checks": checks,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    if all(checks.values()):
        print("ALL_VERTICALS 10/10")
        return 0
    print("ALL_VERTICALS incomplete")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
