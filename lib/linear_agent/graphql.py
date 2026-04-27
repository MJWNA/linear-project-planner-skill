from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from urllib.parse import urlparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .ledger import parse_issue_rows


DEFAULT_API_URL = "https://api.linear.app/graphql"


class LinearAgentError(RuntimeError):
    """Raised for recoverable Linear automation failures."""


@dataclass
class GraphQLResponse:
    data: dict[str, Any]


class GraphQLTransport:
    def execute(
        self,
        operation_name: str,
        query: str,
        variables: dict[str, Any],
    ) -> GraphQLResponse:
        raise NotImplementedError


class HttpGraphQLTransport(GraphQLTransport):
    def __init__(self, api_url: str, token: str, token_kind: str) -> None:
        self.api_url = api_url
        self.token = token
        self.token_kind = token_kind

    def execute(
        self,
        operation_name: str,
        query: str,
        variables: dict[str, Any],
    ) -> GraphQLResponse:
        auth = self.token
        if self.token_kind == "oauth":
            auth = f"Bearer {self.token}"

        body = json.dumps(
            {
                "operationName": operation_name,
                "query": query,
                "variables": variables,
            }
        ).encode("utf-8")
        request = urllib.request.Request(
            self.api_url,
            data=body,
            headers={
                "Authorization": auth,
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise LinearAgentError(f"Linear HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise LinearAgentError(f"Linear request failed: {exc.reason}") from exc

        if payload.get("errors"):
            raise LinearAgentError(f"Linear GraphQL errors: {payload['errors']}")

        data = payload.get("data")
        if not isinstance(data, dict):
            raise LinearAgentError("Linear response missing data object")
        return GraphQLResponse(data=data)


class FakeGraphQLTransport(GraphQLTransport):
    """Stateful fake transport for deterministic local tests."""

    def __init__(self, state_path: Path, requests_path: Path | None = None) -> None:
        self.state_path = state_path
        self.requests_path = requests_path
        self.state = self._read_state()

    def _read_state(self) -> dict[str, Any]:
        if not self.state_path.is_file():
            raise LinearAgentError(f"Fake Linear state not found: {self.state_path}")
        return json.loads(self.state_path.read_text(encoding="utf-8"))

    def _write_state(self) -> None:
        self.state_path.write_text(
            json.dumps(self.state, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def _record_request(self, operation_name: str, variables: dict[str, Any]) -> None:
        if not self.requests_path:
            return
        self.requests_path.parent.mkdir(parents=True, exist_ok=True)
        with self.requests_path.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    {
                        "operationName": operation_name,
                        "variables": variables,
                    },
                    sort_keys=True,
                )
                + "\n"
            )

    def execute(
        self,
        operation_name: str,
        query: str,
        variables: dict[str, Any],
    ) -> GraphQLResponse:
        del query
        self._record_request(operation_name, variables)

        fail_on = self.state.get("fail_on")
        if fail_on == operation_name:
            raise LinearAgentError(f"Fake Linear failure for {operation_name}")

        if operation_name == "IssueByIdentifier":
            issue = self._issue(variables["id"])
            return GraphQLResponse(data={"issue": issue})

        if operation_name == "WorkflowStates":
            team_id = variables["teamId"]
            states = [
                state
                for state in self.state.get("states", [])
                if state.get("team", {}).get("id") == team_id
            ]
            return GraphQLResponse(data={"workflowStates": {"nodes": states}})

        if operation_name == "IssueStateUpdate":
            issue = self._issue(variables["issueId"])
            state = self._state(variables["stateId"])
            issue["state"] = state
            issue["updatedAt"] = self._now()
            self._write_state()
            return GraphQLResponse(data={"issueUpdate": {"success": True, "issue": issue}})

        if operation_name == "CommentCreate":
            issue = self._issue(variables["issueId"])
            comments = issue.setdefault("comments", {"nodes": []})["nodes"]
            comment = {
                "id": f"comment-{len(comments) + 1}",
                "body": variables["body"],
                "createdAt": self._now(),
                "issue": {"id": issue["id"], "identifier": issue["identifier"]},
            }
            comments.append(comment)
            self._write_state()
            return GraphQLResponse(
                data={"commentCreate": {"success": True, "comment": comment}}
            )

        raise LinearAgentError(f"Fake transport does not implement {operation_name}")

    def _issue(self, identifier: str) -> dict[str, Any]:
        issue = self.state.get("issues", {}).get(identifier)
        if issue is None:
            raise LinearAgentError(f"Linear issue not found: {identifier}")
        return issue

    def _state(self, state_id: str) -> dict[str, Any]:
        for state in self.state.get("states", []):
            if state.get("id") == state_id:
                return state
        raise LinearAgentError(f"Linear state not found: {state_id}")

    def _now(self) -> str:
        return os.environ.get("LINEAR_AGENT_NOW", "2026-04-28T00:00:00+10:00")


class LinearClient:
    def __init__(self, transport: GraphQLTransport) -> None:
        self.transport = transport

    @classmethod
    def from_env(cls) -> "LinearClient":
        fake_state = os.environ.get("LINEAR_AGENT_FAKE_STATE")
        if fake_state:
            if os.environ.get("LINEAR_AGENT_TEST_MODE") != "1":
                raise LinearAgentError(
                    "LINEAR_AGENT_FAKE_STATE is test-only. Set "
                    "LINEAR_AGENT_TEST_MODE=1 for local fake transport tests, "
                    "or unset LINEAR_AGENT_FAKE_STATE before using real Linear."
                )
            requests_path = os.environ.get("LINEAR_AGENT_FAKE_REQUESTS")
            return cls(
                FakeGraphQLTransport(
                    Path(fake_state),
                    Path(requests_path) if requests_path else None,
                )
            )

        token = os.environ.get("LINEAR_API_KEY")
        token_kind = "api_key"
        if not token:
            token = os.environ.get("LINEAR_ACCESS_TOKEN")
            token_kind = "oauth"
        if not token:
            raise LinearAgentError(
                "Missing Linear credentials. Set LINEAR_API_KEY or LINEAR_ACCESS_TOKEN, "
                "or use dry-run mode."
            )

        api_url = validated_api_url(os.environ.get("LINEAR_API_URL", DEFAULT_API_URL))
        return cls(HttpGraphQLTransport(api_url, token, token_kind))

    def issue(self, issue_id: str) -> dict[str, Any]:
        response = self.transport.execute(
            "IssueByIdentifier",
            ISSUE_BY_IDENTIFIER,
            {"id": issue_id},
        )
        issue = response.data.get("issue")
        if not issue:
            raise LinearAgentError(f"Linear issue not found: {issue_id}")
        return issue

    def state_by_name(self, team_id: str, name: str) -> dict[str, Any]:
        override = state_override(name)
        if override:
            return {"id": override, "name": name, "type": "custom", "team": {"id": team_id}}

        response = self.transport.execute(
            "WorkflowStates",
            WORKFLOW_STATES,
            {"teamId": team_id},
        )
        states = response.data.get("workflowStates", {}).get("nodes", [])
        exact = [state for state in states if state.get("name") == name]
        if len(exact) == 1:
            return exact[0]
        casefolded = [state for state in states if state.get("name", "").lower() == name.lower()]
        if len(casefolded) == 1:
            return casefolded[0]
        raise LinearAgentError(
            f"Could not resolve Linear state {name!r} for team {team_id}: "
            f"{len(casefolded) or len(exact)} matches"
        )

    def update_issue_state(self, issue_id: str, state_id: str) -> dict[str, Any]:
        response = self.transport.execute(
            "IssueStateUpdate",
            ISSUE_STATE_UPDATE,
            {"issueId": issue_id, "stateId": state_id},
        )
        payload = response.data.get("issueUpdate", {})
        if not payload.get("success"):
            raise LinearAgentError("Linear issueUpdate returned success=false")
        issue = payload.get("issue")
        if not issue:
            raise LinearAgentError("Linear issueUpdate response missing issue")
        return issue

    def create_comment(self, issue_id: str, body: str) -> dict[str, Any]:
        response = self.transport.execute(
            "CommentCreate",
            COMMENT_CREATE,
            {"issueId": issue_id, "body": body},
        )
        payload = response.data.get("commentCreate", {})
        if not payload.get("success"):
            raise LinearAgentError("Linear commentCreate returned success=false")
        comment = payload.get("comment")
        if not comment:
            raise LinearAgentError("Linear commentCreate response missing comment")
        return comment


def state_override(name: str) -> str:
    key = "LINEAR_STATE_" + "".join(
        char if char.isalnum() else "_" for char in name.upper()
    ).strip("_")
    return os.environ.get(key, "")


def validated_api_url(api_url: str) -> str:
    parsed = urlparse(api_url)
    if parsed.scheme != "https":
        if os.environ.get("LINEAR_AGENT_ALLOW_UNSAFE_API_URL") == "1":
            return api_url
        raise LinearAgentError(
            "LINEAR_API_URL must use https. Set "
            "LINEAR_AGENT_ALLOW_UNSAFE_API_URL=1 only for intentional local testing."
        )
    if parsed.hostname != "api.linear.app":
        if os.environ.get("LINEAR_AGENT_ALLOW_NON_LINEAR_API_URL") == "1":
            return api_url
        raise LinearAgentError(
            "LINEAR_API_URL must point to api.linear.app unless "
            "LINEAR_AGENT_ALLOW_NON_LINEAR_API_URL=1 is set intentionally."
        )
    return api_url


def apply_transition(issue_id: str, state_name: str, comment: str, action: str) -> None:
    client = LinearClient.from_env()
    issue = client.issue(issue_id)
    team = issue.get("team") or {}
    team_id = team.get("id")
    if not team_id:
        raise LinearAgentError(f"Linear issue {issue_id} has no team id")

    state = client.state_by_name(team_id, state_name)
    updated = client.update_issue_state(issue_id, state["id"])
    marker = f"<!-- linear-agent:{action}:{issue_id}:{int(time.time())} -->"
    try:
        client.create_comment(issue_id, f"{comment}\n\n{marker}")
        read_back = client.issue(issue_id)
    except LinearAgentError as exc:
        observed = "<unknown>"
        try:
            read_back = client.issue(issue_id)
            observed = read_back.get("state", {}).get("name", "<unknown>")
        except LinearAgentError:
            pass
        raise LinearAgentError(
            f"Linear state update may have succeeded for {issue_id}, but "
            f"post-update confirmation failed: {exc}. Observed state after "
            f"recovery read-back: {observed}. Run linear-agent reconcile before "
            "confirming the ledger."
        ) from exc
    observed = read_back.get("state", {}).get("id")
    if observed != state["id"]:
        raise LinearAgentError(
            f"Linear read-back mismatch for {issue_id}: expected state "
            f"{state_name!r} ({state['id']}), observed {read_back.get('state')}"
        )
    print(
        f"Applied Linear transition: {issue_id} -> "
        f"{updated.get('state', {}).get('name', state_name)}"
    )


def reconcile(ledger: Path) -> int:
    client = LinearClient.from_env()
    rows = parse_issue_rows(ledger)
    if not rows:
        print("empty | ledger has no issue rows")
        print("Reconcile complete: 0 match, 0 mismatch")
        return 1

    mismatches = 0
    for row in rows:
        try:
            issue = client.issue(row.issue)
            state = issue.get("state", {})
            observed = state.get("name", "")
        except LinearAgentError as exc:
            mismatches += 1
            print(f"missing | {row.issue} | {exc}")
            continue
        expected_override = state_override(row.linear_status)
        if expected_override and state.get("id") == expected_override:
            print(
                f"match | {row.issue} | {observed} "
                f"(ledger={row.linear_status}, state-id override)"
            )
            continue
        if observed != row.linear_status:
            mismatches += 1
            print(
                f"mismatch | {row.issue} | ledger={row.linear_status} | "
                f"linear={observed}"
            )
        else:
            print(f"match | {row.issue} | {observed}")
    print(f"Reconcile complete: {len(rows) - mismatches} match, {mismatches} mismatch")
    return 1 if mismatches else 0


ISSUE_BY_IDENTIFIER = """
query IssueByIdentifier($id: String!) {
  issue(id: $id) {
    id
    identifier
    title
    description
    url
    state { id name type }
    team { id key name }
    project { id name url }
    comments(first: 20) {
      nodes { id body createdAt user { id name } }
    }
    updatedAt
  }
}
"""

WORKFLOW_STATES = """
query WorkflowStates($teamId: ID!) {
  workflowStates(first: 100, filter: { team: { id: { eq: $teamId } } }) {
    nodes { id name type team { id key } }
  }
}
"""

ISSUE_STATE_UPDATE = """
mutation IssueStateUpdate($issueId: String!, $stateId: String!) {
  issueUpdate(id: $issueId, input: { stateId: $stateId }) {
    success
    issue { id identifier state { id name type } updatedAt }
  }
}
"""

COMMENT_CREATE = """
mutation CommentCreate($issueId: String!, $body: String!) {
  commentCreate(input: { issueId: $issueId, body: $body }) {
    success
    comment { id body createdAt issue { id identifier } }
  }
}
"""


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print("Usage: python -m linear_agent.graphql <apply-transition|reconcile> ...", file=sys.stderr)
        return 2

    command = args.pop(0)
    values: dict[str, str] = {}
    while args:
        flag = args.pop(0)
        if not flag.startswith("--") or not args:
            print(f"Invalid argument: {flag}", file=sys.stderr)
            return 2
        values[flag[2:].replace("-", "_")] = args.pop(0)

    try:
        if command == "apply-transition":
            apply_transition(
                values["issue"],
                values["state"],
                values["comment"],
                values.get("action", "transition"),
            )
            return 0
        if command == "reconcile":
            return reconcile(Path(values["ledger"]))
    except KeyError as exc:
        print(f"Missing required option: --{str(exc).strip(chr(39)).replace('_', '-')}", file=sys.stderr)
        return 2
    except LinearAgentError as exc:
        print(f"Linear automation failed: {exc}", file=sys.stderr)
        return 1

    print(f"Unknown command: {command}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
