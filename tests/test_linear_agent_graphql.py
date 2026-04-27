from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHONPATH = str(ROOT / "lib")
sys.path.insert(0, PYTHONPATH)


def fake_state(path: Path, state_name: str = "Todo") -> None:
    path.write_text(
        json.dumps(
            {
                "states": [
                    {"id": "todo", "name": "Todo", "type": "unstarted", "team": {"id": "team-mas", "key": "MAS"}},
                    {"id": "in-progress", "name": "In Progress", "type": "started", "team": {"id": "team-mas", "key": "MAS"}},
                    {"id": "done", "name": "Done", "type": "completed", "team": {"id": "team-mas", "key": "MAS"}},
                ],
                "issues": {
                    "MAS-123": {
                        "id": "issue-123",
                        "identifier": "MAS-123",
                        "title": "Example",
                        "description": "",
                        "url": "https://linear.app/example/MAS-123",
                        "state": {"id": state_name.lower().replace(" ", "-"), "name": state_name, "type": "started"},
                        "team": {"id": "team-mas", "key": "MAS", "name": "Master Group Holdings"},
                        "project": {"id": "project", "name": "Project", "url": "https://linear.app/project"},
                        "comments": {"nodes": []},
                        "updatedAt": "2026-04-28T00:00:00+10:00",
                    }
                },
            }
        ),
        encoding="utf-8",
    )


