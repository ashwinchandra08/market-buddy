from src.mood import compute_mood, tier_for
import yaml

CFG = yaml.safe_load(open("config.yaml", encoding="utf-8"))
TH = CFG["mood"]["thresholds"]


def d(india, us, vix=0.0):
    f = lambda p: dict(pct=p)
    return {"^NSEI": f(india), "^GSPC": f(us), "^INDIAVIX": f(vix), "^VIX": f(0.0)}


def test_tiers():
    assert [tier_for(x, TH) for x in (1.5, 0.5, 0.0, -0.5, -2)] == [0, 1, 2, 3, 4]


def test_blend():
    m = compute_mood(d(2.0, 0.0), CFG)
    assert round(m.score, 2) == 1.0 and m.tier == 0


def test_vol_bump():
    assert compute_mood(d(0.5, 0.5, vix=10), CFG).tier == 2


def test_missing_us():
    assert compute_mood({"^NSEI": dict(pct=-2.0)}, CFG).tier == 4


def test_no_data():
    assert compute_mood({}, CFG).tier == 2
