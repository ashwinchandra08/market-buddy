from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
from datetime import datetime, timezone

import yaml
from PIL import Image

from . import fetch as fetchmod
from .mascot import mascot
from .mock import mock_all
from .mood import MESSAGES, TIERS, compute_mood, Mood
from .render import render
from .sprites import fetch_sprite, name_for, prepare

HTML = """<!doctype html><meta charset=utf-8><meta http-equiv=refresh content=900>
<title>Market Buddy</title><body style="margin:0;background:#888;text-align:center">
<img src="dash.png" style="max-width:100%;height:100vh"></body>"""


def all_symbols(cfg):
    syms = [i["symbol"] for i in cfg["indices"]] + [m["symbol"] for m in cfg["macro"]]
    m = cfg["mood"]
    syms += [m["india_symbol"], m["us_symbol"], *m["vol_symbols"].values()]
    return list(dict.fromkeys(syms))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config.yaml")
    ap.add_argument("--out", default="site")
    ap.add_argument("--mock", action="store_true", help="synthetic data, no network for quotes")
    ap.add_argument("--bias", type=float, default=0.0, help="mock: shift all moves by this %%")
    ap.add_argument("--force-tier", type=int, choices=range(5), help="debug: force mood 0..4")
    a = ap.parse_args()

    cfg = yaml.safe_load(open(a.config, encoding="utf-8"))
    os.makedirs(a.out, exist_ok=True)
    now = datetime.now(timezone.utc)

    syms = all_symbols(cfg)
    if a.mock:
        data = mock_all(syms, bias=a.bias)
    else:
        cache = fetchmod.load_cache(url=os.environ.get("CACHE_URL"))
        data = fetchmod.fetch_all(syms, cache)

    mood = compute_mood(data, cfg)
    if a.force_tier is not None:
        mood = Mood(tier=a.force_tier, score=mood.score, parts=mood.parts)
    key = TIERS[mood.tier]
    rnd = random.Random(now.astimezone().strftime("%Y-%m-%d") + key)
    pid = rnd.choice(cfg["pokemon"][key])
    message = rnd.choice(MESSAGES[key])

    raw = fetch_sprite(pid)
    if raw is not None:
        sprite, name = prepare(raw, (410, 410)), name_for(pid)
    else:
        sprite, name = mascot(mood.tier, 380), "Buddy"

    img = render(cfg, data, mood, now, sprite, name, message)
    png = os.path.join(a.out, "dash.png")
    img.save(png, optimize=True)

    digest = hashlib.sha1(open(png, "rb").read()).hexdigest()[:16]
    open(os.path.join(a.out, "meta.txt"), "w").write(digest)
    with open(os.path.join(a.out, "cache.json"), "w", encoding="utf-8") as f:
        json.dump(data, f)
    open(os.path.join(a.out, "index.html"), "w").write(HTML)
    print(f"mood={key} score={mood.score} pokemon={name} -> {png} ({digest})")


if __name__ == "__main__":
    main()
