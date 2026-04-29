from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


class GraphPlanError(ValueError):
    """Raised when a Linear graph plan is invalid."""


@dataclass(frozen=True)
class GraphIssue:
    key: str
    identifier: str = ""
    title: str = ""
    description: str = ""
    parent: str = ""
    milestone: str = ""
    labels: list[str] = field(default_factory=list)
    links: list[dict[str, str]] = field(default_factory=list)
    blocks: list[str] = field(default_factory=list)
    blocked_by: list[str] = field(default_factory=list)
    related: list[str] = field(default_factory=list)
    duplicates: list[str] = field(default_factory=list)
    duplicate_of: list[str] = field(default_factory=list)
    write_set: list[str] = field(default_factory=list)
    serial: bool = False


@dataclass(frozen=True)
class GraphPlan:
    project: dict[str, Any]
    labels: list[str]
    milestones: list[str]
    issues: list[GraphIssue]


def load_graph_plan(path: Path) -> GraphPlan:
    raw = _load_mapping(path)
    project = raw.get("project") or {}
    issues = [
        GraphIssue(
            key=str(item.get("key") or item.get("id") or ""),
            identifier=str(item.get("identifier") or ""),
            title=str(item.get("title") or ""),
            description=str(item.get("description") or item.get("body") or ""),
            parent=str(item.get("parent") or item.get("parentKey") or ""),
            milestone=str(item.get("milestone") or ""),
            labels=list(item.get("labels") or []),
            links=_load_links(item.get("links") or []),
            blocks=list(item.get("blocks") or []),
            blocked_by=list(item.get("blockedBy") or item.get("blocked_by") or []),
            related=list(item.get("related") or item.get("relatedTo") or item.get("related_to") or []),
            duplicates=list(item.get("duplicates") or []),
            duplicate_of=list(item.get("duplicateOf") or item.get("duplicate_of") or []),
            write_set=list(item.get("writeSet") or item.get("write_set") or []),
            serial=bool(item.get("serial") or item.get("serialRequired")),
        )
        for item in raw.get("issues", [])
    ]
    plan = GraphPlan(
        project=project,
        labels=list(raw.get("labels") or []),
        milestones=list(raw.get("milestones") or []),
        issues=issues,
    )
    validate_graph_plan(plan)
    return plan


