#!/usr/bin/env bash
# Install a daily launchd job that runs `run_atlas_cycle.py tick`.
# This only touches local timestamps/state — it does not post or scrape.

set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
PLIST_SRC="$REPO/scripts/com.atlas.cycle.plist.example"
DEST="$HOME/Library/LaunchAgents/com.atlas.cycle.plist"

sed \
  -e "s|REPLACE_WITH_ABSOLUTE_PATH_TO_REPO|$REPO|g" \
  -e "s|REPLACE_WITH_HOME|$HOME|g" \
  "$PLIST_SRC" > "$DEST"

launchctl unload "$DEST" 2>/dev/null || true
launchctl load "$DEST"

echo "Installed $DEST"
echo "Logs: $HOME/Library/Logs/atlas-cycle.out (and .err)"
echo "Edit the plist to change the 9:00 AM schedule if desired."
