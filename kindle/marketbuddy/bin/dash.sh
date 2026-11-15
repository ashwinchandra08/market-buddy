#!/bin/sh
# Main loop. Runs until $BASE/STOP exists.
. "$(dirname "$0")/common.sh"
rm -f "$BASE/STOP"
log "=== dash start ==="

framework_stop
sleep 2
lipc-set-prop com.lab126.powerd preventScreenSaver 1 2>/dev/null
wifi_up

fails=0
while [ ! -f "$BASE/STOP" ]; do
  fetch_if_new; rc=$?
  case $rc in
    0) log "new image"; paint; fails=0 ;;
    1) fails=0 ;;
    *) fails=$((fails+1)); log "fetch failed ($fails)"; wifi_up
       if [ "$fails" -eq 12 ]; then "$FBINK" -q -y 0 -x 0 "OFFLINE - data may be stale"; fi ;;
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
