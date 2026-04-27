#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
SKILL_DIR=$(cd -- "$SCRIPT_DIR/.." && pwd)
BIN="$SKILL_DIR/scripts/linear-agent"
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

assert_contains() {
  local file=$1
  local expected=$2

  if ! grep -Fq -- "$expected" "$file"; then
    echo "Expected to find: $expected" >&2
    echo "--- $file ---" >&2
    cat "$file" >&2
    exit 1
  fi
}

assert_not_contains() {
  local file=$1
  local unexpected=$2

  if grep -Fq -- "$unexpected" "$file"; then
    echo "Did not expect to find: $unexpected" >&2
    echo "--- $file ---" >&2
    cat "$file" >&2
    exit 1
  fi
}

LEDGER="$TMP_DIR/EXECUTION.md"

assert_contains "$SKILL_DIR/SKILL.md" "## Mandatory Parallel Dispatch"
assert_contains "$SKILL_DIR/SKILL.md" "When there are 2+ independent, dependency-ready workstreams with disjoint write scopes"
assert_contains "$SKILL_DIR/SKILL.md" "Parallel write-capable agents must not share one working tree"
assert_contains "$SKILL_DIR/SKILL.md" "## Sparse Link Graph"
assert_contains "$SKILL_DIR/SKILL.md" "links should compress context, not clutter tasks"
assert_contains "$SKILL_DIR/SKILL.md" "## Auto-Research Validation Tasks"
assert_contains "$SKILL_DIR/SKILL.md" "Do not let agents mutate the evaluator during the final validation loop"
assert_contains "$SKILL_DIR/README.md" "### Parallel-Agent Operating Model"
assert_contains "$SKILL_DIR/README.md" "Each write-capable agent gets one Linear issue, one branch, one git worktree, and one explicit write set"
assert_contains "$SKILL_DIR/README.md" "### Sparse Link Graph"
assert_contains "$SKILL_DIR/README.md" "### 5. Auto-Research Validation Loop"
assert_contains "$SKILL_DIR/README.md" "Links should compress context, not clutter tasks"

"$BIN" init \
  --ledger "$LEDGER" \
  --project "Agent Runtime Hardening" \
  --prompt $'Create a Linear project\nand execute it with agents' \
  --linear-project "MAS Agent Runtime Hardening" \
  --repo "/tmp/example-repo" \
  --base-branch "main" \
  >"$TMP_DIR/init.out"

assert_contains "$LEDGER" "# Linear Execution Ledger: Agent Runtime Hardening"
assert_contains "$LEDGER" "Create a Linear project"
assert_contains "$LEDGER" "and execute it with agents"
assert_contains "$LEDGER" "- Linear project: MAS Agent Runtime Hardening"
assert_contains "$LEDGER" "- Repository: /tmp/example-repo"
assert_contains "$LEDGER" "- Base branch: main"
assert_contains "$TMP_DIR/init.out" "Ledger initialized:"
assert_contains "$LEDGER" "## Decisions"
assert_contains "$LEDGER" "## Blockers"
assert_contains "$LEDGER" "## Risks"
assert_contains "$LEDGER" "## Handoff Notes"
assert_contains "$LEDGER" "Checklist marker legend:"
assert_contains "$LEDGER" "- [ ] Final ledger reconciliation completed"
assert_contains "$LEDGER" "## Parallel Agent Allocation"
assert_contains "$LEDGER" "Separate git worktrees are required unless the work is read-only"
assert_contains "$LEDGER" "| Issue | Agent | Branch | Worktree | Ownership Boundary | Status | Merge/Reconcile Notes |"
if [ "$(grep -Fc -- "- TBD" "$LEDGER")" -lt 4 ]; then
  echo "Expected non-activity section placeholders to remain after init" >&2
  cat "$LEDGER" >&2
  exit 1
fi

printf '%s\n' "do not overwrite me" >"$TMP_DIR/existing-ledger.md"
set +e
"$BIN" init \
  --ledger "$TMP_DIR/existing-ledger.md" \
  --project "Overwrite Guard" \
  --prompt "This should fail" \
  >"$TMP_DIR/init-overwrite.out" 2>&1
overwrite_rc=$?
set -e

if [ "$overwrite_rc" -eq 0 ]; then
  echo "Expected init against an existing ledger to fail without --force" >&2
  exit 1
fi
assert_contains "$TMP_DIR/init-overwrite.out" "Ledger already exists"
assert_contains "$TMP_DIR/existing-ledger.md" "do not overwrite me"

