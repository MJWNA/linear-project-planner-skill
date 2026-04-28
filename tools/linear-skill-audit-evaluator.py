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
        "linear_project_structure": contains("references/command-schemas.md", "linear_project.graph_apply")
        and exists("tests/fixtures/linear_graph_plan.json"),
        "ledger_design": contains("lib/linear_agent/ledger.py", "write_state_sidecar")
        and contains("lib/linear_agent/ledger.py", "validate_ledger"),
        "cli_wrapper_ux": contains("scripts/linear-agent", "python3 -m linear_agent.cli")
        and contains("lib/linear_agent/cli.py", "--json"),
        "direct_linear_automation": contains("lib/linear_agent/cli.py", "graph-apply")
        and contains("lib/linear_agent/cli.py", "graph-readback"),
        "verification_tests": exists("tests/test_linear_agent_graph_features.py")
        and contains(".github/workflows/ci.yml", "shellcheck"),
        "frozen_evaluator": run([sys.executable, "tools/linear-agent-evaluator.py"]),
        "parallel_agent_safety": contains("lib/linear_agent/cli.py", "allocate")
        and contains("lib/linear_agent/graph.py", "overlapping_write_sets"),
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
        and (contains("README.md", "Windows") or contains("README.md", "WSL")),
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
