from __future__ import annotations

from datetime import datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

SESSIONS = {
    "IN": ("Asia/Kolkata", time(9, 15), time(15, 30)),
    "US": ("America/New_York", time(9, 30), time(16, 0)),
}


def is_open(market: str, last_ts_iso: str | None, now_utc: datetime | None = None) -> bool:
    """Open = inside regular hours on a weekday AND we have a fresh (<90 min) data point.
    The freshness check quietly handles exchange holidays."""
    now_utc = now_utc or datetime.now(timezone.utc)
    tz, o, c = SESSIONS[market]
    local = now_utc.astimezone(ZoneInfo(tz))
    if local.weekday() >= 5 or not (o <= local.time() <= c):
        return False
    if not last_ts_iso:
        return False
    try:
        ts = datetime.fromisoformat(last_ts_iso)
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        return now_utc - ts < timedelta(minutes=90)
    except ValueError:
        return False
