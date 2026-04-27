from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LedgerIssueRow:
    issue: str
    linear_status: str
    agent_state: str
    agent: str
    worktree: str
    last_update: str
    verification: str


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

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
