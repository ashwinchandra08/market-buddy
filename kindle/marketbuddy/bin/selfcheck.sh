#!/bin/sh
# Writes a report to marketbuddy.log: are curl / fbink / cacert present and runnable? Is the URL reachable?
. "$(dirname "$0")/common.sh"
log "=== selfcheck ==="
log "URL_BASE=$URL_BASE"
[ -f "$BASE/bin/curl" ]    && log "bin/curl: present"   || log "bin/curl: MISSING (falling back to system curl)"
[ -f "$BASE/bin/fbink" ]   && log "bin/fbink: present"  || log "bin/fbink: MISSING (falling back to PATH)"
[ -f "$CACERT" ]           && log "cacert.pem: present" || log "cacert.pem: MISSING"
log "curl : $("$CURL" --version 2>&1 | head -1)"
log "fbink: $("$FBINK" --version 2>&1 | head -1)"
wifi_up; sleep 5
code=$("$CURL" -sS -o /dev/null -w '%{http_code}' --max-time 30 --cacert "$CACERT" "$URL_BASE/meta.txt" 2>&1)
log "GET $URL_BASE/meta.txt -> $code (expect 200)"
"$FBINK" -q -y 2 -x 2 "Market Buddy selfcheck done - see marketbuddy.log" 2>>"$LOG"
