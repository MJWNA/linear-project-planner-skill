#!/usr/bin/env python3
"""Dogfood evaluator for live linear-project-planner project-shape runs."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "dogfood"
BIN = ROOT / "scripts" / "linear-agent"

REQUIRED_ISSUE_SECTIONS = (
    "Objective",
    "Acceptance Criteria",
    "Verification",
)
EXPANDED_SECTIONS = (
    "Background Context",
    "Owned Scope",
    "Non-Owned Scope",
    "Verification Requirements",
)
DISCOVERY_SECTIONS = (
    "Why It Was Discovered",
    "Surfaced By",
    "Classification",
    "Future-Agent Context",
)


def run(command: list[str], env: dict[str, str] | None = None) -> tuple[bool, str]:
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env={**os.environ, **(env or {})},
        check=False,
    )
    return result.returncode == 0, result.stdout


def load_plans() -> list[dict[str, Any]]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(FIXTURE_DIR.glob("*.json"))
    ]


def issue_text(issue: dict[str, Any]) -> str:
    return str(issue.get("description") or "")


def has_sections(issue: dict[str, Any], headings: tuple[str, ...]) -> bool:
    text = issue_text(issue)
    return all(f"## {heading}" in text for heading in headings)


def live_run_plan(plan_path: Path, plan: dict[str, Any]) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        state = tmp / "linear-state.json"
        ledger = tmp / "EXECUTION.md"
        state.write_text("{}", encoding="utf-8")
        env = {
            "LINEAR_AGENT_TEST_MODE": "1",
            "LINEAR_AGENT_FAKE_STATE": str(state),
            "PYTHONPATH": str(ROOT / "lib"),
        }
        graph_ok, graph_out = run([str(BIN), "graph-plan", "--from", str(plan_path), "--json"])
        apply_ok, apply_out = run([str(BIN), "graph-apply", "--from", str(plan_path), "--apply-linear", "--json"], env)
        readback_ok, readback_out = run([str(BIN), "graph-readback", "--from", str(plan_path), "--json"], env)
        init_ok, init_out = run(
            [
                str(BIN),
                "init",
                "--ledger",
                str(ledger),
                "--project",
                plan["project"]["name"],
                "--prompt",
                plan["project"]["brief"],
                "--linear-project",
                plan["project"]["name"],
                "--repo",
                str(ROOT),
                "--base-branch",
                "main",
                "--json",
            ],
        )
        alloc_ok, alloc_out = run(
            [str(BIN), "allocate", "--from", str(plan_path), "--ledger", str(ledger), "--json"],
        )
        state_payload = json.loads(state.read_text(encoding="utf-8")) if state.exists() else {}
        ledger_text = ledger.read_text(encoding="utf-8") if ledger.exists() else ""
        return {
            "graph_ok": graph_ok,
            "graph_out": graph_out,
            "apply_ok": apply_ok,
            "apply_out": apply_out,
            "readback_ok": readback_ok,
            "readback_out": readback_out,
            "init_ok": init_ok,
            "init_out": init_out,
            "alloc_ok": alloc_ok,
            "alloc_out": alloc_out,
            "state": state_payload,
            "ledger": ledger_text,
        }


def score(plans: list[dict[str, Any]], runs: dict[str, dict[str, Any]]) -> dict[str, tuple[int, str]]:
    all_issues = [issue for plan in plans for issue in plan["issues"]]
    by_name = {plan["project"]["name"]: plan for plan in plans}
    run_values = list(runs.values())
    issue_counts: dict[str, int] = {}
    for plan in plans:
        issue_counts[plan["project"]["mode"]] = issue_counts.get(plan["project"]["mode"], 0) + len(plan["issues"])
    dependency_edges = sum(
        len(issue.get("blockedBy") or []) + len(issue.get("blocks") or [])
        for issue in all_issues
    )
    parent_count = len([issue for issue in all_issues if not issue.get("parent")])
    child_count = len(all_issues) - parent_count
    described_state_issues = 0
    linked_state_issues = 0
    for plan in plans:
        state_issues = runs[plan["project"]["name"]]["state"].get("issues", {})
        for issue in plan["issues"]:
            actual = state_issues.get(issue["key"], {})
            if actual.get("description") == issue.get("description"):
                described_state_issues += 1
            if actual.get("links") == issue.get("links", []):
                linked_state_issues += 1

    checks: dict[str, bool] = {
        "brief_preservation": all(
            plan["project"].get("brief") and plan["project"]["brief"] in runs[plan["project"]["name"]]["ledger"]
            for plan in plans
        ),
        "project_decomposition": (
            issue_counts.get("normal", 0) >= 7
            and issue_counts.get("expanded", 0) >= 7
            and issue_counts.get("continuous-discovery", 0) >= 6
            and parent_count >= 5
            and child_count >= 15
        ),
        "linear_issue_sufficiency": all(
            len(plan.get("milestones", [])) >= 3
            and any("Agent Operating Guide" in issue["title"] for issue in plan["issues"])
            and (
                any("Verification Matrix" in issue["title"] for issue in plan["issues"])
                or any("Verify" in issue["title"] or "verification" in issue["title"].lower() for issue in plan["issues"])
                or plan["project"]["mode"] == "expanded"
            )
            for plan in plans
        ),
        "issue_actionability": sum(has_sections(issue, REQUIRED_ISSUE_SECTIONS) for issue in all_issues) >= len(all_issues) - 1,
        "dependency_modeling": dependency_edges >= 18 and all(run["readback_ok"] for run in run_values),
        "companion_ledger_quality": all(
            run["init_ok"]
            and "## Original Prompt" in run["ledger"]
            and "## Continuous Issue Discovery Log" in run["ledger"]
            and "## Safe Parallelism Decisions" in run["ledger"]
            for run in run_values
        ),
        "expanded_mode_artifact_quality": (
            "expanded" in issue_counts
            and all(key in by_name["[SANDBOX] Dogfood Expanded - Agent Workflow Redesign"]["project"].get("requiredArtifacts", []) for key in ("research-dossier", "dependency-map", "qa-plan", "handoff"))
            and sum(has_sections(issue, EXPANDED_SECTIONS) for issue in by_name["[SANDBOX] Dogfood Expanded - Agent Workflow Redesign"]["issues"]) >= 5
        ),
        "continuous_discovery_behavior": (
            len(by_name["[SANDBOX] Dogfood Continuous Discovery - Importer Cleanup"]["project"].get("discoveryEvents", [])) >= 2
            and sum(has_sections(issue, DISCOVERY_SECTIONS) for issue in by_name["[SANDBOX] Dogfood Continuous Discovery - Importer Cleanup"]["issues"]) >= 2
            and any("Discovered blocker" in issue["title"] for issue in by_name["[SANDBOX] Dogfood Continuous Discovery - Importer Cleanup"]["issues"])
            and any("Candidate:" in issue["title"] for issue in by_name["[SANDBOX] Dogfood Continuous Discovery - Importer Cleanup"]["issues"])
        ),
        "parallel_agent_readiness": all(run["alloc_ok"] for run in run_values)
        and any("parallel-safe" in issue.get("labels", []) for issue in all_issues)
        and all(issue.get("writeSet") for issue in all_issues),
        "delivery_feasibility": all(run["graph_ok"] and run["apply_ok"] and run["readback_ok"] for run in run_values),
        "source_checkpoint_discipline": all(
            "links" in issue and issue["links"] and issue.get("milestone") for issue in all_issues
        )
        and described_state_issues == len(all_issues)
        and linked_state_issues == len(all_issues),
    }
    return {
        name: (10 if ok else 0, "pass" if ok else "fail")
        for name, ok in checks.items()
    }


def main() -> int:
    plans = load_plans()
    runs: dict[str, dict[str, Any]] = {}
    for path in sorted(FIXTURE_DIR.glob("*.json")):
        plan = json.loads(path.read_text(encoding="utf-8"))
        runs[plan["project"]["name"]] = live_run_plan(path, plan)

    scores = score(plans, runs)
    total = sum(points for points, _ in scores.values())
    payload = {
        "score": total,
        "maxScore": 110,
        "rubric": {name: {"score": points, "result": result} for name, (points, result) in scores.items()},
        "runs": {
            name: {
                "graph_ok": run["graph_ok"],
                "apply_ok": run["apply_ok"],
                "readback_ok": run["readback_ok"],
                "init_ok": run["init_ok"],
                "alloc_ok": run["alloc_ok"],
            }
            for name, run in runs.items()
        },
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    print(f"DOGFOOD_SCORE {total}/110")
    return 0 if total == 110 else 1


if __name__ == "__main__":
    raise SystemExit(main())