"$BIN" init \
  --ledger "$TMP_DIR/existing-ledger.md" \
  --project "Overwrite Guard" \
  --prompt "Forced overwrite" \
  --force \
  >"$TMP_DIR/init-force.out"

assert_contains "$TMP_DIR/existing-ledger.md" "# Linear Execution Ledger: Overwrite Guard"
assert_not_contains "$TMP_DIR/existing-ledger.md" "do not overwrite me"

set +e
LINEAR_AGENT_TEMPLATE="$TMP_DIR/missing-template.md" "$BIN" init \
  --ledger "$TMP_DIR/missing-template-ledger.md" \
  --project "Missing Template" \
  --prompt "This should fail clearly" \
  >"$TMP_DIR/init-missing-template.out" 2>&1
missing_template_rc=$?
set -e

if [ "$missing_template_rc" -eq 0 ]; then
  echo "Expected init with missing template to fail" >&2
  exit 1
fi
assert_contains "$TMP_DIR/init-missing-template.out" "Template not found"

set +e
"$BIN" start MAS-122 \
  --ledger "$LEDGER" \
  --agent "Codex" \
  --parallel-write \
  >"$TMP_DIR/start-parallel-missing-worktree.out" 2>&1
parallel_missing_worktree_rc=$?
set -e

if [ "$parallel_missing_worktree_rc" -eq 0 ]; then
  echo "Expected parallel write start without --worktree to fail" >&2
  exit 1
fi
assert_contains "$TMP_DIR/start-parallel-missing-worktree.out" "start --parallel-write requires --worktree"

"$BIN" start MAS-123 \
  --ledger "$LEDGER" \
  --agent "Codex" \
  --worktree "/tmp/example|worktree" \
  --parallel-write \
  --note $'Claimed for implementation with "quoted" note\nand pipe | value' \
  >"$TMP_DIR/start.out"

assert_contains "$LEDGER" "- Active issue: MAS-123"
assert_contains "$LEDGER" "- Active agent: Codex"
assert_contains "$LEDGER" "- Active worktree: /tmp/example|worktree"
assert_contains "$LEDGER" "| MAS-123 | In Progress | agent:executing | Codex | /tmp/example\\|worktree |"
assert_contains "$LEDGER" "Claimed for implementation with \"quoted\" note"
assert_contains "$LEDGER" "and pipe | value"
assert_contains "$TMP_DIR/start.out" "Required Linear MCP actions"
assert_contains "$TMP_DIR/start.out" "_save_issue(id=\"MAS-123\", state=\"In Progress\")"
assert_contains "$TMP_DIR/start.out" "_save_comment(issueId=\"MAS-123\", body=<comment body below>)"
assert_contains "$TMP_DIR/start.out" "Comment body:"
assert_contains "$TMP_DIR/start.out" "Claimed for implementation with \"quoted\" note"
assert_contains "$TMP_DIR/start.out" "Parallel write: yes"
assert_contains "$TMP_DIR/start.out" "Verify with _list_issues"

FAKE_STATE="$TMP_DIR/fake-linear-state.json"
FAKE_REQUESTS="$TMP_DIR/fake-linear-requests.jsonl"
cat >"$FAKE_STATE" <<'JSON'
{
  "states": [
    {"id": "todo", "name": "Todo", "type": "unstarted", "team": {"id": "team-mas", "key": "MAS"}},
    {"id": "in-progress", "name": "In Progress", "type": "started", "team": {"id": "team-mas", "key": "MAS"}},
    {"id": "done", "name": "Done", "type": "completed", "team": {"id": "team-mas", "key": "MAS"}}
  ],
  "issues": {
    "MAS-999": {
      "id": "issue-999",
      "identifier": "MAS-999",
      "title": "Fake direct issue",
      "description": "",
      "url": "https://linear.app/example/MAS-999",
      "state": {"id": "todo", "name": "Todo", "type": "unstarted"},
      "team": {"id": "team-mas", "key": "MAS", "name": "Master Group Holdings"},
      "project": {"id": "project", "name": "Project", "url": "https://linear.app/project"},
      "comments": {"nodes": []},
      "updatedAt": "2026-04-28T00:00:00+10:00"
    }
  }
}
JSON

LINEAR_AGENT_TEST_MODE=1 \
LINEAR_AGENT_FAKE_STATE="$FAKE_STATE" \
LINEAR_AGENT_FAKE_REQUESTS="$FAKE_REQUESTS" \
"$BIN" start MAS-999 \
  --ledger "$LEDGER" \
  --agent "Codex" \
  --worktree "/tmp/direct-worktree" \
  --apply-linear \
  --note "Direct apply smoke test" \
  >"$TMP_DIR/start-apply.out"

