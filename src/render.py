from __future__ import annotations

import os
import textwrap
from datetime import datetime
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont

from .market import is_open
from .mood import LABELS, Mood

FONT_DIRS = ["fonts", "/usr/share/fonts/truetype/dejavu", "/usr/share/fonts/dejavu",
             "C:/Windows/Fonts", "/Library/Fonts", "/System/Library/Fonts/Supplemental"]
REG = ["DejaVuSans.ttf", "Arial.ttf", "arial.ttf", "Verdana.ttf"]
BOLD = ["DejaVuSans-Bold.ttf", "Arial Bold.ttf", "arialbd.ttf", "Verdana Bold.ttf"]
_cache: dict = {}


def font(size: int, bold: bool = False):
    key = (size, bold)
    if key not in _cache:
        f = None
        for dname in FONT_DIRS:
            for fn in (BOLD if bold else REG):
                p = os.path.join(dname, fn)
                if os.path.exists(p):
                    f = ImageFont.truetype(p, size)
                    break
            if f:
                break
        _cache[key] = f or ImageFont.load_default(size)
    return _cache[key]


def fmt(v, dec, prefix="", suffix=""):
    return f"{prefix}{v:,.{dec}f}{suffix}"


def arrow(x):
    return "▲" if x > 0 else ("▼" if x < 0 else "■")


