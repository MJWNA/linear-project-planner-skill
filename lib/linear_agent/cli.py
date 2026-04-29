from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from .graph import (
    GraphPlanError,
    allocate_lanes,
    allocation_markdown_rows,
    graph_summary,
    load_graph_plan,
    plan_to_dict,
    render_allocation,
    render_graph_plan,
)
from .graphql import LinearAgentError, apply_transition, reconcile as graphql_reconcile
from .ledger import (
    append_activity,
    existing_worktree,
    parse_issue_rows,
    remove_empty_issue_row,
    replace_line,
    set_check_item,
    timestamp,
    unfinished_issue_rows,
    upsert_issue_row,
    validate_ledger,
    write_state_sidecar,
)


ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = Path(os.environ.get("LINEAR_AGENT_TEMPLATE", ROOT / "templates" / "EXECUTION.md"))


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = args.func(args)
        if isinstance(result, dict):
            print_json_or_text(args, result, result.get("text", ""))
        return int(result.get("code", 0)) if isinstance(result, dict) else int(result)
    except (GraphPlanError, LinearAgentError, ValueError) as exc:
        print(f"linear-agent failed: {redact(str(exc))}", file=sys.stderr)
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="linear-agent")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init")
    init.add_argument("--ledger", required=True)
    init.add_argument("--project", required=True)
    init.add_argument("--prompt", required=True)
    init.add_argument("--linear-project", default="")
    init.add_argument("--repo", default="")
    init.add_argument("--base-branch", default="")
    init.add_argument("--force", action="store_true")
    init.add_argument("--json", action="store_true")
    init.set_defaults(func=cmd_init)

    for name in ("start", "block", "verify", "complete"):
        item = sub.add_parser(name)
        item.add_argument("issue")
        add_common(item)
        item.add_argument("--parallel-write", action="store_true")
        item.add_argument("--apply-linear", action="store_true")
        item.add_argument("--dry-run", action="store_true")
        item.set_defaults(func=cmd_transition)

    handoff = sub.add_parser("handoff")
    add_common(handoff)
    handoff.set_defaults(func=cmd_handoff)

    reconcile = sub.add_parser("reconcile")
    add_common(reconcile)
    reconcile.set_defaults(func=cmd_reconcile)

    finalize = sub.add_parser("finalize")
    add_common(finalize)
    finalize.add_argument("--linear-reconciled", action="store_true")
    finalize.add_argument("--dependencies", default="")
    finalize.add_argument("--production-gates", default="")
    finalize.add_argument("--sink-gates", default="")
    finalize.set_defaults(func=cmd_finalize)

    validate = sub.add_parser("validate-ledger")
    validate.add_argument("--ledger", required=True)
    validate.add_argument("--json", action="store_true")
    validate.set_defaults(func=cmd_validate_ledger)

    graph_plan = sub.add_parser("graph-plan")
    graph_plan.add_argument("--from", dest="from_path", required=True)
    graph_plan.add_argument("--json", action="store_true")
    graph_plan.set_defaults(func=cmd_graph_plan)

    graph_apply = sub.add_parser("graph-apply")
    graph_apply.add_argument("--from", dest="from_path", required=True)
    graph_apply.add_argument("--apply-linear", action="store_true")
    graph_apply.add_argument("--json", action="store_true")
    graph_apply.set_defaults(func=cmd_graph_apply)

    graph_readback = sub.add_parser("graph-readback")
    graph_readback.add_argument("--from", dest="from_path", required=True)
    graph_readback.add_argument("--json", action="store_true")
    graph_readback.set_defaults(func=cmd_graph_readback)

    allocate = sub.add_parser("allocate")
    allocate.add_argument("--from", dest="from_path", required=True)
    allocate.add_argument("--ledger", default="")
    allocate.add_argument("--base-worktree", default="../linear-agent-worktrees")
    allocate.add_argument("--json", action="store_true")
    allocate.set_defaults(func=cmd_allocate)

    inventory = sub.add_parser("inventory")
    inventory.add_argument("--repo", required=True)
    inventory.add_argument("--json", action="store_true")
    inventory.set_defaults(func=cmd_inventory)

    smoke = sub.add_parser("smoke")
    smoke.add_argument("--project", required=True)
    smoke.add_argument("--apply-linear", action="store_true")
    smoke.add_argument("--json", action="store_true")
    smoke.set_defaults(func=cmd_smoke)

    return parser


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--agent", default=os.environ.get("AGENT", "Codex"))
    parser.add_argument("--worktree", default="")
    parser.add_argument("--note", default="")
    parser.add_argument("--next", default="")
    parser.add_argument("--verification", default="")
    parser.add_argument("--evidence", default="")
    parser.add_argument("--json", action="store_true")


