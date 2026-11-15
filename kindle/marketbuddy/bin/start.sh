#!/bin/sh
# Detach fully so the dashboard survives the launcher (and the UI being stopped).
BASE="$(cd "$(dirname "$0")/.." && pwd)"
trap '' HUP TERM
if command -v setsid >/dev/null 2>&1; then
  ( setsid nohup sh "$BASE/bin/dash.sh" >>"$BASE/marketbuddy.log" 2>&1 </dev/null & ) &
else
  ( nohup sh "$BASE/bin/dash.sh" >>"$BASE/marketbuddy.log" 2>&1 </dev/null & ) &
fi
