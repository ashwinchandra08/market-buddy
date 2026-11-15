"""Fetch quotes + mini-series via yfinance, with a last-good-value cache fallback."""
from __future__ import annotations

import json
import time
import urllib.request
from datetime import datetime, timezone

import yfinance as yf


def load_cache(path: str | None = None, url: str | None = None) -> dict:
    try:
        if path:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        if url:
            req = urllib.request.Request(url, headers={"User-Agent": "market-buddy"})
            with urllib.request.urlopen(req, timeout=15) as r:
                return json.load(r)
    except Exception as e:  # first run / offline: fine
        print(f"[cache] none loaded ({e})")
    return {}


def _downsample(vals, n=60):
    if len(vals) <= n:
        return vals
    step = len(vals) / n
    return [vals[int(i * step)] for i in range(n - 1)] + [vals[-1]]


def fetch_symbol(sym: str, retries: int = 2) -> dict:
    last_err = None
    for attempt in range(retries + 1):
        try:
            t = yf.Ticker(sym)
            d = t.history(period="1mo", interval="1d", auto_adjust=False).dropna(subset=["Close"])
            if len(d) < 2:
                raise ValueError("not enough daily rows")
            closes = [float(x) for x in d["Close"]]
            last, prev = closes[-1], closes[-2]

            try:
                i = t.history(period="5d", interval="30m", auto_adjust=False).dropna(subset=["Close"])
            except Exception:
                i = None
            intraday, last_ts = [], d.index[-1]
            if i is not None and len(i):
                day = i.index[-1].date()
                sess = i[i.index.date == day]
                intraday = _downsample([float(x) for x in sess["Close"]])
                last_ts = i.index[-1]
            return dict(
                sym=sym, last=last, prev=prev, chg=last - prev, pct=(last / prev - 1) * 100,
                spark5=closes[-5:], intraday=intraday,
                session_date=str(d.index[-1].date()),
                last_ts=last_ts.tz_convert("UTC").isoformat() if last_ts.tzinfo else str(last_ts),
                fetched_at=datetime.now(timezone.utc).isoformat(),
            )
        except Exception as e:
            last_err = e
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"{sym}: {last_err}")


def fetch_all(symbols, cache: dict) -> dict:
    out = {}
    for s in dict.fromkeys(symbols):
        try:
            out[s] = fetch_symbol(s)
            print(f"[ok]    {s:12s} {out[s]['last']:.2f} ({out[s]['pct']:+.2f}%)")
        except Exception as e:
            if s in cache:
                out[s] = {**cache[s], "stale": True}
                print(f"[stale] {s}: {e}")
            else:
                print(f"[miss]  {s}: {e}")
        time.sleep(0.4)
    return out