class LinearAgentGraphQLTests(unittest.TestCase):
    def run_module(self, *args: str, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
        merged_env = {
            key: value
            for key, value in os.environ.items()
            if not key.startswith("LINEAR_")
        }
        merged_env.update(env)
        merged_env["PYTHONPATH"] = PYTHONPATH
        return subprocess.run(
            [sys.executable, "-m", "linear_agent.graphql", *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=merged_env,
            check=False,
        )

    def test_apply_transition_updates_state_comments_and_readback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state_path = Path(tmp) / "state.json"
            requests_path = Path(tmp) / "requests.jsonl"
            fake_state(state_path, "Todo")

            result = self.run_module(
                "apply-transition",
                "--issue",
                "MAS-123",
                "--state",
                "In Progress",
                "--comment",
                "Started work",
                "--action",
                "start",
                env={
                    "LINEAR_AGENT_TEST_MODE": "1",
                    "LINEAR_AGENT_FAKE_STATE": str(state_path),
                    "LINEAR_AGENT_FAKE_REQUESTS": str(requests_path),
                    "LINEAR_AGENT_NOW": "2026-04-28T10:00:00+10:00",
                },
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Applied Linear transition: MAS-123 -> In Progress", result.stdout)
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(state["issues"]["MAS-123"]["state"]["name"], "In Progress")
            comments = state["issues"]["MAS-123"]["comments"]["nodes"]
            self.assertEqual(len(comments), 1)
            self.assertIn("linear-agent:start:MAS-123", comments[0]["body"])
            operations = [
                json.loads(line)["operationName"]
                for line in requests_path.read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual(
                operations,
                [
                    "IssueByIdentifier",
                    "WorkflowStates",
                    "IssueStateUpdate",
                    "CommentCreate",
                    "IssueByIdentifier",
                ],
            )

    def test_missing_credentials_fail_cleanly(self) -> None:
        result = self.run_module(
            "apply-transition",
            "--issue",
            "MAS-123",
            "--state",
            "Done",
            "--comment",
            "Done",
            "--action",
            "complete",
            env={"LINEAR_API_KEY": "", "LINEAR_ACCESS_TOKEN": ""},
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("Missing Linear credentials", result.stderr)

    def test_fake_transport_requires_explicit_test_mode_even_with_credentials(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state_path = Path(tmp) / "state.json"
            fake_state(state_path, "Todo")

            result = self.run_module(
                "apply-transition",
                "--issue",
                "MAS-123",
                "--state",
                "Done",
                "--comment",
                "Done",
                "--action",
                "complete",
                env={
                    "LINEAR_AGENT_FAKE_STATE": str(state_path),
                    "LINEAR_API_KEY": "real-token-placeholder",
                },
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("LINEAR_AGENT_FAKE_STATE is test-only", result.stderr)

    def test_state_id_override_skips_state_lookup(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state_path = Path(tmp) / "state.json"
            requests_path = Path(tmp) / "requests.jsonl"
            fake_state(state_path, "Todo")

            result = self.run_module(
                "apply-transition",
                "--issue",
                "MAS-123",
                "--state",
                "In Progress",
                "--comment",
                "Started work",
                "--action",
                "start",
                env={
                    "LINEAR_AGENT_TEST_MODE": "1",
                    "LINEAR_AGENT_FAKE_STATE": str(state_path),
                    "LINEAR_AGENT_FAKE_REQUESTS": str(requests_path),
                    "LINEAR_STATE_IN_PROGRESS": "in-progress",
                },
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            operations = [
                json.loads(line)["operationName"]
                for line in requests_path.read_text(encoding="utf-8").splitlines()
            ]
            self.assertNotIn("WorkflowStates", operations)

    def test_reconcile_accepts_custom_state_id_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state_path = Path(tmp) / "state.json"
            ledger_path = Path(tmp) / "EXECUTION.md"
            fake_state(state_path, "Doing")
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["states"].append(
                {"id": "doing", "name": "Doing", "type": "started", "team": {"id": "team-mas", "key": "MAS"}}
            )
            state["issues"]["MAS-123"]["state"] = {
                "id": "doing",
                "name": "Doing",
                "type": "started",
            }
            state_path.write_text(json.dumps(state), encoding="utf-8")
            ledger_path.write_text(
                """# Ledger

## Issue Progress

| Issue | Linear Status | Agent State | Owner/Agent | Worktree | Last Update | Verification |
|---|---|---|---|---|---|---|
| MAS-123 | In Progress | agent:executing | Codex | /tmp/wt | now | tests |

## Decisions
""",
                encoding="utf-8",
            )

            result = self.run_module(
                "reconcile",
                "--ledger",
                str(ledger_path),
                env={
                    "LINEAR_AGENT_TEST_MODE": "1",
                    "LINEAR_AGENT_FAKE_STATE": str(state_path),
                    "LINEAR_STATE_IN_PROGRESS": "doing",
                },
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("state-id override", result.stdout)

    def test_reconcile_reports_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state_path = Path(tmp) / "state.json"
            ledger_path = Path(tmp) / "EXECUTION.md"
            fake_state(state_path, "In Progress")
            ledger_path.write_text(
                """# Ledger

## Issue Progress

| Issue | Linear Status | Agent State | Owner/Agent | Worktree | Last Update | Verification |
|---|---|---|---|---|---|---|
| MAS-123 | Done | agent:pr-ready | Codex | /tmp/wt | now | tests |

## Decisions
""",
                encoding="utf-8",
            )

            result = self.run_module(
                "reconcile",
                "--ledger",
                str(ledger_path),
                env={
                    "LINEAR_AGENT_TEST_MODE": "1",
                    "LINEAR_AGENT_FAKE_STATE": str(state_path),
                },
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("mismatch | MAS-123 | ledger=Done | linear=In Progress", result.stdout)

    def test_reconcile_empty_ledger_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state_path = Path(tmp) / "state.json"
            ledger_path = Path(tmp) / "EXECUTION.md"
            fake_state(state_path, "In Progress")
            ledger_path.write_text(
                """# Ledger

## Issue Progress

| Issue | Linear Status | Agent State | Owner/Agent | Worktree | Last Update | Verification |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

## Decisions
""",
                encoding="utf-8",
            )

            result = self.run_module(
                "reconcile",
                "--ledger",
                str(ledger_path),
                env={
                    "LINEAR_AGENT_TEST_MODE": "1",
                    "LINEAR_AGENT_FAKE_STATE": str(state_path),
                },
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("empty | ledger has no issue rows", result.stdout)

    def test_rejects_unsafe_endpoint_override_by_default(self) -> None:
        result = self.run_module(
            "apply-transition",
            "--issue",
            "MAS-123",
            "--state",
            "Done",
            "--comment",
            "Done",
            "--action",
            "complete",
            env={
                "LINEAR_API_KEY": "real-token-placeholder",
                "LINEAR_API_URL": "http://example.test/graphql",
            },
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("LINEAR_API_URL must use https", result.stderr)

    def test_comment_failure_reports_partial_apply_recovery_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            state_path = Path(tmp) / "state.json"
            fake_state(state_path, "Todo")
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["fail_on"] = "CommentCreate"
            state_path.write_text(json.dumps(state), encoding="utf-8")

            result = self.run_module(
                "apply-transition",
                "--issue",
                "MAS-123",
                "--state",
                "In Progress",
                "--comment",
                "Started work",
                "--action",
                "start",
                env={
                    "LINEAR_AGENT_TEST_MODE": "1",
                    "LINEAR_AGENT_FAKE_STATE": str(state_path),
                },
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("post-update confirmation failed", result.stderr)
            self.assertIn("Run linear-agent reconcile", result.stderr)
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(state["issues"]["MAS-123"]["state"]["name"], "In Progress")

    def test_ledger_row_parser_respects_escaped_pipes(self) -> None:
        from linear_agent.ledger import existing_worktree, parse_issue_rows, unfinished_issue_rows

        with tempfile.TemporaryDirectory() as tmp:
            ledger_path = Path(tmp) / "EXECUTION.md"
            ledger_path.write_text(
                """# Ledger

## Issue Progress

| Issue | Linear Status | Agent State | Owner/Agent | Worktree | Last Update | Verification |
|---|---|---|---|---|---|---|
| MAS-123 | Done | agent:pr-ready | Codex | /tmp/example\\|worktree | now | npm test: pass \\| lint: pass<br>second line |

## Decisions
""",
                encoding="utf-8",
            )

            rows = parse_issue_rows(ledger_path)

            self.assertEqual(rows[0].worktree, "/tmp/example|worktree")
            self.assertEqual(rows[0].verification, "npm test: pass | lint: pass\nsecond line")
            self.assertEqual(existing_worktree(ledger_path, "MAS-123"), "/tmp/example|worktree")
            self.assertEqual(unfinished_issue_rows(ledger_path), [])


if __name__ == "__main__":
    unittest.main()
