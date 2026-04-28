from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


@dataclass(frozen=True)
class LedgerIssueRow:
    issue: str
    linear_status: str
    agent_state: str
    agent: str
    worktree: str
    last_update: str
    verification: str


def configured_timezone() -> str:
    return os.environ.get("LINEAR_AGENT_TIMEZONE", "Australia/Brisbane")


def timestamp() -> str:
    tz_name = configured_timezone()
    try:
        tz = ZoneInfo(tz_name)
    except Exception:
        tz = ZoneInfo("Australia/Brisbane")
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")


def escape_table_cell(value: str | None) -> str:
    value = value or ""
    return (
        value.replace("\\", "\\\\")
        .replace("\r", "")
        .replace("\n", "<br>")
        .replace("|", "\\|")
    )


def state_sidecar_path(path: Path) -> Path:
    return path.with_name(f"{path.stem}.state.json")


def split_markdown_row(line: str) -> list[str]:
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    content = line.strip()
    if content.startswith("|"):
        content = content[1:]
    if content.endswith("|"):
        content = content[:-1]

    for char in content:
        if escaped:
            current.append(char)
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == "|":
            cells.append("".join(current).strip().replace("<br>", "\n"))
            current = []
            continue
        current.append(char)

    if escaped:
        current.append("\\")
    cells.append("".join(current).strip().replace("<br>", "\n"))
    return cells


def parse_issue_rows(path: Path) -> list[LedgerIssueRow]:
    rows: list[LedgerIssueRow] = []
    in_table = False

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line == "## Issue Progress":
            in_table = True
            continue
        if in_table and line.startswith("## "):
            break
        if not in_table or not line.startswith("|"):
            continue
        if line.startswith("|---") or line.startswith("| Issue "):
            continue

        cells = split_markdown_row(line)
        if len(cells) < 7 or not cells[0]:
            continue
        rows.append(
            LedgerIssueRow(
                issue=cells[0],
                linear_status=cells[1],
                agent_state=cells[2],
                agent=cells[3],
                worktree=cells[4],
                last_update=cells[5],
                verification=cells[6],
            )
        )

    return rows


