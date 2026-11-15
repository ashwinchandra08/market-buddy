#!/bin/sh
# Main loop. Runs until $BASE/STOP exists.
. "$(dirname "$0")/common.sh"
rm -f "$BASE/STOP"
trap '' HUP TERM
log "=== dash start (pid $$) ==="

# Fetch first, while the UI is still up, so a failure is visible in the log.
wifi_up; sleep 5
log "stopping framework"
framework_stop
log "framework stopped (rc=$?)"
sleep 2
lipc-set-prop com.lab126.powerd preventScreenSaver 1 2>/dev/null
# hide the status bar / close button that appears on touch
lipc-set-prop com.lab126.pillow disableEnablePillow disable 2>/dev/null
log "pillow disabled (rc=$?)"

fails=0
first=1
while [ ! -f "$BASE/STOP" ]; do
  fetch_if_new; rc=$?
  # the UI was just stopped, so the screen is blank: always paint on the first pass
  if [ "$first" = 1 ] && [ "$rc" -eq 1 ]; then rc=0; fi
  first=0
  case $rc in
    0) log "painting image"; paint; fails=0 ;;
    1) fails=0 ;;
    *) fails=$((fails+1)); log "fetch failed ($fails)"; wifi_up
       if [ "$fails" -eq 12 ]; then say "OFFLINE - data may be stale"; fi ;;
  esac

  # faster polling during India/US market windows (IST weekdays)
  h=$(TZ="$TZ_IST" date +%H | sed 's/^0//'); [ -z "$h" ] && h=0
  wd=$(TZ="$TZ_IST" date +%u)
  nap=$POLL_IDLE
  if [ "$wd" -le 5 ]; then
    if { [ "$h" -ge 9 ] && [ "$h" -le 16 ]; } || [ "$h" -ge 18 ] || [ "$h" -le 3 ]; then nap=$POLL_ACTIVE; fi
  fi
  [ "$fails" -gt 0 ] && nap=60
  i=0; while [ $i -lt $nap ] && [ ! -f "$BASE/STOP" ]; do sleep 5; i=$((i+5)); done
done

log "=== dash stop ==="
framework_start
rm -f "$BASE/STOP"
