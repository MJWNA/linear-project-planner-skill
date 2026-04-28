#!/usr/bin/env bash
set -euo pipefail

REPO_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
CODEX_HOME=${CODEX_HOME:-"$HOME/.codex"}
SKILL_DIR="$CODEX_HOME/skills/linear-project-planner"
BIN_DIR="$HOME/.local/bin"
WITH_DOCS=0
MODE=install
FORCE=0

usage() {
  cat <<'EOF'
Usage:
  ./install.sh [--with-docs]
  ./install.sh --check
  ./install.sh --uninstall [--force]

Options:
  --with-docs   Include README/LICENSE/SUPPORT/SECURITY docs in installed copy.
  --check       Validate installed skill, launcher, and PATH.
  --uninstall   Remove installed skill and launcher.
  --force       Skip uninstall confirmation.
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --with-docs) WITH_DOCS=1; shift ;;
    --check) MODE=check; shift ;;
    --uninstall) MODE=uninstall; shift ;;
    --force) FORCE=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

check_install() {
  local ok=1
  [ -d "$SKILL_DIR" ] || { echo "Missing skill directory: $SKILL_DIR" >&2; ok=0; }
  [ -x "$SKILL_DIR/scripts/linear-agent" ] || { echo "Missing executable skill CLI" >&2; ok=0; }
  [ -x "$BIN_DIR/linear-agent" ] || { echo "Missing launcher: $BIN_DIR/linear-agent" >&2; ok=0; }
  case ":$PATH:" in
    *":$BIN_DIR:"*) ;;
    *) echo "PATH warning: $BIN_DIR is not on PATH" >&2; ok=0 ;;
  esac
  [ "$ok" -eq 1 ] || exit 1
  echo "linear-project-planner install looks healthy"
}

uninstall_skill() {
  if [ "$FORCE" -ne 1 ]; then
    printf 'Remove %s and %s/linear-agent? [y/N] ' "$SKILL_DIR" "$BIN_DIR" >&2
    read -r answer
    case "$answer" in
      y|Y|yes|YES) ;;
      *) echo "Uninstall canceled"; exit 1 ;;
    esac
  fi
  rm -rf "$SKILL_DIR"
  rm -f "$BIN_DIR/linear-agent"
  echo "Uninstalled linear-project-planner"
}

if [ "$MODE" = "check" ]; then
  check_install
  exit 0
fi

if [ "$MODE" = "uninstall" ]; then
  uninstall_skill
  exit 0
fi

mkdir -p "$SKILL_DIR" "$BIN_DIR"

RSYNC_EXCLUDES=(
    --exclude '.git' \
    --exclude '.gitignore' \
    --exclude '.github' \
    --exclude 'install.sh' \
)

if [ "$WITH_DOCS" -ne 1 ]; then
  RSYNC_EXCLUDES+=(--exclude 'README.md' --exclude 'SUPPORT.md' --exclude 'SECURITY.md')
fi

if [ "$REPO_DIR" != "$SKILL_DIR" ]; then
  rsync -a --delete "${RSYNC_EXCLUDES[@]}" "$REPO_DIR/" "$SKILL_DIR/"
fi

cat >"$BIN_DIR/linear-agent" <<EOF
#!/usr/bin/env bash
exec "$SKILL_DIR/scripts/linear-agent" "\$@"
EOF

chmod +x "$SKILL_DIR/scripts/linear-agent" "$BIN_DIR/linear-agent"

echo "Installed linear-project-planner skill to $SKILL_DIR"
echo "Installed linear-agent launcher to $BIN_DIR/linear-agent"
case ":$PATH:" in
  *":$BIN_DIR:"*) ;;
  *) echo "PATH warning: add $BIN_DIR to PATH to run linear-agent directly" >&2 ;;
esac
