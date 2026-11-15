"""Synthetic data so you can preview the layout offline: python -m src.main --mock"""
import random
from datetime import datetime, timezone

BASES = {"^NSEI": 24500, "^BSESN": 80500, "^NSEBANK": 52500, "^GSPC": 6100, "^IXIC": 20200,
         "^DJI": 44500, "USDINR=X": 84.7, "BZ=F": 73.4, "GC=F": 2650, "^INDIAVIX": 14.2,
         "^TNX": 4.31, "RELIANCE.NS": 1245.5, "TCS.NS": 4120.3, "HDFCBANK.NS": 1760.8,
         "AAPL": 228.4, "NVDA": 141.2, "MSFT": 421.9}


def mock_all(symbols, bias=0.0, seed=7):
    rnd = random.Random(seed)
    out = {}
    now = datetime.now(timezone.utc).isoformat()
    for s in symbols:
        base = BASES.get(s, 100.0)
        pct = bias + rnd.uniform(-0.4, 0.4)
        prev = base
        last = prev * (1 + pct / 100)
        d5, v = [], prev * 0.985
        for _ in range(4):
            v *= 1 + rnd.uniform(-0.006, 0.008)
            d5.append(v)
        d5.append(prev)
        d5 = d5[-4:] + [last]
        intra, v = [], prev
        for k in range(26):
            v += (last - v) * 0.12 + base * rnd.uniform(-0.0012, 0.0012)
            intra.append(v)
        intra[-1] = last
        out[s] = dict(sym=s, last=last, prev=prev, chg=last - prev, pct=pct, spark5=d5,
                      intraday=intra, session_date=now[:10], last_ts=now, fetched_at=now)
    return out
