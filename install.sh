#!/bin/sh
# Install the skin on macOS, then use Reload Skin in Football Manager.
set -eu
SKIN_DIR="$(cd "$(dirname "$0")" && pwd)"
SKIN_NAME="FM27 Refined Skin"
SKINS_DIR="${FM27_SKINS_DIR:-$HOME/Library/Application Support/Sports Interactive/Football Manager 27/skins}"

if [ ! -f "$SKIN_DIR/variables.uss" ]; then
  echo "Missing variables.uss. Run ./extract.sh first." >&2
  exit 1
fi

DESTINATION="$SKINS_DIR/$SKIN_NAME"
if [ "$DESTINATION" = "$SKIN_DIR" ]; then
  echo "The installation destination must differ from the source folder." >&2
  exit 1
fi
mkdir -p "$DESTINATION"
# Copy only runtime files, keeping Git metadata and extracted references local.
for file in skin.json main.uss variables.uss custom.uss; do
  cp "$SKIN_DIR/$file" "$DESTINATION/$file"
done
echo "Installed: $DESTINATION"
echo "Reload the skin in Football Manager."
