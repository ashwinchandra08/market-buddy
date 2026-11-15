#!/bin/sh
# Safe smoke test: stop UI, fetch, paint, wait 20s, restore UI. Check marketbuddy.log afterwards.
. "$(dirname "$0")/common.sh"
log "=== test_once ==="
wifi_up; sleep 5
fetch_if_new; rc=$?
log "fetch rc=$rc"
if [ -f "$PNG" ]; then
  framework_stop; sleep 2
  paint; sleep 20
  framework_start
else
  log "no image available"
fi
