# Contributing

Contributions are welcome when they improve the skill's reliability, safety, documentation, or portability.

## Local Setup

```bash
git clone git@github.com:MJWNA/linear-project-planner-skill.git
cd linear-project-planner-skill
```

Install the skill locally when you want to test the Codex integration:

```bash
./install.sh
```

## Development Workflow

- Use a focused branch for each change.
- Keep changes small and tied to one issue or improvement.
- Update `README.md`, `SKILL.md`, or `templates/EXECUTION.md` when behavior changes.
- Add or update tests in `tests/test-linear-agent.sh` for wrapper behavior.
- Do not commit local ledgers, credentials, workspace exports, or personal runtime files.

## Verification

Run the same checks as CI before opening a pull request:

```bash
bash -n install.sh
bash -n scripts/linear-agent
bash -n tests/test-linear-agent.sh
bash tests/test-linear-agent.sh
```

## Pull Requests

Before opening a PR:

- explain what changed and why
- include verification output
- call out any change to Linear status semantics or ledger format
- call out any security-sensitive workflow change

## Security

Do not report vulnerabilities in public issues. Follow [SECURITY.md](SECURITY.md).