def cmd_init(args: argparse.Namespace) -> dict[str, Any]:
    ledger = Path(args.ledger)
    if not TEMPLATE.exists():
        raise ValueError(f"Template not found: {TEMPLATE}")
    if ledger.exists() and not args.force:
        raise ValueError(f"Ledger already exists: {ledger} (use --force to overwrite)")
    ledger.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(TEMPLATE, ledger)
    replace_line(ledger, "# Linear Execution Ledger:", f"# Linear Execution Ledger: {args.project}")
    replace_line(ledger, "<Paste the user request", args.prompt)
    replace_line(ledger, "- Linear project:", f"- Linear project: {args.linear_project or args.project}")
    replace_line(ledger, "- Repository:", f"- Repository: {args.repo}")
    replace_line(ledger, "- Base branch:", f"- Base branch: {args.base_branch}")
    replace_line(ledger, "- Ledger path:", f"- Ledger path: {ledger}")
    replace_line(ledger, "- Overall status:", "- Overall status: initialized")
    replace_line(ledger, "- Last verified:", f"- Last verified: {timestamp()}")
    replace_line(
        ledger,
        "- Next safest action:",
        "- Next safest action: create or reconcile Linear issues, then claim the first dependency-ready issue",
    )
    replace_line(ledger, "- Validation mode:", "- Validation mode: standard")
    replace_line(ledger, "- Deep auto-research loop:", "- Deep auto-research loop: not requested")
    append_activity(ledger, f"Ledger initialized for {args.project}.")
    sidecar = write_state_sidecar(ledger)
    return {"code": 0, "ledger": str(ledger), "sidecar": str(sidecar), "text": f"Ledger initialized: {ledger}"}


def cmd_transition(args: argparse.Namespace) -> dict[str, Any]:
    ledger = Path(args.ledger)
    require_ledger(ledger)
    action = args.command
    worktree = args.worktree or existing_worktree(ledger, args.issue)
    if action == "start" and args.parallel_write and not worktree:
        raise ValueError("start --parallel-write requires --worktree")
    if action == "complete" and not args.verification:
        raise ValueError("complete requires --verification")

    linear_status, agent_state, comment, overall, next_action = transition_values(args, worktree)
    apply_requested = args.apply_linear or (
        os.environ.get("LINEAR_AGENT_APPLY") == "1" and not args.dry_run
    )
    if apply_requested:
        print_direct_apply(args, linear_status, comment, worktree)
        try:
            apply_transition(args.issue, linear_status, comment, action)
        except LinearAgentError:
            append_activity(
                ledger,
                f"{args.issue} {action} failed before ledger confirmation. Intended Linear state: {linear_status}.",
            )
            write_state_sidecar(ledger)
            raise

    replace_line(ledger, "- Overall status:", f"- Overall status: {overall}")
    replace_line(ledger, "- Active issue:", f"- Active issue: {args.issue}")
    replace_line(ledger, "- Active agent:", f"- Active agent: {args.agent}")
    if action == "start" and worktree:
        replace_line(ledger, "- Active worktree:", f"- Active worktree: {worktree}")
    replace_line(ledger, "- Last verified:", f"- Last verified: {timestamp()}")
    replace_line(ledger, "- Next safest action:", f"- Next safest action: {next_action}")
    upsert_issue_row(
        ledger,
        args.issue,
        linear_status,
        agent_state,
        args.agent,
        worktree,
        args.verification or "pending",
    )
    append_activity(ledger, f"{args.issue} {action}. {comment}")
    sidecar = write_state_sidecar(ledger)
    text = (
        "Linear automation applied and read-back verified.\nTransition recorded locally: "
        f"{action}"
        if apply_requested
        else mcp_plan(action, args.issue, linear_status, comment)
    )
    return {"code": 0, "issue": args.issue, "state": linear_status, "sidecar": str(sidecar), "text": text}