assert_contains "$TMP_DIR/start-apply.out" "Linear automation applied and read-back verified"
assert_contains "$LEDGER" "| MAS-999 | In Progress | agent:executing | Codex | /tmp/direct-worktree |"
assert_contains "$FAKE_REQUESTS" "\"operationName\": \"IssueStateUpdate\""

set +e
LINEAR_AGENT_TEST_MODE=1 \
LINEAR_AGENT_FAKE_STATE="$FAKE_STATE" "$BIN" reconcile \
  --ledger "$LEDGER" \
  >"$TMP_DIR/reconcile.out"
reconcile_rc=$?
set -e

if [ "$reconcile_rc" -eq 0 ]; then
  echo "Expected reconcile to find mismatches for fake issues not present in the fake Linear state" >&2
  exit 1
fi
assert_contains "$TMP_DIR/reconcile.out" "match | MAS-999 | In Progress"
assert_contains "$LEDGER" "Linear reconciliation found drift. Summary:"

FAILING_LEDGER="$TMP_DIR/failing-direct-ledger.md"
"$BIN" init \
  --ledger "$FAILING_LEDGER" \
  --project "Failing Direct Apply" \
  --prompt "Exercise failed direct apply" \
  >"$TMP_DIR/failing-direct-init.out"
FAILING_STATE="$TMP_DIR/failing-linear-state.json"
cat >"$FAILING_STATE" <<'JSON'
{
  "fail_on": "IssueStateUpdate",
  "states": [
    {"id": "todo", "name": "Todo", "type": "unstarted", "team": {"id": "team-mas", "key": "MAS"}},
    {"id": "in-progress", "name": "In Progress", "type": "started", "team": {"id": "team-mas", "key": "MAS"}}
  ],
  "issues": {
    "MAS-998": {
      "id": "issue-998",
      "identifier": "MAS-998",
      "title": "Failing direct issue",
      "description": "",
      "url": "https://linear.app/example/MAS-998",
      "state": {"id": "todo", "name": "Todo", "type": "unstarted"},
      "team": {"id": "team-mas", "key": "MAS", "name": "Master Group Holdings"},
      "project": {"id": "project", "name": "Project", "url": "https://linear.app/project"},
      "comments": {"nodes": []},
      "updatedAt": "2026-04-28T00:00:00+10:00"
    }
  }
}
JSON

set +e
LINEAR_AGENT_TEST_MODE=1 \
LINEAR_AGENT_FAKE_STATE="$FAILING_STATE" "$BIN" start MAS-998 \
  --ledger "$FAILING_LEDGER" \
  --agent "Codex" \
  --worktree "/tmp/failing-direct-worktree" \
  --apply-linear \
  --note "This should fail before ledger confirmation" \
  >"$TMP_DIR/start-apply-fail.out" 2>&1
apply_fail_rc=$?
set -e

if [ "$apply_fail_rc" -eq 0 ]; then
  echo "Expected failed direct apply to exit non-zero" >&2
  exit 1
fi
assert_contains "$TMP_DIR/start-apply-fail.out" "Fake Linear failure for IssueStateUpdate"
assert_not_contains "$FAILING_LEDGER" "- Active issue: MAS-998"
assert_not_contains "$FAILING_LEDGER" "| MAS-998 | In Progress |"
assert_contains "$FAILING_LEDGER" "failed before ledger confirmation"

COMMENT_FAIL_LEDGER="$TMP_DIR/comment-fail-ledger.md"
"$BIN" init \
  --ledger "$COMMENT_FAIL_LEDGER" \
  --project "Comment Failure Direct Apply" \
  --prompt "Exercise partial direct apply" \
  >"$TMP_DIR/comment-fail-init.out"
COMMENT_FAIL_STATE="$TMP_DIR/comment-fail-state.json"
cat >"$COMMENT_FAIL_STATE" <<'JSON'
{
  "fail_on": "CommentCreate",
  "states": [
    {"id": "todo", "name": "Todo", "type": "unstarted", "team": {"id": "team-mas", "key": "MAS"}},
    {"id": "in-progress", "name": "In Progress", "type": "started", "team": {"id": "team-mas", "key": "MAS"}}
  ],
  "issues": {
    "MAS-997": {
      "id": "issue-997",
      "identifier": "MAS-997",
      "title": "Partial direct issue",
      "description": "",
      "url": "https://linear.app/example/MAS-997",
      "state": {"id": "todo", "name": "Todo", "type": "unstarted"},
      "team": {"id": "team-mas", "key": "MAS", "name": "Master Group Holdings"},
      "project": {"id": "project", "name": "Project", "url": "https://linear.app/project"},
      "comments": {"nodes": []},
      "updatedAt": "2026-04-28T00:00:00+10:00"
    }
  }
}
JSON

