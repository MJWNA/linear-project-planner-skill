#!/usr/bin/env python3
"""Frozen evaluator for the linear-project-planner automation CLI.

The score is intentionally simple and deterministic. It rewards the behaviors
that matter for this skill: legacy compatibility, direct Linear automation,
offline fake transport tests, reconciliation, docs, and public repo hygiene.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> tuple[bool, str]:
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return result.returncode == 0, result.stdout


def contains(path: str, text: str) -> bool:
    return text in (ROOT / path).read_text(encoding="utf-8")


def main() -> int:
    checks: list[tuple[str, int, bool, str]] = []

    ok, output = run(["bash", "tests/test-linear-agent.sh"])
    checks.append(("legacy shell regression", 20, ok, output))

    ok, output = run(
        [
            sys.executable,
            "-m",
            "unittest",
            "tests/test_linear_agent_graphql.py",
        ]
    )
    checks.append(("fake Linear GraphQL tests", 20, ok, output))

    ok, output = run(
        [
            sys.executable,
            "-m",
            "py_compile",
            "lib/linear_agent/__init__.py",
            "lib/linear_agent/ledger.py",
            "lib/linear_agent/graphql.py",
        ]
    )
    checks.append(("python syntax", 10, ok, output))

    checks.append(
        (
            "direct apply command surface",
            10,
            contains("lib/linear_agent/cli.py", "--apply-linear")
            and contains("lib/linear_agent/cli.py", "LINEAR_AGENT_APPLY"),
            "missing --apply-linear or LINEAR_AGENT_APPLY",
        )
    )
    checks.append(
        (
            "reconcile command surface",
            10,
            contains("lib/linear_agent/cli.py", "reconcile")
            and contains("lib/linear_agent/graphql.py", "def reconcile("),
            "missing reconcile command",
        )
    )
    checks.append(
        (
            "fake transport safety gate",
            10,
            contains("lib/linear_agent/graphql.py", "LINEAR_AGENT_FAKE_STATE")
            and contains("lib/linear_agent/graphql.py", "LINEAR_AGENT_TEST_MODE")
            and contains("tests/test_linear_agent_graphql.py", "test_fake_transport_requires_explicit_test_mode"),
            "missing fake transport safety gate",
        )
    )
    checks.append(
        (
            "partial apply recovery",
            10,
            contains("lib/linear_agent/graphql.py", "post-update confirmation failed")
            and contains("tests/test_linear_agent_graphql.py", "test_comment_failure_reports_partial_apply_recovery_context"),
            "missing partial apply recovery",
        )
    )
    checks.append(
        (
            "docs explain direct mode",
            10,
            contains("README.md", "--apply-linear")
            and contains("README.md", "SCORE 200/200")
            and contains("SKILL.md", "LINEAR_API_KEY")
            and contains("SKILL.md", "Linear GraphQL is the primary path")
            and contains("README.md", "direct GraphQL is the primary route")
            and contains("references/execution-hygiene.md", "direct GraphQL mode is the primary path")
            and contains("references/operator-cheatsheet.md", "fallback when credentials are unavailable")
            and contains("references/operator-cheatsheet.md", "read-back cannot confirm")
            and contains("SKILL.md", "required fallback surface")
            and contains("SKILL.md", "when API read-back cannot confirm")
            and contains("references/command-schemas.md", "required fallback")
            and contains("README.md", "direct API blocks/rejections")
            and contains("README.md", "linear-agent reconcile")
            and contains("lib/linear_agent/cli.py", "finalize refuses unfinished issue rows")
            and contains("tests/test-linear-agent.sh", "Expected reconcile against an empty Issue Progress table to fail")
            and contains("tests/test_linear_agent_graphql.py", "test_reconcile_empty_ledger_fails_closed")
            and contains("SKILL.md", "## Sparse Link Graph")
            and contains("SKILL.md", "## Optional Deep Auto-Research Validation")
            and contains("SKILL.md", "Standard validation is mandatory for every project")
            and contains("SKILL.md", "Do you want standard validation only")
            and contains("README.md", "### Sparse Link Graph")
            and contains("README.md", "### 5. Optional Deep Auto-Research Validation")
            and contains("README.md", "Standard validation is always required")
            and contains("templates/EXECUTION.md", "Validation mode")
            and contains("lib/linear_agent/cli.py", "Validation mode: standard"),
            "missing direct mode docs",
        )
    )
    checks.append(
        (
            "structured tool contract",
            10,
            contains("references/command-schemas.md", "linear_project.finalize")
            and contains("references/command-schemas.md", "Tool Description Checklist")
            and contains("SKILL.md", "## Quick Path")
            and contains("SKILL.md", "## Reference Map"),
            "missing structured command schema or quick path docs",
        )
    )
    checks.append(
        (
            "runtime state guidance",
            10,
            contains("references/runtime-state.md", "previous_response_id")
            and contains("references/runtime-state.md", "phase")
            and contains("README.md", "Responses API State"),
            "missing runtime state guidance",
        )
    )
    checks.append(
        (
            "agent output fixture coverage",
            10,
            contains("tests/fixtures/linear_issue_templates.md", "## Final Completion Comment")
            and contains("tests/fixtures/linear_issue_templates.md", "## Normal-Mode Project Description")
            and contains("tests/fixtures/linear_issue_templates.md", "## Normal-Mode Child Issue")
            and contains("tests/fixtures/linear_issue_templates.md", "## Expanded-Mode Project Charter")
            and contains("tests/fixtures/linear_issue_templates.md", "## Expanded-Mode Issue Body")
            and contains("tests/fixtures/linear_issue_templates.md", "## Continuous Discovery Issue Candidate")
            and contains("tests/fixtures/linear_issue_templates.md", "Standard labels")
            and contains("tests/fixtures/linear_issue_templates.md", "Dependencies")
            and contains("tests/fixtures/linear_issue_templates.md", "Sparse links")
            and contains("tests/fixtures/linear_issue_templates.md", "Residual risks")
            and contains("tests/fixtures/linear_issue_templates.md", "Follow-ups"),
            "missing issue template or final comment fixtures",
        )
    )
    checks.append(
        (
            "live graph mutations",
            15,
            contains("lib/linear_agent/graphql.py", "ProjectCreate")
            and contains("lib/linear_agent/graphql.py", "IssueLabelCreate")
            and contains("lib/linear_agent/graphql.py", "ProjectMilestoneCreate")
            and contains("lib/linear_agent/graphql.py", "IssueBatchCreate")
            and contains("lib/linear_agent/graphql.py", "IssueRelationCreate")
            and contains("lib/linear_agent/graphql.py", "AttachmentCreate")
            and contains("lib/linear_agent/cli.py", "Graph applied to Linear and read-back verified"),
            "missing direct graph mutation operations",
        )
    )
    checks.append(
        (
            "continuous discovery cli",
            10,
            contains("lib/linear_agent/cli.py", "cmd_discover")
            and contains("lib/linear_agent/cli.py", "cmd_promote")
            and contains("lib/linear_agent/cli.py", "Continuous Discovery Issue Candidate"),
            "missing discover/promote command implementation",
        )
    )
    checks.append(
        (
            "live api documentation",
            10,
            contains("README.md", "Linear MCP is no longer required")
            and contains("SKILL.md", "## Live API Mode")
            and contains("references/command-schemas.md", "Live API Mode")
            and contains("docs/research/direct-linear-graphql-adr.md", "Direct Linear GraphQL")
            and contains("docs/research/linear-api-v4-efficiency-adr.md", "Linear API v4 Efficiency"),
            "missing direct API docs or ADR",
        )
    )
    checks.append(
        (
            "scheduled live smoke",
            5,
            contains(".github/workflows/live-linear-smoke.yml", "schedule:")
            and contains(".github/workflows/live-linear-smoke.yml", "linear-agent smoke")
            and contains("lib/linear_agent/graphql.py", "ProjectDelete"),
            "missing scheduled graph smoke workflow",
        )
    )
    checks.append(
        (
            "schema-current API efficiency",
            20,
            contains("lib/linear_agent/graphql.py", "issueBatchCreate")
            and contains("lib/linear_agent/graphql.py", "projectDelete")
            and contains("lib/linear_agent/graphql.py", "project: { id: { eq: $projectId } }")
            and contains("lib/linear_agent/graphql.py", "pageInfo")
            and contains("lib/linear_agent/graphql.py", "while page_info.get(\"hasNextPage\")")
            and contains("lib/linear_agent/graphql.py", "x-ratelimit-complexity-remaining")
            and contains("tests/test_linear_agent_graph_features.py", "test_graph_apply_title_lookup_is_project_scoped")
            and contains("tests/test_linear_agent_graph_features.py", "test_project_readback_paginates_all_issues"),
            "missing batch create, schema-current teardown, pagination, or rate-limit budget coverage",
        )
    )
    checks.append(
        (
            "rich relation and attachment graph",
            10,
            contains("lib/linear_agent/graph.py", "duplicate_of")
            and contains("lib/linear_agent/graphql.py", "\"related\"")
            and contains("lib/linear_agent/graphql.py", "\"duplicate\"")
            and contains("lib/linear_agent/graphql.py", "\"linear-project-planner\"")
            and contains("tests/test_linear_agent_graph_features.py", "test_graph_apply_related_duplicate_and_attachment_metadata"),
            "missing related/duplicate relation or attachment metadata coverage",
        )
    )

    score = 0
    for name, points, ok, detail in checks:
        if ok:
            score += points
            print(f"PASS {points:02d} {name}")
        else:
            print(f"FAIL {points:02d} {name}")
            if detail:
                print(detail.rstrip())

    print(f"SCORE {score}/200")
    return 0 if score == 200 else 1


if __name__ == "__main__":
    raise SystemExit(main())