def sparkline(d, box, vals, fg, mid, base=None, lw=4):
    x0, y0, x1, y1 = box
    if not vals or len(vals) < 2:
        d.line((x0, (y0 + y1) // 2, x1, (y0 + y1) // 2), fill=mid, width=2)
        return
    pool = list(vals) + ([base] if base is not None else [])
    lo, hi = min(pool), max(pool)
    if hi == lo:
        hi = lo + 1e-9 + abs(lo) * 1e-6
    n = len(vals)
    ypos = lambda v: y1 - (y1 - y0) * (v - lo) / (hi - lo)
    pts = [(x0 + (x1 - x0) * k / (n - 1), ypos(v)) for k, v in enumerate(vals)]
    if base is not None:
        by = ypos(base)
        for x in range(int(x0), int(x1), 10):
            d.line((x, by, x + 5, by), fill=mid, width=2)
    d.line(pts, fill=fg, width=lw, joint="curve")
    lx, ly = pts[-1]
    d.ellipse((lx - 6, ly - 6, lx + 6, ly + 6), fill=fg)


def wrap(d, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def render(cfg, data, mood: Mood, now: datetime, sprite, pk_name: str, message: str) -> Image.Image:
    W, H = cfg["size"]["width"], cfg["size"]["height"]
    M = 32
    BG, FG, MID, LIGHT = 255, 0, 105, 205
    img = Image.new("L", (W, H), BG)
    d = ImageDraw.Draw(img)
    local = now.astimezone(ZoneInfo(cfg["timezone"]))

    # ---------- header ----------
    d.text((M, 18), "MARKET BUDDY", font=font(52, True), fill=FG)
    d.text((M, 82), local.strftime("%A, %d %b %Y"), font=font(28), fill=MID)
    d.text((W - M, 22), local.strftime("Updated %H:%M IST"), font=font(24), fill=MID, anchor="ra")
    any_ts = {mk: next((data[i["symbol"]]["last_ts"] for i in cfg["indices"]
                        if i["market"] == mk and i["symbol"] in data), None) for mk in ("IN", "US")}
    for k, (mk, label) in enumerate((("IN", "INDIA"), ("US", "US"))):
        op = is_open(mk, any_ts[mk], now)
        txt = f"{label}  {'● OPEN' if op else '○ CLOSED'}"
        x1 = W - M - (1 - k) * 236
        d.rounded_rectangle((x1 - 224, 62, x1, 104), 20, outline=FG, width=3,
                            fill=FG if op else BG)
        d.text((x1 - 112, 83), txt, font=font(20, True), fill=BG if op else FG, anchor="mm")
    d.line((M, 124, W - M, 124), fill=FG, width=4)

    # ---------- pokemon + bubble ----------
    box = (M, 140, 452, 560)
    if sprite is not None:
        s_img, s_mask = sprite
        sx = box[0] + (box[2] - box[0] - s_img.width) // 2
        sy = box[3] - s_img.height
        img.paste(s_img, (sx, sy), s_mask)
    d.text(((box[0] + box[2]) // 2, 576), pk_name.upper(), font=font(24, True),
           fill=FG, anchor="mm")

    bx0, by0, bx1, by1 = 482, 152, W - M, 572
    d.rounded_rectangle((bx0, by0, bx1, by1), 32, outline=FG, width=5)
    tail = [(bx0 + 6, 290), (bx0 - 42, 330), (bx0 + 6, 370)]
    d.polygon(tail, fill=BG)
    d.line(tail, fill=FG, width=5)
    d.line((bx0 + 2, 292, bx0 + 2, 368), fill=BG, width=8)

    tx = bx0 + 30
    d.text((tx, by0 + 26), f"MOOD: {mood.label}", font=font(40, True), fill=FG)
    y = by0 + 92
    for line in wrap(d, message, font(38), bx1 - tx - 30)[:3]:
        d.text((tx, y), line, font=font(38), fill=FG)
        y += 50
    y = by1 - 112
    d.line((tx, y - 10, bx1 - 30, y - 10), fill=LIGHT, width=2)
    p = mood.parts
    if "india" in p:
        d.text((tx, y), "India", font=font(26, True), fill=FG)
        d.text((tx + 100, y), f"{arrow(p['india'])} {p['india']:+.2f}%", font=font(26, True), fill=FG)
    if "us" in p:
        d.text((tx, y + 36), "US", font=font(26, True), fill=FG)
        d.text((tx + 100, y + 36), f"{arrow(p['us'])} {p['us']:+.2f}%", font=font(26, True), fill=FG)
    if mood.score is not None:
        d.text((bx1 - 30, y + 18), f"score\n{mood.score:+.2f}", font=font(24), fill=MID,
               anchor="rm", align="right")
    if mood.vol_bump:
        d.text((tx, by1 - 34), "⚡ volatility spike: mood lowered", font=font(20), fill=MID)

    # mood meter
    mx0, mx1, my = M, W - M, 590
    seg = (mx1 - mx0) / 5
    for k in range(5):
        x0 = mx0 + k * seg + 3
        sel = k == mood.tier
        d.rounded_rectangle((x0, my, x0 + seg - 6, my + 34), 10, outline=FG, width=3,
                            fill=FG if sel else BG)
        d.text((x0 + (seg - 6) / 2, my + 17), LABELS[k], font=font(17, True),
               fill=BG if sel else MID, anchor="mm")

    # ---------- index table ----------
    ty = 646
    hdr = font(20, True)
    d.text((M, ty + 4), "INDEX", font=hdr, fill=MID)
    d.text((395, ty + 4), "LAST", font=hdr, fill=MID, anchor="ra")
    d.text((570, ty + 4), "CHANGE", font=hdr, fill=MID, anchor="ra")
    d.text((690, ty + 4), "TODAY", font=hdr, fill=MID, anchor="ma")
    d.text((935, ty + 4), "5 DAY", font=hdr, fill=MID, anchor="ma")
    d.line((M, ty + 34, W - M, ty + 34), fill=FG, width=3)
    RH = 92
    y0 = ty + 40
    for r, ix in enumerate(cfg["indices"]):
        row = data.get(ix["symbol"])
        cy = y0 + r * RH + RH // 2
        if r:
            d.line((M, y0 + r * RH, W - M, y0 + r * RH), fill=LIGHT, width=2)
        d.text((M, cy - 11), ix["name"], font=font(30, True), fill=FG, anchor="lm")
        d.text((M, cy + 24), "INDIA" if ix["market"] == "IN" else "US", font=font(18), fill=MID, anchor="lm")
        if not row:
            d.text((395, cy), "n/a", font=font(30), fill=MID, anchor="rm")
            continue
        star = "*" if row.get("stale") else ""
        d.text((395, cy - 10), fmt(row["last"], ix.get("dec", 2)) + star, font=font(30), fill=FG, anchor="rm")
        d.text((570, cy - 11), f"{arrow(row['pct'])} {abs(row['pct']):.2f}%", font=font(32, True),
               fill=FG, anchor="rm")
        d.text((570, cy + 24), f"{row['chg']:+,.2f}", font=font(20), fill=MID, anchor="rm")
        sparkline(d, (595, cy - 30, 790, cy + 30), row.get("intraday", []), FG, MID, base=row["prev"])
        sparkline(d, (835, cy - 30, 1030, cy + 30), row.get("spark5", []), FG, MID)
    d.line((M, y0 + len(cfg["indices"]) * RH, W - M, y0 + len(cfg["indices"]) * RH), fill=FG, width=3)

    # ---------- macro strip ----------
    my0 = y0 + len(cfg["indices"]) * RH + 14
    macro = cfg["macro"][:5]
    cw = (W - 2 * M) / max(1, len(macro))
    for k, mc in enumerate(macro):
        x0 = M + k * cw
        d.rounded_rectangle((x0 + 3, my0, x0 + cw - 3, my0 + 120), 14, outline=FG, width=3)
        row = data.get(mc["symbol"])
        cx = x0 + cw / 2
        d.text((cx, my0 + 24), mc["name"].upper(), font=font(19, True), fill=MID, anchor="mm")
        if row:
            d.text((cx, my0 + 62), fmt(row["last"], mc.get("dec", 2), mc.get("prefix", ""), mc.get("suffix", "")),
                   font=font(32, True), fill=FG, anchor="mm")
            d.text((cx, my0 + 98), f"{arrow(row['pct'])} {abs(row['pct']):.2f}%", font=font(23), fill=FG, anchor="mm")
        else:
            d.text((cx, my0 + 56), "n/a", font=font(29), fill=MID, anchor="mm")

    # ---------- footer ----------
    stale = any(v.get("stale") for v in data.values())
    foot = "Data: Yahoo Finance via yfinance · may be delayed · not investment advice"
    if stale:
        foot = "* stale value (last good fetch) · " + foot
    d.text((W // 2, H - 22), foot, font=font(17), fill=MID, anchor="mm")
    return img