set +e
LINEAR_AGENT_TEST_MODE=1 \
LINEAR_AGENT_FAKE_STATE="$COMMENT_FAIL_STATE" "$BIN" start MAS-997 \
  --ledger "$COMMENT_FAIL_LEDGER" \
  --agent "Codex" \
  --worktree "/tmp/comment-fail-worktree" \
  --apply-linear \
  --note "This should fail after Linear state update" \
  >"$TMP_DIR/start-comment-fail.out" 2>&1
comment_fail_rc=$?
set -e

if [ "$comment_fail_rc" -eq 0 ]; then
  echo "Expected comment failure after direct apply to exit non-zero" >&2
  exit 1
fi
assert_contains "$TMP_DIR/start-comment-fail.out" "post-update confirmation failed"
assert_contains "$TMP_DIR/start-comment-fail.out" "Run linear-agent reconcile"
assert_not_contains "$COMMENT_FAIL_LEDGER" "- Active issue: MAS-997"
assert_not_contains "$COMMENT_FAIL_LEDGER" "| MAS-997 | In Progress |"
assert_contains "$COMMENT_FAIL_LEDGER" "failed before ledger confirmation"
assert_contains "$COMMENT_FAIL_STATE" "\"name\": \"In Progress\""

"$BIN" block MAS-124 \
  --ledger "$LEDGER" \
  --agent "Codex" \
  --note "Waiting on Linear read-back" \
  --next "Continue MAS-125" \
  >"$TMP_DIR/block.out"

assert_contains "$LEDGER" "| MAS-124 | In Progress | agent:blocked | Codex |"
assert_contains "$LEDGER" "Waiting on Linear read-back"
assert_contains "$TMP_DIR/block.out" "_save_issue(id=\"MAS-124\", state=\"In Progress\")"
assert_contains "$TMP_DIR/block.out" "_save_comment(issueId=\"MAS-124\", body=<comment body below>)"

"$BIN" verify MAS-125 \
  --ledger "$LEDGER" \
  --agent "Codex" \
  --verification "bash tests: pass" \
  --note "Frozen evaluator result" \
  >"$TMP_DIR/verify.out"

assert_contains "$LEDGER" "| MAS-125 | In Progress | agent:verifying | Codex |"
assert_contains "$LEDGER" "bash tests: pass"
assert_contains "$TMP_DIR/verify.out" "_save_issue(id=\"MAS-125\", state=\"In Progress\")"
assert_contains "$TMP_DIR/verify.out" "_save_comment(issueId=\"MAS-125\", body=<comment body below>)"

set +e
"$BIN" complete MAS-126 --ledger "$LEDGER" --agent "Codex" >"$TMP_DIR/complete-missing-verification.out" 2>&1
missing_verification_rc=$?
set -e

if [ "$missing_verification_rc" -eq 0 ]; then
  echo "Expected complete without --verification to fail" >&2
  exit 1
fi
assert_contains "$TMP_DIR/complete-missing-verification.out" "complete requires --verification"

"$BIN" complete MAS-123 \
  --ledger "$LEDGER" \
  --agent "Codex" \
  --verification $'npm test: pass | lint: pass\nsecond line' \
  --note "Implemented and verified" \
  >"$TMP_DIR/complete.out"

assert_contains "$LEDGER" "| MAS-123 | Done | agent:pr-ready | Codex | /tmp/example\\|worktree |"
assert_contains "$LEDGER" "npm test: pass \\| lint: pass<br>second line"
assert_contains "$LEDGER" "Implemented and verified"
assert_contains "$TMP_DIR/complete.out" "_save_comment(issueId=\"MAS-123\", body=<comment body below>)"
assert_contains "$TMP_DIR/complete.out" "_save_issue(id=\"MAS-123\", state=\"Done\")"
assert_contains "$TMP_DIR/complete.out" "Verify with _list_issues"
assert_contains "$LEDGER" "## Activity Log"
if [ "$(grep -Ec '^\| MAS-123 \|' "$LEDGER")" -ne 1 ]; then
  echo "Expected repeated MAS-123 transitions to update one row" >&2
  cat "$LEDGER" >&2
  exit 1
fi

