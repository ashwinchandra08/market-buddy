#!/bin/sh
BASE="$(cd "$(dirname "$0")/.." && pwd)"
nohup sh "$BASE/bin/dash.sh" >/dev/null 2>&1 &
