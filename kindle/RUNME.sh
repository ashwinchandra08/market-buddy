#!/bin/sh
# Market Buddy launcher for setups WITHOUT KUAL.
# Copy this file to the ROOT of the Kindle (next to "documents"), then type  ;log runme  in the home-screen search bar.
# What it runs is decided by the one-word file  extensions/marketbuddy/ACTION :
#   selfcheck  -> check files, TLS and your URL (default)      test -> paint once, restore UI      start -> run the dashboard
BASE=/mnt/us/extensions/marketbuddy
ACTION=$(cat "$BASE/ACTION" 2>/dev/null | tr -d ' \r\n')
echo "$(date '+%F %T') RUNME.sh action='$ACTION'" >> "$BASE/marketbuddy.log"
case "$ACTION" in
  test)  sh "$BASE/bin/test_once.sh" ;;
  start) sh "$BASE/bin/start.sh" ;;
  *)     sh "$BASE/bin/selfcheck.sh" ;;
esac
