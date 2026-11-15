from __future__ import annotations

from dataclasses import dataclass, field

TIERS = ["very_happy", "happy", "neutral", "worried", "scary"]
LABELS = ["VERY HAPPY", "HAPPY", "CALM", "WORRIED", "SCARY"]
MESSAGES = {
    "very_happy": ["Green everywhere! Party time!", "Markets are flying today!", "What a day for the bulls!"],
    "happy": ["Nice and steady. Good vibes!", "Markets are smiling today.", "A pleasant day to be invested."],
    "neutral": ["Not much happening. Nap time...", "Sideways day. Stay calm.", "Quiet markets. Snacks instead?"],
    "worried": ["Hmm, red is showing up...", "Rough patch. Hold tight!", "Markets look a bit nervous."],
    "scary": ["Yikes! Big sell-off!", "Hide the portfolio!", "Storm warning: stay calm and breathe."],
}


@dataclass
class Mood:
    tier: int
    score: float | None
    parts: dict = field(default_factory=dict)
    vol_bump: bool = False

    @property
    def key(self): return TIERS[self.tier]

    @property
    def label(self): return LABELS[self.tier]


def tier_for(score: float, th: dict) -> int:
    if score >= th["very_happy"]: return 0
    if score >= th["happy"]: return 1
    if score >= th["neutral"]: return 2
    if score > th["worried"]: return 3
    return 4


def compute_mood(data: dict, cfg: dict) -> Mood:
    m = cfg["mood"]
    w = m["weights"]
    parts = {}
    for key in ("india", "us"):
        d = data.get(m[f"{key}_symbol"])
        if d is not None:
            parts[key] = d["pct"]
    if not parts:
        return Mood(tier=2, score=None)
    tw = sum(w[k] for k in parts)
    score = sum(parts[k] * w[k] for k in parts) / tw
    tier = tier_for(score, m["thresholds"])

    bump = False
    for key, sym in m["vol_symbols"].items():
        d = data.get(sym)
        if d is not None and d["pct"] >= m["vol_spike_pct"]:
            bump = True
    if bump and tier < 4:
        tier += 1
    return Mood(tier=tier, score=score, parts=parts, vol_bump=bump)