"$BIN" handoff \
  --ledger "$LEDGER" \
  --note "Ready for next session" \
  --next "Reconcile Linear and ledger" \
  >"$TMP_DIR/handoff.out"

assert_contains "$LEDGER" "- Overall status: handoff"
assert_contains "$LEDGER" "Ready for next session"
assert_contains "$TMP_DIR/handoff.out" "Required Linear MCP actions"
assert_contains "$TMP_DIR/handoff.out" "_save_comment"
assert_contains "$TMP_DIR/handoff.out" "Reconcile"

awk '
  $0 == "Checklist marker legend: `[ ]` pending, `[x]` complete, `[~]` not applicable with a reason. During final reconciliation, do not leave conditional items unchecked if they were intentionally not needed." { next }
  $0 == "- [ ] Final ledger reconciliation completed" { next }
  { print }
' "$LEDGER" >"$TMP_DIR/legacy-ledger.md"
mv "$TMP_DIR/legacy-ledger.md" "$LEDGER"
assert_not_contains "$LEDGER" "Checklist marker legend:"
assert_not_contains "$LEDGER" "Final ledger reconciliation completed"

"$BIN" finalize \
  --ledger "$LEDGER" \
  --agent "Codex" \
  --verification "all Linear issues done; fixed evaluator passed" \
  --linear-reconciled \
  --dependencies "not-applicable:no blocking dependencies were required" \
  --production-gates "not-applicable:not a production application" \
  --sink-gates "not-applicable:no sync or output sink in scope" \
  --note "Project-level checklist reconciled" \
  >"$TMP_DIR/finalize.out"

assert_contains "$LEDGER" "- Overall status: completed"
assert_contains "$LEDGER" "- Active issue: None"
assert_contains "$LEDGER" "- Active worktree: None"
assert_contains "$LEDGER" "- Next safest action: Project complete; reopen only for new findings or expanded verification scope"
assert_contains "$LEDGER" "Checklist marker legend:"
assert_contains "$LEDGER" "- [x] Project created or selected"
assert_contains "$LEDGER" "- [x] Project status update or operating-guide comment posted"
assert_contains "$LEDGER" "- [~] Dependencies/blockers linked (N/A: no blocking dependencies were required)"
assert_contains "$LEDGER" "- [~] Production gates created if needed (N/A: not a production application)"
assert_contains "$LEDGER" "- [~] Sink/output preservation gates created if needed (N/A: no sync or output sink in scope)"
assert_contains "$LEDGER" "- [x] First issue chosen by dependency order"
assert_contains "$LEDGER" "- [x] Follow-up issues created or linked"
assert_contains "$LEDGER" "- [x] Final ledger reconciliation completed"
assert_not_contains "$LEDGER" "|  |  |  |  |  |  |  |"
assert_contains "$LEDGER" "Finalized ledger. Agent: Codex. Verification: all Linear issues done; fixed evaluator passed. Note: Project-level checklist reconciled."
assert_contains "$TMP_DIR/finalize.out" "Required Linear MCP actions"
assert_contains "$TMP_DIR/finalize.out" "_save_comment(issueId=\"<operating-guide-or-final-verification-issue>\""
assert_contains "$TMP_DIR/finalize.out" "Verify with Linear project read-back"

set +e
"$BIN" finalize \
  --ledger "$LEDGER" \
  --agent "Codex" \
  --verification "should fail without explicit gates" \
  --linear-reconciled \
  --dependencies "not-applicable:no blocking dependencies were required" \
  >"$TMP_DIR/finalize-missing-gates.out" 2>&1
missing_gates_rc=$?
set -e

if [ "$missing_gates_rc" -eq 0 ]; then
  echo "Expected finalize without explicit gate outcomes to fail" >&2
  exit 1
fi
assert_contains "$TMP_DIR/finalize-missing-gates.out" "finalize requires --production-gates"

set +e
"$BIN" finalize \
  --ledger "$LEDGER" \
  --agent "Codex" \
  --verification "should fail without Linear reconciliation" \
  --dependencies "not-applicable:no blocking dependencies were required" \
  --production-gates "not-applicable:not a production application" \
  --sink-gates "not-applicable:no sync or output sink in scope" \
  >"$TMP_DIR/finalize-missing-reconcile.out" 2>&1
missing_reconcile_rc=$?
set -e

if [ "$missing_reconcile_rc" -eq 0 ]; then
  echo "Expected finalize without --linear-reconciled to fail" >&2
  exit 1
fi
assert_contains "$TMP_DIR/finalize-missing-reconcile.out" "finalize requires --linear-reconciled"

echo "linear-agent tests passed"