def transition_values(args: argparse.Namespace, worktree: str) -> tuple[str, str, str, str, str]:
    if args.command == "start":
        return (
            "In Progress",
            "agent:executing",
            f"Started work. Agent: {args.agent}. Worktree: {worktree or 'n/a'}. Parallel write: {'yes' if args.parallel_write else 'no'}. Note: {args.note or 'claimed for execution'}.",
            "executing",
            f"execute {args.issue} and record verification before completion",
        )
    if args.command == "block":
        return (
            "In Progress",
            "agent:blocked",
            f"Blocked. Agent: {args.agent}. Blocker: {args.note or 'not specified'}. Safest next action: {args.next or 'choose another dependency-ready issue'}.",
            "blocked",
            args.next or "resolve blocker or choose another dependency-ready issue",
        )
    if args.command == "verify":
        return (
            "In Progress",
            "agent:verifying",
            f"Verification update. Agent: {args.agent}. Verification: {args.verification or 'not specified'}. Note: {args.note or 'none'}.",
            "verifying",
            f"complete {args.issue} only after verification and Linear read-back pass",
        )
    return (
        "Done",
        "agent:pr-ready",
        f"Completed. Agent: {args.agent}. Verification: {args.verification}. Note: {args.note or 'none'}.",
        "issue completed",
        "reconcile Linear, then choose the next dependency-ready issue",
    )


def cmd_handoff(args: argparse.Namespace) -> dict[str, Any]:
    ledger = Path(args.ledger)
    require_ledger(ledger)
    comment = f"Handoff. Agent: {args.agent}. Note: {args.note or 'none'}. Next: {args.next or 'read ledger, reconcile Linear, then continue from the highest-priority unblocked issue'}."
    replace_line(ledger, "- Overall status:", "- Overall status: handoff")
    replace_line(ledger, "- Last verified:", f"- Last verified: {timestamp()}")
    replace_line(
        ledger,
        "- Next safest action:",
        f"- Next safest action: {args.next or 'read ledger, reconcile Linear, then continue from the highest-priority unblocked issue'}",
    )
    append_activity(ledger, comment)
    sidecar = write_state_sidecar(ledger)
    return {"code": 0, "sidecar": str(sidecar), "text": handoff_plan(comment)}


