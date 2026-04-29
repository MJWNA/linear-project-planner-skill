from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BIN = ROOT / "scripts" / "linear-agent"


class LinearAgentGraphFeatureTests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        env = {**os.environ, "PYTHONPATH": str(ROOT / "lib")}
        return subprocess.run(
            [str(BIN), *args],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            check=False,
        )

    def write_plan(self, tmp: Path) -> Path:
        plan = {
            "project": {"name": "Example 10/10 Project"},
            "labels": ["agent-ready", "serial-required"],
            "milestones": ["Graph Automation"],
            "issues": [
                {
                    "key": "MAS-1",
                    "identifier": "MAS-1",
                    "title": "Define schema",
                    "description": "## Objective\nDefine schema.\n\n## Acceptance Criteria\n- Done.\n\n## Verification\nRun graph-plan.",
                    "milestone": "Graph Automation",
                    "links": [{"title": "Schema docs", "url": "https://github.com/MJWNA/linear-project-planner-skill/blob/main/references/command-schemas.md"}],
                    "writeSet": ["references/command-schemas.md"],
                },
                {"key": "MAS-2", "title": "Apply graph", "parent": "MAS-1", "blockedBy": ["MAS-1"], "writeSet": ["lib/linear_agent/graph.py"], "serial": True},
                {"key": "MAS-3", "title": "Docs", "writeSet": ["README.md"]},
            ],
        }
        path = tmp / "graph.json"
        path.write_text(json.dumps(plan), encoding="utf-8")
        return path

    def test_graph_plan_json_and_readback(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            plan = self.write_plan(tmp)
            result = self.run_cli("graph-plan", "--from", str(plan), "--json")

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["summary"]["issues"], 3)
            self.assertEqual(payload["summary"]["dependencyEdges"], 1)

    def test_graph_apply_fake_state_and_readback(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            plan = self.write_plan(tmp)
            state = tmp / "linear-state.json"
            requests = tmp / "requests.jsonl"
            state.write_text("{}", encoding="utf-8")
            env = {
                **os.environ,
                "LINEAR_AGENT_FAKE_STATE": str(state),
                "LINEAR_AGENT_FAKE_REQUESTS": str(requests),
                "LINEAR_AGENT_TEST_MODE": "1",
            }
            apply_result = subprocess.run(
                [str(BIN), "graph-apply", "--from", str(plan), "--apply-linear"],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                check=False,
            )

            self.assertEqual(apply_result.returncode, 0, apply_result.stderr)
            readback = subprocess.run(
                [str(BIN), "graph-readback", "--from", str(plan)],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                check=False,
            )
            self.assertEqual(readback.returncode, 0, readback.stderr)
            self.assertIn("Graph read-back matched Linear state", readback.stdout)
            operations = [
                json.loads(line)["operationName"]
                for line in requests.read_text(encoding="utf-8").splitlines()
            ]
            for operation in (
                "Teams",
                "ProjectCreate",
                "IssueLabelCreate",
                "ProjectMilestoneCreate",
                "IssueCreate",
                "IssueRelationCreate",
                "AttachmentCreate",
                "ProjectReadback",
            ):
                self.assertIn(operation, operations)
            payload = json.loads(plan.read_text(encoding="utf-8"))
            payload["issues"][0]["description"] += "\nUpdated."
            plan.write_text(json.dumps(payload), encoding="utf-8")
            requests.write_text("", encoding="utf-8")
            update_result = subprocess.run(
                [str(BIN), "graph-apply", "--from", str(plan), "--apply-linear"],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                check=False,
            )
            self.assertEqual(update_result.returncode, 0, update_result.stderr)
            update_operations = [
                json.loads(line)["operationName"]
                for line in requests.read_text(encoding="utf-8").splitlines()
            ]
            self.assertIn("IssueUpdate", update_operations)

    def test_graph_plan_rejects_blocked_by_cycles(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            plan = tmp / "cycle.json"
            plan.write_text(
                json.dumps(
                    {
                        "project": {"name": "Cycle"},
                        "issues": [
                            {"key": "MAS-1", "title": "One", "blockedBy": ["MAS-2"]},
                            {"key": "MAS-2", "title": "Two", "blockedBy": ["MAS-1"]},
                        ],
                    }
                ),
                encoding="utf-8",
            )

            result = self.run_cli("graph-plan", "--from", str(plan))

            self.assertEqual(result.returncode, 1)
            self.assertIn("dependency cycle", result.stderr)

    def test_graph_fake_state_requires_test_mode(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            plan = self.write_plan(tmp)
            state = tmp / "linear-state.json"
            state.write_text("{}", encoding="utf-8")
            env = {**os.environ, "LINEAR_AGENT_FAKE_STATE": str(state)}

            apply_result = subprocess.run(
                [str(BIN), "graph-apply", "--from", str(plan), "--apply-linear"],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                check=False,
            )
            readback_result = subprocess.run(
                [str(BIN), "graph-readback", "--from", str(plan)],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                check=False,
            )
            smoke_result = subprocess.run(
                [str(BIN), "smoke", "--project", "Disposable", "--apply-linear"],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                check=False,
            )

            self.assertEqual(apply_result.returncode, 1)
            self.assertEqual(readback_result.returncode, 1)
            self.assertEqual(smoke_result.returncode, 1)
            self.assertIn("LINEAR_AGENT_FAKE_STATE is test-only", apply_result.stderr)
            self.assertIn("LINEAR_AGENT_FAKE_STATE is test-only", readback_result.stderr)
            self.assertIn("LINEAR_AGENT_FAKE_STATE is test-only", smoke_result.stderr)

    def test_graph_apply_updates_and_readback_reports_drift(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            plan = self.write_plan(tmp)
            state = tmp / "linear-state.json"
            state.write_text("{}", encoding="utf-8")
            env = {**os.environ, "LINEAR_AGENT_FAKE_STATE": str(state), "LINEAR_AGENT_TEST_MODE": "1"}

            apply_result = subprocess.run(
                [str(BIN), "graph-apply", "--from", str(plan), "--apply-linear"],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                check=False,
            )
            self.assertEqual(apply_result.returncode, 0, apply_result.stderr)
            payload = json.loads(state.read_text(encoding="utf-8"))
            payload["issues"]["MAS-1"]["title"] = "Drifted"
            payload["issues"]["MAS-1"]["description"] = "Missing actionability"
            state.write_text(json.dumps(payload), encoding="utf-8")

            readback = subprocess.run(
                [str(BIN), "graph-readback", "--from", str(plan), "--json"],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                check=False,
            )

            self.assertEqual(readback.returncode, 1)
            drift = json.loads(readback.stdout)["drift"]
            fields = {item["field"]: item["actual"] for item in drift}
            self.assertEqual(fields["title"], "Drifted")
            self.assertEqual(fields["description"], "Missing actionability")

    def test_allocate_writes_ledger_rows_and_json_sidecar(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            plan = self.write_plan(tmp)
            ledger = tmp / "EXECUTION.md"
            init = self.run_cli("init", "--ledger", str(ledger), "--project", "Alloc", "--prompt", "test")
            self.assertEqual(init.returncode, 0, init.stderr)

            result = self.run_cli("allocate", "--from", str(plan), "--ledger", str(ledger))

            self.assertEqual(result.returncode, 0, result.stderr)
            text = ledger.read_text(encoding="utf-8")
            self.assertIn("| MAS-1 | Codex | agent/mas-1-define-schema |", text)
            self.assertTrue((tmp / "EXECUTION.state.json").exists())

    def test_validate_ledger_detects_missing_sidecar(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            ledger = Path(raw) / "EXECUTION.md"
            ledger.write_text("# Test\n\n## Issue Progress\n\n| Issue | Linear Status | Agent State | Owner/Agent | Worktree | Last Update | Verification |\n|---|---|---|---|---|---|---|\n", encoding="utf-8")

            result = self.run_cli("validate-ledger", "--ledger", str(ledger))

            self.assertEqual(result.returncode, 1)
            self.assertIn("missing sidecar", result.stdout)

    def test_inventory_and_smoke_dry_run_are_local_only(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            (tmp / "package.json").write_text("{}", encoding="utf-8")
            (tmp / "auth.ts").write_text("// auth", encoding="utf-8")

            inventory = self.run_cli("inventory", "--repo", str(tmp), "--json")
            smoke = self.run_cli("smoke", "--project", "Disposable", "--json")

            self.assertEqual(inventory.returncode, 0, inventory.stderr)
            self.assertEqual(smoke.returncode, 0, smoke.stderr)
            self.assertFalse(json.loads(smoke.stdout)["applied"])

    def test_smoke_fake_apply_records_run(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            state = tmp / "linear-state.json"
            state.write_text("{}", encoding="utf-8")
            env = {**os.environ, "LINEAR_AGENT_FAKE_STATE": str(state), "LINEAR_AGENT_TEST_MODE": "1"}

            result = subprocess.run(
                [str(BIN), "smoke", "--project", "Disposable", "--apply-linear", "--json"],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["smokeRuns"], 1)
            payload = json.loads(state.read_text(encoding="utf-8"))
            self.assertEqual(payload["smokeRuns"][0]["project"], "Disposable")

    def test_discover_propose_records_continuous_discovery_row(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            ledger = Path(raw) / "EXECUTION.md"
            init = self.run_cli("init", "--ledger", str(ledger), "--project", "Discovery", "--prompt", "test")
            self.assertEqual(init.returncode, 0, init.stderr)

            result = self.run_cli(
                "discover",
                "--classification",
                "QA gap",
                "--surfaced-by",
                "MAS-123",
                "--reason",
                "Need live graph-readback coverage",
                "--acceptance",
                "Read-back drift is reported",
                "--ledger",
                str(ledger),
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            text = ledger.read_text(encoding="utf-8")
            self.assertIn("QA gap", text)
            self.assertIn("Need live graph-readback coverage", text)
            self.assertIn("proposed", text)


if __name__ == "__main__":
    unittest.main()
