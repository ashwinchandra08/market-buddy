#!/bin/sh
# Writes a report to marketbuddy.log: are curl / fbink / cacert present and runnable? Is the URL reachable?
. "$(dirname "$0")/common.sh"
log "=== selfcheck ==="
log "URL_BASE=$URL_BASE"
log "running as: $(id 2>&1)"
[ -x /etc/init.d/framework ] && log "framework init script: found" || log "framework init script: NOT found"
[ -w /dev/fb0 ] && log "/dev/fb0: writable" || log "/dev/fb0: NOT writable (may need root)"
command -v eips >/dev/null 2>&1 && log "eips: $(command -v eips)" || log "eips: NOT found"
[ -f "$BASE/bin/curl" ]    && log "bin/curl: present"   || log "bin/curl: MISSING (falling back to system curl)"
[ -f "$BASE/bin/fbink" ]   && log "bin/fbink: present"  || log "bin/fbink: not added (OK - will use built-in eips)"
[ -f "$CACERT" ]           && log "cacert.pem: present" || log "cacert.pem: MISSING"
log "curl : $("$CURL" --version 2>&1 | head -1)"
if [ -n "$FBINK" ] && [ -x "$FBINK" ]; then log "fbink: $("$FBINK" --version 2>&1 | head -1)"; else log "painter: eips ($(command -v eips))"; fi
wifi_up; sleep 5
code=$("$CURL" -sS -o /dev/null -w '%{http_code}' --max-time 30 --cacert "$CACERT" "$URL_BASE/meta.txt" 2>&1)
log "GET $URL_BASE/meta.txt -> $code (expect 200)"
say "Market Buddy selfcheck done - see marketbuddy.log"