def cmd_reconcile(args: argparse.Namespace) -> dict[str, Any]:
    ledger = Path(args.ledger)
    require_ledger(ledger)
    proc = subprocess.run(
        [sys.executable, "-m", "linear_agent.graphql", "reconcile", "--ledger", str(ledger)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env={**os.environ, "PYTHONPATH": str(ROOT / "lib") + os.pathsep + os.environ.get("PYTHONPATH", "")},
        check=False,
    )
    output = proc.stdout
    print(output, end="")
    apply_reconcile_output(ledger, output, args.agent)
    summary = "; ".join(line for line in output.splitlines() if line)
    if proc.returncode == 0:
        replace_line(ledger, "- Overall status:", "- Overall status: reconciled")
        append_activity(ledger, f"Linear reconciliation passed. Summary: {summary}")
    else:
        replace_line(ledger, "- Overall status:", "- Overall status: reconciliation drift found")
        replace_line(ledger, "- Next safest action:", "- Next safest action: inspect reconciled drift rows before claiming or completing more work")
        append_activity(ledger, f"Linear reconciliation found drift. Summary: {summary or 'no issue rows found'}")
    replace_line(ledger, "- Last verified:", f"- Last verified: {timestamp()}")
    write_state_sidecar(ledger)
    return {"code": proc.returncode, "text": ""}


def apply_reconcile_output(ledger: Path, output: str, agent: str) -> None:
    for line in output.splitlines():
        parts = [part.strip() for part in line.split("|")]
        if len(parts) < 3:
            continue
        kind, issue = parts[0], parts[1]
        worktree = existing_worktree(ledger, issue)
        if kind == "mismatch" and len(parts) >= 4:
            ledger_status = parts[2].replace("ledger=", "")
            linear_status = parts[3].replace("linear=", "")
            upsert_issue_row(
                ledger,
                issue,
                linear_status,
                "agent:pr-ready" if linear_status in {"Done", "Completed"} else "agent:blocked",
                agent,
                worktree,
                f"Reconciled from Linear: ledger was {ledger_status}; Linear is {linear_status}",
            )
        elif kind == "missing":
            upsert_issue_row(ledger, issue, "Missing in Linear", "agent:blocked", agent, worktree, parts[2])


def cmd_finalize(args: argparse.Namespace) -> dict[str, Any]:
    ledger = Path(args.ledger)
    require_ledger(ledger)
    if not args.verification:
        raise ValueError("finalize requires --verification")
    if not args.evidence:
        raise ValueError("finalize requires --evidence with a Linear read-back summary, evidence file, or release/CI link")
    if not args.linear_reconciled:
        raise ValueError("finalize requires --linear-reconciled after a successful Linear/project read-back")
    for flag, value in (
        ("dependencies", args.dependencies),
        ("production-gates", args.production_gates),
        ("sink-gates", args.sink_gates),
    ):
        if not value:
            raise ValueError(f"finalize requires --{flag}")
    rows = parse_issue_rows(ledger)
    if not rows:
        raise ValueError("finalize refuses an empty Issue Progress table; reconcile or record completed issue rows first")
    unfinished = unfinished_issue_rows(ledger)
    if unfinished:
        raise ValueError("finalize refuses unfinished issue rows:\n" + "\n".join(unfinished))

    ensure_ledger_compat_items(ledger)
    replace_line(ledger, "- Overall status:", "- Overall status: completed")
    replace_line(ledger, "- Active issue:", "- Active issue: None")
    replace_line(ledger, "- Active agent:", f"- Active agent: {args.agent}")
    replace_line(ledger, "- Active worktree:", "- Active worktree: None")
    replace_line(ledger, "- Last verified:", f"- Last verified: {timestamp()}")
    replace_line(
        ledger,
        "- Next safest action:",
        "- Next safest action: Project complete; reopen only for new findings or expanded verification scope",
    )
    for label in (
        "Project created or selected",
        "Operating guide issue created",
        "Verification matrix issue created",
        "Milestones created",
        "Parent workstreams created",
        "Child issues created",
        "Labels applied",
        "Project status update or operating-guide comment posted",
        "First issue chosen by dependency order",
        "Active issue moved to In Progress",
        "Active issue acknowledgement comment posted",
        "Worktree or workspace recorded",
        "Verification run recorded",
        "Completion comment posted",
        "Active issue moved to Done only after verification",
        "Follow-up issues created or linked",
        "Final verification/release gate completed",
        "Final ledger reconciliation completed",
    ):
        set_check_item(ledger, label, "x", label)
    apply_gate_item(ledger, "Dependencies/blockers linked", args.dependencies)
    apply_gate_item(ledger, "Production gates created if needed", args.production_gates)
    apply_gate_item(ledger, "Sink/output preservation gates created if needed", args.sink_gates)
    remove_empty_issue_row(ledger)
    comment = f"Finalized ledger. Agent: {args.agent}. Verification: {args.verification}. Evidence: {args.evidence}. Note: {args.note or 'none'}."
    append_activity(ledger, comment)
    sidecar = write_state_sidecar(ledger)
    return {"code": 0, "sidecar": str(sidecar), "text": finalize_plan(comment)}


def ensure_ledger_compat_items(ledger: Path) -> None:
    text = ledger.read_text(encoding="utf-8")
    if "Checklist marker legend:" not in text:
        replace_line(
            ledger,
            "- Deep auto-research loop:",
            "- Deep auto-research loop: not requested\n\nChecklist marker legend: `[ ]` pending, `[x]` complete, `[~]` not applicable with a reason. During final reconciliation, do not leave conditional items unchecked if they were intentionally not needed.",
        )
    text = ledger.read_text(encoding="utf-8")
    if "Final ledger reconciliation completed" not in text:
        lines: list[str] = []
        for line in text.splitlines():
            lines.append(line)
            if line.endswith("Final verification/release gate completed"):
                lines.append("- [ ] Final ledger reconciliation completed")
        ledger.write_text("\n".join(lines) + "\n", encoding="utf-8")


def apply_gate_item(ledger: Path, label: str, value: str) -> None:
    if value == "satisfied":
        set_check_item(ledger, label, "x", label)
        return
    if value.startswith("not-applicable:") and value.split(":", 1)[1]:
        set_check_item(ledger, label, "~", f"{label} (N/A: {value.split(':', 1)[1]})")
        return
    raise ValueError(f"{label} must be 'satisfied' or 'not-applicable:<reason>'")


def cmd_validate_ledger(args: argparse.Namespace) -> dict[str, Any]:
    ledger = Path(args.ledger)
    require_ledger(ledger)
    problems = validate_ledger(ledger)
    if problems:
        return {"code": 1, "problems": problems, "text": "\n".join(problems)}
    return {"code": 0, "problems": [], "text": "ledger valid"}


def cmd_graph_plan(args: argparse.Namespace) -> dict[str, Any]:
    plan = load_graph_plan(Path(args.from_path))
    return {"code": 0, **plan_to_dict(plan), "text": render_graph_plan(plan)}


def cmd_graph_apply(args: argparse.Namespace) -> dict[str, Any]:
    plan = load_graph_plan(Path(args.from_path))
    if not args.apply_linear:
        return {
            "code": 0,
            **plan_to_dict(plan),
            "applied": False,
            "text": render_graph_plan(plan) + "\n\nDry-run only. Re-run with --apply-linear to mutate Linear.",
        }
    state_path = os.environ.get("LINEAR_AGENT_FAKE_STATE")
    if not state_path:
        raise LinearAgentError("graph-apply live GraphQL is intentionally gated; use the Linear MCP or fake transport until live project mutations are configured.")
    require_fake_test_mode()
    apply_graph_to_fake_state(Path(state_path), plan_to_dict(plan))
    return {"code": 0, **plan_to_dict(plan), "applied": True, "text": "Graph applied to fake Linear state."}


def cmd_graph_readback(args: argparse.Namespace) -> dict[str, Any]:
    plan = load_graph_plan(Path(args.from_path))
    state_path = os.environ.get("LINEAR_AGENT_FAKE_STATE")
    if not state_path:
        return {"code": 0, **plan_to_dict(plan), "text": "Graph read-back dry-run: plan is structurally valid."}
    require_fake_test_mode()
    state = json.loads(Path(state_path).read_text(encoding="utf-8"))
    drift = graph_drift(state, plan_to_dict(plan))
    code = 1 if drift else 0
    text = "Graph read-back matched fake state." if not drift else "Graph drift: " + json.dumps(drift, sort_keys=True)
    return {"code": code, "drift": drift, "text": text}


def cmd_allocate(args: argparse.Namespace) -> dict[str, Any]:
    plan = load_graph_plan(Path(args.from_path))
    allocation = allocate_lanes(plan, args.base_worktree)
    if args.ledger:
        insert_allocation(Path(args.ledger), allocation)
    return {"code": 1 if allocation["conflicts"] else 0, **allocation, "text": render_allocation(allocation)}


def cmd_inventory(args: argparse.Namespace) -> dict[str, Any]:
    repo = Path(args.repo)
    if not repo.exists():
        raise ValueError(f"repo not found: {repo}")
    files = {str(path.relative_to(repo)) for path in repo.rglob("*") if path.is_file() and ".git" not in path.parts}
    checks = {
        "envDeploy": sorted(item for item in files if item in {"vercel.json", "Dockerfile", "package.json"} or item.startswith(".github/workflows/")),
        "authRbac": sorted(item for item in files if "auth" in item.lower() or "permission" in item.lower() or "rbac" in item.lower()),
        "cronJobs": sorted(item for item in files if "cron" in item.lower() or "schedule" in item.lower()),
        "dataSemantics": sorted(item for item in files if "schema" in item.lower() or "migration" in item.lower() or "drizzle" in item.lower()),
        "sinks": sorted(item for item in files if any(word in item.lower() for word in ("sync", "export", "report", "webhook"))),
    }
    text = "\n".join([f"{key}: {', '.join(value) or '<review required>'}" for key, value in checks.items()])
    return {"code": 0, "repo": str(repo), "checks": checks, "text": text}


def cmd_smoke(args: argparse.Namespace) -> dict[str, Any]:
    if not args.apply_linear:
        return {
            "code": 0,
            "project": args.project,
            "applied": False,
            "text": f"Smoke dry-run for project {args.project}: no Linear writes performed.",
        }
    state_path = os.environ.get("LINEAR_AGENT_FAKE_STATE")
    if state_path:
        require_fake_test_mode()
        state = json.loads(Path(state_path).read_text(encoding="utf-8")) if Path(state_path).exists() else {}
        runs = state.setdefault("smokeRuns", [])
        runs.append({"project": args.project, "timestamp": timestamp(), "mode": "fake"})
        Path(state_path).write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return {
            "code": 0,
            "project": args.project,
            "applied": True,
            "smokeRuns": len(runs),
            "text": f"Smoke fake apply recorded for {args.project}.",
        }
    if not (os.environ.get("LINEAR_API_KEY") or os.environ.get("LINEAR_ACCESS_TOKEN")):
        raise LinearAgentError("smoke --apply-linear requires Linear credentials or fake transport")
    return {"code": 0, "project": args.project, "applied": True, "text": f"Smoke apply gate reached for {args.project}."}


def print_json_or_text(args: argparse.Namespace, payload: dict[str, Any], text: str) -> None:
    if getattr(args, "json", False):
        print(json.dumps({key: value for key, value in payload.items() if key != "text"}, indent=2, sort_keys=True))
    elif text:
        print(text)


def mcp_plan(action: str, issue: str, state: str, comment: str) -> str:
    return f"""Required Linear MCP actions:
1. _save_issue(id="{issue}", state="{state}")
2. _save_comment(issueId="{issue}", body=<comment body below>)
3. Verify with _list_issues(query="{issue}") and confirm state="{state}".
4. If verification fails, leave a comment describing intended state, observed state, and next retry point.
Transition recorded locally: {action}

Comment body:
```md
{comment}
```"""


def handoff_plan(comment: str) -> str:
    return f"""Required Linear MCP actions:
1. _save_comment(issueId="<active-or-operating-guide-issue>", body=<comment body below>)
2. Verify with _list_comments(issueId="<active-or-operating-guide-issue>") and confirm the handoff comment exists.
3. Reconcile with _list_issues(project="<project-name>") before choosing the next issue.
4. If verification fails, retry the comment once and record the mismatch in the ledger.
Transition recorded locally: handoff

Comment body:
```md
{comment}
```"""


def finalize_plan(comment: str) -> str:
    return f"""Required Linear MCP actions:
1. _save_comment(issueId="<operating-guide-or-final-verification-issue>", body=<comment body below>)
2. Verify with Linear project read-back that no Todo or In Progress issues remain.
3. If any unfinished issue remains, reopen the ledger with linear-agent start/block/handoff before calling the project complete.
Transition recorded locally: finalize

Comment body:
```md
{comment}
```"""


def print_direct_apply(args: argparse.Namespace, state: str, comment: str, worktree: str) -> None:
    print(
        "\n".join(
            [
                "Direct Linear apply requested:",
                f"- Issue: {args.issue}",
                f"- Target state: {state}",
                f"- Ledger: {args.ledger}",
                f"- Agent: {args.agent}",
                f"- Worktree: {worktree or 'n/a'}",
                f"- Action: {args.command}",
                f"- Comment preview: {comment}",
            ]
        )
    )


def insert_allocation(ledger: Path, allocation: dict[str, Any]) -> None:
    require_ledger(ledger)
    rows = allocation_markdown_rows(allocation)
    lines = ledger.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    in_allocation = False
    inserted = False
    for line in lines:
        if line == "## Parallel Agent Allocation":
            in_allocation = True
            out.append(line)
            continue
        if in_allocation and line.startswith("## "):
            if not inserted:
                out.extend(rows)
                inserted = True
            in_allocation = False
        if in_allocation and line == "|  |  |  |  |  |  |  |":
            continue
        out.append(line)
    ledger.write_text("\n".join(out) + "\n", encoding="utf-8")
    write_state_sidecar(ledger)


def apply_graph_to_fake_state(path: Path, plan: dict[str, Any]) -> None:
    state = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    state["project"] = plan["project"]
    state["labels"] = plan["labels"]
    state["milestones"] = plan["milestones"]
    issues = state.setdefault("issues", {})
    for issue in plan["issues"]:
        key = issue["key"]
        current = issues.setdefault(key, {})
        current.update(
            {
                "id": current.get("id", f"issue-{key.lower()}"),
                "identifier": key,
                "title": issue["title"],
                "description": issue.get("description", current.get("description", "")),
                "url": current.get("url", f"https://linear.app/example/{key}"),
                "state": current.get("state", {"id": "todo", "name": "Todo", "type": "unstarted"}),
                "team": current.get("team", {"id": "team-mas", "key": "MAS", "name": "Master Group Holdings"}),
                "project": current.get(
                    "project",
                    {"id": "project", "name": plan["project"]["name"], "url": "https://linear.app/project"},
                ),
                "comments": current.get("comments", {"nodes": []}),
                "updatedAt": timestamp(),
                "labels": issue.get("labels", []),
                "parent": issue.get("parent", ""),
                "milestone": issue.get("milestone", ""),
                "links": issue.get("links", []),
                "blocks": issue.get("blocks", []),
                "blockedBy": issue.get("blocked_by", []),
            }
        )
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def graph_drift(state: dict[str, Any], plan: dict[str, Any]) -> list[dict[str, Any]]:
    drift: list[dict[str, Any]] = []
    if state.get("project", {}).get("name") != plan["project"].get("name"):
        drift.append(
            {
                "scope": "project",
                "field": "name",
                "expected": plan["project"].get("name"),
                "actual": state.get("project", {}).get("name"),
            }
        )
    if sorted(state.get("labels", [])) != sorted(plan.get("labels", [])):
        drift.append(
            {
                "scope": "project",
                "field": "labels",
                "expected": sorted(plan.get("labels", [])),
                "actual": sorted(state.get("labels", [])),
            }
        )
    if sorted(state.get("milestones", [])) != sorted(plan.get("milestones", [])):
        drift.append(
            {
                "scope": "project",
                "field": "milestones",
                "expected": sorted(plan.get("milestones", [])),
                "actual": sorted(state.get("milestones", [])),
            }
        )
    issues = state.get("issues", {})
    for issue in plan["issues"]:
        actual = issues.get(issue["key"])
        if not actual:
            drift.append({"issue": issue["key"], "field": "exists", "expected": "present", "actual": "missing"})
            continue
        expected_fields = {
            "title": issue["title"],
            "description": issue.get("description", ""),
            "labels": sorted(issue.get("labels", [])),
            "parent": issue.get("parent", ""),
            "milestone": issue.get("milestone", ""),
            "links": sorted(issue.get("links", []), key=lambda item: (item.get("title", ""), item.get("url", ""))),
            "blocks": sorted(issue.get("blocks", [])),
            "blockedBy": sorted(issue.get("blocked_by", [])),
        }
        actual_fields = {
            "title": actual.get("title", ""),
            "description": actual.get("description", ""),
            "labels": sorted(actual.get("labels", [])),
            "parent": actual.get("parent", ""),
            "milestone": actual.get("milestone", ""),
            "links": sorted(actual.get("links", []), key=lambda item: (item.get("title", ""), item.get("url", ""))),
            "blocks": sorted(actual.get("blocks", [])),
            "blockedBy": sorted(actual.get("blockedBy", [])),
        }
        for field, expected in expected_fields.items():
            if actual_fields[field] != expected:
                drift.append(
                    {
                        "issue": issue["key"],
                        "field": field,
                        "expected": expected,
                        "actual": actual_fields[field],
                    }
                )
    return drift


def require_fake_test_mode() -> None:
    if os.environ.get("LINEAR_AGENT_TEST_MODE") != "1":
        raise LinearAgentError(
            "LINEAR_AGENT_FAKE_STATE is test-only. Set "
            "LINEAR_AGENT_TEST_MODE=1 for local fake transport tests, "
            "or unset LINEAR_AGENT_FAKE_STATE before using real Linear."
        )


def require_ledger(path: Path) -> None:
    if not path.is_file():
        raise ValueError(f"Ledger not found: {path}")


def redact(value: str) -> str:
    redacted = value
    for token in (os.environ.get("LINEAR_API_KEY"), os.environ.get("LINEAR_ACCESS_TOKEN")):
        if token:
            redacted = redacted.replace(token, "[REDACTED]")
    return redacted


if __name__ == "__main__":
    raise SystemExit(main())
