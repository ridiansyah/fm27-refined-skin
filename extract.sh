#!/bin/sh
# Refresh local native styles after a game update. custom.uss is preserved.
set -eu
SKIN_DIR="$(cd "$(dirname "$0")" && pwd)"
GAME_DIR="${FM27_GAME_DIR:-$HOME/Library/Application Support/Steam/steamapps/common/Football Manager 27/fm.app/Contents/Resources/Data/StreamingAssets/aa/StandaloneOSX}"

set -- "$GAME_DIR"/ui-styles_assets_*.bundle
if [ ! -f "$1" ]; then
  echo "No UI style bundles found in: $GAME_DIR" >&2
  echo "Set FM27_GAME_DIR to the folder containing ui-styles_assets_*.bundle." >&2
  exit 1
fi

WORK_DIR="$(mktemp -d)"
trap 'rm -rf "$WORK_DIR"' EXIT
python3 -m venv "$WORK_DIR/venv"
"$WORK_DIR/venv/bin/pip" install -q UnityPy
mkdir "$WORK_DIR/out"
"$WORK_DIR/venv/bin/python" -I "$SKIN_DIR/tools/uss_decompile.py" "$SKIN_DIR/tools/unityref" "$WORK_DIR/out" "$@" >/dev/null
"$WORK_DIR/venv/bin/python" -I "$SKIN_DIR/tools/build_base.py" "$WORK_DIR/out" "$SKIN_DIR"
echo "Extraction complete. Run ./install.sh, then reload the skin in Football Manager."