def _load_mapping(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        payload = json.loads(text)
    else:
        try:
            import yaml  # type: ignore

            payload = yaml.safe_load(text)
        except Exception as exc:
            raise GraphPlanError(
                "YAML graph plans require PyYAML. Use JSON or install PyYAML."
            ) from exc
    if not isinstance(payload, dict):
        raise GraphPlanError("graph plan must be a mapping")
    return payload


def _load_links(raw_links: Any) -> list[dict[str, str]]:
    if not isinstance(raw_links, list):
        raise GraphPlanError("issue links must be a list")
    links: list[dict[str, str]] = []
    for raw_link in raw_links:
        if not isinstance(raw_link, dict):
            raise GraphPlanError("issue links must be objects with title and url")
        title = str(raw_link.get("title") or "")
        url = str(raw_link.get("url") or "")
        if not title or not url:
            raise GraphPlanError("issue links require title and url")
        links.append({"title": title, "url": url})
    return links


def validate_graph_plan(plan: GraphPlan) -> None:
    if not plan.project.get("name"):
        raise GraphPlanError("project.name is required")
    seen: set[str] = set()
    for issue in plan.issues:
        if not issue.key:
            raise GraphPlanError("issue key is required")
        if not issue.title:
            raise GraphPlanError(f"{issue.key}: title is required")
        if issue.key in seen:
            raise GraphPlanError(f"duplicate issue key: {issue.key}")
        seen.add(issue.key)
    for issue in plan.issues:
        refs = [issue.parent, *issue.blocks, *issue.blocked_by, *issue.related, *issue.duplicates, *issue.duplicate_of]
        for ref in refs:
            if ref and ref not in seen:
                raise GraphPlanError(f"{issue.key}: unknown issue reference {ref}")
    _detect_dependency_cycles(plan)


def _detect_dependency_cycles(plan: GraphPlan) -> None:
    graph = {issue.key: set(issue.blocks) for issue in plan.issues}
    for issue in plan.issues:
        for blocker in issue.blocked_by:
            graph.setdefault(blocker, set()).add(issue.key)
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            raise GraphPlanError(f"dependency cycle includes {node}")
        if node in visited:
            return
        visiting.add(node)
        for child in graph.get(node, set()):
            visit(child)
        visiting.remove(node)
        visited.add(node)

    for key in graph:
        visit(key)


def graph_summary(plan: GraphPlan) -> dict[str, Any]:
    parent_count = len([issue for issue in plan.issues if not issue.parent])
    child_count = len([issue for issue in plan.issues if issue.parent])
    edge_count = sum(
        len(issue.blocks)
        + len(issue.blocked_by)
        + len(issue.related)
        + len(issue.duplicates)
        + len(issue.duplicate_of)
        for issue in plan.issues
    )
    described_count = len([issue for issue in plan.issues if issue.description.strip()])
    link_count = sum(len(issue.links) for issue in plan.issues)
    return {
        "project": plan.project.get("name", ""),
        "labels": len(plan.labels),
        "milestones": len(plan.milestones),
        "issues": len(plan.issues),
        "parents": parent_count,
        "children": child_count,
        "dependencyEdges": edge_count,
        "describedIssues": described_count,
        "links": link_count,
    }


def plan_to_dict(plan: GraphPlan) -> dict[str, Any]:
    return {
        "project": plan.project,
        "labels": plan.labels,
        "milestones": plan.milestones,
        "issues": [issue.__dict__ for issue in plan.issues],
        "summary": graph_summary(plan),
    }


def render_graph_plan(plan: GraphPlan) -> str:
    summary = graph_summary(plan)
    lines = [
        f"Graph plan: {summary['project']}",
        f"- labels: {summary['labels']}",
        f"- milestones: {summary['milestones']}",
        f"- issues: {summary['issues']} ({summary['parents']} parents, {summary['children']} children)",
        f"- dependency edges: {summary['dependencyEdges']}",
        "",
        "Issues:",
    ]
    for issue in plan.issues:
        parent = f" parent={issue.parent}" if issue.parent else ""
        milestone = f" milestone={issue.milestone}" if issue.milestone else ""
        blocked = f" blockedBy={','.join(issue.blocked_by)}" if issue.blocked_by else ""
        blocks = f" blocks={','.join(issue.blocks)}" if issue.blocks else ""
        related = f" related={','.join(issue.related)}" if issue.related else ""
        duplicates = f" duplicates={','.join(issue.duplicates)}" if issue.duplicates else ""
        duplicate_of = f" duplicateOf={','.join(issue.duplicate_of)}" if issue.duplicate_of else ""
        described = " described=yes" if issue.description.strip() else " described=no"
        links = f" links={len(issue.links)}" if issue.links else ""
        lines.append(
            f"- {issue.key}: {issue.title}{parent}{milestone}{blocked}{blocks}"
            f"{related}{duplicates}{duplicate_of}{described}{links}"
        )
    return "\n".join(lines)


def allocate_lanes(plan: GraphPlan, base_worktree: str = "../linear-agent-worktrees") -> dict[str, Any]:
    ready: list[dict[str, Any]] = []
    blocked: list[dict[str, Any]] = []
    by_key = {issue.key: issue for issue in plan.issues}
    blocked_targets = {target for issue in plan.issues for target in issue.blocks}
    for issue in plan.issues:
        blockers = set(issue.blocked_by)
        blockers.update(key for key, other in by_key.items() if issue.key in other.blocks)
        lane = {
            "issue": issue.key,
            "branch": f"agent/{issue.key.lower()}-{slug(issue.title)}",
            "worktree": f"{base_worktree}/{issue.key.lower()}",
            "writeSet": issue.write_set,
            "mergeAfter": sorted(blockers),
            "serial": issue.serial or bool(blockers),
        }
        if blockers or issue.key in blocked_targets or issue.serial:
            blocked.append(lane)
        else:
            ready.append(lane)
    conflicts = overlapping_write_sets(ready)
    return {"ready": ready, "blocked": blocked, "conflicts": conflicts}


def overlapping_write_sets(lanes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    conflicts: list[dict[str, Any]] = []
    for index, left in enumerate(lanes):
        for right in lanes[index + 1 :]:
            overlap = sorted(set(left.get("writeSet") or []) & set(right.get("writeSet") or []))
            if overlap:
                conflicts.append(
                    {
                        "left": left["issue"],
                        "right": right["issue"],
                        "writeSet": overlap,
                    }
                )
    return conflicts


def render_allocation(allocation: dict[str, Any]) -> str:
    lines = ["Parallel allocation:"]
    for group in ("ready", "blocked"):
        lines.append(f"{group.title()} lanes:")
        for lane in allocation[group]:
            lines.append(
                f"- {lane['issue']} branch={lane['branch']} worktree={lane['worktree']} "
                f"writeSet={','.join(lane.get('writeSet') or ['<review-required>'])}"
            )
    if allocation["conflicts"]:
        lines.append("Conflicts:")
        for conflict in allocation["conflicts"]:
            lines.append(
                f"- {conflict['left']} overlaps {conflict['right']}: "
                f"{', '.join(conflict['writeSet'])}"
            )
    return "\n".join(lines)


def allocation_markdown_rows(allocation: dict[str, Any]) -> list[str]:
    rows: list[str] = []
    for status, lanes in (("ready", allocation["ready"]), ("blocked", allocation["blocked"])):
        for lane in lanes:
            rows.append(
                "| {issue} | Codex | {branch} | {worktree} | {write_set} | {status} | {merge} |".format(
                    issue=lane["issue"],
                    branch=lane["branch"],
                    worktree=lane["worktree"],
                    write_set=", ".join(lane.get("writeSet") or ["review required"]),
                    status=status,
                    merge=", ".join(lane.get("mergeAfter") or ["none"]),
                )
            )
    return rows


def slug(text: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return value[:48] or "issue"
