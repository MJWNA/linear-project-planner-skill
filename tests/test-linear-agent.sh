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

"$BIN" init \
  --ledger "$LEDGER" \
  --project "Agent Runtime Hardening" \
  --prompt "Create a Linear project and execute it with agents" \
  --linear-project "MAS Agent Runtime Hardening" \
  --repo "/tmp/example-repo" \
  --base-branch "main" \
  >"$TMP_DIR/init.out"

assert_contains "$LEDGER" "# Linear Execution Ledger: Agent Runtime Hardening"
assert_contains "$LEDGER" "Create a Linear project and execute it with agents"
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
if [ "$(grep -Fc -- "- TBD" "$LEDGER")" -lt 4 ]; then
  echo "Expected non-activity section placeholders to remain after init" >&2
  cat "$LEDGER" >&2
  exit 1
fi

"$BIN" start MAS-123 \
  --ledger "$LEDGER" \
  --agent "Codex" \
  --worktree "/tmp/example-worktree" \
  --note "Claimed for implementation with \"quoted\" note" \
  >"$TMP_DIR/start.out"

assert_contains "$LEDGER" "- Active issue: MAS-123"
assert_contains "$LEDGER" "- Active agent: Codex"
assert_contains "$LEDGER" "- Active worktree: /tmp/example-worktree"
assert_contains "$LEDGER" "| MAS-123 | In Progress | agent:executing | Codex | /tmp/example-worktree |"
assert_contains "$LEDGER" "Claimed for implementation with \"quoted\" note"
assert_contains "$TMP_DIR/start.out" "Required Linear MCP actions"
assert_contains "$TMP_DIR/start.out" "_save_issue(id=\"MAS-123\", state=\"In Progress\")"
assert_contains "$TMP_DIR/start.out" "_save_comment(issueId=\"MAS-123\", body=<comment body below>)"
assert_contains "$TMP_DIR/start.out" "Comment body:"
assert_contains "$TMP_DIR/start.out" "Claimed for implementation with \"quoted\" note"
assert_contains "$TMP_DIR/start.out" "Verify with _list_issues"

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
  --verification "npm test: pass" \
  --note "Implemented and verified" \
  >"$TMP_DIR/complete.out"

assert_contains "$LEDGER" "| MAS-123 | Done | agent:pr-ready | Codex | /tmp/example-worktree |"
assert_contains "$LEDGER" "npm test: pass"
assert_contains "$LEDGER" "Implemented and verified"
assert_contains "$TMP_DIR/complete.out" "_save_comment(issueId=\"MAS-123\", body=<comment body below>)"
assert_contains "$TMP_DIR/complete.out" "_save_issue(id=\"MAS-123\", state=\"Done\")"
assert_contains "$TMP_DIR/complete.out" "Verify with _list_issues"
assert_contains "$LEDGER" "## Activity Log"

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

echo "linear-agent tests passed"
