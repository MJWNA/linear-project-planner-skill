from __future__ import annotations

import json
import os
import random
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
        for attempt in range(6):
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
                if exc.code == 429 and attempt < 5:
                    sleep_with_jitter(attempt)
                    continue
                raise LinearAgentError(f"Linear HTTP {exc.code}: {redact_secrets(detail)}") from exc
            except urllib.error.URLError as exc:
                raise LinearAgentError(f"Linear request failed: {redact_secrets(str(exc.reason))}") from exc

            if payload.get("errors"):
                errors = payload["errors"]
                if is_rate_limited(errors) and attempt < 5:
                    sleep_with_jitter(attempt)
                    continue
                raise LinearAgentError(f"Linear GraphQL errors: {redact_secrets(str(errors))}")
            break

        data = payload.get("data")
        if not isinstance(data, dict):
            raise LinearAgentError("Linear response missing data object")
        return GraphQLResponse(data=data)


def is_rate_limited(errors: Any) -> bool:
    if not isinstance(errors, list):
        return False
    for error in errors:
        extensions = error.get("extensions", {}) if isinstance(error, dict) else {}
        code = str(extensions.get("code", "")).upper()
        if code == "RATELIMITED" or "RATE" in code:
            return True
        if "rate limit" in str(error).lower():
            return True
    return False


