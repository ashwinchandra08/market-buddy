#!/bin/sh
# Only reachable if the Kindle UI is running (e.g. USB/SSH). Normal escape: hold power ~40s to reboot.
BASE="$(cd "$(dirname "$0")/.." && pwd)"
touch "$BASE/STOP"
