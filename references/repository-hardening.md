# Repository Hardening Policy

This repo is designed for a small or solo-maintainer workflow. Hardening should catch release mistakes without creating a rule that prevents the maintainer from shipping.

## Enabled Controls

- CI runs syntax checks, shellcheck, unit/regression tests, frozen evaluator, all-verticals evaluator, and trailing whitespace checks.
- Gitleaks runs in CI to catch committed secrets.
- CodeQL runs for Python on push, pull request, and weekly schedule.
- The manual release workflow verifies `VERSION`, `CHANGELOG.md`, tag, tests, evaluator results, install check, and archive artifact.

## Branch And Ruleset Guidance

For solo-maintainer repos, avoid CODEOWNER or branch rules that require an independent reviewer who does not exist. Prefer:

- require CI before merging
- require linear history if desired
- allow admin bypass for emergency release
- protect tags for published versions

If the repo gains multiple active maintainers, add CODEOWNERS and require at least one review.

## Skipped Controls

OpenSSF Scorecard is useful but not mandatory for this skill release. It may be added later as an informational scheduled workflow. The replacement controls are CodeQL, gitleaks, release workflow verification, and the all-verticals evaluator.
