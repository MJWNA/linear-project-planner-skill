# Example: Local Skill Audit

## Intended Linear Graph

- Guide: Agent Operating Guide
- Guide: Verification Matrix
- Workstream: Audit
- Workstream: Final Signoff
- Child: Inspect `SKILL.md`, scripts, tests, and docs
- Child: Run verification suite
- Child: Produce scored Markdown audit

## Ledger Snippet

```md
- Validation mode: standard
- Next safest action: run read-only audit checks, then write audit report
```

## Verification Matrix

- syntax checks
- unit/regression tests
- evaluator score
- installed-copy parity

## Final Completion Comment

Record the audit path, checks run, score, gaps, and whether live Linear mutation was intentionally skipped.