def sleep_with_jitter(attempt: int) -> None:
    delay = min(8.0, 0.5 * (2**attempt)) + random.uniform(0, 0.25)
    time.sleep(delay)


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

        if operation_name == "Teams":
            return GraphQLResponse(data={"teams": {"nodes": self._teams()}})

        if operation_name == "ProjectByName":
            project = self._project_by_name(variables["teamId"], variables["name"])
            return GraphQLResponse(data={"team": {"projects": {"nodes": [project] if project else []}}})

        if operation_name == "ProjectCreate":
            team_id = variables["input"]["teamIds"][0]
            project = {
                "id": variables["input"].get("id") or f"project-{len(self.state.setdefault('projects', [])) + 1}",
                "name": variables["input"]["name"],
                "description": variables["input"].get("description") or "",
                "url": f"https://linear.app/example/project/{slug_id(variables['input']['name'])}",
                "teams": {"nodes": [self._team(team_id)]},
            }
            self.state.setdefault("projects", []).append(project)
            self._write_state()
            return GraphQLResponse(data={"projectCreate": {"success": True, "project": project}})

        if operation_name == "ProjectUpdate":
            project = self._project_by_id(variables["id"])
            project.update({key: value for key, value in variables["input"].items() if value is not None})
            self._write_state()
            return GraphQLResponse(data={"projectUpdate": {"success": True, "project": project}})

        if operation_name == "LabelsByTeam":
            team_id = variables["teamId"]
            labels = [
                label for label in self.state.setdefault("labels", [])
                if label.get("team", {}).get("id") == team_id
                and label.get("name", "").lower() == variables["name"].lower()
            ]
            return GraphQLResponse(data={"team": {"labels": {"nodes": labels}}})

        if operation_name == "IssueLabelCreate":
            label = {
                "id": variables["input"].get("id") or f"label-{len(self.state.setdefault('labels', [])) + 1}",
                "name": variables["input"]["name"],
                "description": variables["input"].get("description") or "",
                "color": variables["input"].get("color") or "#bec2c8",
                "team": self._team(variables["input"].get("teamId") or self._teams()[0]["id"]),
            }
            self.state.setdefault("labels", []).append(label)
            self._write_state()
            return GraphQLResponse(data={"issueLabelCreate": {"success": True, "issueLabel": label}})

        if operation_name == "IssueLabelUpdate":
            label = self._label_by_id(variables["id"])
            label.update({key: value for key, value in variables["input"].items() if value is not None})
            self._write_state()
            return GraphQLResponse(data={"issueLabelUpdate": {"success": True, "issueLabel": label}})

        if operation_name == "ProjectMilestonesByProject":
            milestones = [
                milestone for milestone in self.state.setdefault("milestones", [])
                if milestone.get("project", {}).get("id") == variables["projectId"]
                and milestone.get("name", "").lower() == variables["name"].lower()
            ]
            return GraphQLResponse(data={"project": {"projectMilestones": {"nodes": milestones}}})

        if operation_name == "ProjectMilestoneCreate":
            milestone = {
                "id": variables["input"].get("id") or f"milestone-{len(self.state.setdefault('milestones', [])) + 1}",
                "name": variables["input"]["name"],
                "description": variables["input"].get("description") or "",
                "project": self._project_by_id(variables["input"]["projectId"]),
            }
            self.state.setdefault("milestones", []).append(milestone)
            self._write_state()
            return GraphQLResponse(data={"projectMilestoneCreate": {"success": True, "projectMilestone": milestone}})

        if operation_name == "ProjectMilestoneUpdate":
            milestone = self._milestone_by_id(variables["id"])
            milestone.update({key: value for key, value in variables["input"].items() if value is not None})
            self._write_state()
            return GraphQLResponse(data={"projectMilestoneUpdate": {"success": True, "projectMilestone": milestone}})

        if operation_name == "IssueByTitle":
            team_id = variables["teamId"]
            issues = [
                issue for issue in self.state.setdefault("issues", {}).values()
                if issue.get("team", {}).get("id") == team_id
                and issue.get("title", "").lower() == variables["title"].lower()
            ]
            return GraphQLResponse(data={"team": {"issues": {"nodes": issues}}})

        if operation_name == "IssueCreate":
            team = self._team(variables["input"]["teamId"])
            number = len(self.state.setdefault("issues", {})) + 1
            identifier = variables["input"].get("id") or f"{team.get('key', 'MAS')}-{number}"
            issue = self._issue_from_input(identifier, variables["input"])
            self.state.setdefault("issues", {})[identifier] = issue
            self._write_state()
            return GraphQLResponse(data={"issueCreate": {"success": True, "issue": issue}})

        if operation_name == "IssueUpdate":
            issue = self._issue_by_internal_id(variables["id"])
            self._apply_issue_input(issue, variables["input"])
            self._write_state()
            return GraphQLResponse(data={"issueUpdate": {"success": True, "issue": issue}})

        if operation_name == "IssueRelationCreate":
            relations = self.state.setdefault("relations", [])
            relation = {
                "id": variables["input"].get("id") or f"relation-{len(relations) + 1}",
                "type": variables["input"]["type"],
                "issue": self._issue_by_internal_id(variables["input"]["issueId"]),
                "relatedIssue": self._issue_by_internal_id(variables["input"]["relatedIssueId"]),
            }
            relations.append(relation)
            self._write_state()
            return GraphQLResponse(data={"issueRelationCreate": {"success": True, "issueRelation": relation}})

        if operation_name == "AttachmentCreate":
            attachments = self.state.setdefault("attachments", [])
            attachment = {
                "id": variables["input"].get("id") or f"attachment-{len(attachments) + 1}",
                "title": variables["input"]["title"],
                "url": variables["input"]["url"],
                "issue": self._issue_by_internal_id(variables["input"]["issueId"]),
            }
            attachments.append(attachment)
            self._write_state()
            return GraphQLResponse(data={"attachmentCreate": {"success": True, "attachment": attachment}})

        if operation_name == "AttachmentUpdate":
            attachment = self._attachment_by_id(variables["id"])
            attachment.update({key: value for key, value in variables["input"].items() if value is not None})
            self._write_state()
            return GraphQLResponse(data={"attachmentUpdate": {"success": True, "attachment": attachment}})

        if operation_name == "ProjectReadback":
            project = self._project_by_name_or_id(variables["project"])
            issues = [
                self._issue_with_edges(issue)
                for issue in self.state.setdefault("issues", {}).values()
                if issue.get("project", {}).get("id") == project["id"]
            ]
            first = variables.get("first") or 250
            return GraphQLResponse(
                data={
                    "project": {
                        **project,
                        "issues": {
                            "nodes": issues[:first],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        },
                    }
                }
            )

        if operation_name == "ProjectArchive":
            project = self._project_by_id(variables["id"])
            project["archivedAt"] = self._now()
            self._write_state()
            return GraphQLResponse(data={"projectArchive": {"success": True}})

        if operation_name == "IssueArchive":
            issue = self._issue(variables["id"])
            issue["archivedAt"] = self._now()
            self._write_state()
            return GraphQLResponse(data={"issueArchive": {"success": True}})

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

    def _teams(self) -> list[dict[str, Any]]:
        teams = self.state.setdefault(
            "teams",
            [{"id": "team-mas", "key": "MAS", "name": "Master Group Holdings"}],
        )
        return teams

    def _team(self, team_id: str) -> dict[str, Any]:
        for team in self._teams():
            if team.get("id") == team_id or team.get("key") == team_id or team.get("name") == team_id:
                return team
        raise LinearAgentError(f"Linear team not found: {team_id}")

    def _project_by_name(self, team_id: str, name: str) -> dict[str, Any] | None:
        for project in self.state.setdefault("projects", []):
            team_ids = {team.get("id") for team in project.get("teams", {}).get("nodes", [])}
            if team_id in team_ids and project.get("name", "").lower() == name.lower():
                return project
        return None

    def _project_by_id(self, project_id: str) -> dict[str, Any]:
        for project in self.state.setdefault("projects", []):
            if project.get("id") == project_id:
                return project
        raise LinearAgentError(f"Linear project not found: {project_id}")

    def _project_by_name_or_id(self, value: str) -> dict[str, Any]:
        for project in self.state.setdefault("projects", []):
            if project.get("id") == value or project.get("name") == value:
                return project
        raise LinearAgentError(f"Linear project not found: {value}")

    def _label_by_id(self, label_id: str) -> dict[str, Any]:
        for label in self.state.setdefault("labels", []):
            if label.get("id") == label_id:
                return label
        raise LinearAgentError(f"Linear label not found: {label_id}")

    def _milestone_by_id(self, milestone_id: str) -> dict[str, Any]:
        for milestone in self.state.setdefault("milestones", []):
            if milestone.get("id") == milestone_id:
                return milestone
        raise LinearAgentError(f"Linear milestone not found: {milestone_id}")

    def _issue_by_internal_id(self, issue_id: str) -> dict[str, Any]:
        for issue in self.state.setdefault("issues", {}).values():
            if issue.get("id") == issue_id:
                return issue
        raise LinearAgentError(f"Linear issue not found: {issue_id}")

    def _attachment_by_id(self, attachment_id: str) -> dict[str, Any]:
        for attachment in self.state.setdefault("attachments", []):
            if attachment.get("id") == attachment_id:
                return attachment
        raise LinearAgentError(f"Linear attachment not found: {attachment_id}")

    def _issue_from_input(self, identifier: str, values: dict[str, Any]) -> dict[str, Any]:
        team = self._team(values["teamId"])
        issue = {
            "id": f"issue-{identifier.lower()}",
            "identifier": identifier,
            "title": values.get("title") or "",
            "description": values.get("description") or "",
            "url": f"https://linear.app/example/{identifier}",
            "state": {"id": "todo", "name": "Todo", "type": "unstarted"},
            "team": team,
            "project": self._project_by_id(values["projectId"]) if values.get("projectId") else None,
            "projectMilestone": self._milestone_by_id(values["projectMilestoneId"]) if values.get("projectMilestoneId") else None,
            "parent": self._issue_by_internal_id(values["parentId"]) if values.get("parentId") else None,
            "labels": {"nodes": [self._label_by_id(label_id) for label_id in values.get("labelIds") or []]},
            "comments": {"nodes": []},
            "updatedAt": self._now(),
        }
        return self._issue_with_edges(issue)

    def _apply_issue_input(self, issue: dict[str, Any], values: dict[str, Any]) -> None:
        for field in ("title", "description"):
            if field in values:
                issue[field] = values[field]
        if "projectId" in values:
            issue["project"] = self._project_by_id(values["projectId"]) if values["projectId"] else None
        if "projectMilestoneId" in values:
            issue["projectMilestone"] = self._milestone_by_id(values["projectMilestoneId"]) if values["projectMilestoneId"] else None
        if "parentId" in values:
            issue["parent"] = self._issue_by_internal_id(values["parentId"]) if values["parentId"] else None
        if "labelIds" in values:
            issue["labels"] = {"nodes": [self._label_by_id(label_id) for label_id in values.get("labelIds") or []]}
        issue["updatedAt"] = self._now()

    def _issue_with_edges(self, issue: dict[str, Any]) -> dict[str, Any]:
        issue["relations"] = {
            "nodes": [
                relation for relation in self.state.setdefault("relations", [])
                if relation.get("issue", {}).get("id") == issue.get("id")
            ]
        }
        issue["attachments"] = {
            "nodes": [
                attachment for attachment in self.state.setdefault("attachments", [])
                if attachment.get("issue", {}).get("id") == issue.get("id")
            ]
        }
        issue.setdefault("labels", {"nodes": []})
        return issue

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

    def teams(self) -> list[dict[str, Any]]:
        response = self.transport.execute("Teams", TEAMS, {})
        return response.data.get("teams", {}).get("nodes", [])

    def resolve_team(self, project: dict[str, Any] | None = None) -> dict[str, Any]:
        project = project or {}
        wanted = project.get("teamId") or project.get("team_id") or project.get("teamKey") or project.get("team")
        teams = self.teams()
        if wanted:
            matches = [
                team for team in teams
                if wanted in {team.get("id"), team.get("key"), team.get("name")}
            ]
            if len(matches) == 1:
                return matches[0]
            raise LinearAgentError(f"Could not resolve Linear team {wanted!r}: {len(matches)} matches")
        if len(teams) == 1:
            return teams[0]
        raise LinearAgentError("Project graph needs project.teamId or project.teamKey when multiple Linear teams are visible")

    def project_by_name(self, team_id: str, name: str) -> dict[str, Any] | None:
        response = self.transport.execute(
            "ProjectByName",
            PROJECT_BY_NAME,
            {"teamId": team_id, "name": name},
        )
        nodes = response.data.get("team", {}).get("projects", {}).get("nodes", [])
        return nodes[0] if nodes else None

    def ensure_project(self, team_id: str, project: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        name = project["name"]
        description = project.get("description") or project.get("content") or ""
        current = self.project_by_name(team_id, name)
        if not current:
            response = self.transport.execute(
                "ProjectCreate",
                PROJECT_CREATE,
                {"input": compact({"name": name, "description": description, "teamIds": [team_id]})},
            )
            created = mutation_payload(response, "projectCreate", "project")
            read_back = self.project_by_name(team_id, name)
            if not read_back:
                raise LinearAgentError(f"Linear project read-back failed after create: {name}")
            return "created", created
        changes = {}
        if description and current.get("description", "") != description:
            changes["description"] = description
        if not changes:
            return "reused", current
        response = self.transport.execute(
            "ProjectUpdate",
            PROJECT_UPDATE,
            {"id": current["id"], "input": changes},
        )
        updated = mutation_payload(response, "projectUpdate", "project")
        read_back = self.project_by_name(team_id, name)
        if not read_back or read_back.get("description", "") != description:
            raise LinearAgentError(f"Linear project read-back mismatch after update: {name}")
        return "updated", updated

    def label_by_name(self, team_id: str, name: str) -> dict[str, Any] | None:
        response = self.transport.execute(
            "LabelsByTeam",
            LABELS_BY_TEAM,
            {"teamId": team_id, "name": name},
        )
        nodes = response.data.get("team", {}).get("labels", {}).get("nodes", [])
        return nodes[0] if nodes else None

    def ensure_label(self, team_id: str, label: str | dict[str, Any]) -> tuple[str, dict[str, Any]]:
        data = {"name": label} if isinstance(label, str) else dict(label)
        name = data["name"]
        description = data.get("description") or ""
        color = data.get("color") or "#bec2c8"
        current = self.label_by_name(team_id, name)
        if not current:
            response = self.transport.execute(
                "IssueLabelCreate",
                ISSUE_LABEL_CREATE,
                {"input": compact({"name": name, "description": description, "color": color, "teamId": team_id})},
            )
            created = mutation_payload(response, "issueLabelCreate", "issueLabel")
            return "created", created
        changes = {}
        if "description" in data and current.get("description", "") != description:
            changes["description"] = description
        if "color" in data and current.get("color") != color:
            changes["color"] = color
        if not changes:
            return "reused", current
        response = self.transport.execute(
            "IssueLabelUpdate",
            ISSUE_LABEL_UPDATE,
            {"id": current["id"], "input": changes},
        )
        return "updated", mutation_payload(response, "issueLabelUpdate", "issueLabel")

    def milestone_by_name(self, project_id: str, name: str) -> dict[str, Any] | None:
        response = self.transport.execute(
            "ProjectMilestonesByProject",
            PROJECT_MILESTONES_BY_PROJECT,
            {"projectId": project_id, "name": name},
        )
        nodes = response.data.get("project", {}).get("projectMilestones", {}).get("nodes", [])
        return nodes[0] if nodes else None

    def ensure_milestone(self, project_id: str, milestone: str | dict[str, Any]) -> tuple[str, dict[str, Any]]:
        data = {"name": milestone} if isinstance(milestone, str) else dict(milestone)
        name = data["name"]
        description = data.get("description") or ""
        current = self.milestone_by_name(project_id, name)
        if not current:
            response = self.transport.execute(
                "ProjectMilestoneCreate",
                PROJECT_MILESTONE_CREATE,
                {"input": compact({"name": name, "description": description, "projectId": project_id})},
            )
            return "created", mutation_payload(response, "projectMilestoneCreate", "projectMilestone")
        changes = {}
        if "description" in data and current.get("description", "") != description:
            changes["description"] = description
        if not changes:
            return "reused", current
        response = self.transport.execute(
            "ProjectMilestoneUpdate",
            PROJECT_MILESTONE_UPDATE,
            {"id": current["id"], "input": changes},
        )
        return "updated", mutation_payload(response, "projectMilestoneUpdate", "projectMilestone")

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

    def issue_by_title(self, team_id: str, title: str) -> dict[str, Any] | None:
        response = self.transport.execute(
            "IssueByTitle",
            ISSUE_BY_TITLE,
            {"teamId": team_id, "title": title},
        )
        nodes = response.data.get("team", {}).get("issues", {}).get("nodes", [])
        return nodes[0] if nodes else None

    def ensure_issue(
        self,
        team_id: str,
        project_id: str,
        issue: dict[str, Any],
        labels: dict[str, dict[str, Any]],
        milestones: dict[str, dict[str, Any]],
        issues_by_key: dict[str, dict[str, Any]],
    ) -> tuple[str, dict[str, Any]]:
        current = None
        identifier = issue.get("identifier") or ""
        if identifier:
            try:
                current = self.issue(identifier)
            except LinearAgentError:
                current = None
        if not current:
            current = self.issue_by_title(team_id, issue["title"])

        label_ids = [labels[name]["id"] for name in issue.get("labels", []) if name in labels]
        milestone = milestones.get(issue.get("milestone", ""))
        parent = issues_by_key.get(issue.get("parent", ""))
        wanted = {
            "teamId": team_id,
            "projectId": project_id,
            "title": issue["title"],
            "description": issue.get("description") or "",
            "labelIds": label_ids,
            "projectMilestoneId": milestone.get("id") if milestone else None,
            "parentId": parent.get("id") if parent else None,
        }
        wanted = {key: value for key, value in wanted.items() if value is not None}
        if not current:
            response = self.transport.execute("IssueCreate", ISSUE_CREATE, {"input": wanted})
            created = mutation_payload(response, "issueCreate", "issue")
            return "created", created

        changes = issue_update_changes(current, wanted)
        if not changes:
            return "reused", current
        response = self.transport.execute(
            "IssueUpdate",
            ISSUE_UPDATE,
            {"id": current["id"], "input": changes},
        )
        updated = mutation_payload(response, "issueUpdate", "issue")
        read_back = self.issue(updated["identifier"])
        if read_back.get("title") != issue["title"]:
            raise LinearAgentError(f"Linear issue read-back mismatch after update: {issue['title']}")
        return "updated", read_back

    def ensure_relation(self, issue: dict[str, Any], related: dict[str, Any], relation_type: str) -> tuple[str, dict[str, Any]]:
        for relation in issue.get("relations", {}).get("nodes", []):
            if (
                relation.get("type") == relation_type
                and relation.get("relatedIssue", {}).get("id") == related["id"]
            ):
                return "reused", relation
        response = self.transport.execute(
            "IssueRelationCreate",
            ISSUE_RELATION_CREATE,
            {"input": {"issueId": issue["id"], "relatedIssueId": related["id"], "type": relation_type}},
        )
        return "created", mutation_payload(response, "issueRelationCreate", "issueRelation")

    def ensure_attachment(self, issue: dict[str, Any], link: dict[str, str]) -> tuple[str, dict[str, Any]]:
        for attachment in issue.get("attachments", {}).get("nodes", []):
            if attachment.get("url") == link["url"]:
                if attachment.get("title") == link["title"]:
                    return "reused", attachment
                response = self.transport.execute(
                    "AttachmentUpdate",
                    ATTACHMENT_UPDATE,
                    {"id": attachment["id"], "input": {"title": link["title"]}},
                )
                return "updated", mutation_payload(response, "attachmentUpdate", "attachment")
        response = self.transport.execute(
            "AttachmentCreate",
            ATTACHMENT_CREATE,
            {"input": {"issueId": issue["id"], "title": link["title"], "url": link["url"]}},
        )
        return "created", mutation_payload(response, "attachmentCreate", "attachment")

    def project_readback(self, project: str, first: int = 50, after: str | None = None) -> dict[str, Any]:
        response = self.transport.execute(
            "ProjectReadback",
            PROJECT_READBACK,
            {"project": project, "first": first, "after": after},
        )
        return response.data.get("project") or {}

    def archive_project(self, project_id: str) -> None:
        response = self.transport.execute(
            "ProjectArchive",
            PROJECT_ARCHIVE,
            {"id": project_id},
        )
        payload = response.data.get("projectArchive", {})
        if not payload.get("success"):
            raise LinearAgentError("Linear projectArchive returned success=false")

    def archive_issue(self, issue_id: str) -> None:
        response = self.transport.execute(
            "IssueArchive",
            ISSUE_ARCHIVE,
            {"id": issue_id},
        )
        payload = response.data.get("issueArchive", {})
        if not payload.get("success"):
            raise LinearAgentError("Linear issueArchive returned success=false")


def compact(values: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in values.items() if value not in (None, "")}


def mutation_payload(response: GraphQLResponse, mutation: str, entity: str) -> dict[str, Any]:
    payload = response.data.get(mutation, {})
    if not payload.get("success"):
        raise LinearAgentError(f"Linear {mutation} returned success=false")
    item = payload.get(entity)
    if not item:
        raise LinearAgentError(f"Linear {mutation} response missing {entity}")
    return item


def issue_update_changes(current: dict[str, Any], wanted: dict[str, Any]) -> dict[str, Any]:
    changes: dict[str, Any] = {}
    if current.get("title") != wanted.get("title"):
        changes["title"] = wanted.get("title")
    if (current.get("description") or "") != wanted.get("description"):
        changes["description"] = wanted.get("description", "")
    if wanted.get("projectId") and (current.get("project") or {}).get("id") != wanted.get("projectId"):
        changes["projectId"] = wanted.get("projectId")
    if (current.get("projectMilestone") or {}).get("id") != wanted.get("projectMilestoneId"):
        changes["projectMilestoneId"] = wanted.get("projectMilestoneId")
    if (current.get("parent") or {}).get("id") != wanted.get("parentId"):
        changes["parentId"] = wanted.get("parentId")
    current_labels = sorted(label.get("id") for label in current.get("labels", {}).get("nodes", []))
    wanted_labels = sorted(wanted.get("labelIds") or [])
    if current_labels != wanted_labels:
        changes["labelIds"] = wanted_labels
    return {key: value for key, value in changes.items() if value is not None}


def apply_graph(plan: dict[str, Any]) -> dict[str, Any]:
    client = LinearClient.from_env()
    team = client.resolve_team(plan.get("project") or {})
    summary: dict[str, dict[str, int]] = {
        "project": {"created": 0, "reused": 0, "updated": 0, "skipped": 0},
        "labels": {"created": 0, "reused": 0, "updated": 0, "skipped": 0},
        "milestones": {"created": 0, "reused": 0, "updated": 0, "skipped": 0},
        "issues": {"created": 0, "reused": 0, "updated": 0, "skipped": 0},
        "relations": {"created": 0, "reused": 0, "updated": 0, "skipped": 0},
        "attachments": {"created": 0, "reused": 0, "updated": 0, "skipped": 0},
    }

    project_status, project = client.ensure_project(team["id"], plan["project"])
    summary["project"][project_status] += 1

    labels: dict[str, dict[str, Any]] = {}
    for label in plan.get("labels", []):
        status, item = client.ensure_label(team["id"], label)
        labels[item["name"]] = item
        summary["labels"][status] += 1

    milestones: dict[str, dict[str, Any]] = {}
    for milestone in plan.get("milestones", []):
        status, item = client.ensure_milestone(project["id"], milestone)
        milestones[item["name"]] = item
        summary["milestones"][status] += 1

    issues_by_key: dict[str, dict[str, Any]] = {}
    for issue in plan.get("issues", []):
        if issue.get("parent"):
            continue
        status, item = client.ensure_issue(team["id"], project["id"], issue, labels, milestones, issues_by_key)
        issues_by_key[issue["key"]] = item
        summary["issues"][status] += 1

    for issue in plan.get("issues", []):
        if not issue.get("parent"):
            continue
        status, item = client.ensure_issue(team["id"], project["id"], issue, labels, milestones, issues_by_key)
        issues_by_key[issue["key"]] = item
        summary["issues"][status] += 1

    for issue in plan.get("issues", []):
        source = issues_by_key[issue["key"]]
        for target_key in issue.get("blocks", []):
            status, _ = client.ensure_relation(source, issues_by_key[target_key], "blocks")
            summary["relations"][status] += 1
        for blocker_key in issue.get("blocked_by", []):
            status, _ = client.ensure_relation(issues_by_key[blocker_key], source, "blocks")
            summary["relations"][status] += 1
        for link in issue.get("links", []):
            if not is_allowed_attachment_url(link["url"]):
                summary["attachments"]["skipped"] += 1
                continue
            status, _ = client.ensure_attachment(source, link)
            summary["attachments"][status] += 1

    read_back = client.project_readback(project["id"])
    if not read_back.get("id"):
        raise LinearAgentError(f"Linear project read-back failed after graph apply: {project['name']}")
    return {
        "project": project,
        "team": team,
        "summary": summary,
        "issues": {key: {"id": item["id"], "identifier": item["identifier"], "url": item.get("url", "")} for key, item in issues_by_key.items()},
    }


def readback_graph(plan: dict[str, Any]) -> list[dict[str, Any]]:
    client = LinearClient.from_env()
    project_id = plan["project"].get("id")
    if not project_id:
        team = client.resolve_team(plan.get("project") or {})
        project = client.project_by_name(team["id"], plan["project"]["name"])
        project_id = project.get("id") if project else ""
    read_back = client.project_readback(project_id)
    if not read_back:
        return [{"scope": "project", "field": "exists", "expected": "present", "actual": "missing"}]
    return live_graph_drift(read_back, plan)


def live_graph_drift(read_back: dict[str, Any], plan: dict[str, Any]) -> list[dict[str, Any]]:
    drift: list[dict[str, Any]] = []
    if read_back.get("name") != plan["project"].get("name"):
        drift.append({"scope": "project", "field": "name", "expected": plan["project"].get("name"), "actual": read_back.get("name")})
    issues = {issue.get("title"): issue for issue in read_back.get("issues", {}).get("nodes", [])}
    issues_by_identifier = {
        issue.get("identifier"): issue
        for issue in read_back.get("issues", {}).get("nodes", [])
    }
    for expected in plan.get("issues", []):
        actual = issues_by_identifier.get(expected.get("identifier") or "") or issues.get(expected["title"])
        if not actual:
            drift.append({"issue": expected["key"], "field": "exists", "expected": "present", "actual": "missing"})
            continue
        if actual.get("title") != expected.get("title"):
            drift.append({"issue": expected["key"], "field": "title", "expected": expected.get("title"), "actual": actual.get("title")})
        actual_description = actual.get("description") or ""
        expected_description = expected.get("description", "")
        if not descriptions_match(expected_description, actual_description):
            drift.append({"issue": expected["key"], "field": "description", "expected": expected_description, "actual": actual_description})
        expected_labels = sorted(expected.get("labels", []))
        actual_labels = sorted(label.get("name") for label in actual.get("labels", {}).get("nodes", []))
        if expected_labels != actual_labels:
            drift.append({"issue": expected["key"], "field": "labels", "expected": expected_labels, "actual": actual_labels})
    return drift


def slug_id(value: str) -> str:
    return "".join(char.lower() if char.isalnum() else "-" for char in value).strip("-")


def is_allowed_attachment_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def descriptions_match(expected: str, actual: str) -> bool:
    if expected == actual:
        return True
    if not expected.strip():
        return not actual.strip()
    headings = [line.strip() for line in expected.splitlines() if line.startswith("## ")]
    if headings and all(heading in actual for heading in headings):
        return True
    return False


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


def redact_secrets(value: str) -> str:
    redacted = value
    for token in (os.environ.get("LINEAR_API_KEY"), os.environ.get("LINEAR_ACCESS_TOKEN")):
        if token:
            redacted = redacted.replace(token, "[REDACTED]")
    return redacted


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


ISSUE_FIELDS = """
fragment IssueFields on Issue {
  id
  identifier
  title
  description
  url
  state { id name type }
  team { id key name }
  project { id name url }
  projectMilestone { id name }
  parent { id identifier title }
  labels(first: 100) { nodes { id name color description team { id key name } } }
  relations(first: 100) {
    nodes {
      id
      type
      issue { id identifier title }
      relatedIssue { id identifier title }
    }
  }
  attachments(first: 100) {
    nodes { id title url }
  }
  comments(first: 20) {
    nodes { id body createdAt user { id name } }
  }
  updatedAt
}
"""

TEAMS = """
query Teams {
  teams(first: 100) {
    nodes { id key name }
  }
}
"""

PROJECT_BY_NAME = """
query ProjectByName($teamId: String!, $name: String!) {
  team(id: $teamId) {
    projects(first: 20, filter: { name: { eqIgnoreCase: $name } }) {
      nodes {
        id
        name
        description
        url
        teams(first: 20) { nodes { id key name } }
      }
    }
  }
}
"""

PROJECT_CREATE = """
mutation ProjectCreate($input: ProjectCreateInput!) {
  projectCreate(input: $input) {
    success
    project {
      id
      name
      description
      url
      teams(first: 20) { nodes { id key name } }
    }
  }
}
"""

PROJECT_UPDATE = """
mutation ProjectUpdate($id: String!, $input: ProjectUpdateInput!) {
  projectUpdate(id: $id, input: $input) {
    success
    project {
      id
      name
      description
      url
      teams(first: 20) { nodes { id key name } }
    }
  }
}
"""

LABELS_BY_TEAM = """
query LabelsByTeam($teamId: String!, $name: String!) {
  team(id: $teamId) {
    labels(first: 20, filter: { name: { eqIgnoreCase: $name } }) {
      nodes { id name description color team { id key name } }
    }
  }
}
"""

ISSUE_LABEL_CREATE = """
mutation IssueLabelCreate($input: IssueLabelCreateInput!) {
  issueLabelCreate(input: $input) {
    success
    issueLabel { id name description color team { id key name } }
  }
}
"""

ISSUE_LABEL_UPDATE = """
mutation IssueLabelUpdate($id: String!, $input: IssueLabelUpdateInput!) {
  issueLabelUpdate(id: $id, input: $input) {
    success
    issueLabel { id name description color team { id key name } }
  }
}
"""

PROJECT_MILESTONES_BY_PROJECT = """
query ProjectMilestonesByProject($projectId: String!, $name: String!) {
  project(id: $projectId) {
    projectMilestones(first: 20, filter: { name: { eqIgnoreCase: $name } }) {
      nodes { id name description project { id name url } }
    }
  }
}
"""

PROJECT_MILESTONE_CREATE = """
mutation ProjectMilestoneCreate($input: ProjectMilestoneCreateInput!) {
  projectMilestoneCreate(input: $input) {
    success
    projectMilestone { id name description project { id name url } }
  }
}
"""

PROJECT_MILESTONE_UPDATE = """
mutation ProjectMilestoneUpdate($id: String!, $input: ProjectMilestoneUpdateInput!) {
  projectMilestoneUpdate(id: $id, input: $input) {
    success
    projectMilestone { id name description project { id name url } }
  }
}
"""

ISSUE_BY_TITLE = """
query IssueByTitle($teamId: String!, $title: String!) {
  team(id: $teamId) {
    issues(first: 20, filter: { title: { eqIgnoreCase: $title } }) {
      nodes { ...IssueFields }
    }
  }
}
""" + ISSUE_FIELDS

ISSUE_CREATE = """
mutation IssueCreate($input: IssueCreateInput!) {
  issueCreate(input: $input) {
    success
    issue { ...IssueFields }
  }
}
""" + ISSUE_FIELDS

ISSUE_UPDATE = """
mutation IssueUpdate($id: String!, $input: IssueUpdateInput!) {
  issueUpdate(id: $id, input: $input) {
    success
    issue { ...IssueFields }
  }
}
""" + ISSUE_FIELDS

ISSUE_RELATION_CREATE = """
mutation IssueRelationCreate($input: IssueRelationCreateInput!) {
  issueRelationCreate(input: $input) {
    success
    issueRelation {
      id
      type
      issue { id identifier title }
      relatedIssue { id identifier title }
    }
  }
}
"""

ATTACHMENT_CREATE = """
mutation AttachmentCreate($input: AttachmentCreateInput!) {
  attachmentCreate(input: $input) {
    success
    attachment { id title url issue { id identifier title } }
  }
}
"""

ATTACHMENT_UPDATE = """
mutation AttachmentUpdate($id: String!, $input: AttachmentUpdateInput!) {
  attachmentUpdate(id: $id, input: $input) {
    success
    attachment { id title url issue { id identifier title } }
  }
}
"""

PROJECT_READBACK = """
query ProjectReadback($project: String!, $first: Int!, $after: String) {
  project(id: $project) {
    id
    name
    description
    url
    issues(first: $first, after: $after) {
      nodes {
        id
        identifier
        title
        description
        url
        state { id name type }
        team { id key name }
        project { id name url }
        projectMilestone { id name }
        parent { id identifier title }
        labels(first: 15) { nodes { id name color description } }
        relations(first: 10) {
          nodes {
            id
            type
            issue { id identifier title }
            relatedIssue { id identifier title }
          }
        }
        attachments(first: 10) { nodes { id title url } }
      }
      pageInfo { hasNextPage endCursor }
    }
  }
}
"""

PROJECT_ARCHIVE = """
mutation ProjectArchive($id: String!) {
  projectArchive(id: $id) {
    success
  }
}
"""

ISSUE_ARCHIVE = """
mutation IssueArchive($id: String!) {
  issueArchive(id: $id) {
    success
  }
}
"""

ISSUE_BY_IDENTIFIER = """
query IssueByIdentifier($id: String!) {
  issue(id: $id) { ...IssueFields }
}
""" + ISSUE_FIELDS

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
