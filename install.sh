#!/usr/bin/env bash
set -euo pipefail

REPO_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
CODEX_HOME=${CODEX_HOME:-"$HOME/.codex"}
SKILL_DIR="$CODEX_HOME/skills/linear-project-planner"
BIN_DIR="$HOME/.local/bin"

mkdir -p "$SKILL_DIR" "$BIN_DIR"

rsync -a --delete \
  --exclude '.git' \
  --exclude '.gitignore' \
  --exclude '.github' \
  --exclude 'LICENSE' \
  --exclude 'README.md' \
  --exclude 'install.sh' \
  "$REPO_DIR/" "$SKILL_DIR/"

cat >"$BIN_DIR/linear-agent" <<EOF
#!/usr/bin/env bash
exec "$SKILL_DIR/scripts/linear-agent" "\$@"
EOF

chmod +x "$SKILL_DIR/scripts/linear-agent" "$BIN_DIR/linear-agent"

echo "Installed linear-project-planner skill to $SKILL_DIR"
echo "Installed linear-agent launcher to $BIN_DIR/linear-agent"
