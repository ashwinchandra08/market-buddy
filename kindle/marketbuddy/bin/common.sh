# shared helpers (busybox ash compatible)
BASE="$(cd "$(dirname "$0")/.." && pwd)"
. "$BASE/config.sh"
STATE="$BASE/state"; mkdir -p "$STATE"
LOG="$BASE/marketbuddy.log"
CACERT="$BASE/cacert.pem"

# /mnt/us is FAT: copy our binaries to tmpfs and chmod +x so they always run
TMPBIN=/tmp/marketbuddy-bin; mkdir -p "$TMPBIN"
for b in curl fbink; do
  if [ -f "$BASE/bin/$b" ]; then cp "$BASE/bin/$b" "$TMPBIN/$b" 2>/dev/null; chmod +x "$TMPBIN/$b" 2>/dev/null; fi
done
CURL="$TMPBIN/curl"; [ -x "$CURL" ] || CURL="$(command -v curl)"
FBINK="$TMPBIN/fbink"; [ -x "$FBINK" ] || FBINK="$(command -v fbink)"   # optional; empty => use built-in eips
PNG="$STATE/dash.png"

log() { echo "$(date '+%F %T') $*" >> "$LOG"; }

wifi_up() {
  lipc-set-prop com.lab126.cmd wirelessEnable 1 2>/dev/null
  lipc-set-prop com.lab126.wifid enable 1 2>/dev/null
}

# returns 0 and updates $PNG if a new image was painted-worthy; 1 if unchanged; 2 on error
fetch_if_new() {
  t=$(date +%s)
  new=$("$CURL" -fsS --max-time 30 --cacert "$CACERT" "$URL_BASE/meta.txt?t=$t" 2>>"$LOG") || return 2
  [ -n "$new" ] || return 2
  old=$(cat "$STATE/meta" 2>/dev/null)
  [ "$new" = "$old" ] && [ -f "$PNG" ] && return 1
  "$CURL" -fsS --max-time 90 --cacert "$CACERT" -o "$STATE/dash.tmp" "$URL_BASE/dash.png?t=$t" 2>>"$LOG" || return 2
  sz=$(wc -c < "$STATE/dash.tmp")
  [ "$sz" -gt 20000 ] || { log "download too small ($sz)"; return 2; }
  mv "$STATE/dash.tmp" "$PNG"
  echo "$new" > "$STATE/meta"
  return 0
}

# Paint the PNG full-screen. Uses FBInk if present, otherwise the Kindle's built-in eips.
paint() {
  if [ -n "$FBINK" ] && [ -x "$FBINK" ]; then
    "$FBINK" -q -c -f -g file="$PNG"
  else
    eips -c; eips -f -g "$PNG"
  fi
}
# Print a short text line at the top-left of the screen.
say() {
  if [ -n "$FBINK" ] && [ -x "$FBINK" ]; then "$FBINK" -q -y 0 -x 0 "$1"; else eips 0 0 "$1"; fi
}

framework_stop()  { /etc/init.d/framework stop 2>/dev/null || stop framework 2>/dev/null; }
framework_start() { /etc/init.d/framework start 2>/dev/null || start framework 2>/dev/null; }