def replace_line(path: Path, prefix: str, replacement: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    changed = False
    next_lines: list[str] = []
    for line in lines:
        if line.startswith(prefix):
            next_lines.append(replacement)
            changed = True
        else:
            next_lines.append(line)
    if not changed:
        next_lines.append(replacement)
    path.write_text("\n".join(next_lines) + "\n", encoding="utf-8")


def append_activity(path: Path, message: str) -> None:
    content = path.read_text(encoding="utf-8")
    if "## Activity Log" not in content:
        content = content.rstrip() + "\n\n## Activity Log\n\n"
    lines = content.splitlines()
    out: list[str] = []
    in_activity = False
    for line in lines:
        if line == "## Activity Log":
            in_activity = True
            out.append(line)
            continue
        if in_activity and line.startswith("## "):
            in_activity = False
        if in_activity and line == "- TBD":
            continue
        out.append(line)
    out.append(f"- {timestamp()} - {message}")
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def remove_empty_issue_row(path: Path) -> None:
    lines = [
        line
        for line in path.read_text(encoding="utf-8").splitlines()
        if line != "|  |  |  |  |  |  |  |"
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def upsert_issue_row(
    path: Path,
    issue: str,
    linear_status: str,
    agent_state: str,
    agent: str,
    worktree: str,
    verification: str,
) -> None:
    remove_empty_issue_row(path)
    row = (
        f"| {escape_table_cell(issue)} | {escape_table_cell(linear_status)} | "
        f"{escape_table_cell(agent_state)} | {escape_table_cell(agent)} | "
        f"{escape_table_cell(worktree)} | {timestamp()} | "
        f"{escape_table_cell(verification)} |"
    )
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    replaced = False
    inserted = False
    in_issue_table = False
    for line in lines:
        if line == "## Issue Progress":
            in_issue_table = True
            out.append(line)
            continue
        if in_issue_table and line.startswith("## "):
            if not replaced and not inserted:
                out.append(row)
                inserted = True
            in_issue_table = False
        if in_issue_table and line.startswith(f"| {issue} |"):
            out.append(row)
            replaced = True
            continue
        out.append(line)
    if not replaced and not inserted:
        out.append(row)
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def set_check_item(path: Path, label: str, marker: str, replacement: str) -> None:
    out: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("- [") and len(line) > 6:
            text = line[6:]
            if text.startswith(label):
                out.append(f"- [{marker}] {replacement}")
                continue
        out.append(line)
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def get_prefixed_value(path: Path, prefix: str) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith(prefix):
            return line[len(prefix) :].strip()
    return ""


def write_state_sidecar(path: Path) -> Path:
    rows = parse_issue_rows(path)
    payload = {
        "ledger": str(path),
        "updatedAt": timestamp(),
        "timezone": configured_timezone(),
        "currentState": {
            "overallStatus": get_prefixed_value(path, "- Overall status:"),
            "activeIssue": get_prefixed_value(path, "- Active issue:"),
            "activeAgent": get_prefixed_value(path, "- Active agent:"),
            "activeWorktree": get_prefixed_value(path, "- Active worktree:"),
            "nextSafestAction": get_prefixed_value(path, "- Next safest action:"),
            "validationMode": get_prefixed_value(path, "- Validation mode:"),
        },
        "issues": [row.__dict__ for row in rows],
    }
    sidecar = state_sidecar_path(path)
    sidecar.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return sidecar


def validate_ledger(path: Path) -> list[str]:
    problems: list[str] = []
    sidecar = state_sidecar_path(path)
    rows = parse_issue_rows(path)
    if not sidecar.exists():
        problems.append(f"missing sidecar: {sidecar}")
        return problems
    payload = json.loads(sidecar.read_text(encoding="utf-8"))
    sidecar_issues = payload.get("issues", [])
    if len(sidecar_issues) != len(rows):
        problems.append(
            f"issue row count mismatch: markdown={len(rows)} sidecar={len(sidecar_issues)}"
        )
    sidecar_by_issue = {item.get("issue"): item for item in sidecar_issues}
    for row in rows:
        item = sidecar_by_issue.get(row.issue)
        if not item:
            problems.append(f"sidecar missing issue row: {row.issue}")
            continue
        if item.get("linear_status") != row.linear_status:
            problems.append(f"status mismatch for {row.issue}")
    return problems


def existing_worktree(path: Path, issue: str) -> str:
    for row in parse_issue_rows(path):
        if row.issue == issue:
            return row.worktree
    return ""


def unfinished_issue_rows(path: Path) -> list[str]:
    unfinished: list[str] = []
    for row in parse_issue_rows(path):
        if row.linear_status not in {"Done", "Completed"}:
            unfinished.append(f"- {row.issue} is {row.linear_status} ({row.agent_state})")
    return unfinished


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m linear_agent.ledger")
    subparsers = parser.add_subparsers(dest="command", required=True)

    count_parser = subparsers.add_parser("issue-row-count")
    count_parser.add_argument("--ledger", required=True)

    unfinished_parser = subparsers.add_parser("unfinished-issue-rows")
    unfinished_parser.add_argument("--ledger", required=True)

    worktree_parser = subparsers.add_parser("existing-worktree")
    worktree_parser.add_argument("--ledger", required=True)
    worktree_parser.add_argument("--issue", required=True)

    state_parser = subparsers.add_parser("write-state")
    state_parser.add_argument("--ledger", required=True)

    validate_parser = subparsers.add_parser("validate-ledger")
    validate_parser.add_argument("--ledger", required=True)

    args = parser.parse_args(argv)
    ledger = Path(args.ledger)

    if args.command == "issue-row-count":
        print(len(parse_issue_rows(ledger)))
        return 0
    if args.command == "unfinished-issue-rows":
        for row in unfinished_issue_rows(ledger):
            print(row)
        return 0
    if args.command == "existing-worktree":
        print(existing_worktree(ledger, args.issue), end="")
        return 0
    if args.command == "write-state":
        print(write_state_sidecar(ledger))
        return 0
    if args.command == "validate-ledger":
        problems = validate_ledger(ledger)
        if problems:
            for problem in problems:
                print(problem)
            return 1
        print("ledger valid")
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
