#!/bin/sh
# Detach fully so the dashboard survives the launcher (and the UI being stopped).
BASE="$(cd "$(dirname "$0")/.." && pwd)"
if command -v setsid >/dev/null 2>&1; then
  setsid nohup sh "$BASE/bin/dash.sh" >/dev/null 2>&1 &
else
  nohup sh "$BASE/bin/dash.sh" >/dev/null 2>&1 &
fi
